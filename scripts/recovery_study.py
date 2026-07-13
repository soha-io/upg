#!/usr/bin/env python3
"""
Recovery study (roadmap Step 3): how much data does it take to estimate a person?

Sweeps recovery quality against the three levers a data-collection design can
actually control — series length, measurement reliability, and sampling
compliance — plus a prior-anchored-vs-free comparison. Aggregates across a
population and writes:

  * recovery_results.json   — all sweep numbers
  * recovery_curves.png     — the 4-panel figure
  * recovery_findings.md    — plain-language data-gathering guidance (templated)

Run:  python scripts/recovery_study.py --out datasets/recovery_v1
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from upg.recover import recover_dataset                    # noqa: E402
from upg.simulate import SimConfig, simulate_population    # noqa: E402

# population defaults (heterogeneous, spanning the bifurcation)
POP = dict(kappa_mean=0.44, kappa_sd=0.09, adversity_mean=0.55, adversity_sd=0.50)


def make_pop(T, meas, samp, procn, npers, seed, dropout=0.0):
    cfg = SimConfig(T=T, meas_noise=meas, sampling_rate=samp, dropout_prob=dropout,
                    process_noise=procn, seed=seed)
    return simulate_population(npers, config=cfg, pop_seed=seed, **POP)


def sweep_length(npers, seed, procn):
    rows = []
    for T in (30, 60, 120, 250, 500, 1000):
        ds = make_pop(T, 0.05, 1.0, procn, npers, seed)
        anc = recover_dataset(ds, ridge=0.2, anchor=True)["aggregate"]
        fre = recover_dataset(ds, ridge=1e-6, anchor=False)["aggregate"]
        rows.append({"T": T,
                     "edge_rmse": anc["median_edge_rmse"],
                     "edge_rmse_free": fre["median_edge_rmse"],
                     "edge_corr": anc["median_edge_corr"],
                     "regime_acc": anc["regime_accuracy"],
                     "attractor_err": anc["median_attractor_abs_err"],
                     "prior_rmse": anc["median_prior_rmse"]})
    return rows


def sweep_measurement(npers, seed, procn):
    rows = []
    for meas in (0.0, 0.05, 0.10, 0.15, 0.20):
        ds = make_pop(250, meas, 1.0, procn, npers, seed)
        a = recover_dataset(ds, ridge=0.2, anchor=True)["aggregate"]
        rows.append({"meas_noise": meas, "edge_rmse": a["median_edge_rmse"],
                     "attractor_err": a["median_attractor_abs_err"],
                     "regime_acc": a["regime_accuracy"]})
    return rows


def sweep_sampling(npers, seed, procn):
    rows = []
    for samp in (1.0, 0.8, 0.6, 0.4, 0.25):
        ds = make_pop(250, 0.05, samp, procn, npers, seed)
        a = recover_dataset(ds, ridge=0.2, anchor=True)["aggregate"]
        rows.append({"sampling_rate": samp,
                     "median_transitions": a["median_transitions"],
                     "edge_rmse": a["median_edge_rmse"],
                     "regime_acc": a["regime_accuracy"]})
    return rows


def make_figure(results, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False

    L, M, S = results["length"], results["measurement"], results["sampling"]
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))

    # A: edge recovery vs T (anchored vs free vs prior floor)
    T = [r["T"] for r in L]
    ax[0, 0].plot(T, [r["edge_rmse"] for r in L], "o-", color="#2a6f97",
                  label="prior-anchored (W7)")
    ax[0, 0].plot(T, [r["edge_rmse_free"] for r in L], "s--", color="#bc4749",
                  label="free (unregularized)")
    ax[0, 0].axhline(L[0]["prior_rmse"], color="#6c757d", ls=":",
                     label="consensus prior alone")
    ax[0, 0].set_xscale("log")
    ax[0, 0].set_title("A. Edge-structure recovery vs. series length")
    ax[0, 0].set_xlabel("occasions per person (T)")
    ax[0, 0].set_ylabel("edge RMSE  (lower = better)")
    ax[0, 0].legend(fontsize=8)

    # B: clinical recovery vs T
    ax2 = ax[0, 1]
    ax2.plot(T, [r["regime_acc"] for r in L], "o-", color="#2a9d8f",
             label="regime accuracy")
    ax2.set_ylim(0, 1.02)
    ax2.set_xscale("log")
    ax2.set_ylabel("regime accuracy", color="#2a9d8f")
    ax2b = ax2.twinx()
    ax2b.plot(T, [r["attractor_err"] for r in L], "s--", color="#e76f51",
              label="attractor DIS error")
    ax2b.set_ylabel("attractor DIS abs. error", color="#e76f51")
    ax2.set_title("B. Clinical quantities recover early")
    ax2.set_xlabel("occasions per person (T)")

    # C: measurement-noise floor
    m = [r["meas_noise"] for r in M]
    ax[1, 0].plot(m, [r["edge_rmse"] for r in M], "o-", color="#bc4749",
                  label="edge RMSE")
    ax[1, 0].plot(m, [r["attractor_err"] for r in M], "s--", color="#e76f51",
                  label="attractor error")
    ax[1, 0].set_title("C. Measurement noise sets a floor (T=250)")
    ax[1, 0].set_xlabel("measurement noise (sd)")
    ax[1, 0].set_ylabel("error")
    ax[1, 0].legend(fontsize=8)

    # D: sampling / missingness
    s = [r["sampling_rate"] for r in S]
    ax[1, 1].plot(s, [r["edge_rmse"] for r in S], "o-", color="#2a6f97",
                  label="edge RMSE")
    ax4b = ax[1, 1].twinx()
    ax4b.plot(s, [r["regime_acc"] for r in S], "s--", color="#2a9d8f",
              label="regime accuracy")
    ax4b.set_ylim(0, 1.02)
    ax[1, 1].set_title("D. Sampling compliance (T=250)")
    ax[1, 1].set_xlabel("per-occasion compliance (sampling rate)")
    ax[1, 1].set_ylabel("edge RMSE", color="#2a6f97")
    ax4b.set_ylabel("regime accuracy", color="#2a9d8f")
    ax[1, 1].invert_xaxis()

    fig.suptitle("How much data does it take to estimate one person? "
                 "(synthetic recovery study)", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return True


def write_findings(results, path):
    L, M, S = results["length"], results["measurement"], results["sampling"]
    prior = L[0]["prior_rmse"]
    t60 = next(r for r in L if r["T"] == 60)
    t1000 = next(r for r in L if r["T"] == 1000)
    m0 = M[0]; m20 = M[-1]
    lines = f"""# Recovery study — what it means for data gathering

