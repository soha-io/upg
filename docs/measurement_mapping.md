# Measurement Mapping

Status: pre-Step-4 measurement contract.

Principle: do not invent the estimator before defining what it is estimating.
The estimator receives graph-node activations, not raw questionnaire rows. This
file defines the default bridge from observed items to dimension-level nodes.

## Common Scoring Rules

1. Orient every item so higher values mean greater activation of the target
   dimension as modeled in the dimension-level dynamics. Protective items are
   reverse-scored when they feed a load/thwart node.
2. Convert raw item responses to a 0-1 metric before node aggregation.
3. Compute a node score only when at least 60% of that node's scheduled items are
   present at that occasion. Otherwise mark the node missing for that occasion.
4. Do not mean-impute missing occasions before estimation. Pass missingness to
   the estimator or to a state-space measurement model.
5. Pass uncertainty with each node score: `x_hat`, `measurement_sd`,
   `n_items_answered`, `reliability_assumption`, and `missing_rule`.
6. Static or slow-moving instruments update standing conditions `b`, priors, or
   person covariates. Repeated EMA items update time-varying activations `x(t)`.

Default conversion from reliability to observation uncertainty:

```text
measurement_sd = observed_sd * sqrt((1 - reliability) / reliability)
```

When an empirical reliability estimate is unavailable, use the conservative
defaults below and flag the value as assumed.

## Dimension-Level Mapping

| Node | What it measures | Candidate instruments or item families | Items | Scale | Reliability assumption | Missingness rule | Aggregation | Uncertainty passed |
|---|---|---|---:|---|---|---|---|---|
| `TEM` | Temperamental reactivity and regulation load | Negative affectivity, behavioral inhibition, effortful-control, arousal/reactivity EMA items | 4-8 EMA items plus baseline temperament scale | 0-4 or 1-5, normalized to 0-1 | >=0.80 baseline, >=0.70 EMA | Score if >=60% items present | Mean of oriented items, optionally blended with baseline temperament prior | Node-level `measurement_sd`; baseline prior variance |
| `DEV` | Developmental history, learning history, adversity, sensitive-period load | ACE/CTQ-style adversity, developmental events, attachment/caregiving history, major transitions | 6-12 baseline items; event updates as needed | Count/severity normalized to 0-1 | >=0.80 for scales; event reliability documented separately | Do not prorate if sentinel adversity items are absent | Baseline standing load `b_DEV`; event shocks can be logged separately | Prior variance plus missing-history flag |
| `PER` | Trait and facet disposition relevant to ongoing dynamics | Big Five / HiTOP trait markers / IPIP or BFI-style facets | 10-30 baseline items, shorter repeated trait-state markers optional | 1-5 normalized to 0-1 | >=0.85 baseline target | Score if >=70% items present | Facet-weighted mean into personality load or stabilizing tendency | Trait-score standard error |
| `NEED` | Need satisfaction, frustration, deprivation, and resource pressure | Autonomy, competence, relatedness, safety, esteem, meaning, material need items | 6-14 EMA or weekly items | 0-4 or 1-7 normalized to 0-1 | >=0.80 target | Score if >=60% items present | Separate satisfaction/frustration internally, then orient to modeled activation | Node-level `measurement_sd`; channel flag if available |
| `ME` | Motivation and emotion state | Core affect, discrete negative affect, avoidance/approach drive, wanting/liking, regulation effort | 6-12 EMA items | 0-100 slider or 0-4 normalized to 0-1 | >=0.75 EMA target | Score if >=60% items present | Mean or two-channel readout collapsed to dimension activation for current simulator | Node-level `measurement_sd`; item-count penalty |
| `DIS` | Symptom and disorder-load activation | PHQ/GAD/HiTOP/SCL-style symptom items, impairment, risk flags | 8-20 items depending on study | 0-3 or 0-4 normalized to 0-1 | >=0.85 target | Score if >=70% symptom items present; risk items never silently imputed | Severity-weighted mean, with risk indicators retained separately | Node-level `measurement_sd`; risk-missing flag |
| `SYS` | Environmental load, support, threat, and access constraints | Family conflict/support, financial strain, food/housing security, discrimination, sleep/workload, care access | 6-12 EMA/weekly items plus baseline context | Mixed, normalized to 0-1 | >=0.75 target | Score if >=60% items present | Support/thwart items oriented to net system load; major events retained as event flags | Node-level `measurement_sd`; event-source flag |
| `THER` | Treatment/control input, not an endogenous node in the dimension simulator | Session attendance, medication exposure, alliance, homework/practice, dose/intensity | 2-8 per treatment window | Dose or Likert normalized to 0-1 | >=0.75 target where multi-item | Missing dose is unknown, not zero, unless verified no treatment occurred | Produces control input `u(t)` and treatment-quality modifiers | Dose uncertainty and verified-zero flag |

## Measurement Quality Gates

Before Step 4, every dataset must declare:

| Field | Required answer |
|---|---|
| Item source | Which questionnaire, EMA item, sensor, event log, or clinician rating feeds each node? |
| Item count | How many items per node per occasion? |
| Scale | Raw response scale and transformation to 0-1. |
| Reliability | Empirical reliability if available; otherwise an explicit assumption. |
| Missingness | Per-item and per-occasion missingness rule. |
| Aggregation | Mean, weighted mean, latent score, or state-space observation model. |
| Uncertainty | Observation variance passed into the graph estimator. |

## Current Simulator Approximation

The current simulator compresses this layer to one observed value per node per
occasion and one global measurement-noise parameter, `SimConfig.meas_noise`.
That is acceptable for Step 3 recovery, but Step 4 should replace it with a
node-specific observation model that uses the uncertainty fields above.

Measurement target before Step 4: keep effective measurement-noise sd near
0.05-0.10 when possible. The recovery study shows that sd 0.20 can dominate the
estimation problem.
