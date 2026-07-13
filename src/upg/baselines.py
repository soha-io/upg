"""
Step 4 of the estimation roadmap: interpretable temporal-network baselines
with uncertainty.

Three estimators, each a principled upgrade of the Step 3 structure-
constrained arctanh-VAR (see ``recover.py``), all honouring rules W1
(structure before weights) and W7 (personalize from the prior):

1. **Bayesian anchored VAR** (``fit_bayes_person``): the Step 3 ridge
   regression re-derived as exact conjugate Bayesian linear regression with a
   Normal-Inverse-Gamma prior centred on the consensus.  Returns the full
   posterior — mean, per-edge sd, Student-t credible intervals — so every
   personalized edge weight ships with calibrated uncertainty (the missing
   deliverable of Step 3, and the "Uncertainty" axis of the baseline
   contract).

   Model, per target row i (m usable transitions):
       z = X beta + eps,   eps ~ N(0, sigma^2 I)
       beta | sigma^2 ~ N(beta0, sigma^2 / tau * I),   sigma^2 ~ IG(a0, b0)
   Posterior:
       V_n = (tau*I + X'X)^-1,   m_n = V_n (tau*beta0 + X'z)
       a_n = a0 + m/2
       b_n = b0 + (z'z + tau*|beta0|^2 - m_n' V_n^-1 m_n) / 2
   Marginal:  beta_j ~ t_{2 a_n}( m_{n,j},  (b_n/a_n) * V_{n,jj} ).

2. **Errors-in-variables corrected VAR** (``fit_ev_person``): the Step 3
   recovery study showed measurement noise imposes an attenuation floor that
   more occasions do not remove.  The classical method-of-moments correction
   removes the bias: with predictors observed as x = x* + v, v ~ N(0, Lambda),
       E[X'X] = X*'X* + m * Lambda,
   so the corrected normal equations use  X'X - m*Lambda  (eigenvalue-floored
   to stay positive definite).  Response noise (on arctanh(y_{t+1})) is mean-
   zero to first order and only inflates variance, so no response correction
   is applied; the second-order arctanh bias term 2x/(1-x^2)^2 * sd^2/2 is
   ignored and documented.

3. **EKF-EM state-space estimator** (``fit_kalman_person``): the DSEM-style
   baseline.  Latent state zeta_t = arctanh(x_t) follows the *exact*
   generative transition
       zeta_{t+1} = kappa (B tanh(zeta_t) + g u_t) + b + eps_t
   (additive Gaussian process noise — no approximation), with nonlinear
   observation y_t = tanh(zeta_t) + v_t.  An extended Kalman filter +
   Rauch-Tung-Striebel smoother handles missing occasions natively (predict
   through gaps, partial-row updates), and an EM-style M-step re-estimates
   (B, g, b) by the anchored regression on smoothed states.  This addresses
   the two failure axes of Step 3 at once: errors-in-variables (smoothed
   states are denoised) and missingness (no transition is discarded).

All estimators assume kappa known (identifiability: only kappa*B enters the
likelihood; see recover.py notes).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .recover import RecoveredPerson, arctanh_clip, recovery_metrics
from .simulate import dimension_base

# ==========================================================================
# Student-t utilities (no scipy: regularized incomplete beta by Lentz's
# continued fraction, quantiles by bisection)
# ==========================================================================


def _betacf(a: float, b: float, x: float, max_iter: int = 200,
            eps: float = 3e-12) -> float:
    """Continued fraction for the incomplete beta function (Lentz)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betainc_reg(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    import math
    ln_front = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                + a * math.log(x) + b * math.log1p(-x))
    front = math.exp(ln_front)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_cdf(t: float, df: float) -> float:
    """CDF of Student's t with ``df`` degrees of freedom."""
    x = df / (df + t * t)
    p = 0.5 * betainc_reg(df / 2.0, 0.5, x)
    return 1.0 - p if t > 0 else p


