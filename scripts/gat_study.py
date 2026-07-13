"""
Step 5 study: train the structure-constrained graph-attention estimator per
benchmark preset and score it, cell by cell, against the Step 4 temporal
baselines (the contract bar: beat the *best* step-4 value per cell, not
step 3).

Staged so every stage fits a short execution window; all stages are
idempotent (cached artifacts are reused):

    python scripts/gat_study.py --stage prep              # training sets -> npz
    python scripts/gat_study.py --stage train --preset X  # one model
    python scripts/gat_study.py --stage eval              # all cells + verdicts
    python scripts/gat_study.py --stage figure            # comparison figure

Evaluation populations are simulate_preset(preset, n_eval, T, seed=0) — the
same populations, bit for bit, that produced docs/step4_baseline_report.md.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from upg.gat import (GATConfig, MaskedGraphAttentionEstimator,  # noqa: E402
                     build_training_set, deviation_rank_spectrum,
                     gat_recover_dataset)
from upg.simulate import simulate_preset  # noqa: E402

T_GRID = (30, 60, 120, 250)
PRESETS = ("balanced_regimes", "clinical_realistic", "transition_rich")
BASELINE_METHODS = ("step3", "bayes", "ev", "kalman")
KEY_AXES = ("median_edge_rmse", "median_edge_dev_corr", "median_rho_abs_err",
            "regime_accuracy", "median_attractor_abs_err")


# ---------------------------------------------------------------------------
# Training-set cache
# ---------------------------------------------------------------------------


def _save_examples(path: str, examples) -> None:
    node = np.stack([e[0][0] for e in examples])
    edge = np.stack([e[0][1] for e in examples])
    glob = np.stack([e[0][2] for e in examples])
    t_edge = np.stack([e[1]["t_edge"] for e in examples])
    t_g = np.stack([e[1]["t_g"] for e in examples])
    t_b = np.stack([e[1]["t_b"] for e in examples])
    np.savez_compressed(path, node=node, edge=edge, glob=glob,
                        t_edge=t_edge, t_g=t_g, t_b=t_b)


def _load_examples(path: str):
    z = np.load(path, allow_pickle=False)
    out = []
    for i in range(z["node"].shape[0]):
        feats = (z["node"][i], z["edge"][i], z["glob"][i])
        targets = {"t_edge": z["t_edge"][i], "t_g": z["t_g"][i],
                   "t_b": z["t_b"][i]}
        out.append((feats, targets))
    return out


def stage_prep(out_dir: str, n_train: int, n_val: int) -> None:
    for idx, preset in enumerate(PRESETS):
        tr_path = os.path.join(out_dir, f"train_{preset}.npz")
        va_path = os.path.join(out_dir, f"val_{preset}.npz")
        if os.path.exists(tr_path) and os.path.exists(va_path):
            print(f"[{preset}] cached training sets found", flush=True)
            continue
        t0 = time.time()
        train = build_training_set(preset, n_train, seed=1000 + idx,
                                   T_grid=T_GRID)
        val = build_training_set(preset, n_val, seed=2000 + idx, T_grid=T_GRID)
        _save_examples(tr_path, train)
        _save_examples(va_path, val)
        spec = deviation_rank_spectrum(train)
        with open(os.path.join(out_dir, f"spectrum_{preset}.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(spec, fh, indent=2)
        print(f"[{preset}] prepared {len(train)}/{len(val)} examples "
              f"in {time.time()-t0:.1f}s (dev eff.rank "
              f"{spec['effective_rank']:.1f}/{spec['n_edges']})", flush=True)


def stage_train(out_dir: str, preset: str, force: bool = False) -> None:
    idx = PRESETS.index(preset)
    model_path = os.path.join(out_dir, f"gat_{preset}.npz")
    if os.path.exists(model_path) and not force:
        print(f"[{preset}] model already trained", flush=True)
        return
    train = _load_examples(os.path.join(out_dir, f"train_{preset}.npz"))
    val = _load_examples(os.path.join(out_dir, f"val_{preset}.npz"))
    t0 = time.time()
    model = MaskedGraphAttentionEstimator(GATConfig(seed=idx))
    fit = model.fit(train, val, verbose=True)
    model.save(model_path)
    with open(os.path.join(out_dir, f"spectrum_{preset}.json"),
              encoding="utf-8") as fh:
        spectrum = json.load(fh)
    meta = {
        "preset": preset, "n_examples": len(train), "T_grid": list(T_GRID),
        "config": model.config.as_dict(), "best_val": fit["best_val"],
        "best_epoch": fit["best_epoch"], "epochs_run": fit["epochs_run"],
        "val_curve": [h["val"] for h in fit["history"]],
        "deviation_rank_spectrum": spectrum,
        "train_seconds": round(time.time() - t0, 1),
    }
    with open(os.path.join(out_dir, f"gat_{preset}_training.json"), "w",
              encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    print(f"[{preset}] trained in {meta['train_seconds']}s "
          f"(best epoch {fit['best_epoch']}, val {fit['best_val']:.4f})",
          flush=True)


def stage_eval(out_dir: str, baselines_dir: str, n_eval: int) -> None:
    results = {}
    for preset in PRESETS:
        model = MaskedGraphAttentionEstimator.load(
            os.path.join(out_dir, f"gat_{preset}.npz"))
        with open(os.path.join(out_dir, f"gat_{preset}_training.json"),
                  encoding="utf-8") as fh:
            meta = json.load(fh)
        cells = []
        for T in T_GRID:
            ds = simulate_preset(preset, n_persons=n_eval, T=T, seed=0)
            agg = gat_recover_dataset(ds, model)["aggregate"]
            cells.append({"T": T, "gat": agg})
            print(f"[{preset}] T={T}: rmse={agg['median_edge_rmse']:.3f} "
                  f"dev={agg['median_edge_dev_corr']:.3f} "
                  f"regime={agg['regime_accuracy']:.3f} "
                  f"cov={agg['mean_coverage']:.2f}", flush=True)
        cells = _compare(preset, cells, baselines_dir)
        results[preset] = {"training": meta, "cells": cells}
        with open(os.path.join(out_dir, f"{preset}_eval.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(results[preset], fh, indent=2)
    with open(os.path.join(out_dir, "gat_results.json"), "w",
              encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    _print_verdicts(results)


def _compare(preset: str, cells: list[dict], baselines_dir: str) -> list[dict]:
    path = os.path.join(baselines_dir, f"{preset}.json")
    if not os.path.exists(path):
        print(f"warning: {path} missing; run baseline_study first")
        return cells
    with open(path, encoding="utf-8") as fh:
        base = json.load(fh)
    by_T = {c["T"]: c["results"] for c in base["cells"]}
    for cell in cells:
        res = by_T.get(cell["T"])
        if res is None:
            continue
        cell["baselines"] = res
        verdict = {}
        for axis in KEY_AXES:
            higher_better = axis in ("median_edge_dev_corr", "regime_accuracy")
            vals = {m: res[m][axis] for m in BASELINE_METHODS if axis in res[m]}
            best_m = (max if higher_better else min)(vals, key=vals.get)
            gat_v = cell["gat"][axis]
            beats = (gat_v >= vals[best_m]) if higher_better \
                else (gat_v <= vals[best_m])
            verdict[axis] = {"gat": gat_v, "best_baseline": vals[best_m],
                             "best_method": best_m, "gat_wins": bool(beats)}
        cell["verdict"] = verdict
    return cells


def _print_verdicts(results: dict) -> None:
    print("\n=== Contract verdicts (GAT vs best step-4 baseline) ===")
    for preset in PRESETS:
        for cell in results[preset]["cells"]:
            if "verdict" not in cell:
                continue
            wins = [a.replace("median_", "") for a, v in cell["verdict"].items()
                    if v["gat_wins"]]
            print(f"{preset:20s} T={cell['T']:4d}  wins: {', '.join(wins) or '-'}")


def stage_figure(out_dir: str) -> None:
    with open(os.path.join(out_dir, "gat_results.json"), encoding="utf-8") as fh:
        results = json.load(fh)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(3, 3, figsize=(13, 10), sharex=True)
    for col, preset in enumerate(PRESETS):
        cells = results[preset]["cells"]
        Ts = [c["T"] for c in cells]
        rows = [("median_edge_rmse", "edge RMSE", 0),
                ("median_edge_dev_corr", "deviation corr", 1),
                ("regime_accuracy", "regime accuracy", 2)]
        for key, label, row in rows:
            ax = axes[row][col]
            ax.plot(Ts, [c["gat"][key] for c in cells], "o-", color="#7c3aed",
                    lw=2, label="GAT (step 5)", zorder=5)
            for m, color in zip(BASELINE_METHODS,
                                ("#9ca3af", "#60a5fa", "#f59e0b", "#10b981")):
                if "baselines" in cells[0] and key in cells[0]["baselines"][m]:
                    ax.plot(Ts, [c["baselines"][m][key] for c in cells], "s--",
                            color=color, alpha=0.8, label=m)
            if key == "median_edge_rmse" and "baselines" in cells[0]:
                prior = cells[0]["baselines"]["step3"]["median_prior_rmse"]
                ax.axhline(prior, color="k", ls=":", lw=1, label="prior alone")
            ax.set_xscale("log")
            ax.set_xticks(Ts)
            ax.set_xticklabels(Ts)
            if row == 0:
                ax.set_title(preset)
            if col == 0:
                ax.set_ylabel(label)
            if row == 2:
                ax.set_xlabel("T (occasions)")
            ax.grid(alpha=0.25)
    axes[0][0].legend(fontsize=7, ncol=2)
    fig.suptitle("Step 5: structure-constrained GAT vs. step-4 baselines "
                 "(same populations, same skeleton, same prior)")
    fig.tight_layout()
    path = os.path.join(out_dir, "gat_vs_baselines.png")
    fig.savefig(path, dpi=150)
    print("wrote", path, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("prep", "train", "eval", "figure"),
                    required=True)
    ap.add_argument("--preset", choices=PRESETS, default=None)
    ap.add_argument("--n-train", type=int, default=240)
    ap.add_argument("--n-val", type=int, default=60)
    ap.add_argument("--n-eval", type=int, default=40)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "..", "datasets", "gat_v1"))
    ap.add_argument("--baselines", default=os.path.join(
        os.path.dirname(__file__), "..", "datasets", "baselines_v1"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.stage == "prep":
        stage_prep(args.out, args.n_train, args.n_val)
    elif args.stage == "train":
        presets = (args.preset,) if args.preset else PRESETS
        for preset in presets:
            stage_train(args.out, preset, force=args.force)
    elif args.stage == "eval":
        stage_eval(args.out, args.baselines, args.n_eval)
    elif args.stage == "figure":
        stage_figure(args.out)


if __name__ == "__main__":
    main()
