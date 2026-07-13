# Data-Gathering Protocol — From Simulated Recovery to Real Persons

Status: Phase-4 design document (pre-registration draft).
Companion to `measurement_mapping.md` (the item→node bridge; this document
is the study-design layer above it), `baseline_contract.md` (what counts as
good), and the step 3–6 reports (where every design number below comes from).

Everything here is derived from what the synthetic studies already
demonstrated. The plan buys, in order, the things the recovery curves said
are binding constraints — and refuses to buy things they said are not.

---

## 1. Design principles (each traceable to a measured result)

| # | Principle | Source result |
|---|---|---|
| P1 | **Reliability before quantity.** Measurement-noise sd 0.20 raised edge RMSE 0.17→0.68 at T=250; no amount of extra T removes the errors-in-variables floor. | Step 3, Result 4; step 4, Finding 1 |
| P2 | **Movement is information.** Quiescent series are weakly informative (persistent excitation); `transition_rich` gave the best deviation recovery for every estimator family. | recover.py notes; step 4 Finding 4; step 5 tables |
| P3 | **Two goals, two data shapes.** Regime/attractor/prognosis recover at T≈30–60; person-specific edges keep improving to T≈1000+. Design separate tiers, not one compromise study. | Step 3 Results 1–2 |
| P4 | **Moderate missingness is survivable.** Compliance 60–80% barely moved clinical recovery; do not burden participants into dropout chasing 100%. | Step 3 Result 5 |
| P5 | **Treatment schedules are gold.** Known-future u(t) is both the forecaster's privileged input and the excitation that identifies edges and direction (rule W4). | Step 6 design; casestudy control results |
| P6 | **Only κ·B is identifiable.** Scales must be harmonized across sites and waves, or estimates are of effective coupling only — acceptable, but it must be pre-registered as such. | recover.py identifiability notes |

---

## 2. Phased plan

### Phase A — Retrospective fitting on existing data (start immediately; no collection)

| Dataset family | Strata exercised | Claim tested | Note |
|---|---|---|---|
| Open ESM/EMA depression datasets (critical-slowing-down and symptom-network literature) | ME, DIS | ρ(J) early warning, retrospectively | Named in Batch J §10.4 |
| ABCD | DEV, TEM, SYS | developmental gates g(t) | access application required — as of 2025-06-02 the NIMH Data Archive (NDA) no longer accepts new ABCD requests; access moved to the NBDC Data Hub (nbdc-datahub.org): Data Use Certification + responsible-use training + NIST-compliant compute (non-NIST in-place workflow expected late spring 2026) |
| RADAR-MDD | DIS, THER | relapse dynamics (transition-rich shape) | access application required — no self-serve portal; data available from the corresponding author on reasonable request via the RADAR-CNS consortium (data-sharing agreement) |
| Open Big Five / HiTOP item pools | PER, TEM | disposition measurement models | free |

Why first: months faster than collection, provides real falsifiers, and
calibrates the simulator's realism (noise, missingness texture, movement
rates) before prospective money is spent. Deliverable: a Layer-2 report in
the style of the step reports, per dataset.

### Phase B — Measurement pilot (n ≈ 30, 14 days, 3 prompts/day)

The highest-ROI step in the plan (P1). Goals, in order:

1. **Per-node EMA reliability.** Estimate within-occasion reliability per
   node (split-half across the node's items; multilevel reliability across
   days). Target: effective measurement sd ≈ 0.05–0.10 after the 0–1
   transform, using the contract's conversion
   `measurement_sd = observed_sd * sqrt((1 - reliability) / reliability)`.
2. **Item pruning and spacing.** Drop items that don't load; set response
   thresholds empirically (quantile spacing per the IRT/NF4 argument,
   note 34) rather than assuming equal intervals.
3. **Burden calibration.** Measure completion time and compliance decay;
   the main study's cadence is whatever the pilot shows participants sustain
   at ≥ 70% for the burst length.
4. **Missingness taxonomy.** Log *why* occasions are missed (asleep, busy,
   distressed, technical) — the MNAR audit the estimators need.

Iterate items and repeat once if any node misses the reliability target.
No dynamics analyses are run on pilot data; it is a measurement study.

### Phase C — Prospective cohort, two tiers

**Tier 1 — breadth (formulation-level claims, theory tournament).**
Many persons × short reliable windows: target **P ≈ 150–300 persons,
T ≈ 45–60 usable occasions each** (≈ 3–4 weeks at 2–3 prompts/day). Powers
the concurrent-validity claim, regime/attractor recovery, and step 7's
tournament, where population-level comparison matters more than per-person
edge precision.

**Tier 2 — depth (person-specific structure).**
A nested subsample: **P ≈ 20–40 persons followed 6–18 months** (burst
design, Section 4), yielding hundreds to low-thousands of occasions each.
This is the only tier from which individual edge estimates should ever be
reported (P3).