def t_ppf(q: float, df: float, tol: float = 1e-10) -> float:
    """Quantile of Student's t by bisection on ``t_cdf``."""
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0, 1)")
    if abs(q - 0.5) < 1e-15:
        return 0.0
    lo, hi = -1000.0, 1000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ==========================================================================
# Shared design-matrix construction (identical to Step 3)
# ==========================================================================


def _design(observations: np.ndarray, u: np.ndarray):
    """Complete-case transitions: predictors x_t, responses arctanh(x_{t+1})."""
    present = ~np.isnan(observations).any(axis=1)
    trans = np.where(present[:-1] & present[1:])[0]
    X_cur = observations[trans]
    Z_next = arctanh_clip(observations[trans + 1])
    u_cur = u[trans]
    return X_cur, Z_next, u_cur, len(trans)


# ==========================================================================
# 1. Bayesian anchored VAR (conjugate NIG, full posterior)
# ==========================================================================


@dataclass
class BayesPerson:
    """Posterior summary for one person (B entries scaled back by 1/kappa)."""
    B_mean: np.ndarray
    B_sd: np.ndarray
    B_lo: np.ndarray          # lower credible bound per edge
    B_hi: np.ndarray          # upper credible bound per edge
    g_mean: np.ndarray
    b_mean: np.ndarray
    n_transitions: int
    level: float
    dims: list[str] = field(default_factory=list)

    def as_recovered(self) -> RecoveredPerson:
        return RecoveredPerson(B_hat=self.B_mean, g_hat=self.g_mean,
                               b_hat=self.b_mean,
                               n_transitions=self.n_transitions,
                               dims=self.dims)


def fit_bayes_person(observations: np.ndarray, u: np.ndarray, kappa: float,
                     tau: float = 0.2, a0: float = 2.0, b0: float = 0.02,
                     level: float = 0.90,
                     base: tuple | None = None) -> BayesPerson:
    """Exact conjugate Bayesian linear regression per row, anchored to the
    consensus prior (rule W7 with a posterior instead of a point estimate).

    ``tau`` is the prior precision (equals the Step 3 ridge for matched
    posterior mode); ``a0, b0`` set the Inverse-Gamma prior on the residual
    variance (prior mean b0/(a0-1) = 0.02, matching process noise ~0.14 sd,
    deliberately weak).
    """
    if base is None:
        base = dimension_base()
    B0, g0, dims, _k = base
    n = len(dims)
    support = B0 != 0.0

    X_cur, Z_next, u_cur, m = _design(observations, u)

    B_mean = np.zeros((n, n))
    B_sd = np.zeros((n, n))
    B_lo = np.zeros((n, n))
    B_hi = np.zeros((n, n))
    g_mean = np.zeros(n)
    b_mean = np.zeros(n)

    alpha = 1.0 - level
    for i in range(n):
        cols = np.where(support[i])[0]
        X = np.column_stack([X_cur[:, cols], u_cur, np.ones(m)])
        z = Z_next[:, i]
        p = X.shape[1]
        beta0 = np.concatenate([kappa * B0[i, cols], [kappa * g0[i], 0.0]])

        Vn_inv = tau * np.eye(p) + X.T @ X
        Vn = np.linalg.inv(Vn_inv)
        mn = Vn @ (tau * beta0 + X.T @ z)
        an = a0 + 0.5 * m
        bn = b0 + 0.5 * float(z @ z + tau * beta0 @ beta0 - mn @ Vn_inv @ mn)
        bn = max(bn, 1e-12)
        df = 2.0 * an
        scale = np.sqrt((bn / an) * np.diag(Vn))       # marginal t scale
        tq = t_ppf(1.0 - alpha / 2.0, df)

        B_mean[i, cols] = mn[:len(cols)] / kappa
        B_sd[i, cols] = scale[:len(cols)] / kappa
        B_lo[i, cols] = (mn[:len(cols)] - tq * scale[:len(cols)]) / kappa
        B_hi[i, cols] = (mn[:len(cols)] + tq * scale[:len(cols)]) / kappa
        g_mean[i] = mn[len(cols)] / kappa
        b_mean[i] = mn[len(cols) + 1]

    return BayesPerson(B_mean=B_mean, B_sd=B_sd, B_lo=B_lo, B_hi=B_hi,
                       g_mean=g_mean, b_mean=b_mean, n_transitions=m,
                       level=level, dims=list(dims))


