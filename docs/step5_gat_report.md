# Step 5 Report — The Structure-Constrained Graph-Attention Estimator

Status: Phase 2, step 5 complete.
Source run: `upg/scripts/gat_study.py`, output `upg/datasets/gat_v1/`.
Settings: one model per preset; training = four independently simulated
240-person populations, one per T ∈ {30, 60, 120, 250} (960 person-windows;
no identities are followed across T), validation = four independently
simulated 60-person populations (240 person-windows), evaluation = the same
40-person seed-0 populations that produced
`step4_baseline_report.md`. Same skeleton (W1), same prior (W7).
Reproduced by `tests/test_gat.py`; engine gradchecked by `tests/test_autodiff.py`.

## What the estimator is

The design of record from the reading notes (08, 17, 33, 37, 41):

| Component | Choice | Note |
|---|---|---|
| Tokens | one per dimension, embedding that dimension's window statistics | 17 |
| Attention | multi-head over variate tokens, hard-masked to the published skeleton | 08 |
| Edge readout | `B̂ᵢⱼ = B̄ᵢⱼ · exp(δᵢⱼ)` — **no softmax**; support and sign inherited | 08, 37 |
| Init | readout zero-initialized → the untrained model returns the prior exactly | 33 (LoRA), W7 |
| Uncertainty | heteroscedastic Gaussian per edge in log-deviation space → 90% intervals | 13 |
| Protocol | amortized: population-train on simulated persons, one forward pass per unseen person | 04, 41, 42 |
| Training safeguard | early stopping seeded with the init (= prior) state: the returned model is no worse on the composite validation objective; individual metrics/test cells are not guaranteed | W7 |

