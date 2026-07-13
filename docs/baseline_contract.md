# Baseline Contract

Status: contract for Step 4 and later estimators.

Step 4 is the baseline layer: VAR, graphical VAR, DSEM, Bayesian state-space, or
Bayesian structural time-series models. The graph-attention and transformer
estimators only become meaningful after they beat these baselines on this
contract.

## Fixed Inputs

Use the same benchmark presets and scorecard:

```text
balanced_regimes
clinical_realistic
transition_rich
```

Use the metrics in `benchmark_scorecard.md`. Use the measurement rules in
`measurement_mapping.md`. Report all headline numbers with uncertainty across
seeds or bootstrap replicates.

## Current Baseline Snapshot

From `upg/datasets/recovery_v1/recovery_results.json`:

| Comparator | T | Edge RMSE | Edge correlation | Regime accuracy | Attractor error |
|---|---:|---:|---:|---:|---:|
| Prior alone | any | 0.082 | n/a | n/a | n/a |
| Free estimator | 60 | 0.558 | n/a | n/a | n/a |
| Prior-anchored estimator | 60 | 0.354 | 0.266 | 0.912 | 0.022 |
| Free estimator | 1000 | 0.193 | n/a | n/a | n/a |
| Prior-anchored estimator | 1000 | 0.183 | 0.622 | 0.963 | 0.010 |

Measurement-noise stress test at T=250:

| Measurement-noise sd | Edge RMSE | Regime accuracy | Attractor error |
|---:|---:|---:|---:|
| 0.00 | 0.167 | 0.963 | 0.004 |
| 0.05 | 0.233 | 0.950 | 0.011 |
| 0.10 | 0.394 | 0.925 | 0.035 |
| 0.15 | 0.573 | 0.938 | 0.069 |
| 0.20 | 0.683 | 0.912 | 0.099 |

Sampling stress test at T=250 and measurement-noise sd 0.05:

| Sampling rate | Median transitions | Edge RMSE | Regime accuracy |
|---:|---:|---:|---:|
| 1.00 | 249.0 | 0.233 | 0.950 |
| 0.80 | 158.5 | 0.248 | 0.938 |
| 0.60 | 90.5 | 0.295 | 0.912 |
| 0.40 | 39.5 | 0.327 | 0.938 |
| 0.25 | 14.0 | 0.307 | 0.900 |

## What Step 4 Must Beat

The temporal-network baseline must improve the Step 3 prior-anchored estimator
on at least one important axis without degrading the others:

| Axis | Minimum expectation |
|---|---|
| Clinical | Match or improve regime accuracy and attractor error at T=30-60 on `clinical_realistic` and `balanced_regimes`. |
| Structural | Improve edge correlation or edge RMSE at T>=250, especially in `transition_rich`, without relying on free dense structure. |
| Dynamical | Improve `rho`, `kappa*`, loop-gain, stability-class, or transition-prediction metrics. |
| Missingness | Handle incomplete EMA directly rather than relying only on complete transitions. |
| Uncertainty | Return calibrated intervals or credible intervals for person-level quantities. |

Failure mode to avoid: a Step 4 model lowers edge RMSE but worsens regime
accuracy, attractor error, transition prediction, or calibration.

## What Future GAT / Transformer Estimators Must Beat

The future graph-attention estimator must beat the best Step 4 temporal-network
baseline on the same benchmark presets, not only the old Step 3 estimator.

Minimum claims required:

| Future estimator | Must beat temporal baseline on |
|---|---|
| Structure-constrained GAT | Edge RMSE/correlation, loop-gain recovery, or person-specific heterogeneity recovery, with the published skeleton as the mask. |
| Transformer measurement model | Node activation calibration, missing/irregular item handling, and observation uncertainty. |
| Transformer forecaster | Transition prediction, relapse/recovery early warning, and calibrated prognosis on `transition_rich`. |

No deep estimator counts as an improvement if it learns outside the published
edge skeleton without a separately registered theory-comparison test.

## Separate Success Targets

Case formulation target:

```text
T = 30-60 may be enough for regime, attractor, and prognosis when measurement
is reliable and the estimator is prior-anchored.
```

Person-specific edge target:

```text
Hundreds to thousands of occasions may be needed for stable individual edge
weights, especially without strong transitions or experimental perturbation.
```

Theory-testing target:

```text
Population-level recovery and model comparison may matter more than perfect
one-person edge recovery. Use the benchmark to compare theories, not merely to
chase individual edge accuracy.
```

## Contract Sentence

The baseline layer exists to protect the invention from the wrong metric:

```text
Estimate clinical dynamics early, estimate fine structure cautiously, never
estimate freely, anchor to theory, and treat measurement quality as sacred.
```