def edge_coverage(bp: BayesPerson, B_true: np.ndarray,
                  base_B: np.ndarray | None = None) -> dict:
    """Empirical coverage and width of the credible intervals on the support."""
    if base_B is None:
        base_B, _g, _d, _k = dimension_base()
    support = base_B != 0.0
    inside = (B_true[support] >= bp.B_lo[support]) & \
             (B_true[support] <= bp.B_hi[support])
    width = bp.B_hi[support] - bp.B_lo[support]
    return {"coverage": float(np.mean(inside)),
            "mean_width": float(np.mean(width)),
            "level": bp.level}


# ==========================================================================
# 2. Errors-in-variables corrected VAR
# ==========================================================================


def fit_ev_person(observations: np.ndarray, u: np.ndarray, kappa: float,
                  meas_sd: float, ridge: float = 0.2, anchor: bool = True,
                  gamma: float = 1.0,
                  base: tuple | None = None) -> RecoveredPerson:
    """Method-of-moments errors-in-variables correction of the Step 3 ridge,
    restricted to the *identified subspace*.

    With predictors observed as x = x* + v, E[X'X] = X*'X* + m*Lambda, so the
    corrected Gram matrix is S_corr = X'X - m*Lambda (state columns only; u
    and the intercept are noise-free).  Near an attractor the predictors are
    almost collinear: several eigendirections of X'X carry variance close to
    the pure-noise level m*sigma_v^2, and after correction those directions
    hold no usable signal — inverting them amplifies the measurement noise
    that remains in X'z (this failure mode was observed directly: unfloored
    correction overshoots to edge-RMSE > 1).

    Fix: solve for the *deviation from the prior* only inside the subspace
    where the corrected eigenvalue exceeds gamma * m * meas_sd^2 (direction
    carries at least ``gamma`` noise-units of true signal); in the complement
    the estimate defers to the prior exactly.  Writing r = X'z - S_corr@prior,

        beta = prior + V_keep (w_keep + ridge)^-1 V_keep' r,

    which equals the anchored EIV ridge in the kept subspace and the prior in
    the discarded one.
    """
    if base is None:
        base = dimension_base()
    B0, g0, dims, _k = base
    n = len(dims)
    support = B0 != 0.0

    X_cur, Z_next, u_cur, m = _design(observations, u)

    B_hat = np.zeros((n, n))
    g_hat = np.zeros(n)
    b_hat = np.zeros(n)

    for i in range(n):
        cols = np.where(support[i])[0]
        X = np.column_stack([X_cur[:, cols], u_cur, np.ones(m)])
        z = Z_next[:, i]
        p = X.shape[1]
        prior = np.concatenate([kappa * B0[i, cols], [kappa * g0[i], 0.0]])
        if not anchor:
            prior = np.zeros(p)

        S = X.T @ X
        Lam = np.zeros((p, p))
        Lam[:len(cols), :len(cols)] = np.eye(len(cols)) * meas_sd ** 2
        S_corr = S - m * Lam
        w, V = np.linalg.eigh(0.5 * (S_corr + S_corr.T))

        thresh = gamma * m * meas_sd ** 2
        keep = w > thresh
        r = X.T @ z - S_corr @ prior
        delta = np.zeros(p)
        if keep.any():
            Vk = V[:, keep]
            delta = Vk @ ((Vk.T @ r) / (w[keep] + ridge))
        beta = prior + delta
        B_hat[i, cols] = beta[:len(cols)] / kappa
        g_hat[i] = beta[len(cols)] / kappa
        b_hat[i] = beta[len(cols) + 1]

    return RecoveredPerson(B_hat=B_hat, g_hat=g_hat, b_hat=b_hat,
                           n_transitions=m, dims=list(dims))


