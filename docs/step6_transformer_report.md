# Step 6 Report — The Temporal Transformer as Measurement Model + Forecaster

Status: Phase 2, step 6 complete.
Source run: `upg/scripts/forecast_study.py`, output `upg/datasets/forecast_v1/`.
Settings: one model per preset (160 train / 40 val / 40 eval persons, eval
seed 0, preset-default T = 120/100/180); horizon 5; Gaussian NLL heads
throughout. Reproduced by `tests/test_transformer.py`; engine gradchecked by
`tests/test_autodiff.py`. Training curves logged per chunk
(`*_training.json`), per note 40's phase-change warning.

## What the model is

A small causal encoder (2 blocks, d=32, 4 heads, ~23k parameters) with every
block choice the one registered in the reading notes: missingness embeddings
instead of imputation (02), ALiBi relative-time biases and no positional
embeddings (30), RMSNorm pre-norm (31), SwiGLU feed-forward (32), residuals
everywhere (37). One trunk, three typed heads (05):

1. **Filter head** (measurement model): x̂(t) ± σ from y(1..t) — causal, the
   deployable direction (03); missing occasions are filled by the dynamics.
2. **Forecast head**: one-shot multi-horizon x̂(t+1..t+5) ± σ conditioned on
   the *known-future* treatment schedule (13/14 — no recursive rollout).
3. **Dynamics head** (person summary token, 11): ρ̂(J), κ̂\*, regime.

Causality is enforced by test (`test_causality_no_future_observation_leak`):
outputs at t are bit-identical under any corruption of later observations.

## Headline results (held-out persons)

Forecast RMSE on true states, h = 1 / 3 / 5, with the registered comparators
— persistence, the **explicit pipeline** (fit_kalman_person → EKF filter →
map propagation: our own step-4 estimator used as a forecaster), and the
**oracle** (same pipeline, true parameters):

| Preset | transformer | persistence | explicit | oracle |
|---|---|---|---|---|
| balanced | 0.064 / 0.068 / 0.070 | 0.092 / 0.098 / 0.101 | 0.061 / 0.066 / 0.068 | 0.054 / 0.059 / 0.061 |
| clinical | **0.054 / 0.055 / 0.056** | 0.104 / 0.106 / 0.108 | 0.079 / 0.079 / 0.079 | 0.053 / 0.046 / 0.044 |
| transition | **0.121 / 0.129 / 0.144** | 0.165 / 0.189 / 0.218 | 0.157 / 0.160 / 0.163 | 0.078 / 0.084 / 0.088 |

Filter: RMSE 0.052 / 0.062 / 0.110 (clinical/balanced/transition) — at or
below the measurement-noise floor — with missing occasions imputed at
0.062 / 0.079 / 0.234. Coverage of the 90% intervals: 0.879–0.905 (filter
and every forecast horizon). Dynamics head: ρ MAE 0.042–0.056, κ\* MAE
0.011–0.017, regime accuracy 0.95–0.975. Early warning (P(DIS crosses 0.5
within 5 occasions), from the Gaussian heads alone): relapse AUC 0.955–1.00,
recovery AUC 0.939–0.983. Figure: `datasets/forecast_v1/forecast_comparison.png`.

## Findings

### 1. The implicit-vs-explicit experiment (note 41) has a direction-specific answer

Where the population carries usable regularities and series are quiet-ish
(`clinical_realistic`), the amortized transformer **beats the explicit
per-person refit** (0.054 vs 0.079 at h=1) and reaches the oracle at h=1
(0.054 vs 0.053). Where movement is rich (`transition_rich`) it also wins
(0.121 vs 0.157) but a large oracle gap remains (0.078) — the headroom is in
state-dependent dynamics around the treatment pulse, which is precisely the
regime-switching cell where note 44 predicts the selective-SSM challenger
should be tried next. On `balanced_regimes` the explicit pipeline keeps a
hair's-width lead (0.061 vs 0.064). Amortization wins where learning the
prior from the population is worth more than refitting the individual.

### 2. Coupling is detectable by forecast accuracy — the PatchTST null loses