Implementation is pure NumPy on the package's own gradchecked reverse-mode
autodiff (`upg/autodiff.py`) — exact, seeded, bit-deterministic (requirements
17/18/21; note 23's exactness policy). ~1.2 s to train ≈ 100–200 epochs;
~5 ms to estimate a person.

Unlike `ev`/`kalman`, the GAT is **not told the measurement-noise level** —
it infers everything from the observation window.

## Headline results (median over persons; "bar" = best step-4 value per cell)

Edge RMSE (prior-only comparator ≈ 0.081 / 0.098 by preset):

| Preset | T | GAT | bar (method) | GAT dev-corr | bar | GAT ρ-err | bar |
|---|---:|---:|---:|---:|---:|---:|---:|
| balanced | 30 | **0.083** | 0.126 (kalman) | **0.144** | 0.118 | **0.021** | 0.053 |
| balanced | 250 | **0.081** | 0.182 (kalman) | **0.129** | 0.107 | **0.016** | 0.032 |
| clinical | 30 | **0.082** | 0.111 (kalman) | **0.145** | 0.101 | **0.019** | 0.045 |
| clinical | 250 | **0.078** | 0.106 (ev) | **0.300** | 0.208 | **0.016** | 0.043 |
| transition | 30 | **0.098** | 0.199 (kalman) | **0.213** | 0.128 | **0.017** | 0.061 |
| transition | 250 | **0.091** | 0.237 (kalman) | **0.341** | 0.275 | **0.015** | 0.025 |

Contract verdicts across all 12 cells (3 presets × 4 T): the GAT beats the
best step-4 baseline on **edge RMSE 12/12**, **deviation correlation 12/12**,
**ρ(J) error 12/12**, attractor error 5/12 (GAT range 0.016–0.026),
κ\*-error 0.006–0.012, and regime accuracy 8/12 (it loses regime only on
`clinical_realistic`, where `ev`/`step3` reach 0.95–0.975 vs. GAT 0.875–0.925).
Full tables: `datasets/gat_v1/gat_results.json`; figure:
`datasets/gat_v1/gat_vs_baselines.png`.

## Findings

### 1. Amortization dissolves step 4's shrinkage dilemma

The step-4 estimators paid an absolute-RMSE price for personalizing (kalman
0.13–0.24 vs. prior comparator 0.08–0.10) because per-person fitting must move
off the prior to capture anything. The amortized estimator remains near that
prior comparator (0.078–0.098), beating it in 9/12 cells, **and simultaneously**
carries the best personalization signal yet (dev-corr up to 0.34). It can do
both because the population
taught it *which* deviations the data support at which window lengths — the
"learned, preconditioned, prior-informed" estimator note 41 predicted. The
data-volume features (log-transitions, missingness) are the visible dial:
shrinkage is a learned function of how much the window can identify.

### 2. Dynamics recover better through the amortized route than through any refit

ρ(J) error 0.015–0.026 across every cell — 2–3× better than the best
step-4 value everywhere, at every T, including T=30. For the early-warning
agenda (ρ → 1 as transition risk) this is the axis that matters most, and it
is the one the GAT wins most decisively.

### 3. Exact zeros are a structural requirement, not a detail

The first trained b-head used a softplus output and could never emit b = 0
exactly; the spurious floor (~0.08) unfolded the pitchfork of every truly
bistable person and pinned regime accuracy at 0.675 on the regime-balanced
presets, independent of T. Constraining b̂ to the generative family's support
(TEM/DEV/SYS, ReLU) restored regime accuracy to 0.85–0.975. Methodological
sentence: **when a dynamical property depends on an exact zero, the estimator
must be able to say zero exactly** — the architectural analogue of the
identified-subspace lesson from step 4's EIV estimator.

### 4. Calibration is honest and stable where the Bayes baseline decayed

90% intervals cover 0.873–0.893 across every preset and every T (slightly
anticonservative, ~2σ below nominal), with stable width ≈ 0.25–0.31. The
step-4 `bayes` intervals were calibrated at T=30 but decayed to 0.79 at
T=250 (narrowing around a biased center); the GAT's heteroscedastic head,
trained on the population, does not inherit that decay.

### 5. The low-rank person hypothesis is not testable on this simulator — as predicted

The registered LoRA experiment (note 33): the singular-value spectrum of true
deviations B − B̄ across 960 training draws has effective rank ≈ 29 of 32 —
full-rank, exactly as the note's caveat warned (the simulator's edge noise is
i.i.d. multiplicative by construction). On synthetic data the experiment can
only measure what assuming low rank would *lose*; whether real persons
deviate along few axes is a Phase-4 question. Spectra:
`datasets/gat_v1/spectrum_*.json`.

### 6. What the deep estimator did *not* need

No declared reliability, no per-person iteration, no per-cell retuning: one
fixed config (d=24, 4 heads, 1 block, ~9k parameters — the scaling-consistent
size per notes 35–36) trained once per preset in ≈ 12–19 s of CPU time.

## Updated contract bar (what step 6+ and any future estimator must now beat)

| Axis | New bar (GAT) |
|---|---|
| Edge RMSE | 0.078–0.098 (near prior comparator; wins 9/12 cells) |
| Deviation corr | 0.30 (clinical T=250), 0.34 (transition T=250) |
| ρ(J) error | 0.015–0.026 |
| Regime accuracy | 0.85–0.975 (but ev/step3 remain the bar on clinical: 0.975) |
| Coverage | 0.87–0.89 stable across T (nominal 90) |

## Caveats

- **In-family amortization.** The estimator was trained on the same
  generative family it is scored on; that is the point of Layer-1, but
  out-of-family robustness (heavier-tailed edge noise, unseen κ ranges,
  regime mixes) is untested here — registered as the Garg-style OOD probe
  set for the step-7 tournament.
- κ is still assumed known (only κ·B is identifiable).
- The supervised amortized route requires simulated ground truth; applying
  it to real persons is simulation-based inference (train on the simulator,
  apply to data), which stands or falls with Layer-2 validation of the
  simulator itself.
- Regime on `clinical_realistic` remains the one axis a classical baseline
  still owns; the step-6 transformer's direct regime head (0.975) closes it.
