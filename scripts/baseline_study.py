"""
Step 4 baseline study: run the temporal-network baselines (Bayesian anchored
VAR, errors-in-variables corrected VAR, EKF-EM state-space) against the Step 3
estimator on the three benchmark presets, across a grid of series lengths.

Usage:
    python scripts/baseline_study.py [--preset NAME] [--n-persons N] [--out DIR]

Writes one JSON per preset into --out (default upg/datasets/baselines_v1) and,
when all presets exist, a combined summary with recovery scaling-law fits.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from upg.baselines import baseline_recover_dataset, fit_scaling_law  # noqa: E402
from upg.recover import recover_dataset  # noqa: E402
from upg.simulate import simulate_preset  # noqa: E402

T_GRID = (30, 60, 120, 250)
PRESETS = ("balanced_regimes", "clinical_realistic", "transition_rich")
METHODS = ("step3", "bayes", "ev", "kalman")


def run_preset(preset: str, n_persons: int, seed: int = 0) -> dict:
    out = {"preset": preset, "n_persons": n_persons, "seed": seed, "cells": []}
    for T in T_GRID:
        ds = simulate_preset(preset, n_persons=n_persons, T=T, seed=seed)
        cell = {"T": T, "results": {}}
        cell["results"]["step3"] = recover_dataset(ds)["aggregate"]
        cell["results"]["bayes"] = baseline_recover_dataset(ds, "bayes")["aggregate"]
        cell["results"]["ev"] = baseline_recover_dataset(ds, "ev")["aggregate"]
        cell["results"]["kalman"] = baseline_recover_dataset(ds, "kalman")["aggregate"]
        out["cells"].append(cell)
        print(f"[{preset}] T={T} done", flush=True)
    return out


def summarize(out_dir: str) -> None:
    combined = {}
    for preset in PRESETS:
        path = os.path.join(out_dir, f"{preset}.json")
        if not os.path.exists(path):
            print(f"missing {path}; run that preset first")
            return
        with open(path, encoding="utf-8") as fh:
            combined[preset] = json.load(fh)

    # scaling-law fits on edge RMSE per method (pooled over presets by mean)
    laws = {}
    for method in METHODS:
        Ts, errs = [], []
        for preset in PRESETS:
            for cell in combined[preset]["cells"]:
                Ts.append(cell["T"])
                errs.append(cell["results"][method]["median_edge_rmse"])
        Ts = np.asarray(Ts, float)
        errs = np.asarray(errs, float)
        # average duplicates at same T
        uT = np.unique(Ts)
        mErr = np.array([errs[Ts == t].mean() for t in uT])
        laws[method] = fit_scaling_law(uT, mErr)
        laws[method]["T"] = uT.tolist()
        laws[method]["mean_edge_rmse"] = mErr.tolist()

    summary = {"presets": combined, "scaling_laws": laws}
    with open(os.path.join(out_dir, "baseline_results.json"), "w",
              encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    print("wrote", os.path.join(out_dir, "baseline_results.json"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=PRESETS + ("all", "summary"),
                    default="all")
    ap.add_argument("--n-persons", type=int, default=40)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "..", "datasets", "baselines_v1"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.preset == "summary":
        summarize(args.out)
        return

    presets = PRESETS if args.preset == "all" else (args.preset,)
    for preset in presets:
        res = run_preset(preset, args.n_persons, args.seed)
        with open(os.path.join(args.out, f"{preset}.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(res, fh, indent=2)
    summarize(args.out)


if __name__ == "__main__":
    main()
