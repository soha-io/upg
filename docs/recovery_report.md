# Minimum Publishable Recovery Report

Status: pre-Step-4 internal report.

Source run: `upg/scripts/recovery_study.py`, output `upg/datasets/recovery_v1`.
Settings: 80 synthetic persons, seed 0, process noise 0.10. The population is
dimension-level over `TEM`, `DEV`, `PER`, `NEED`, `ME`, `DIS`, and `SYS`.

## Question

How much data does it take to estimate one person?

The answer depends on what "estimate" means. Clinical dynamics recover much
earlier than fine person-specific edge structure. The benchmark therefore must
score clinical, structural, dynamical, and practical recovery separately.

## Method

The simulator perturbs the consensus dimension-level prior into person-specific
ground truth. It then emits noisy EMA-style observations with known latent
states, known coupling matrix `B`, known standing conditions `b`, known global
coupling `kappa`, and known dynamical labels.

The Step 3 estimator is a structure-constrained arctanh-VAR:

```text
arctanh(x[t+1]) = kappa * B * x[t] + kappa * g * u[t] + b + error
```

It estimates only edges present in the theory skeleton and shrinks coefficients
toward the consensus prior. This is rule W1 plus rule W7 in executable form.

## Result 1: Clinical State Recovers Quickly

At T=60 occasions, regime accuracy is 91.25% and attractor DIS absolute error is
0.022. At T=30, regime accuracy is already 87.50% and attractor error is 0.022.

This supports the practical claim that short reliable series can support case
formulation: regime, attractor, and prognosis are available before the full
edge matrix is accurately personalized.

## Result 2: Full Edge Structure Needs Much More Data

Edge recovery improves slowly:

| T | Edge RMSE | Edge correlation | Regime accuracy | Attractor error |
|---:|---:|---:|---:|---:|
| 30 | 0.364 | 0.257 | 0.875 | 0.022 |
| 60 | 0.354 | 0.266 | 0.912 | 0.022 |
| 120 | 0.285 | 0.341 | 0.925 | 0.018 |
| 250 | 0.233 | 0.408 | 0.950 | 0.011 |
| 500 | 0.207 | 0.520 | 0.938 | 0.010 |
| 1000 | 0.183 | 0.622 | 0.963 | 0.010 |

The consensus-prior edge RMSE baseline is 0.082, so absolute recovery of
person-specific edges is not the right first success criterion at T=30-60.

## Result 3: Prior Anchoring Beats Free Estimation

At T=60, the prior-anchored estimator has edge RMSE 0.354. The free
unregularized estimator has edge RMSE 0.558. At T=30, the gap is even larger:
0.364 versus 0.846.

The strongest methodological sentence from Step 3 is:

```text
Do not estimate freely; estimate from theory plus shrinkage.
```

## Result 4: Measurement Reliability Matters More Than Quantity

At T=250, increasing measurement-noise sd from 0.00 to 0.20 raises edge RMSE
from 0.167 to 0.683. Attractor error rises from 0.004 to 0.099.

This is the main design constraint before Step 4. A better temporal estimator
cannot rescue an undefined or unreliable measurement layer.

## Result 5: Moderate Missingness Is Tolerable

At T=250 and measurement-noise sd 0.05:

| Sampling rate | Median usable transitions | Edge RMSE | Regime accuracy |
|---:|---:|---:|---:|
| 1.00 | 249.0 | 0.233 | 0.950 |
| 0.80 | 158.5 | 0.248 | 0.938 |
| 0.60 | 90.5 | 0.295 | 0.912 |
| 0.40 | 39.5 | 0.327 | 0.938 |
| 0.25 | 14.0 | 0.307 | 0.900 |

Compliance in the 60-80% EMA range is workable for clinical dynamics when the
prior is strong. The caveat is that sparse sampling loses transitions, which
matters for fine structure and transition forecasting.

## Interpretation

Step 3 does not say "T=60 estimates the person graph." It says T=60 is already
useful for clinical dynamics when the estimator is anchored to theory and the
measurement layer is reliable.

The next estimator should not optimize edge RMSE alone. It must preserve the
early clinical signal while improving structural and dynamical recovery where
the data contain enough movement.

## Caveats

- These are synthetic data under the model's own generative assumptions.
- The estimator assumes known `kappa`; only the effective product `kappa * B` is
  directly identifiable without additional constraints.
- Stable persons near one attractor are weakly informative for edge structure.
- Measurement noise creates an errors-in-variables floor that more occasions do
  not automatically remove.
