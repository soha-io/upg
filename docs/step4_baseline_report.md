# Step 4 Report — Temporal-Network Baselines with Uncertainty

Status: Phase 2, step 4 complete.
Source run: `upg/scripts/baseline_study.py`, output `upg/datasets/baselines_v1/`.
Settings: 40 synthetic persons per preset, seed 0, T ∈ {30, 60, 120, 250},
three benchmark presets (`balanced_regimes`, `clinical_realistic`,
`transition_rich`). All estimators receive the same data, the same skeleton
(rule W1), and the same prior (rule W7). Reproduced by `tests/test_baselines.py`.

## The estimators

| Name | What it adds over Step 3 | Module |
|---|---|---|
| `step3` | reference: structure-constrained anchored arctanh-VAR | `recover.fit_person` |
| `bayes` | same estimator as exact conjugate NIG posterior → per-edge sd + Student-t credible intervals (no scipy: incomplete-beta continued fraction + bisection quantiles) | `baselines.fit_bayes_person` |
| `ev` | errors-in-variables moment correction `X'X − mΛ`, solved only in the identified eigensubspace (threshold γ·m·σ²meas), prior in the complement | `baselines.fit_ev_person` |
| `kalman` | EKF + RTS smoother on the *exact* generative state-space (latent ζ=arctanh x; additive process noise, nonlinear observation) + EM re-estimation on smoothed states; handles missing occasions natively | `baselines.fit_kalman_person` |

A new benchmark metric was added in this step: **`edge_dev_corr`** —
correlation of estimated vs. true *deviations from the prior*,
corr(B̂−B̄, B−B̄). The old `edge_corr` is dominated by the prior's own
correlation with the truth (edge magnitudes vary more across edges than
across persons); `edge_dev_corr` is the honest measure of personalization.

## Headline results (median over persons)

Edge RMSE (consensus-prior-alone baseline ≈ 0.08):

| Preset | T | step3 | bayes | ev | kalman |
|---|---:|---:|---:|---:|---:|
| balanced | 30 | 0.299 | 0.299 | 0.222 | **0.126** |
| balanced | 250 | 0.294 | 0.294 | 0.188 | **0.182** |
| clinical | 30 | 0.358 | 0.358 | 0.203 | **0.111** |
| clinical | 250 | 0.461 | 0.461 | **0.106** | 0.163 |
| transition | 30 | 0.460 | 0.460 | 0.458 | **0.199** |
| transition | 250 | 0.578 | 0.578 | 0.415 | **0.237** |

Personalization signal (`edge_dev_corr`) and dynamics (ρ error), T = 250:

| Preset | step3 dev | ev dev | kalman dev | step3 ρ-err | ev ρ-err | kalman ρ-err |
|---|---:|---:|---:|---:|---:|---:|
| balanced | 0.080 | 0.079 | **0.107** | 0.187 | **0.032** | 0.131 |
| clinical | 0.061 | **0.208** | 0.122 | 0.262 | **0.043** | 0.133 |
| transition | 0.143 | 0.147 | **0.275** | 0.044 | **0.025** | 0.042 |

## Findings

### 1. Modeling measurement error is the single biggest win available

Both estimators that account for observation noise (`ev`, `kalman`) dominate
both that don't (`step3`, `bayes`) on essentially every structural and
dynamical axis. This upgrades Step 3's Result 4 ("reliability matters more
than quantity") from a warning into a solved design requirement: the
estimator must carry an explicit measurement model.

### 2. More data can make the naive estimator *worse* — bias is the reason

`step3`/`bayes` edge RMSE *rises* with T in the low-excitation presets
(clinical: 0.358 → 0.461 from T=30 to 250) and edge correlation collapses
(0.258 → 0.023). Mechanism: as data accumulate, the prior's share of the
anchored estimate fades and the estimate converges to the *attenuated*
errors-in-variables limit, which is farther from the truth than the prior
was. Small-T performance was being protected by the prior, not by the data.
This is the sharpest available argument for step 4's existence.

### 3. Credible intervals are honest until bias dominates

The `bayes` estimator's 90% intervals cover the true edges at ≈ 95–99% for
T = 30–60 (conservative, prior-dominated) but decay to ≈ 79–91% at T = 250 —
narrowing intervals around a biased center. Calibrated uncertainty therefore
also requires the measurement model; posterior width alone is not honesty.

### 4. Division of labor between the two measurement-aware estimators

`kalman` is the best all-rounder: best at short T on every preset, best on
`transition_rich` (its smoother exploits the movement), best attractor
recovery throughout (att-err 0.013–0.024), and it handles missingness
natively (uses all T−1 smoothed transitions vs. ~50–70% complete-case
pairs). `ev` wins the long-quiet-series cell (clinical T=250: RMSE 0.106,
dev-corr 0.208) where its moment correction is exact and the smoother's
prior-coupling costs more than it buys. Both are kept in the toolbox; the
report of record for any future comparison must include both.

### 5. Personalization stays hard — as predicted

Even the best `edge_dev_corr` is 0.275 (kalman, transition-rich, T=250).
Individual deviation-recovery remains data-hungry, exactly as the baseline
contract's "person-specific edge target" warned. The clinical quantities
(regime accuracy 0.70–0.975, attractor error ≤ 0.08) remain recoverable at
T = 30–60. Nothing in step 4 changes the contract's separation of success
targets; the ceiling simply moved up.

### 6. EIV correction needs the identified-subspace guard

The naive correction `(X'X − mΛ)⁻¹` exploded (edge RMSE > 1) because
attractor-dominated series make several eigendirections of X'X pure noise
(eigenvalue ≈ m·σ²): subtracting the noise leaves nothing to invert, while
the rhs retains noise of order √m·σ. Truncating to eigendirections with
signal > γ·m·σ² (γ=1) and deferring to the prior in the complement fixed it
(clinical T=250: 1.214 → 0.106). Methodological sentence for the
manuscript: *correct only where the data identify; defer to theory where
they do not* — rule W7 restated as a subspace decomposition.

## What the deep estimators must now beat (updated contract bar)

Per `baseline_contract.md`, steps 5–6 are scored against the *best* step-4
baseline per cell, not against step 3:

| Axis | Bar (best step-4 value) |
|---|---|
| Edge RMSE, short T | kalman: 0.111–0.199 at T=30 |
| Edge RMSE, long T | ev/kalman: 0.106–0.237 at T=250 |
| Deviation corr | kalman: 0.28 (transition-rich, T=250) |
| ρ(J) error | ev: 0.025–0.053 |
| Regime accuracy | 0.775–0.975 by preset |
| Missingness | kalman handles incomplete occasions natively |
| Uncertainty | bayes: calibrated at small T; must fix the large-T decay |

## Caveats

- Synthetic data under the model's own generative assumptions; `kalman`
  benefits from knowing the true noise magnitudes (they are passed from the
  config, as a real study would pass reliability-derived values — see
  `measurement_mapping.md`).
- κ is still assumed known (only κ·B is identifiable).
- The EM smoother couples the smoothed states to the current parameter
  estimate; its residual prior-confirmation bias is visible in the
  balanced-preset dev-corr plateau (~0.11) and is documented rather than
  hidden.
- Scaling-law fits (`fit_scaling_law`) are meaningful only for estimators
  whose error *decreases* with T; for `step3` in low-excitation presets the
  premise fails (finding 2), so the law is reported for the recovery_v1
  curve and the measurement-aware estimators only.