# ==========================================================================
# 3. EKF + RTS smoother + EM (state-space / DSEM-style baseline)
# ==========================================================================


def _ekf_smoother(y: np.ndarray, u: np.ndarray, B: np.ndarray, g: np.ndarray,
                  b: np.ndarray, kappa: float, meas_sd: float,
                  process_sd: float):
    """Extended Kalman filter + RTS smoother for the exact generative model.

    Latent zeta_t = arctanh(x_t):
        zeta_{t+1} = kappa (B tanh(zeta_t) + g u_t) + b + eps,  eps~N(0,Q)
        y_t        = tanh(zeta_t) + v_t,                        v ~N(0,R)
    Missing entries of y_t (NaN) are dropped from the update row-wise.
    Returns smoothed means (T, n).
    """
    T, n = y.shape
    Q = process_sd ** 2 * np.eye(n)
    Rfull = meas_sd ** 2 * np.eye(n)

    # storage
    zeta_f = np.zeros((T, n))       # filtered means
    P_f = np.zeros((T, n, n))
    zeta_p = np.zeros((T, n))       # one-step predictions
    P_p = np.zeros((T, n, n))

    # initial: diffuse prior around first observation (or 0)
    z0 = np.zeros(n)
    first = y[0]
    obs0 = ~np.isnan(first)
    if obs0.any():
        z0[obs0] = arctanh_clip(first[obs0])
    P0 = np.eye(n) * 1.0

    zeta, P = z0, P0
    for t in range(T):
        if t > 0:
            x_prev = np.tanh(zeta)
            zeta_pred = kappa * (B @ x_prev + g * u[t - 1]) + b
            F = kappa * B * (1.0 - x_prev ** 2)[None, :]
            P_pred = F @ P @ F.T + Q
        else:
            zeta_pred, P_pred = zeta, P
        zeta_p[t], P_p[t] = zeta_pred, P_pred

        obs = ~np.isnan(y[t])
        if obs.any():
            x_pred = np.tanh(zeta_pred)
            Hd = (1.0 - x_pred ** 2)
            H = np.diag(Hd)[obs, :]
            R = Rfull[np.ix_(obs, obs)]
            innov = y[t][obs] - x_pred[obs]
            S = H @ P_pred @ H.T + R
            K = P_pred @ H.T @ np.linalg.inv(S)
            zeta = zeta_pred + K @ innov
            P = (np.eye(n) - K @ H) @ P_pred
        else:
            zeta, P = zeta_pred, P_pred
        zeta_f[t], P_f[t] = zeta, P

    # RTS smoother
    zeta_s = np.zeros_like(zeta_f)
    zeta_s[-1] = zeta_f[-1]
    P_s = P_f[-1]
    for t in range(T - 2, -1, -1):
        x_t = np.tanh(zeta_f[t])
        F = kappa * B * (1.0 - x_t ** 2)[None, :]
        P_pred = P_p[t + 1]
        G = P_f[t] @ F.T @ np.linalg.inv(P_pred)
        zeta_s[t] = zeta_f[t] + G @ (zeta_s[t + 1] - zeta_p[t + 1])
        P_s = P_f[t] + G @ (P_s - P_pred) @ G.T
    return zeta_s


