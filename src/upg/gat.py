"""
Step 5 of the estimation roadmap: the structure-constrained graph-attention
estimator.

Design of record (from the transformer reading notes, ``docs/transformers``):

  * **Skeleton-masked attention over variate tokens** (notes 08, 17): one
    token per dimension, each embedding that dimension's observed-series
    summary statistics; attention is masked to the published edge skeleton
    (rule W1), so the model cannot use influence paths the theory does not
    license.
  * **Multiplicative log-corrections on the prior** (notes 08, 33, 37):
    the edge readout is
        B_hat[i, j] = B_bar[i, j] * exp(delta[i, j]),
    with the readout layer zero-initialized so training *starts exactly at
    the consensus prior* (rule W7 as architecture; LoRA's init).  Support
    and sign are inherited from theory by construction, and there is **no
    softmax on the readout** — rows of B are not normalized quantities, and
    row-stochastic mixing would shrink person heterogeneity toward uniform
    (note 37's rank-collapse warning).
  * **Amortized estimation** (notes 04, 41, 42): the model is trained across
    a population of synthetic persons with known ground truth and then maps
    an unseen person's observation window to their personalized (B, g, b) in
    one forward pass — a learned, prior-informed estimator whose implicit
    shrinkage is *fit to the generative family* rather than hand-chosen.
  * **Calibrated uncertainty** (note 13; baseline contract): every edge
    ships a heteroscedastic Gaussian head in log-deviation space, so the
    estimator returns per-edge credible intervals whose empirical coverage
    is measured, not asserted.

The estimator assumes ``kappa`` known, like every estimator in this package
(only kappa*B is identifiable; see ``recover.py``).

Reproducibility: pure NumPy + the package's own gradchecked autodiff; all
RNGs seeded; training is full-batch and therefore bit-deterministic.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field

import numpy as np

from .autodiff import Adam, Tensor, concat, rms_norm, softmax_masked
from .recover import RecoveredPerson, arctanh_clip
from .simulate import STANDING_NOMINAL, dimension_base, simulate_preset

# ==========================================================================
# Window features: NaN-aware sufficient statistics of one observation window
# ==========================================================================


def _nancorr(a: np.ndarray, b: np.ndarray, min_pairs: int = 4) -> tuple[float, float]:
    """Pairwise-complete correlation and the usable-pair fraction."""
    ok = np.isfinite(a) & np.isfinite(b)
    m = int(ok.sum())
    frac = m / max(1, len(a))
    if m < min_pairs:
        return 0.0, frac
    x, y = a[ok], b[ok]
    sx, sy = x.std(), y.std()
    if sx < 1e-9 or sy < 1e-9:
        return 0.0, frac
    return float(np.corrcoef(x, y)[0, 1]), frac


def edge_list(base_B: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Fixed row-major ordering of the published support (targets, sources)."""
    tgt, src = np.nonzero(base_B)
    return tgt, src


N_NODE_FEATS = 6      # mean, sd, lag1 autocorr, missing rate, u->next corr, movement
N_EDGE_FEATS = 5      # lag1 j->i, lag1 i->j, contemporaneous, prior weight, pair frac
N_GLOBAL_FEATS = 6    # kappa, log1p(#transitions), missing frac, mean u, sd u, mean |dy|