*Generated by `scripts/recovery_study.py`. All numbers are medians across a
synthetic population spanning the bifurcation. "Edge RMSE" is error in the
person-specific coupling matrix `B`; "regime" is the quiescent / pinned-high /
bistable label; "attractor" is the disorder fixed point.*

## The four findings

1. **Clinical quantities recover almost immediately; fine structure does not.**
   Even at T=60 occasions, regime accuracy is **{t60['regime_acc']:.0%}** and the
   attractor error is **{t60['attractor_err']:.3f}**, because a good prior plus a
   short series pins the dynamics. Recovering the full edge matrix is far harder:
   edge RMSE only falls from **{t60['edge_rmse']:.3f}** (T=60) to
   **{t1000['edge_rmse']:.3f}** (T=1000), against a consensus-prior baseline of
   **{prior:.3f}**. To beat the prior on absolute edge accuracy takes on the order
   of a couple thousand clean, well-excited occasions.

2. **Never estimate freely — anchor to the prior (rule W7).** At T=60 the
   prior-anchored estimator scores edge RMSE **{t60['edge_rmse']:.3f}** vs
   **{t60['edge_rmse_free']:.3f}** for free (unregularized) estimation — the free
   estimate is worse than doing nothing. Structure-from-theory (W1) plus
   shrinkage-to-prior (W7) is what makes short idiographic series usable.

