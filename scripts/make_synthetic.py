#!/usr/bin/env python3
"""
Generate, save, and summarize a synthetic-person population (roadmap Step 2).

    python scripts/make_synthetic.py --n 300 --out datasets/synthetic_v1

Produces, under the output directory:
  * population.npz + manifest.json  — the dataset (ground truth + observations)
  * summary.json                    — population-level summary statistics
  * synthetic_overview.png          — a 3-panel figure (if matplotlib present)

The saved dataset is exactly what Step 3 (method recovery) will consume: it
holds each person's true B, b, kappa, and latent states alongside the noisy,
partially observed EMA series an estimator actually sees.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from upg.registry import ENDO                                   # noqa: E402
from upg.simulate import generator_preset_names, get_generator_preset, simulate_preset  # noqa: E402


def summarize(ds) -> dict:
    dis = ENDO.index("DIS")
    kappa = np.array([r.params.kappa for r in ds.records])
    kstar = np.array([r.params.kappa_star for r in ds.records])
    attractor = np.array([r.params.attractor_dis for r in ds.records])
    dropouts = sum(r.dropout_time is not None for r in ds.records)
    return {
        "n_persons": len(ds.records),
        "n_dims": len(ds.dims),
        "T": ds.config.T,
        "regime_mix": ds.regime_counts(),
        "missing_fraction": round(ds.missing_fraction(), 4),
        "dropout_persons": dropouts,
        "kappa_mean": round(float(kappa.mean()), 3),
        "kappa_sd": round(float(kappa.std()), 3),
        "frac_supercritical(kappa>kappa*)": round(float(np.mean(kappa > kstar)), 3),
        "attractor_DIS_mean": round(float(attractor.mean()), 3),
        "observed_DIS_mean": round(float(np.nanmean(
            np.stack([r.observations[:, dis] for r in ds.records]))), 3),
    }


def make_figure(ds, path: str) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False

    dis = ENDO.index("DIS")
    colors = {"quiescent": "#2a9d8f", "pinned_high": "#e76f51", "bistable": "#e9c46a"}
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))

    # Panel 1: one pinned-high person's DIS trajectory (true vs observed).
    pick = next((r for r in ds.records if r.params.regime == "pinned_high"),
                ds.records[0])
    t = np.arange(ds.config.T)
    ax[0].plot(t, pick.states[:, dis], color="#264653", lw=1.6,
               label="true latent DIS")
    obs = pick.observations[:, dis]
    seen = ~np.isnan(obs)
    ax[0].scatter(t[seen], obs[seen], s=16, color="#e76f51", zorder=3,
                  label="observed (EMA)")
    ax[0].set_title(f"One person's disorder trajectory\n({pick.params.person_id}, "
                    f"regime={pick.params.regime})")
    ax[0].set_xlabel("occasion"); ax[0].set_ylabel("DIS activation")
    ax[0].set_ylim(-0.05, 1.05); ax[0].legend(fontsize=8, loc="lower right")

    # Panel 2: distribution of attractor DIS, stacked by regime.
    by = {k: [r.params.attractor_dis for r in ds.records if r.params.regime == k]
          for k in colors}
    ax[1].hist([by[k] for k in colors], bins=18, stacked=True,
               color=[colors[k] for k in colors], label=list(colors))
    ax[1].set_title("Population: disorder attractor by regime")
    ax[1].set_xlabel("attractor DIS activation"); ax[1].set_ylabel("persons")
    ax[1].legend(fontsize=8)

    # Panel 3: kappa vs kappa* — who sits above their own bifurcation.
    for k, c in colors.items():
        rs = [r for r in ds.records if r.params.regime == k]
        if rs:
            ax[2].scatter([r.params.kappa for r in rs],
                          [r.params.kappa_star for r in rs],
                          s=14, color=c, alpha=0.7, label=k)
    lim = [0.2, 0.75]
    ax[2].plot(lim, lim, "k--", lw=1, label="kappa = kappa*")
    ax[2].set_xlim(*lim); ax[2].set_ylim(0.3, 0.6)
    ax[2].set_title("Coupling vs. bifurcation threshold")
    ax[2].set_xlabel("kappa (person)"); ax[2].set_ylabel("kappa* = 1/lambda_max(B)")
    ax[2].legend(fontsize=8, loc="upper left")

    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300, help="number of persons")
    ap.add_argument("--T", type=int, default=None, help="occasions per person")
    ap.add_argument("--out", default="datasets/synthetic_v1")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--preset", default="clinical_realistic",
                    choices=generator_preset_names(),
                    help="synthetic generator preset")
    ap.add_argument("--no-figure", action="store_true")
    args = ap.parse_args()

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = args.out if os.path.isabs(args.out) else os.path.join(repo, args.out)

    ds = simulate_preset(args.preset, args.n, T=args.T, seed=args.seed)

    ds.save(out)
    summary = summarize(ds)
    preset = get_generator_preset(args.preset)
    summary["preset"] = args.preset
    summary["preset_description"] = preset.description
    with open(os.path.join(out, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print(f"saved {summary['n_persons']} persons to {out}")
    print(json.dumps(summary, indent=2))

    if not args.no_figure:
        fig_path = os.path.join(out, "synthetic_overview.png")
        if make_figure(ds, fig_path):
            print(f"figure: {fig_path}")
        else:
            print("matplotlib not available; skipped figure")


if __name__ == "__main__":
    main()
