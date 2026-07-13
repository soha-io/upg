"""
Step 6 study: train the causal temporal transformer per benchmark preset and
evaluate it as (i) measurement model and (ii) forecaster, against the
comparators the reading notes register:

  * persistence null (carry last observation forward);
  * the PatchTST channel-independent null (note 16) on transition_rich —
    the coupling-detection experiment;
  * the uniform-attention null (note 14);
  * the explicit pipeline (note 41): fit_kalman_person -> EKF filter ->
    map propagation, i.e. our own step-4 estimator used as a forecaster;
  * the oracle: the same pipeline with the true person parameters (upper
    bound; the residual gap is irreducible process noise).

Staged and idempotent, like gat_study.py:

    python scripts/forecast_study.py --stage data
    python scripts/forecast_study.py --stage train --preset X [--null]
    python scripts/forecast_study.py --stage eval
    python scripts/forecast_study.py --stage figure
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from upg.baselines import (ekf_filter_states, fit_kalman_person,  # noqa: E402
                           map_forecast)
from upg.simulate import SyntheticDataset, simulate_preset  # noqa: E402
from upg.transformer import (ForecastConfig, TemporalTransformer,  # noqa: E402
                             evaluate_model, make_batches)

PRESETS = ("balanced_regimes", "clinical_realistic", "transition_rich")
N_TRAIN, N_VAL, N_EVAL = 160, 40, 40
HORIZON = 5
DIS_INDEX = 5                     # ENDO.index("DIS")


def _dsdir(out: str, split: str, preset: str) -> str:
    return os.path.join(out, f"{split}_{preset}")


def stage_data(out: str) -> None:
    for idx, preset in enumerate(PRESETS):
        for split, n, seed in (("train", N_TRAIN, 3000 + idx),
                               ("val", N_VAL, 4000 + idx),
                               ("eval", N_EVAL, 0)):
            path = _dsdir(out, split, preset)
            if os.path.exists(os.path.join(path, "manifest.json")):
                continue
            t0 = time.time()
            ds = simulate_preset(preset, n_persons=n, seed=seed)
            ds.save(path)
            print(f"[{preset}] {split}: {n} persons T={ds.config.T} "
                  f"({time.time()-t0:.1f}s)", flush=True)


def _model_path(out: str, preset: str, null: bool) -> str:
    tag = "null_ci" if null else "tf"
    return os.path.join(out, f"{tag}_{preset}.npz")


def stage_train(out: str, preset: str, null: bool, epochs: int,
                force: bool = False) -> None:
    idx = PRESETS.index(preset)
    mpath = _model_path(out, preset, null)
    jpath = mpath.replace(".npz", "_training.json")
    done = {}
    if os.path.exists(jpath):
        with open(jpath, encoding="utf-8") as fh:
            done = json.load(fh)
    if os.path.exists(mpath) and done.get("finished") and not force:
        print(f"[{preset}] {'null' if null else 'model'} already trained",
              flush=True)
        return

    train = SyntheticDataset.load(_dsdir(out, "train", preset))
    val = SyntheticDataset.load(_dsdir(out, "val", preset))
    if null:
        # channels-as-sequences multiplies examples x7; keep the null's
        # compute budget comparable by subsampling persons (documented in
        # the step-6 report; a win for the null under a smaller budget would
        # only strengthen the null's claim)
        train.records = train.records[:60]
        val.records = val.records[:20]
    # T=180 sequences hit a memory cliff at batch 32 in the NumPy engine;
    # smaller batches keep every step in cache (same flops, less residency)
    bs = 16 if train.config.T >= 150 else 32
    cfg = ForecastConfig(seed=idx + (100 if null else 0), horizon=HORIZON,
                         epochs=epochs, channel_independent=null,
                         n_dims=len(train.dims), batch_size=bs)
    tb = make_batches(train, HORIZON, channel_independent=null)
    vb = make_batches(val, HORIZON, channel_independent=null)

    # resume from checkpoint when present (epochs are chunked across runs)
    if os.path.exists(mpath) and done and not done.get("finished") and not force:
        model = TemporalTransformer.load(mpath)
        model.config.epochs = epochs
        print(f"[{preset}] resuming at chunk {done.get('chunks', 0)}", flush=True)
    else:
        model = TemporalTransformer(cfg)
        done = {"chunks": 0, "epochs_done": 0, "val_curve": []}

    t0 = time.time()
    fit = model.fit(tb, vb, verbose=True)
    model.save(mpath)
    done["chunks"] = done.get("chunks", 0) + 1
    done["epochs_done"] = done.get("epochs_done", 0) + fit["epochs_run"]
    done["val_curve"] = done.get("val_curve", []) + [h["val"] for h in fit["history"]]
    stalled = fit["epochs_run"] >= fit["best_epoch"] + model.config.patience
    done.update(finished=bool(stalled or fit["epochs_run"] < epochs),
                best_val=fit["best_val"], config=model.config.as_dict(),
                train_seconds=round(time.time() - t0, 1))
    with open(jpath, "w", encoding="utf-8") as fh:
        json.dump(done, fh, indent=2)
    print(f"[{preset}] chunk done in {done['train_seconds']}s "
          f"(best val {fit['best_val']:.4f}, finished={done['finished']})",
          flush=True)


def _explicit_and_oracle(ds, horizon: int) -> dict:
    """Forecast RMSE by horizon for the explicit pipeline and the oracle."""
    cfgm = ds.config
    sq_ex = {h: [] for h in range(1, horizon + 1)}
    sq_or = {h: [] for h in range(1, horizon + 1)}
    for r in ds.records:
        p = r.params
        rec = fit_kalman_person(r.observations, r.u, p.kappa,
                                meas_sd=cfgm.meas_noise,
                                process_sd=cfgm.process_noise, n_em=2)
        for (B, g, b) in ((rec.B_hat, rec.g_hat, rec.b_hat), (p.B, p.g, p.b)):
            x_f = ekf_filter_states(r.observations, r.u, B, g, b, p.kappa,
                                    cfgm.meas_noise, cfgm.process_noise)
            tgt = sq_ex if B is rec.B_hat else sq_or
            T = len(r.u)
            for t in range(T - 1):
                hmax = min(horizon, T - 1 - t)
                fc = map_forecast(x_f[t], r.u[t + 1:t + 1 + hmax], B, g, b,
                                  p.kappa)
                for h in range(1, hmax + 1):
                    err = fc[h - 1] - r.states[t + h]
                    tgt[h].append(np.mean(err ** 2))
    return {
        "explicit_rmse_by_horizon": {h: float(np.sqrt(np.mean(v)))
                                     for h, v in sq_ex.items()},
        "oracle_rmse_by_horizon": {h: float(np.sqrt(np.mean(v)))
                                   for h, v in sq_or.items()},
    }


def _eval_null_chunked(model, batch, chunk: int = 16) -> dict:
    """Chunked evaluation for the channel-independent null (long sequences x
    many scalar channels exceed memory in one forward).  RMSEs are combined
    as weighted root-mean-squares; coverage as weighted means."""
    n = batch["y0"].shape[0]
    parts, weights = [], []
    for s in range(0, n, chunk):
        idx = np.arange(s, min(s + chunk, n))
        sub = {k: v[idx] for k, v in batch.items()}
        parts.append(evaluate_model(model, sub))
        weights.append(len(idx))
    w = np.asarray(weights, float)
    w /= w.sum()

    def _rms(vals):
        return float(np.sqrt(np.sum(w * np.asarray(vals) ** 2)))

    def _mean(vals):
        return float(np.sum(w * np.asarray(vals)))

    fbh = {}
    for h in parts[0]["forecast_by_horizon"]:
        fbh[h] = {
            "rmse": _rms([p["forecast_by_horizon"][h]["rmse"] for p in parts]),
            "nll": _mean([p["forecast_by_horizon"][h]["nll"] for p in parts]),
            "coverage": _mean([p["forecast_by_horizon"][h]["coverage"]
                               for p in parts]),
        }
    return {"forecast_by_horizon": fbh,
            "filter_rmse": _rms([p["filter_rmse"] for p in parts])}


def stage_eval(out: str) -> None:
    results = {}
    for preset in PRESETS:
        cache = os.path.join(out, f"eval_{preset}.json")
        if os.path.exists(cache):
            with open(cache, encoding="utf-8") as fh:
                results[preset] = json.load(fh)
            print(f"[{preset}] cached eval found", flush=True)
            continue
        ds = SyntheticDataset.load(_dsdir(out, "eval", preset))
        model = TemporalTransformer.load(_model_path(out, preset, False))
        batch = make_batches(ds, HORIZON)
        ev = evaluate_model(model, batch, dis_index=DIS_INDEX)
        ev_uniform = evaluate_model(model, batch, dis_index=DIS_INDEX,
                                    uniform_attention=True)
        ev["uniform_attention_forecast_rmse_h1"] = \
            ev_uniform["forecast_by_horizon"][1]["rmse"]
        ev["comparators"] = _explicit_and_oracle(ds, HORIZON)

        null_path = _model_path(out, preset, True)
        if os.path.exists(null_path):
            null_model = TemporalTransformer.load(null_path)
            nb = make_batches(ds, HORIZON, channel_independent=True)
            ev["channel_independent_null"] = _eval_null_chunked(null_model, nb)
        results[preset] = ev
        with open(cache, "w", encoding="utf-8") as fh:
            json.dump(ev, fh, indent=2)
        h1 = ev["forecast_by_horizon"][1]
        print(f"[{preset}] filter={ev['filter_rmse']:.3f} "
              f"h1={h1['rmse']:.3f} (pers {ev['persistence_rmse_by_horizon'][1]:.3f}, "
              f"expl {ev['comparators']['explicit_rmse_by_horizon'][1]:.3f}, "
              f"orac {ev['comparators']['oracle_rmse_by_horizon'][1]:.3f}) "
              f"cov={h1['coverage']:.2f} warn={ev['early_warning']}", flush=True)
    with open(os.path.join(out, "forecast_results.json"), "w",
              encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print("wrote forecast_results.json", flush=True)


def stage_figure(out: str) -> None:
    with open(os.path.join(out, "forecast_results.json"), encoding="utf-8") as fh:
        results = json.load(fh)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=False)
    for ax, preset in zip(axes, PRESETS):
        ev = results[preset]
        hs = sorted(int(h) for h in ev["forecast_by_horizon"])
        ax.plot(hs, [ev["forecast_by_horizon"][str(h)]["rmse"] for h in hs],
                "o-", color="#7c3aed", lw=2, label="transformer")
        ax.plot(hs, [ev["persistence_rmse_by_horizon"][str(h)] for h in hs],
                "s--", color="#9ca3af", label="persistence")
        comp = ev["comparators"]
        ax.plot(hs, [comp["explicit_rmse_by_horizon"][str(h)] for h in hs],
                "^--", color="#10b981", label="explicit (kalman fit)")
        ax.plot(hs, [comp["oracle_rmse_by_horizon"][str(h)] for h in hs],
                "k:", label="oracle (true params)")
        if "channel_independent_null" in ev:
            ax.plot(hs, [ev["channel_independent_null"]["forecast_by_horizon"][str(h)]["rmse"]
                         for h in hs], "d--", color="#f59e0b",
                    label="channel-indep. null")
        ax.set_title(preset)
        ax.set_xlabel("horizon (occasions ahead)")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("forecast RMSE (true states)")
    axes[0].legend(fontsize=8)
    fig.suptitle("Step 6: implicit (transformer) vs explicit (state-space) "
                 "forecasting on held-out persons")
    fig.tight_layout()
    path = os.path.join(out, "forecast_comparison.png")
    fig.savefig(path, dpi=150)
    print("wrote", path, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("data", "train", "eval", "figure"),
                    required=True)
    ap.add_argument("--preset", choices=PRESETS, default=None)
    ap.add_argument("--null", action="store_true",
                    help="train the channel-independent null instead")
    ap.add_argument("--epochs", type=int, default=40,
                    help="epoch budget for this chunk (resumable)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "..", "datasets", "forecast_v1"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.stage == "data":
        stage_data(args.out)
    elif args.stage == "train":
        presets = (args.preset,) if args.preset else PRESETS
        for preset in presets:
            stage_train(args.out, preset, args.null, args.epochs,
                        force=args.force)
    elif args.stage == "eval":
        stage_eval(args.out)
    elif args.stage == "figure":
        stage_figure(args.out)


if __name__ == "__main__":
    main()