**Recruit at treatment entry.** People beginning psychotherapy or starting/
changing medication are a natural pulsed-treatment cohort — onset, response,
maintenance, sometimes withdrawal — the most informative occasions per
prompt available (P2, P5). Complement with a non-treatment community arm as
the quiescent reference.

**Quota the sample like `balanced_regimes`.** Recruit across severity
(community / subclinical / clinical), across ages (the gates are the
all-ages mechanism; child and adolescent arms use age-appropriate
instruments and consent/assent), and explicitly include neurodivergent
participants (project requirement 14). Averages hide minority-regime
failures; quotas prevent that.

---

## 3. What to collect (the streams)

### 3.1 Baseline battery (once, plus annual re-administration in Tier 2)

| Node | Instrument candidates | Purpose | Licensing check |
|---|---|---|---|
| TEM | ATQ short form (adults) / EATQ-R (adolescents) / CBQ (children); EAS as fallback | reactivity/regulation priors | mostly research-free |
| DEV | ACE questionnaire; CTQ-SF; life-events checklist; attachment/caregiving history | standing load b_DEV; gate placement | **CTQ-SF is proprietary** — verify or substitute |
| PER | BFI-2 (60 items, facets) or IPIP-NEO-120 | trait priors; bridge-dimension tests | BFI-2 free for research; IPIP public domain |
| DIS | PHQ-9, GAD-7 + a HiTOP-consistent broad inventory | severity anchor; disorder priors | PHQ/GAD public domain |
| NEED | BPNSFS (satisfaction + frustration subscales) | dual-channel priors | research-free |
| SYS | household composition, financial strain, USDA 6-item food security, neighborhood/discrimination short forms | environment priors; b_SYS | mostly public |
| — | demographics, exact date of birth, medication list, diagnosis history | gates g(t); covariates | — |

### 3.2 EMA core (every prompt; the x(t) stream)

Per `measurement_mapping.md`, oriented and 0–1 normalized; 2–4 items per
node per prompt, rotating item subsets to control burden while keeping ≥ 2
anchors fixed:

- **ME**: core affect (valence, arousal sliders), 2–3 discrete negative
  affect items, wanting/approach vs avoidance, regulation effort.
- **DIS**: 3–4 symptom items matched to the person's presenting problem +
  1 impairment item; risk items per site protocol, never silently imputed.
- **NEED**: 2–3 satisfaction/frustration items (rotating domains).
- **SYS (state)**: 1–2 items — current context, conflict/support since last
  prompt.
- **TEM (state marker)**: 1 arousal/reactivity item.
- Skipped items are *absent*, never imputed at collection time (mask
  embeddings and state-space handling exist for exactly this).

### 3.3 Treatment log u(t) — collected, not inferred (P5)

- **Planned schedule** (known-future input): upcoming session dates, planned
  dose changes, planned discontinuation.
- **Delivered**: attendance, session type, medication taken (dose, time),
  homework done.
- **Quality modifiers**: alliance short form (e.g., WAI-SR) monthly;
  adherence self-report weekly.
- Missing dose = *unknown*, distinct from verified zero (contract rule).

### 3.4 Events (timestamped, both arms)

Life events (loss, conflict, job/school change, move, health event),
reported at each weekly review with date; these mark expected transitions,
trigger bursts (Section 4), and provide the SYS shock ledger.

### 3.5 Passive sensing (optional; per-stream consent; Tier 2 default-on)

Only streams that map to a named node: sleep duration/timing and step
count/activity (ME/DIS proxies, circadian structure); optionally phone-use
rhythm. Nothing collected "because we can" — data minimization is a design
rule, not a compliance afterthought (Section 7).

### 3.6 Anchors and outcomes (the criterion-validity stream)

- Monthly validated scales: PHQ-9/GAD-7, BPNSFS short, need-relevant and
  functioning measures — the *concurrent* claim (estimated activations
  track validated instruments) is scored against these.
- Clinician severity rating at intake, 3, 6, 12 months (clinical arm).
- **Adjudicated events**: relapse, remission, hospitalization, therapy
  termination, dropout — with dates. The *predictive* claim (rising ρ̂
  precedes transitions; forecast crossing probabilities are calibrated) is
  scored against these.

### 3.7 Metadata (always, every record)

Exact timestamps and timezone; item-level raw responses (not only node
scores); response latency per item; prompt-delivery status; missingness
reason when volunteered; instrument version; device. Rationale: irregular
gaps feed the Δt-aware estimators (RoPE/SSM discretization, notes 29/43/44);
item-level storage lets the measurement model be retrained later without
recollection.

---

## 4. Sampling design

**Burst design (Tier 2, and around events in Tier 1):**