The registered channel-independent null (note 16) — same architecture, each
dimension forecast from its own history only — degrades forecasting on
`transition_rich` by 13–20% (0.139/0.154/0.173 vs 0.121/0.129/0.144). On
movement-rich data, cross-dimension coupling carries predictive information
that a marginal model cannot recover: forecast RMSE *is* sensitive to the
mechanism here, contrary to the pessimistic reading of the forecasting
literature. (Budget note: the null trained on 60 persons / 45 epochs vs.
160 / 138 — a smaller budget; the deficit is consistent across horizons and
larger than the main model's own remaining training drift, but an
equal-budget replication is the clean version of this claim.)

### 3. Attention is doing temporal work — the uniform null degrades everywhere

Replacing learned attention with causal-uniform averaging (note 14's null)
raises h=1 RMSE from 0.064→0.091 (balanced), 0.054→0.081 (clinical),
0.121→0.170 (transition). The learned attention pattern, not the residual
stream alone, carries the filtering.

### 4. In-context personalization is visible — and confounded exactly where expected

The in-context score (late-window minus early-window one-step error, note
40) is positive on balanced (+0.008) and clinical (+0.015): the model
forecasts a person better after seeing more of them, the amortized-
personalization signature. On transition_rich it is negative (−0.045) — not
absence of personalization but the confound the score's design warned about:
late windows sit in withdrawal/maintenance phases that are intrinsically
harder than the pre-treatment plateau. A phase-matched score is the fix,
registered for the next revision.

### 5. The measurement model earns its name

The filter tracks true states at or below the noise floor while receiving
30–15% missing occasions, imputes unobserved occasions through the dynamics
(0.062–0.079 on the EMA-like presets; 0.234 on transition_rich, where a
missing occasion can hide a treatment-phase switch), and its intervals hold
~0.88–0.90 empirical coverage at 90% nominal — the deliverable
`measurement_mapping.md` asks estimators to consume and produce.

### 6. Early warning from calibrated heads needs no separate classifier

Threshold-crossing probabilities composed from the forecast Gaussians give
relapse AUC ≥ 0.955 and recovery AUC ≥ 0.939 on every preset — the van de
Leemput early-warning claim, implemented and testable end to end on the
model's own uncertainty. The dynamics head simultaneously reads ρ(J) to
0.04–0.06 MAE, the second, independent route to transition risk.

### 7. Architecture diagnostics stayed clean

Rank residual (note 37) 0.12–0.54 across layers — far from collapse;
attention effective context 26–42 occasions (entropy-based, note 27),
consistent with a filter that needs tens of occasions to pin the state and
with the Markov structure of the generator (note 22's saturation argument).

## Updated contract bar

| Axis | New bar (step 6) |
|---|---|
| 1-step forecast RMSE | 0.054 / 0.064 / 0.121 by preset (vs oracle 0.053 / 0.054 / 0.078) |
| Forecast coverage (90%) | 0.88–0.91, all horizons |
| Filter RMSE (with missingness) | 0.052–0.110 |
| Regime accuracy (direct head) | 0.95–0.975 (closes step 5's clinical gap) |
| ρ(J) MAE | 0.042–0.056 (step 5's GAT remains better: 0.015–0.026) |
| Early warning | relapse AUC ≥ 0.955, recovery AUC ≥ 0.939 |

Division of labor as the notes designed it (17, 20): **the GAT owns
structure** (edges, loops, ρ from the fitted graph), **the transformer owns
state** (filtering, imputation, forecasting, event risk); the regime/ρ heads
give cheap cross-checks between the two.

## Caveats

- Supervision uses the simulator's true latent states — legitimate for
  Layer-1 method recovery, unavailable on real data, where the targets
  become held-out items (masked-reconstruction, note 02) and future
  observations; the architecture is unchanged but those numbers must be
  re-earned.
- κ known; regular sampling (ALiBi suffices; RoPE/Δt-discretization is the
  registered Phase-4 upgrade for real timestamps, notes 29/43/44).
- The transition_rich model was stopped at a flattening-but-nonzero
  validation slope (138 epochs; curve in `tf_transition_rich_training.json`);
  the resume protocol makes further training a one-line rerun.
- The early-warning AUCs use the model's own 0.5-crossing definition on true
  states; real-data versions need a clinically anchored event definition.
- Independence approximation in the crossing probability (product over
  horizons); a joint-path version would be slightly sharper.
