"""
Step 6 of the estimation roadmap: a small causal temporal transformer as
(i) measurement model — filtered node activations x_hat(t) with calibrated
uncertainty from partially missing EMA — and (ii) forecaster — one-shot
multi-horizon predictions whose implied crossing probabilities are a
testable early-warning signal.

Every architectural choice is the one registered in ``docs/transformers``:

  * causal decoder-style encoder, next-step/multi-horizon Gaussian NLL
    (notes 01, 03, 13): filtering, the clinically deployable direction;
  * missingness embeddings, not imputation (note 02): unanswered occasions
    enter as mask embeddings, values zeroed;
  * ALiBi relative-time biases, no positional embeddings (note 30): the
    estimator cannot condition on absolute study time, and the geometric
    slope spectrum matches the rho(J)^k decay of influence near attractors;
  * RMSNorm pre-norm blocks (note 31), SwiGLU feed-forward (note 32),
    residuals everywhere (note 37's rank-collapse theorem);
  * one trunk, typed heads (note 05): reconstruction/filter head, direct
    multi-horizon forecast head with known-future treatment inputs
    (notes 13/14 — no recursive rollout), and a person-level dynamics head
    (rho, kappa*, regime) off a mean-pooled summary (note 11's CLS pattern);
  * training across a synthetic population, evaluation on unseen persons =
    amortized personalization (notes 04, 41, 42).

Supervision uses the simulator's retained ground truth (true latent states,
rho, regime) — this is Layer-1 method recovery, where knowing the answers is
the point.  On real data the reconstruction target becomes held-out items
and the forecast target future observations; the architecture is unchanged.

Registered diagnostics implemented here: attention entropy as effective
context (note 27), the layer rank-residual monitor (note 37), the
uniform-attention null (note 14), and the in-context score (note 40).
Pure NumPy on the package's gradchecked autodiff; deterministic given seeds.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass

import numpy as np

from .autodiff import Adam, Tensor, concat, rms_norm, softmax_masked
from .simulate import REGIME_ORDER

# ==========================================================================
# Config and containers
# ==========================================================================


@dataclass
class ForecastConfig:
    n_dims: int = 7
    d_model: int = 32
    n_heads: int = 4
    n_layers: int = 2
    d_ff: int = 48
    horizon: int = 5
    seed: int = 0
    lr: float = 3e-3
    epochs: int = 150
    patience: int = 25
    batch_size: int = 32
    lam_recon: float = 1.0
    lam_forecast: float = 1.0
    lam_dyn: float = 0.5
    channel_independent: bool = False   # the PatchTST null (note 16)
    level: float = 0.90

    def as_dict(self) -> dict:
        return asdict(self)


def alibi_biases(n_heads: int, T: int) -> np.ndarray:
    """(H, T, T) constant causal biases  -m_h * (t - s), s <= t (note 30)."""
    slopes = 2.0 ** (-8.0 * (np.arange(n_heads) + 1) / n_heads)
    t = np.arange(T)
    dist = t[:, None] - t[None, :]
    return -slopes[:, None, None] * np.maximum(dist, 0)[None, :, :]


def causal_mask(T: int) -> np.ndarray:
    return np.tril(np.ones((T, T)))


# ==========================================================================
# Model
# ==========================================================================


class TemporalTransformer:
    """Causal trunk + typed heads over EMA sequences."""

    def __init__(self, config: ForecastConfig | None = None):
        self.config = config or ForecastConfig()
        c = self.config
        self.nc = 1 if c.channel_independent else c.n_dims
        self._build_params()

    def _build_params(self) -> None:
        c = self.config
        rng = np.random.default_rng(c.seed)
        d, nc, H = c.d_model, self.nc, c.horizon

        def W(*shape, scale=None):
            scale = scale if scale is not None else 1.0 / np.sqrt(shape[0])
            return Tensor(rng.normal(0.0, scale, size=shape), requires_grad=True)

        def zeros(*shape):
            return Tensor(np.zeros(shape), requires_grad=True)

        p: dict[str, Tensor] = {}
        # token embedding: values (masked), missingness pattern, u, kappa
        p["W_val"] = W(nc, d); p["W_msk"] = W(nc, d)
        p["w_u"] = W(1, d); p["w_kap"] = W(1, d); p["b_tok"] = zeros(d)
        for layer in range(c.n_layers):
            s = f"L{layer}_"
            p[s + "g1"] = Tensor(np.ones(d), requires_grad=True)
            p[s + "Wq"] = W(d, d); p[s + "Wk"] = W(d, d); p[s + "Wv"] = W(d, d)
            p[s + "Wo"] = W(d, d)
            p[s + "g2"] = Tensor(np.ones(d), requires_grad=True)
            p[s + "Wg"] = W(d, c.d_ff); p[s + "Wv2"] = W(d, c.d_ff)
            p[s + "W2"] = W(c.d_ff, d)
        p["g_out"] = Tensor(np.ones(d), requires_grad=True)
        # heads
        p["W_rec"] = zeros(d, 2 * nc); p["b_rec"] = zeros(2 * nc)
        p["W_for"] = zeros(d + H, 2 * nc * H); p["b_for"] = zeros(2 * nc * H)
        p["W_dyn1"] = W(d, 24); p["b_dyn1"] = zeros(24)
        p["W_dyn2"] = zeros(24, 2 + len(REGIME_ORDER)); p["b_dyn2"] = zeros(2 + len(REGIME_ORDER))
        self.params = p

    def param_list(self) -> list[Tensor]:
        return [self.params[k] for k in sorted(self.params)]

    # -- trunk ---------------------------------------------------------------
    def _trunk(self, y0: np.ndarray, msk: np.ndarray, u: np.ndarray,
               kappa: np.ndarray, uniform_attention: bool = False):
        """y0 (P,T,nc) NaN->0, msk (P,T,nc) 1=observed, u (P,T), kappa (P,).

        Returns (h (P,T,d) Tensor, diagnostics dict of constants)."""
        p, c = self.params, self.config
        P, T, _ = y0.shape
        d, Hh = c.d_model, c.n_heads
        dk = d // Hh

        u3 = u[:, :, None]
        kap3 = np.broadcast_to(kappa[:, None, None], (P, T, 1)).copy()
        h = (Tensor(y0 * msk) @ p["W_val"] + Tensor(msk) @ p["W_msk"]
             + Tensor(u3) @ p["w_u"] + Tensor(kap3) @ p["w_kap"] + p["b_tok"])

        mask = causal_mask(T)
        bias = Tensor(alibi_biases(Hh, T))
        diags = {"attn_entropy": [], "rank_residual": []}
        for layer in range(c.n_layers):
            s = f"L{layer}_"
            hn = rms_norm(h, p[s + "g1"])
            q = (hn @ p[s + "Wq"]).reshape(P, T, Hh, dk).transpose((0, 2, 1, 3))
            k = (hn @ p[s + "Wk"]).reshape(P, T, Hh, dk).transpose((0, 2, 1, 3))
            v = (hn @ p[s + "Wv"]).reshape(P, T, Hh, dk).transpose((0, 2, 1, 3))
            logits = (q @ k.transpose((0, 1, 3, 2))) * (1.0 / np.sqrt(dk)) + bias
            att = softmax_masked(logits, mask)
            if uniform_attention:                     # note 14's null
                att = Tensor(np.broadcast_to(
                    mask / np.maximum(mask.sum(axis=-1, keepdims=True), 1.0),
                    att.shape).copy())
            aw = att.data
            ent = -np.sum(aw * np.log(aw + 1e-12), axis=-1)      # (P,H,T)
            diags["attn_entropy"].append(float(np.mean(np.exp(ent))))
            mixed = (att @ v).transpose((0, 2, 1, 3)).reshape(P, T, d)
            h = h + (mixed @ p[s + "Wo"])
            hn2 = rms_norm(h, p[s + "g2"])
            ff = ((hn2 @ p[s + "Wg"]).silu() * (hn2 @ p[s + "Wv2"])) @ p[s + "W2"]
            h = h + ff
            hd = h.data
            mean_tok = hd.mean(axis=1, keepdims=True)
            res = np.linalg.norm(hd - mean_tok) / (np.linalg.norm(hd) + 1e-12)
            diags["rank_residual"].append(float(res))            # note 37
        return rms_norm(h, p["g_out"]), diags

    # -- heads ------------------------------------------------------------------
    def _heads(self, h: Tensor, u_future: np.ndarray):
        """h (P,T,d); u_future (P,T,H) known-future treatment (TFT typing).

        Returns recon (mu, sigma) each (P,T,nc); forecast (mu, sigma) each
        (P,T,H,nc); dyn (rho, kstar, regime_logits)."""
        p, c = self.params, self.config
        P, T, d = h.shape
        nc, H = self.nc, c.horizon

        rec = (h @ p["W_rec"]) + p["b_rec"]
        rec_mu = rec[:, :, :nc]
        rec_sd = rec[:, :, nc:].softplus() + 1e-3

        fin = concat([h, Tensor(u_future)], axis=-1)
        fo = (fin @ p["W_for"]) + p["b_for"]                     # (P,T,2*nc*H)
        fo = fo.reshape(P, T, 2 * nc, H).transpose((0, 1, 3, 2))  # (P,T,H,2nc)
        for_mu = fo[:, :, :, :nc]
        for_sd = fo[:, :, :, nc:].softplus() + 1e-3

        pooled = h.mean(axis=1)                                  # (P,d)
        dyn = ((pooled @ p["W_dyn1"] + p["b_dyn1"]).leaky_relu(0.2)
               @ p["W_dyn2"]) + p["b_dyn2"]                      # (P,2+3)
        rho_hat = dyn[:, 0].sigmoid() * 1.2                      # rho in [0,1.2)
        kstar_hat = dyn[:, 1].softplus()
        regime_logits = dyn[:, 2:]
        return (rec_mu, rec_sd), (for_mu, for_sd), (rho_hat, kstar_hat,
                                                    regime_logits)

    def forward(self, batch: dict, uniform_attention: bool = False):
        h, diags = self._trunk(batch["y0"], batch["msk"], batch["u"],
                               batch["kappa"], uniform_attention)
        return self._heads(h, batch["u_future"]), diags

    # -- loss -----------------------------------------------------------------------
    def loss(self, batch: dict, outputs=None) -> Tensor:
        c = self.config
        if outputs is None:
            outputs, _ = self.forward(batch)
        (rec_mu, rec_sd), (for_mu, for_sd), (rho_h, ks_h, reg_lg) = outputs

        x_true = Tensor(batch["x_true"])                          # (P,T,nc)
        z = (x_true - rec_mu) / rec_sd
        recon_nll = (z * z * 0.5 + rec_sd.log()).mean()

        xf = Tensor(batch["x_future"])                            # (P,T,H,nc)
        vm = batch["valid"][:, :, :, None]                        # (P,T,H,1)
        zf = (xf - for_mu) / for_sd
        nll_terms = (zf * zf * 0.5 + for_sd.log()) * Tensor(vm)
        forecast_nll = nll_terms.sum() * (1.0 / max(vm.sum() * self.nc, 1.0))

        rho_t = Tensor(batch["rho"])
        ks_t = Tensor(batch["kappa_star"])
        dr = rho_h - rho_t
        dk_ = ks_h - ks_t
        m = np.max(reg_lg.data, axis=-1, keepdims=True)
        lse = Tensor(m[:, 0]) + ((reg_lg - Tensor(m)).exp().sum(axis=-1)).log()
        picked = (reg_lg * Tensor(batch["regime_onehot"])).sum(axis=-1)
        ce = (lse - picked).mean()
        dyn_loss = (dr * dr).mean() + (dk_ * dk_).mean() + ce

        return (c.lam_recon * recon_nll + c.lam_forecast * forecast_nll
                + c.lam_dyn * dyn_loss)

    # -- training -----------------------------------------------------------------------
    def fit(self, train_batchable: dict, val_batchable: dict,
            verbose: bool = True) -> dict:
        c = self.config
        rng = np.random.default_rng(c.seed + 999)
        P = train_batchable["y0"].shape[0]
        opt = Adam(self.param_list(), lr=c.lr)

        best_val = self._eval_loss(val_batchable)
        best_state = {k: v.data.copy() for k, v in self.params.items()}
        best_epoch = -1
        history = [{"epoch": -1, "val": best_val}]
        for epoch in range(c.epochs):
            order = rng.permutation(P)
            tr_losses = []
            for start in range(0, P, c.batch_size):
                idx = order[start:start + c.batch_size]
                sub = _index_batch(train_batchable, idx)
                opt.zero_grad()
                loss = self.loss(sub)
                loss.backward()
                opt.step()
                tr_losses.append(float(loss.data))
            val = self._eval_loss(val_batchable)
            history.append({"epoch": epoch, "train": float(np.mean(tr_losses)),
                            "val": val})
            if val < best_val - 1e-6:
                best_val, best_epoch = val, epoch
                best_state = {k: v.data.copy() for k, v in self.params.items()}
            if epoch - best_epoch >= c.patience:
                break
            if verbose and epoch % 10 == 0:
                print(f"  epoch {epoch:4d}  train {np.mean(tr_losses):.4f}  "
                      f"val {val:.4f}", flush=True)
        for k, v in best_state.items():
            self.params[k].data = v.copy()
        return {"best_val": best_val, "best_epoch": best_epoch,
                "epochs_run": len(history) - 1, "history": history}

    def _eval_loss(self, batchable: dict, chunk: int = 32) -> float:
        P = batchable["y0"].shape[0]
        tot, cnt = 0.0, 0
        for start in range(0, P, chunk):
            idx = np.arange(start, min(start + chunk, P))
            sub = _index_batch(batchable, idx)
            tot += float(self.loss(sub).data) * len(idx)
            cnt += len(idx)
        return tot / max(cnt, 1)

    # -- persistence -----------------------------------------------------------------------
    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        arrays = {f"p_{k}": v.data for k, v in self.params.items()}
        np.savez_compressed(path, config=json.dumps(self.config.as_dict()),
                            **arrays)

    @classmethod
    def load(cls, path: str) -> "TemporalTransformer":
        z = np.load(path, allow_pickle=False)
        model = cls(ForecastConfig(**json.loads(str(z["config"]))))
        for k in model.params:
            model.params[k].data = z[f"p_{k}"]
        return model


def _index_batch(batchable: dict, idx: np.ndarray) -> dict:
    return {k: v[idx] for k, v in batchable.items()}


# ==========================================================================
# Batch construction from a SyntheticDataset
# ==========================================================================


def make_batches(dataset, horizon: int, channel_independent: bool = False) -> dict:
    """Package a SyntheticDataset into dense arrays for the model.

    Targets are the simulator's true latent states (Layer-1 supervision).
    ``channel_independent=True`` reshapes persons x channels into separate
    scalar sequences sharing the treatment input — the PatchTST null.
    """
    T = dataset.config.T
    recs = dataset.records
    y = np.stack([r.observations for r in recs])            # (P,T,n)
    x = np.stack([r.states for r in recs])
    u = np.stack([r.u for r in recs])
    kappa = np.array([r.params.kappa for r in recs])
    rho = np.array([r.params.rho for r in recs])
    ks = np.array([r.params.kappa_star for r in recs])
    reg = np.zeros((len(recs), len(REGIME_ORDER)))
    for i, r in enumerate(recs):
        reg[i, REGIME_ORDER.index(r.params.regime)] = 1.0

    if channel_independent:
        P, _, n = y.shape
        y = y.transpose(0, 2, 1).reshape(P * n, T, 1)
        x = x.transpose(0, 2, 1).reshape(P * n, T, 1)
        u = np.repeat(u, n, axis=0)
        kappa = np.repeat(kappa, n)
        rho = np.repeat(rho, n)
        ks = np.repeat(ks, n)
        reg = np.repeat(reg, n, axis=0)

    msk = (~np.isnan(y)).astype(float)
    y0 = np.nan_to_num(y, nan=0.0)

    P2, _, nc = y.shape
    H = horizon
    x_future = np.zeros((P2, T, H, nc))
    u_future = np.zeros((P2, T, H))
    valid = np.zeros((P2, T, H))
    for h in range(1, H + 1):
        upto = T - h
        x_future[:, :upto, h - 1, :] = x[:, h:, :]
        u_future[:, :upto, h - 1] = u[:, h:]
        valid[:, :upto, h - 1] = 1.0

    return {"y0": y0, "msk": msk, "u": u, "kappa": kappa,
            "x_true": x, "x_future": x_future, "u_future": u_future,
            "valid": valid, "rho": rho, "kappa_star": ks,
            "regime_onehot": reg}


# ==========================================================================
# Evaluation utilities
# ==========================================================================


def normal_cdf(z: np.ndarray) -> np.ndarray:
    from math import erf, sqrt
    return np.vectorize(lambda v: 0.5 * (1.0 + erf(v / sqrt(2.0))))(z)


def auc_score(labels: np.ndarray, scores: np.ndarray) -> float:
    """Rank-based AUC (Mann-Whitney), NaN-safe."""
    ok = np.isfinite(scores)
    labels, scores = labels[ok].astype(bool), scores[ok]
    n1, n0 = int(labels.sum()), int((~labels).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores))
    sorted_scores = scores[order]
    i = 0
    r = np.arange(1, len(scores) + 1, dtype=float)
    while i < len(scores):                       # average ranks over ties
        j = i
        while j + 1 < len(scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        r[i:j + 1] = 0.5 * (i + 1 + j + 1)
        i = j + 1
    ranks[order] = r
    return float((ranks[labels].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def evaluate_model(model: TemporalTransformer, batch: dict,
                   dis_index: int = 5, cross_level: float = 0.5,
                   uniform_attention: bool = False) -> dict:
    """Contract metrics for one evaluation population.

    Includes: filter RMSE (all + missing-only occasions) and coverage;
    per-horizon forecast RMSE/NLL/coverage; regime/rho/kappa* from the
    dynamics head; DIS threshold-crossing early warning (AUC both
    directions); attention diagnostics; the in-context score (note 40).
    """
    c = model.config
    z = _z_from_level(c.level)
    outputs, diags = model.forward(batch, uniform_attention=uniform_attention)
    (rec_mu, rec_sd), (for_mu, for_sd), (rho_h, ks_h, reg_lg) = outputs
    rec_mu, rec_sd = rec_mu.data, rec_sd.data
    for_mu, for_sd = for_mu.data, for_sd.data

    x = batch["x_true"]
    err = rec_mu - x
    obs_any = batch["msk"] > 0
    filter_rmse = float(np.sqrt(np.mean(err ** 2)))
    miss = ~obs_any
    filter_rmse_missing = (float(np.sqrt(np.mean(err[miss] ** 2)))
                           if miss.any() else float("nan"))
    inside = np.abs(err) <= z * rec_sd
    filter_coverage = float(np.mean(inside))

    xf, valid = batch["x_future"], batch["valid"].astype(bool)
    fe = for_mu - xf
    per_h = {}
    for h in range(c.horizon):
        v = valid[:, :, h]
        e = fe[:, :, h, :][v]
        sd = for_sd[:, :, h, :][v]
        tgt = xf[:, :, h, :][v]
        mu = for_mu[:, :, h, :][v]
        nll = float(np.mean(0.5 * ((tgt - mu) / sd) ** 2 + np.log(sd)))
        per_h[h + 1] = {
            "rmse": float(np.sqrt(np.mean(e ** 2))),
            "nll": nll,
            "coverage": float(np.mean(np.abs(e) <= z * sd)),
        }

    # persistence null: carry the last observed value forward
    y0, msk = batch["y0"], batch["msk"]
    P, T, nc = y0.shape
    last = np.zeros((P, T, nc))
    carry = np.zeros((P, nc))
    seen = np.zeros((P, nc), dtype=bool)
    for t in range(T):
        m = msk[:, t, :] > 0
        carry = np.where(m, y0[:, t, :], carry)
        seen |= m
        last[:, t, :] = np.where(seen, carry, 0.0)
    pers = {}
    for h in range(c.horizon):
        v = valid[:, :, h]
        e = last[:, :, None, :].repeat(c.horizon, axis=2)[:, :, h, :][v] \
            - xf[:, :, h, :][v]
        pers[h + 1] = float(np.sqrt(np.mean(e ** 2)))

    # dynamics head
    rho_mae = float(np.mean(np.abs(rho_h.data - batch["rho"])))
    ks_mae = float(np.mean(np.abs(ks_h.data - batch["kappa_star"])))
    regime_acc = float(np.mean(np.argmax(reg_lg.data, axis=-1)
                               == np.argmax(batch["regime_onehot"], axis=-1)))

    # early warning: P(DIS crosses `cross_level` within the horizon)
    warn = {}
    if not model.config.channel_independent:
        di = dis_index
        below = x[:, :, di] < cross_level
        truth_up = np.zeros((P, T), dtype=bool)
        truth_dn = np.zeros((P, T), dtype=bool)
        for h in range(1, c.horizon + 1):
            fut = np.full((P, T), np.nan)
            fut[:, :T - h] = x[:, h:, di]
            truth_up |= (fut > cross_level) & below
            truth_dn |= (fut < cross_level) & ~below
        mu_d = for_mu[:, :, :, di]
        sd_d = for_sd[:, :, :, di]
        p_above = 1.0 - normal_cdf((cross_level - mu_d) / sd_d)
        p_below = normal_cdf((cross_level - mu_d) / sd_d)
        vh = valid
        p_up = 1.0 - np.prod(np.where(vh, 1.0 - p_above, 1.0), axis=2)
        p_dn = 1.0 - np.prod(np.where(vh, 1.0 - p_below, 1.0), axis=2)
        vt = valid[:, :, 0].astype(bool)          # occasions with any horizon
        warn["relapse_auc"] = auc_score(truth_up[vt & below],
                                        p_up[vt & below])
        warn["recovery_auc"] = auc_score(truth_dn[vt & ~below],
                                         p_dn[vt & ~below])

    # in-context score (note 40): early-window minus late-window 1-step RMSE
    q = max(T // 4, 1)
    v1 = valid[:, :, 0]
    early = fe[:, :q, 0, :][v1[:, :q].astype(bool)]
    late = fe[:, T - q:, 0, :][v1[:, T - q:].astype(bool)]
    icl = (float(np.sqrt(np.mean(early ** 2)) - np.sqrt(np.mean(late ** 2)))
           if early.size and late.size else float("nan"))

    return {
        "filter_rmse": filter_rmse,
        "filter_rmse_missing_occasions": filter_rmse_missing,
        "filter_coverage": filter_coverage,
        "forecast_by_horizon": per_h,
        "persistence_rmse_by_horizon": pers,
        "rho_mae": rho_mae,
        "kappa_star_mae": ks_mae,
        "regime_accuracy": regime_acc,
        "early_warning": warn,
        "in_context_score": icl,
        "attn_effective_context": diags["attn_entropy"],
        "rank_residual_by_layer": diags["rank_residual"],
        "level": c.level,
    }


def _z_from_level(level: float) -> float:
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