3. **Measurement reliability beats quantity.** Holding T=250, edge RMSE rises
   from **{m0['edge_rmse']:.3f}** (noiseless) to **{m20['edge_rmse']:.3f}** at
   measurement-noise sd 0.20, and attractor error from **{m0['attractor_err']:.3f}**
   to **{m20['attractor_err']:.3f}**. This is errors-in-variables attenuation: it
   does **not** wash out with more timepoints. Invest in reliable instruments.

4. **Moderate missingness is tolerable.** Dropping per-occasion compliance from
   100% to {S[-1]['sampling_rate']:.0%} leaves regime accuracy near
   **{S[-1]['regime_acc']:.0%}** and edge RMSE roughly flat, because the prior
   absorbs the lost transitions. Compliance in the 60–80% EMA range is workable.

## Concrete design implications

- **Goal = case formulation (regime, attractor, prognosis):** ~4–8 weeks of
  daily EMA (T ≈ 30–60) per person is plenty, *provided* measurement is reliable
  and you anchor to the consensus prior.
- **Goal = person-specific structure (individual edge weights):** budget for
  intensive, long series (many hundreds to a few thousand occasions) and/or
  natural or induced variability — the estimate needs the state to move.
- **Excitation matters as much as N.** A stable person hovering at one attractor
  is weakly informative; the informative data are periods of change (life events,
  treatment onset, symptom flux). Sample denser around transitions.
- **Prioritize reliability, then variability, then sheer length** — in that order.

*Caveats: this is a synthetic recovery study under the model's own generative
assumptions (a best case for the estimator). It sets necessary, not sufficient,
sample-size targets; real data add model misspecification. It uses a complete-case
arctanh-VAR baseline — a state-space/EM treatment of missingness (roadmap Step 4)
will relax the compliance findings further.*
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="datasets/recovery_v1")
    ap.add_argument("--npers", type=int, default=80)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--procn", type=float, default=0.10, help="process noise / excitation")
    args = ap.parse_args()

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = args.out if os.path.isabs(args.out) else os.path.join(repo, args.out)
    os.makedirs(out, exist_ok=True)

    print("running length sweep ...")
    L = sweep_length(args.npers, args.seed, args.procn)
    print("running measurement-noise sweep ...")
    M = sweep_measurement(args.npers, args.seed, args.procn)
    print("running sampling sweep ...")
    S = sweep_sampling(args.npers, args.seed, args.procn)
    results = {"length": L, "measurement": M, "sampling": S,
               "settings": {"npers": args.npers, "seed": args.seed,
                            "process_noise": args.procn}}

    with open(os.path.join(out, "recovery_results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    write_findings(results, os.path.join(out, "recovery_findings.md"))
    fig_ok = make_figure(results, os.path.join(out, "recovery_curves.png"))

    print("\n=== LENGTH SWEEP (anchored vs free; prior_rmse=%.3f) ===" % L[0]["prior_rmse"])
    for r in L:
        print(f"  T={r['T']:4d}  rmse={r['edge_rmse']:.3f}  free={r['edge_rmse_free']:.3f}  "
              f"corr={r['edge_corr']:.2f}  regime={r['regime_acc']:.2f}  attr={r['attractor_err']:.3f}")
    print("=== MEASUREMENT SWEEP (T=250) ===")
    for r in M:
        print(f"  meas={r['meas_noise']:.2f}  rmse={r['edge_rmse']:.3f}  attr={r['attractor_err']:.3f}  regime={r['regime_acc']:.2f}")
    print("=== SAMPLING SWEEP (T=250) ===")
    for r in S:
        print(f"  samp={r['sampling_rate']:.2f}  trans={r['median_transitions']:.0f}  rmse={r['edge_rmse']:.3f}  regime={r['regime_acc']:.2f}")
    print(f"\nsaved results + findings to {out}" + ("" if fig_ok else " (figure skipped)"))


if __name__ == "__main__":
    main()