def person_features(observations: np.ndarray, u: np.ndarray, kappa: float,
                    base_B: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute (node_feats (n,Fn), edge_feats (E,Fe), global_feats (Fg,)).

    All statistics are pairwise-complete over the window (missingness enters
    as *absence*, never as imputation), matching the measurement contract's
    rule against mean-imputation.
    """
    T, n = observations.shape
    y = observations
    tgt, src = edge_list(base_B)

    present = ~np.isnan(y).any(axis=1)
    n_trans = int(np.sum(present[:-1] & present[1:]))
    miss_frac = float(np.mean(np.isnan(y)))
    dy = np.diff(y, axis=0)
    mean_abs_dy = float(np.nanmean(np.abs(dy))) if np.isfinite(dy).any() else 0.0

    node = np.zeros((n, N_NODE_FEATS))
    for j in range(n):
        col = y[:, j]
        fin = np.isfinite(col)
        node[j, 0] = float(np.nanmean(col)) if fin.any() else 0.0
        node[j, 1] = float(np.nanstd(col)) if fin.any() else 0.0
        node[j, 2], _ = _nancorr(col[:-1], col[1:])
        node[j, 3] = float(np.mean(~fin))
        node[j, 4], _ = _nancorr(u[:-1], col[1:])
        dj = np.diff(col)
        node[j, 5] = float(np.nanmean(np.abs(dj))) if np.isfinite(dj).any() else 0.0

    E = len(tgt)
    edge = np.zeros((E, N_EDGE_FEATS))
    for e in range(E):
        i, j = int(tgt[e]), int(src[e])
        c_fwd, frac = _nancorr(y[:-1, j], y[1:, i])       # source_t -> target_{t+1}
        c_rev, _ = _nancorr(y[:-1, i], y[1:, j])          # directionality contrast
        c_now, _ = _nancorr(y[:, i], y[:, j])
        edge[e] = (c_fwd, c_rev, c_now, base_B[i, j], frac)

    glob = np.array([kappa, np.log1p(n_trans), miss_frac,
                     float(np.mean(u)), float(np.std(u)), mean_abs_dy])
    return node, edge, glob


# ==========================================================================
# Model
# ==========================================================================


@dataclass
class GATConfig:
    d_model: int = 24
    n_heads: int = 4
    d_ff: int = 32
    hidden: int = 32
    seed: int = 0
    lr: float = 3e-3
    epochs: int = 400
    patience: int = 60
    lam_abs: float = 5.0     # absolute-scale edge MSE (ties loss to benchmark)
    lam_g: float = 1.0       # treatment-gain log-deviation MSE
    lam_b: float = 5.0       # standing-condition MSE
    level: float = 0.90      # credible-interval level for coverage reporting
    sigma0: float = 0.15     # initial edge sd in log space (= population edge_sigma)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class GATPerson:
    """Amortized estimate for one person, with per-edge intervals."""
    B_hat: np.ndarray
    B_sd: np.ndarray
    B_lo: np.ndarray
    B_hi: np.ndarray
    g_hat: np.ndarray
    b_hat: np.ndarray
    n_transitions: int
    level: float
    dims: list[str] = field(default_factory=list)

    def as_recovered(self) -> RecoveredPerson:
        return RecoveredPerson(B_hat=self.B_hat, g_hat=self.g_hat,
                               b_hat=self.b_hat,
                               n_transitions=self.n_transitions,
                               dims=self.dims)


def _z_from_level(level: float) -> float:
    """Two-sided standard-normal quantile via bisection on erf (no scipy)."""
    import math
    p = 0.5 + level / 2.0
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 0.5 * (1.0 + math.erf(mid / math.sqrt(2.0))) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


class MaskedGraphAttentionEstimator:
    """Skeleton-masked attention over variate tokens -> (B_hat, g_hat, b_hat)."""

    def __init__(self, config: GATConfig | None = None, base: tuple | None = None):
        self.config = config or GATConfig()
        if base is None:
            base = dimension_base()
        self.B0, self.g0, self.dims, _k = base
        self.n = len(self.dims)
        self.tgt, self.src = edge_list(self.B0)
        self.E = len(self.tgt)
        self.g_nodes = np.where(self.g0 != 0.0)[0]
        # standing-condition support of the generative family (b lives on
        # constitution/history/environment only; exact zeros elsewhere)
        self.b_mask = np.array([1.0 if d in STANDING_NOMINAL else 0.0
                                for d in self.dims])
        # attention mask: token i attends to its theory sources and itself
        self.att_mask = ((self.B0 != 0.0) | np.eye(self.n, dtype=bool)).astype(float)
        self._build_params()
        # feature standardization (fit on the training set)
        fn = N_NODE_FEATS + self.n            # node feats + one-hot identity
        self.node_mu = np.zeros(fn); self.node_sd = np.ones(fn)
        self.edge_mu = np.zeros(N_EDGE_FEATS); self.edge_sd = np.ones(N_EDGE_FEATS)
        self.glob_mu = np.zeros(N_GLOBAL_FEATS); self.glob_sd = np.ones(N_GLOBAL_FEATS)

    # -- parameters ---------------------------------------------------------
    def _build_params(self) -> None:
        c = self.config
        rng = np.random.default_rng(c.seed)
        d, h = c.d_model, c.hidden
        fn = N_NODE_FEATS + self.n
        fe = N_EDGE_FEATS
        fg = N_GLOBAL_FEATS

        def W(*shape, scale=None):
            scale = scale if scale is not None else 1.0 / np.sqrt(shape[0])
            return Tensor(rng.normal(0.0, scale, size=shape), requires_grad=True)

        def zeros(*shape):
            return Tensor(np.zeros(shape), requires_grad=True)

        p: dict[str, Tensor] = {}
        p["W_in"] = W(fn + fg, d); p["b_in"] = zeros(d)
        p["Wq"] = W(d, d); p["Wk"] = W(d, d); p["Wv"] = W(d, d)
        p["Wo"] = W(d, d); p["g1"] = Tensor(np.ones(d), requires_grad=True)
        p["Wg"] = W(d, c.d_ff); p["Wv2"] = W(d, c.d_ff); p["W2"] = W(c.d_ff, d)
        p["g2"] = Tensor(np.ones(d), requires_grad=True)
        # edge head: [h_tgt, h_src, edge_feats, glob] -> hidden -> (mu, s_raw)
        p["We1"] = W(2 * d + fe + fg, h); p["be1"] = zeros(h)
        p["We2"] = zeros(h, 2); p["be2"] = zeros(2)          # zero-init: start at prior
        # gain head: [h_node, glob] -> hidden -> delta_g
        p["Wg1"] = W(d + fg, h); p["bg1"] = zeros(h)
        p["Wg2"] = zeros(h, 1); p["bg2"] = zeros(1)          # zero-init: g_hat = g_bar
        # standing-condition head: [h_node, glob] -> hidden -> raw,
        # b = relu(raw) * b_mask  — exact zeros attainable (bistability needs
        # b = 0 exactly; a softplus floor would erase the low attractor)
        p["Wb1"] = W(d + fg, h); p["bb1"] = zeros(h)
        p["Wb2"] = zeros(h, 1)
        p["bb2"] = Tensor(np.array([0.05]), requires_grad=True)   # start alive
        # sigma offset so initial interval width matches the population prior
        p["be2"].data[1] = np.log(np.expm1(c.sigma0))             # softplus^-1(sigma0)
        self.params = p

    def param_list(self) -> list[Tensor]:
        return [self.params[k] for k in sorted(self.params)]

    # -- forward -------------------------------------------------------------
    def _forward(self, node_f: np.ndarray, edge_f: np.ndarray,
                 glob_f: np.ndarray):
        """Batched forward.  Shapes: node (P,n,Fn'), edge (P,E,Fe), glob (P,Fg).
        Returns Tensors mu (P,E), sigma (P,E), dg (P,|g_nodes|), b_hat (P,n)."""
        p = self.params
        c = self.config
        P = node_f.shape[0]
        d, H = c.d_model, c.n_heads
        dk = d // H

        glob_t = Tensor(glob_f)                                   # (P,Fg)
        glob_nodes = Tensor(np.broadcast_to(
            glob_f[:, None, :], (P, self.n, glob_f.shape[1])).copy())
        x_in = concat([Tensor(node_f), glob_nodes], axis=-1)      # (P,n,Fn+Fg)
        h0 = (x_in @ p["W_in"]) + p["b_in"]                       # (P,n,d)

        # masked multi-head attention over variate tokens (pre-norm residual)
        hn = rms_norm(h0, p["g1"])
        q = (hn @ p["Wq"]).reshape(P, self.n, H, dk).transpose((0, 2, 1, 3))
        k = (hn @ p["Wk"]).reshape(P, self.n, H, dk).transpose((0, 2, 1, 3))
        v = (hn @ p["Wv"]).reshape(P, self.n, H, dk).transpose((0, 2, 1, 3))
        logits = (q @ k.transpose((0, 1, 3, 2))) * (1.0 / np.sqrt(dk))
        att = softmax_masked(logits, self.att_mask)               # (P,H,n,n)
        mixed = (att @ v).transpose((0, 2, 1, 3)).reshape(P, self.n, d)
        h1 = h0 + (mixed @ p["Wo"])

        # SwiGLU feed-forward (pre-norm residual)
        hn2 = rms_norm(h1, p["g2"])
        ff = ((hn2 @ p["Wg"]).silu() * (hn2 @ p["Wv2"])) @ p["W2"]
        h2 = h1 + ff                                              # (P,n,d)

        # edge readout (no softmax; unnormalized log-corrections)
        h_tgt = h2[:, self.tgt, :]                                # (P,E,d)
        h_src = h2[:, self.src, :]
        glob_edges = Tensor(np.broadcast_to(
            glob_f[:, None, :], (P, self.E, glob_f.shape[1])).copy())
        e_in = concat([h_tgt, h_src, Tensor(edge_f), glob_edges], axis=-1)
        e_h = ((e_in @ p["We1"]) + p["be1"]).leaky_relu(0.2)
        e_out = (e_h @ p["We2"]) + p["be2"]                       # (P,E,2)
        mu = e_out[:, :, 0]
        sigma = e_out[:, :, 1].softplus() + 1e-3

        # node readouts
        n_in = concat([h2, glob_nodes], axis=-1)                  # (P,n,d+Fg)
        gh = ((n_in @ p["Wg1"]) + p["bg1"]).leaky_relu(0.2)
        dg_all = ((gh @ p["Wg2"]) + p["bg2"])[:, :, 0]            # (P,n)
        dg = dg_all[:, self.g_nodes]                              # (P,|g|)
        bh = ((n_in @ p["Wb1"]) + p["bb1"]).leaky_relu(0.2)
        b_raw = (((bh @ p["Wb2"]) + p["bb2"])[:, :, 0]).leaky_relu(0.0)
        b_hat = b_raw * Tensor(self.b_mask[None, :])              # (P,n)

        return mu, sigma, dg, b_hat

    # -- feature preparation ---------------------------------------------------
    def _prep(self, feats: list[tuple[np.ndarray, np.ndarray, np.ndarray]]):
        """Stack per-person features, add node identity, standardize."""
        node = np.stack([f[0] for f in feats])                    # (P,n,Fn)
        edge = np.stack([f[1] for f in feats])                    # (P,E,Fe)
        glob = np.stack([f[2] for f in feats])                    # (P,Fg)
        P = node.shape[0]
        eye = np.broadcast_to(np.eye(self.n), (P, self.n, self.n))
        node = np.concatenate([node, eye], axis=-1)               # identity one-hot
        node = (node - self.node_mu) / self.node_sd
        edge = (edge - self.edge_mu) / self.edge_sd
        glob = (glob - self.glob_mu) / self.glob_sd
        return node, edge, glob

    def _fit_standardizer(self, feats) -> None:
        node = np.stack([f[0] for f in feats])
        edge = np.stack([f[1] for f in feats])
        glob = np.stack([f[2] for f in feats])
        P = node.shape[0]
        eye = np.broadcast_to(np.eye(self.n), (P, self.n, self.n))
        node = np.concatenate([node, eye], axis=-1)
        self.node_mu = node.reshape(-1, node.shape[-1]).mean(axis=0)
        self.node_sd = node.reshape(-1, node.shape[-1]).std(axis=0) + 1e-6
        self.edge_mu = edge.reshape(-1, edge.shape[-1]).mean(axis=0)
        self.edge_sd = edge.reshape(-1, edge.shape[-1]).std(axis=0) + 1e-6
        self.glob_mu = glob.mean(axis=0)
        self.glob_sd = glob.std(axis=0) + 1e-6

    # -- loss -------------------------------------------------------------------
    def _loss(self, batch) -> Tensor:
        node, edge, glob, t_edge, t_g, t_b = batch
        c = self.config
        mu, sigma, dg, b_hat = self._forward(node, edge, glob)
        te = Tensor(t_edge)
        z = (te - mu) / sigma
        nll = (z * z * 0.5 + sigma.log()).mean()
        prior_edges = self.B0[self.tgt, self.src][None, :]        # (1,E)
        B_pred = Tensor(prior_edges) * mu.exp()
        B_true = Tensor(prior_edges * np.exp(t_edge))
        abs_mse = ((B_pred - B_true) * (B_pred - B_true)).mean()
        g_mse = ((dg - Tensor(t_g)) * (dg - Tensor(t_g))).mean()
        b_mse = ((b_hat - Tensor(t_b)) * (b_hat - Tensor(t_b))).mean()
        return nll + c.lam_abs * abs_mse + c.lam_g * g_mse + c.lam_b * b_mse

    # -- training -----------------------------------------------------------------
    def fit(self, train_examples, val_examples, verbose: bool = True) -> dict:
        """Full-batch Adam with early stopping on the validation loss.

        ``examples`` are tuples (features, targets) built by
        ``build_training_set``.  Deterministic given the config seed.
        """
        c = self.config
        feats_tr = [e[0] for e in train_examples]
        self._fit_standardizer(feats_tr)
        batch_tr = self._make_batch(train_examples)
        batch_va = self._make_batch(val_examples)

        opt = Adam(self.param_list(), lr=c.lr)
        # Seed early stopping with the *initial* state (= the consensus prior,
        # by zero-init): training can therefore never end worse than the prior
        # on validation — rule W7 as a training guarantee.
        best_val = float(self._loss(batch_va).data)
        best_state = self._state_dict()
        best_epoch = -1
        history = [{"epoch": -1, "train": float("nan"), "val": best_val}]
        for epoch in range(c.epochs):
            opt.zero_grad()
            loss = self._loss(batch_tr)
            loss.backward()
            opt.step()
            val = float(self._loss(batch_va).data)
            history.append({"epoch": epoch, "train": float(loss.data), "val": val})
            if val < best_val - 1e-6:
                best_val, best_epoch = val, epoch
                best_state = self._state_dict()
            if epoch - best_epoch >= c.patience:
                break
            if verbose and epoch % 50 == 0:
                print(f"  epoch {epoch:4d}  train {float(loss.data):.4f}  val {val:.4f}",
                      flush=True)
        self._load_state(best_state)
        return {"best_val": best_val, "best_epoch": best_epoch,
                "epochs_run": len(history), "history": history}

    def _make_batch(self, examples):
        feats = [e[0] for e in examples]
        node, edge, glob = self._prep(feats)
        t_edge = np.stack([e[1]["t_edge"] for e in examples])
        t_g = np.stack([e[1]["t_g"] for e in examples])
        t_b = np.stack([e[1]["t_b"] for e in examples])
        return node, edge, glob, t_edge, t_g, t_b

    # -- inference ------------------------------------------------------------------
    def estimate(self, observations: np.ndarray, u: np.ndarray,
                 kappa: float) -> GATPerson:
        node_f, edge_f, glob_f = person_features(observations, u, kappa, self.B0)
        node, edge, glob = self._prep([(node_f, edge_f, glob_f)])
        mu, sigma, dg, b_hat = self._forward(node, edge, glob)
        mu = mu.data[0]; sigma = sigma.data[0]
        dg = dg.data[0]; b_vec = b_hat.data[0]

        B_hat = np.zeros_like(self.B0)
        B_sd = np.zeros_like(self.B0)
        B_lo = np.zeros_like(self.B0)
        B_hi = np.zeros_like(self.B0)
        prior = self.B0[self.tgt, self.src]
        z = _z_from_level(self.config.level)
        B_hat[self.tgt, self.src] = prior * np.exp(mu)
        B_sd[self.tgt, self.src] = prior * np.exp(mu) * sigma     # delta-method sd
        B_lo[self.tgt, self.src] = prior * np.exp(mu - z * sigma)
        B_hi[self.tgt, self.src] = prior * np.exp(mu + z * sigma)

        g_hat = self.g0.copy()
        g_hat[self.g_nodes] = self.g0[self.g_nodes] * np.exp(dg)

        present = ~np.isnan(observations).any(axis=1)
        n_tr = int(np.sum(present[:-1] & present[1:]))
        return GATPerson(B_hat=B_hat, B_sd=B_sd, B_lo=B_lo, B_hi=B_hi,
                         g_hat=g_hat, b_hat=b_vec, n_transitions=n_tr,
                         level=self.config.level, dims=list(self.dims))

    # -- persistence -------------------------------------------------------------------
    def _state_dict(self) -> dict[str, np.ndarray]:
        return {k: v.data.copy() for k, v in self.params.items()}

    def _load_state(self, state: dict[str, np.ndarray]) -> None:
        for k, v in state.items():
            self.params[k].data = v.copy()

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        arrays = {f"p_{k}": v.data for k, v in self.params.items()}
        arrays.update(node_mu=self.node_mu, node_sd=self.node_sd,
                      edge_mu=self.edge_mu, edge_sd=self.edge_sd,
                      glob_mu=self.glob_mu, glob_sd=self.glob_sd)
        np.savez_compressed(path, config=json.dumps(self.config.as_dict()),
                            **arrays)

    @classmethod
    def load(cls, path: str) -> "MaskedGraphAttentionEstimator":
        z = np.load(path, allow_pickle=False)
        config = GATConfig(**json.loads(str(z["config"])))
        model = cls(config=config)
        for k in model.params:
            model.params[k].data = z[f"p_{k}"]
        model.node_mu, model.node_sd = z["node_mu"], z["node_sd"]
        model.edge_mu, model.edge_sd = z["edge_mu"], z["edge_sd"]
        model.glob_mu, model.glob_sd = z["glob_mu"], z["glob_sd"]
        return model


# ==========================================================================
# Training-set construction (amortized protocol, notes 04/42)
# ==========================================================================


def build_training_set(preset: str, n_persons: int, seed: int,
                       T_grid=(30, 60, 120, 250), base: tuple | None = None):
    """Simulate a training population and package (features, targets).

    Each person is simulated once at every T in the grid (fresh noise and
    missingness draws per length — note 06's dynamic-masking discipline), so
    one model learns the whole data-budget range and can modulate its own
    shrinkage with the amount of data it sees (note 41's learned
    preconditioning).
    """
    if base is None:
        base = dimension_base()
    base_B, g0, dims, _k = base
    tgt, src = edge_list(base_B)
    g_nodes = np.where(g0 != 0.0)[0]

    examples = []
    for gi, T in enumerate(T_grid):
        ds = simulate_preset(preset, n_persons=n_persons, T=int(T),
                             seed=seed + 17 * gi)
        for r in ds.records:
            feats = person_features(r.observations, r.u, r.params.kappa, base_B)
            t_edge = np.log(r.params.B[tgt, src] / base_B[tgt, src])
            t_g = np.log(r.params.g[g_nodes] / g0[g_nodes])
            targets = {"t_edge": t_edge, "t_g": t_g, "t_b": r.params.b.copy()}
            examples.append((feats, targets))
    return examples


# ==========================================================================
# Dataset-level evaluation (mirrors baselines.baseline_recover_dataset)
# ==========================================================================


def gat_recover_dataset(dataset, model: MaskedGraphAttentionEstimator) -> dict:
    """Estimate every person in a dataset; per-person + aggregate metrics,
    including credible-interval coverage on the true edges."""
    from .recover import recovery_metrics
    base_B = model.B0
    sup = base_B != 0.0
    per_person: list[dict] = []
    for r in dataset.records:
        gp = model.estimate(r.observations, r.u, r.params.kappa)
        m = recovery_metrics(r.params, gp.as_recovered(), base_B=base_B)
        inside = (r.params.B[sup] >= gp.B_lo[sup]) & (r.params.B[sup] <= gp.B_hi[sup])
        m["coverage"] = float(np.mean(inside))
        m["mean_width"] = float(np.mean(gp.B_hi[sup] - gp.B_lo[sup]))
        per_person.append(m)

    def agg(key: str) -> float:
        vals = [m[key] for m in per_person if key in m]
        return float(np.median(vals)) if vals else float("nan")

    aggregate = {
        "method": "gat",
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
        "mean_coverage": float(np.mean([m["coverage"] for m in per_person])),
        "median_ci_width": agg("mean_width"),
    }
    return {"per_person": per_person, "aggregate": aggregate}


def deviation_rank_spectrum(examples, base: tuple | None = None) -> dict:
    """The registered LoRA experiment (note 33): SVD of the population's true
    deviations B - B_bar on the support.  Reports the singular-value spectrum
    and the effective rank exp(H(sigma_i^2 / sum))."""
    if base is None:
        base = dimension_base()
    base_B = base[0]
    tgt, src = edge_list(base_B)
    prior = base_B[tgt, src]
    devs = np.stack([prior * np.exp(e[1]["t_edge"]) - prior for e in examples])
    s = np.linalg.svd(devs - devs.mean(axis=0), compute_uv=False)
    p = s ** 2 / np.sum(s ** 2)
    p = p[p > 1e-12]
    eff_rank = float(np.exp(-np.sum(p * np.log(p))))
    return {"singular_values": s.tolist(), "effective_rank": eff_rank,
            "n_edges": len(prior), "n_examples": devs.shape[0]}