def fit_kalman_person(observations: np.ndarray, u: np.ndarray, kappa: float,
                      meas_sd: float = 0.08, process_sd: float = 0.08,
                      ridge: float = 0.2, n_em: int = 3,
                      base: tuple | None = None) -> RecoveredPerson:
    """EKF-EM: alternate latent-state smoothing (E) and anchored regression
    on smoothed states (M).  Initialized at the consensus prior.
    """
    if base is None:
        base = dimension_base()
    B0, g0, dims, _k = base
    n = len(dims)
    support = B0 != 0.0

    B_hat, g_hat, b_hat = B0.copy(), g0.copy(), np.zeros(n)
    m_used = 0
    for _ in range(n_em):
        zeta_s = _ekf_smoother(observations, u, B_hat, g_hat, b_hat, kappa,
                               meas_sd, process_sd)
        x_s = np.tanh(zeta_s)
        # M-step: anchored ridge on ALL smoothed transitions
        X_cur = x_s[:-1]
        Z_next = zeta_s[1:]
        u_cur = u[:-1]
        m_used = X_cur.shape[0]
        for i in range(n):
            cols = np.where(support[i])[0]
            X = np.column_stack([X_cur[:, cols], u_cur, np.ones(m_used)])
            z = Z_next[:, i]
            p = X.shape[1]
            prior = np.concatenate([kappa * B0[i, cols], [kappa * g0[i], 0.0]])
            A = X.T @ X + ridge * np.eye(p)
            rhs = X.T @ z + ridge * prior
            beta = np.linalg.solve(A, rhs)
            B_hat[i, cols] = beta[:len(cols)] / kappa
            g_hat[i] = beta[len(cols)] / kappa
            b_hat[i] = beta[len(cols) + 1]

    return RecoveredPerson(B_hat=B_hat, g_hat=g_hat, b_hat=b_hat,
                           n_transitions=m_used, dims=list(dims))


def ekf_filter_states(y: np.ndarray, u: np.ndarray, B: np.ndarray,
                      g: np.ndarray, b: np.ndarray, kappa: float,
                      meas_sd: float, process_sd: float) -> np.ndarray:
    """Causal EKF *filter* (no smoothing): E[x_t | y_{1:t}] under given
    parameters.  The deployable direction of the state-space baseline, and
    the state layer both forecast comparators share (Step 6): with true
    parameters it is the oracle filter; with estimated parameters it is the
    explicit-pipeline filter of the implicit-vs-explicit experiment
    (transformer note 41).
    """
    T, n = y.shape
    Q = process_sd ** 2 * np.eye(n)
    Rfull = meas_sd ** 2 * np.eye(n)
    zeta = np.zeros(n)
    first = y[0]
    obs0 = ~np.isnan(first)
    if obs0.any():
        zeta[obs0] = arctanh_clip(first[obs0])
    P = np.eye(n)
    x_filt = np.zeros((T, n))
    for t in range(T):
        if t > 0:
            x_prev = np.tanh(zeta)
            zeta = kappa * (B @ x_prev + g * u[t - 1]) + b
            F = kappa * B * (1.0 - x_prev ** 2)[None, :]
            P = F @ P @ F.T + Q
        obs = ~np.isnan(y[t])
        if obs.any():
            x_pred = np.tanh(zeta)
            Hd = (1.0 - x_pred ** 2)
            H = np.diag(Hd)[obs, :]
            R = Rfull[np.ix_(obs, obs)]
            innov = y[t][obs] - x_pred[obs]
            S = H @ P @ H.T + R
            K = P @ H.T @ np.linalg.inv(S)
            zeta = zeta + K @ innov
            P = (np.eye(n) - K @ H) @ P
        x_filt[t] = np.tanh(zeta)
    return x_filt


def map_forecast(x_now: np.ndarray, u_future: np.ndarray, B: np.ndarray,
                 g: np.ndarray, b: np.ndarray, kappa: float) -> np.ndarray:
    """Deterministic h-step-ahead propagation of the generative map from a
    state estimate, using the (known-future) treatment schedule."""
    H = len(u_future)
    out = np.zeros((H, len(x_now)))
    x = x_now.copy()
    for h in range(H):
        x = np.tanh(kappa * (B @ x + g * u_future[h]) + b)
        out[h] = x
    return out


