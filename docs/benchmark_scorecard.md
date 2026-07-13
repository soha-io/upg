# Benchmark Scorecard

Status: frozen pre-Step-4 scorecard.

Purpose: define what counts as "good" before adding VAR, graphical VAR, DSEM,
Bayesian time-series, graph-attention, or transformer estimators.

## Benchmark Populations

Every Step 4 estimator must report results separately on:

| Preset | Purpose |
|---|---|
| `balanced_regimes` | Protects minority regimes. Quiescent, pinned-high, and bistable persons are quota-sampled in roughly equal numbers. |
| `clinical_realistic` | Keeps the EMA-like population mix: more pinned-high and quiescent persons, fewer bistable persons, with realistic missingness/dropout. |
| `transition_rich` | Tests state movement, recovery, relapse, withdrawal, and maintenance under a pulsed treatment schedule. |

Do not collapse these into one average. A model can look good on
`clinical_realistic` while failing bistability or transitions.

## Clinical Recovery

| Metric | Code key or required output | Primary horizon | Interpretation |
|---|---|---:|---|
| Regime accuracy | `regime_accuracy` | T=30-60 | Quiescent / pinned-high / bistable state recovery. Also report macro accuracy on `balanced_regimes`. |
| Attractor error | `median_attractor_abs_err` | T=30-60 | Absolute error in the disorder fixed point. |
| Prognosis / transition prediction | Required for Step 4 | T=30-250 | Predict recovery, relapse, destabilization, or threshold crossing on `transition_rich`. Report balanced accuracy or AUC plus calibration. |

Current Step 3 snapshot: at T=60, regime accuracy is 0.9125 and attractor error
is 0.022.

## Structural Recovery

| Metric | Code key or required output | Primary horizon | Interpretation |
|---|---|---:|---|
| Edge RMSE | `median_edge_rmse` | T=250-1000+ | Absolute recovery of person-specific edge weights. |
| Edge correlation | `median_edge_corr` | T=250-1000+ | Whether the personalized edge ranking is recovered. |
| Prior RMSE | `median_prior_rmse` | All horizons | The consensus prior alone. This is the "do nothing personalized" floor. |
| Loop gain recovery | Required for Step 4 | T=250-1000+ | RMSE or rank correlation of named loop gains, especially amplifying and regulating loops. |

Current Step 3 snapshot: at T=60, edge RMSE is 0.354 and edge correlation is
0.266. At T=1000, edge RMSE is 0.183 and edge correlation is 0.622. The
consensus-prior edge RMSE is 0.082.

Rule: do not judge early person-specific modeling by absolute edge RMSE alone.
At T=30-60, the clinical target matters more than full edge personalization.

## Dynamical Recovery

| Metric | Code key or required output | Primary horizon | Interpretation |
|---|---|---:|---|
| Stability error | `median_rho_abs_err` | T=60-250 | Error in local Jacobian spectral radius. |
| Bifurcation-threshold error | `median_kappastar_abs_err` | T=250-1000+ | Error in `kappa* = 1 / lambda_max(B)`. |
| Stability-class accuracy | Required for Step 4 | T=60-250 | Stable / near-critical / unstable or analogous classes. |
| Transition prediction | Required for Step 4 | T=60-250 | Early warning for relapse, recovery, or destabilization in `transition_rich`. |

Step 4 must make these dynamical metrics first-class. A temporal-network
baseline that lowers edge RMSE but worsens transition prediction is not a win.

## Practical Usefulness

| Metric | Required output | Primary horizon | Interpretation |
|---|---|---:|---|
| Case-formulation adequacy | Pass/fail plus clinical metrics | T=30-60 | Can the model support a defensible TND-style formulation? |
| Missingness robustness | Sweep by sampling rate | T=60-250 | Does performance survive realistic EMA compliance? |
| Reliability sensitivity | Sweep by measurement-noise sd | T=60-250 | Does performance degrade gracefully as item reliability falls? |
| Uncertainty usefulness | Calibration curve or coverage | T=30-250 | Are intervals credible enough for decision support? |

Current Step 3 snapshot: measurement-noise sd 0.20 at T=250 raises edge RMSE to
0.683 and attractor error to 0.099. Measurement reliability is therefore a
benchmark variable, not a nuisance setting.

## Required Reporting Template

Each estimator report must include:

1. Results by preset: `balanced_regimes`, `clinical_realistic`,
   `transition_rich`.
2. Results by T: 30, 60, 120, 250, 500, and 1000 where feasible.
3. Results by measurement-noise sd: 0.00, 0.05, 0.10, 0.15, 0.20.
4. Results by sampling rate: 1.00, 0.80, 0.60, 0.40, 0.25.
5. Comparisons against prior alone, free estimation, prior-anchored estimation,
   and the current temporal baseline.
6. Uncertainty intervals or seed variability for every headline number.

## Non-Negotiable Decision Rule

The project optimizes for:

```text
clinical dynamics early,
fine structure cautiously,
theory anchoring always,
measurement reliability first.
```

No model passes the benchmark by improving only edge RMSE while degrading
regime recovery, attractor recovery, transition prediction, or calibration.