| Phase | Cadence | Duration | Trigger |
|---|---|---|---|
| Intake burst | 3–4/day | 2–3 weeks | enrollment |
| Treatment-change burst | 3–4/day | 2 weeks | session 1, dose change, discontinuation (planned = scheduled in advance) |
| Event burst | 3/day | 10 days | reported life event |
| Maintenance | 1/day (or 3–4/week) | between bursts | — |

Why: P2 — variance per prompt is highest around change; the maintenance
trickle keeps the filter anchored (P4 says thin sampling is fine there).

**Prompt-level rules:** random within-window prompting (not fixed times, to
avoid absolute-time confounds the estimators are built to ignore); 15-minute
response window; no retrospective back-filling beyond 30 minutes.

**Budget optimization — computed, not guessed.** Before finalizing P and T,
fit the additive law `Err(P, T) ≈ E + A·P^-α + B·T^-β` (note 36 template,
`fit_scaling_law` machinery) **on the estimator of record (step 5 GAT /
step 6 transformer) over the simulator**, then minimize for the funded
prompt budget C = P × T̄. The step-4 pooled fits are *not* usable for this
(the naive estimators' error rises with T in low-excitation cells — finding
2 — so their fitted laws are degenerate); the law must be re-fit per
estimator before it prices a study. The Tier-1/Tier-2 numbers in Section 2
are priors to be replaced by this computation.

---

## 5. Identifiability commitments (pre-registered)

1. **κ·B only**: report effective coupling; harmonize response scales and
   transforms across sites/waves/instruments (P6).
2. **Structure fixed (W1)**: only published edges are estimated; the
   tournament (step 7), not exploratory fitting, is where structure itself
   is questioned.
3. **Prior-anchored always (W7)**: free estimation is used only as a
   reported comparator, never as the estimate of record.
4. **Excitation audit**: every person-window ships with a movement statistic
   (usable transitions, variance of Δx); edge estimates from windows below
   a pre-set excitation floor are flagged as prior-dominated.

---

## 6. Pre-registration: claims and falsifiers

Registered before any Phase-C data:

| Claim | Falsifier |
|---|---|
| Estimated dimension activations track validated scales (concurrent) | near-zero within-person correlation with matched instruments |
| Rising ρ̂(J) precedes transitions (predictive) | stable ρ̂ before adjudicated relapses; AUC ≈ 0.5 |
| Forecast intervals are calibrated | 90% coverage materially off nominal on held-out persons |
| Coupling is forecast-relevant on real data | channel-independent null matches the coupled forecaster (the step-6 result fails to replicate) |
| Need-frustration engine loop marks maintenance | loop-gain rankings uncorrelated with course |

Analysis code is frozen at pre-registration; the benchmark scorecard's
reporting template applies (results by preset→cohort, by T, by missingness,
with uncertainty).

---

## 7. Ethics and governance (Batch J §12, operationalized)

- **Consent per stream**, revocable per stream; passive sensing opt-in
  separately from EMA; child/adolescent assent + guardian consent.
- **Data minimization**: no stream without a named node and a named claim.
- **Reviewable outputs**: participants can see and contest their own data;
  clinician-facing outputs are decision support, never autonomous labels.
- **Hard prohibition**: no graph-derived output may serve as sole
  determinant of any coercive action — stated in consent materials.
- **Fairness audits**: measurement invariance and recovery quality checked
  across age, gender, and socioeconomic strata before any pooled claim.
- **Risk protocol**: EMA risk items route to the site's clinical escalation
  path; the model is not the escalation path.
- **Storage**: item-level data encrypted at rest, identifiers separated,
  area-level SYS linkage performed on coded IDs; retention and deletion
  schedule fixed at consent.

---

## 8. Data schema (what lands on disk)

One row per (person, occasion, item): `person_id, ts, tz, item_id,
instrument_version, raw_response, latency_ms, prompt_id, delivery_status`.
Derived per (person, occasion, node), computed by versioned code, never by
hand: `x_hat, measurement_sd, n_items_answered, reliability_assumption,
missing_rule` — exactly the fields `measurement_mapping.md` requires the
estimators to consume. Treatment, events, anchors, and outcomes in separate
timestamped tables keyed by `person_id`. Raw and derived layers never mix;
every derived table carries the git hash of the code that produced it.

---

## 9. Sequencing summary

1. Phase A retrospective fits (now; no collection).
2. Phase B measurement pilot → item set frozen, reliability documented.
3. Budget optimization run on the simulator with the frozen measurement
   model's noise estimates → final P/T split.
4. Pre-registration filed (claims, falsifiers, frozen code).
5. Phase C Tier 1 + Tier 2 collection, treatment-entry recruitment, burst
   sampling.
6. Layer-2 analysis per the benchmark scorecard; Layer-3 (TND-guided care
   trial) only after Layer 2 returns.

The protocol's one-sentence version, matching the contract's:

```text
Buy reliability first, sample where change happens, log treatment as a
known future, keep two tiers for two questions, pre-register the
falsifiers, and let the simulator price the study before money moves.
```