# ==========================================================================
# Dataset-level runners (mirror recover.recover_dataset)
# ==========================================================================


def baseline_recover_dataset(dataset, method: str = "bayes",
                             **kwargs) -> dict:
    """Recover every person with a Step 4 estimator.

    method: 'bayes' | 'ev' | 'kalman'.  Extra kwargs go to the fitter.
    For 'bayes', per-person coverage/width of credible intervals is added.
    """
    base = dimension_base()
    base_B = base[0]
    per_person: list[dict] = []
    for r in dataset.records:
        if method == "bayes":
            bp = fit_bayes_person(r.observations, r.u, r.params.kappa,
                                  base=base, **kwargs)
            rec = bp.as_recovered()
            m = recovery_metrics(r.params, rec, base_B=base_B)
            m.update(edge_coverage(bp, r.params.B, base_B=base_B))
        elif method == "ev":
            kwargs.setdefault("meas_sd", dataset.config.meas_noise)
            rec = fit_ev_person(r.observations, r.u, r.params.kappa,
                                base=base, **kwargs)
            m = recovery_metrics(r.params, rec, base_B=base_B)
        elif method == "kalman":
            kwargs.setdefault("meas_sd", dataset.config.meas_noise)
            kwargs.setdefault("process_sd", dataset.config.process_noise)
            rec = fit_kalman_person(r.observations, r.u, r.params.kappa,
                                    base=base, **kwargs)
            m = recovery_metrics(r.params, rec, base_B=base_B)
        else:
            raise ValueError(f"unknown method {method!r}")
        per_person.append(m)

    def agg(key: str) -> float:
        vals = [m[key] for m in per_person if key in m]
        return float(np.median(vals)) if vals else float("nan")

    aggregate = {
        "method": method,
        "n_persons": len(per_person),
        "median_transitions": agg("n_transitions"),
        "median_edge_rmse": agg("edge_rmse"),
        "median_edge_corr": agg("edge_corr"),
        "median_edge_dev_corr": agg("edge_dev_corr"),
        "median_prior_rmse": agg("prior_rmse"),
        "median_attractor_abs_err": agg("attractor_abs_err"),
        "median_rho_abs_err": agg("rho_abs_err"),
        "median_kappastar_abs_err": agg("kappastar_abs_err"),
        "regime_accuracy": float(np.mean([m["regime_match"]
                                          for m in per_person])),
    }
    if method == "bayes":
        aggregate["mean_coverage"] = float(np.mean([m["coverage"]
                                                    for m in per_person]))
        aggregate["median_ci_width"] = agg("mean_width")
    return {"per_person": per_person, "aggregate": aggregate}


# ==========================================================================
# Recovery scaling law (notes 35-36): err(T) = floor + A * T^(-beta)
# ==========================================================================


def fit_scaling_law(T_values, errors, beta_grid=None) -> dict:
    """Fit err(T) = E + A T^-beta by profiling beta over a grid (E, A by LS).

    Returns dict with E (noise floor), A, beta, sse, and the fitted curve.
    """
    T = np.asarray(T_values, dtype=float)
    y = np.asarray(errors, dtype=float)
    if beta_grid is None:
        beta_grid = np.arange(0.05, 1.51, 0.01)
    best = None
    for beta in beta_grid:
        X = np.column_stack([np.ones_like(T), T ** (-beta)])
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        E, A = float(coef[0]), float(coef[1])
        if E < 0.0:                       # floor cannot be negative
            A = float(np.sum(T ** (-beta) * y) / np.sum(T ** (-2 * beta)))
            E = 0.0
        pred = E + A * T ** (-beta)
        sse = float(np.sum((y - pred) ** 2))
        if best is None or sse < best["sse"]:
            best = {"E": E, "A": A, "beta": float(beta), "sse": sse,
                    "fitted": pred.tolist()}
    return best
