"""
Step 3 of the estimation roadmap: recover a person's dynamics from their
observed EMA series, and score the estimate against the retained ground truth.

The estimator is deliberately the interpretable baseline the roadmap calls for,
built to honour the project's own rules:

  * **Structure is fixed from theory (rule W1).**  Only the edges the consensus
    prior declares are estimated; every other entry stays zero.  Each target
    node's update is therefore a regression on a handful of predictors, which
    is what makes a 7x7 person-graph identifiable from a short series.

  * **Personalize from a strong prior (rule W7).**  Estimation is ridge
    regression that shrinks each coefficient toward the consensus prior, not
    toward zero.  With little data the estimate returns the prior; as data
    accumulate it moves to the person.  Setting ``anchor=False`` recovers the
    free (unregularized) estimator for comparison.

Because the generative nonlinearity is known (tanh), applying ``arctanh`` to the
next state linearizes the map:

    arctanh(x_{t+1}) = kappa*B x_t + kappa*g u_t + b + eps_t,

so recovery is a masked linear regression, one row per node, over the
transitions where both occasions were observed.

Identifiability notes (worth knowing before collecting data):
  * kappa and B enter only as the product kappa*B, so B is recovered up to the
    global scale kappa (assumed known here; the *effective* coupling kappa*B is
    identifiable regardless).
  * Persistent excitation is required: a perfectly quiescent, unvarying series
    carries no information about B.  Natural within-person fluctuation is the
    signal.
  * Measurement noise induces errors-in-variables attenuation that does **not**
    vanish with series length — reliability matters, not only quantity.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dynamics import iterate, jacobian_rho
from .registry import ENDO
from .simulate import PersonParams, characterize, dimension_base


def known_support(base_B: np.ndarray | None = None) -> np.ndarray:
    """Boolean mask of the consensus edge skeleton (rule W1)."""
    if base_B is None:
        base_B, _g, _dims, _k = dimension_base()
    return base_B != 0.0


def arctanh_clip(y: np.ndarray, eps: float = 1e-4) -> np.ndarray:
    return np.arctanh(np.clip(y, -1.0 + eps, 1.0 - eps))


@dataclass
class RecoveredPerson:
    B_hat: np.ndarray
    g_hat: np.ndarray
    b_hat: np.ndarray
    n_transitions: int
    dims: list[str]


def _observed_mask(obs: np.ndarray) -> np.ndarray:
    """An occasion is present iff it has no missing entries."""
    return ~np.isnan(obs).any(axis=1)


def fit_person(observations: np.ndarray, u: np.ndarray, kappa: float,
               ridge: float = 0.2, anchor: bool = True,
               base: tuple | None = None) -> RecoveredPerson:
    """Recover (B_hat, g_hat, b_hat) by structure-constrained arctanh-VAR.

    ``ridge`` is the prior strength; with ``anchor=True`` coefficients shrink
    toward the consensus prior (kappa*B_bar, kappa*g_bar, 0), i.e. rule W7.
    """
    if base is None:
        base = dimension_base()
    B0, g0, dims, _k = base
    n = len(dims)
    support = B0 != 0.0

    present = _observed_mask(observations)
    trans = np.where(present[:-1] & present[1:])[0]     # usable t -> t+1
    n_tr = int(len(trans))

    X_cur = observations[trans]                          # (m, n) predictors x_t
    Z_next = arctanh_clip(observations[trans + 1])       # (m, n) responses
    u_cur = u[trans]                                     # (m,) input

    B_hat = np.zeros((n, n))
    g_hat = np.zeros(n)
    b_hat = np.zeros(n)

    for i in range(n):
        cols = np.where(support[i])[0]                   # source nodes for row i
        # design: [x_j (j in support), u, 1]
        X = np.column_stack([X_cur[:, cols], u_cur, np.ones(n_tr)])
        z = Z_next[:, i]
        p = X.shape[1]
        # prior mean for the coefficients (kappa*B_bar on support, kappa*g_bar, 0)
        prior = np.concatenate([kappa * B0[i, cols], [kappa * g0[i], 0.0]])
        if not anchor:
            prior = np.zeros(p)
        A = X.T @ X + ridge * np.eye(p)
        rhs = X.T @ z + ridge * prior
        beta = np.linalg.solve(A, rhs)
        B_hat[i, cols] = beta[:len(cols)] / kappa
        g_hat[i] = beta[len(cols)] / kappa
        b_hat[i] = beta[len(cols) + 1]

    return RecoveredPerson(B_hat=B_hat, g_hat=g_hat, b_hat=b_hat,
                           n_transitions=n_tr, dims=dims)


def recovery_metrics(true: PersonParams, rec: RecoveredPerson,
                     base_B: np.ndarray | None = None) -> dict:
    """Score a recovered person against ground truth."""
    if base_B is None:
        base_B, _g, _d, _k = dimension_base()
    support = base_B != 0.0
    bt = true.B[support]
    bh = rec.B_hat[support]

    edge_rmse = float(np.sqrt(np.mean((bh - bt) ** 2)))
    edge_corr = float(np.corrcoef(bh, bt)[0, 1]) if np.std(bh) > 1e-9 else 0.0
    # baseline error of the prior alone (how much personalization is possible)
    prior_rmse = float(np.sqrt(np.mean((base_B[support] - bt) ** 2)))
    # personalization signal: correlation of *deviations from the prior*.
    # edge_corr is dominated by the prior's own correlation with the truth
    # (magnitudes vary more across edges than across persons), so this is the
    # honest measure of person-specific recovery.
    dh = bh - base_B[support]
    dt = bt - base_B[support]
    edge_dev_corr = (float(np.corrcoef(dh, dt)[0, 1])
                     if np.std(dh) > 1e-9 and np.std(dt) > 1e-9 else 0.0)

    rec_params = characterize(PersonParams(
        "rec", true.dims, rec.B_hat, rec.g_hat, rec.b_hat, true.kappa))
    return {
        "n_transitions": rec.n_transitions,
        "edge_rmse": edge_rmse,
        "edge_corr": edge_corr,
        "edge_dev_corr": edge_dev_corr,
        "prior_rmse": prior_rmse,
        "attractor_abs_err": abs(rec_params.attractor_dis - true.attractor_dis),
        "rho_abs_err": abs(rec_params.rho - true.rho),
        "kappastar_abs_err": abs(rec_params.kappa_star - true.kappa_star),
        "regime_match": rec_params.regime == true.regime,
        "true_regime": true.regime,
        "rec_regime": rec_params.regime,
    }


def recover_dataset(dataset, ridge: float = 0.2, anchor: bool = True) -> dict:
    """Recover every person in a dataset; return per-person + aggregate metrics."""
    base = dimension_base()
    base_B = base[0]
    per_person: list[dict] = []
    for r in dataset.records:
        rec = fit_person(r.observations, r.u, r.params.kappa,
                         ridge=ridge, anchor=anchor, base=base)
        m = recovery_metrics(r.params, rec, base_B=base_B)
        per_person.append(m)

    def agg(key: str) -> float:
        return float(np.median([m[key] for m in per_person]))

    aggregate = {
        "n_persons": len(per_person),
        "median_transitions": agg("n_transitions"),
        "median_edge_rmse": agg("edge_rmse"),
        "median_edge_corr": agg("edge_corr"),
        "median_edge_dev_corr": agg("edge_dev_corr"),
        "median_prior_rmse": agg("prior_rmse"),
        "median_attractor_abs_err": agg("attractor_abs_err"),
        "median_rho_abs_err": agg("rho_abs_err"),
        "median_kappastar_abs_err": agg("kappastar_abs_err"),
        "regime_accuracy": float(np.mean([m["regime_match"] for m in per_person])),
    }
    return {"per_person": per_person, "aggregate": aggregate}
