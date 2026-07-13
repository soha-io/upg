# From Graph to Guidance: Applications, Operating Rules, and Real-World Use of the Unified Person Graph

**[Author 1 name], [Author 2 name]**

[Affiliations]

**Author note.** This article is the eleventh application article in the Unified Person Graph (UPG) series. Its claims are accompanied by cleaning code, model checkpoints, held-out evaluations, a source-card table, a claim ledger, and a self-contained HTML report. Both uploaded source libraries were audited: 223 registered sources (222 PDFs and one HTML source), with OCR fallback for two image-only scans. The UPG remains a research framework. It is not a validated diagnostic device or treatment-selection system and must not be the sole basis of clinical, legal, employment, insurance, educational, or coercive decisions. Author names, affiliations, conflicts, funding, ethics identifiers, and journal-specific declarations remain placeholders until supplied by the authors.

---

## Abstract

The first ten articles derived and composed eight psychological strata into the Unified Person Graph: temperament, development, personality, needs, motivation--emotion, psychopathology, therapy, and systems. This article asks how the model should actually be used. We define its five W's and H; distinguish observations, latent state, standing conditions, theory priors, personalized temporal operators, context, controls, goals, and uncertainty; and bound Topographic Network Diagnosis as a research formulation protocol for psychotherapists, psychiatrists, patients, community users, and researchers. The protocol has eight analytic stages and six safety gates. Its output is a versioned formulation with data quality, a state/resource map, alternative hypotheses, uncertainty, provisional loops or regimes only when identifiable, state/structure/context levers, and monitoring and stop rules. Identical admissible inputs produce identical computational outputs, while meaning, goals, consent, and decisions remain collaborative and contestable.

The empirical program separates formal, synthetic, retrospective, and prospective evidence. All 95 implementation tests passed; the current Great Graph reproduced 253 nodes, 522 edges, and zero encapsulation violations. Fresh graph-attention training on three synthetic populations reproduced median edge RMSE .078--.098, person-deviation correlations .129--.341, and 90% interval coverage .873--.893; it beat every Step-4 baseline on edge RMSE, deviation correlation, and spectral-radius error in all 12 cells. A fresh 200-epoch balanced-population temporal retrain plus reevaluation of two versioned uploaded checkpoints yielded one-step forecast RMSE .060, .054, and .121 versus persistence .092, .104, and .165. These are in-family method results. Real evidence is narrower. In 619,150 IPIP-NEO-120 records, domain reliability was alpha=.817--.905; five varimax components accounted for 57.95% of facet-correlation variance and recovered the intended primary domain for 25/30 facets. In one 1,476-row depression ESM archive, a transparent 20-item motivation--emotion load was reliable (alpha=.940) and correlated with concurrent weekly depression (Spearman rho=.625; circular-block 95% interval [.403,.800]; 27 anchors). Neither 21-day autocorrelation nor variance predicted next-week depression change, and a strict 15-point rolling forecast lost to persistence (RMSE .135 vs .118). Thus the current data support reproducible computation, a PER measurement layer, and a single-person ME feasibility result; they do not validate complete diagnosis, treatment selection, clinical benefit, or cure. The article ends with role-specific workflows, real-life examples, a deterministic agent contract, falsifiers, and a standards-aligned route to prospective validation.

**Keywords:** case formulation, graph models, computational psychiatry, psychotherapy, shared decision making, experience sampling, personalized assessment, psychological networks

---

## 1. Purpose, Status, and the Central Distinction

The UPG is easiest to misuse when different objects are all called "the model." Batch K therefore begins by typing them.

1. **The theory graph** is the published Great Graph: 253 nodes and 522 signed, weighted, gated edges organized into eight strata. Its current weights are consensus priors.
2. **Observations** are $y_p(t)$: item responses, interview codes, events, doses, or sensor values, with provenance and missingness. They are not latent states.
3. **A person's estimated state** is the fast vector $x_p(t)$: where measured constructs appear to be at an occasion, with uncertainty $q_p(t)$.
4. **Standing conditions** are $b_p$: slow loads and resources such as temperament, developmental history, and persistent environmental conditions.
5. **The theory prior** is $\bar W$: the published, sourced skeleton and provisional population weights.
6. **A personalized temporal operator** is $B_p$: a prior-anchored estimate of how states predict later states in a defined window; it is not automatically causal.
7. **Context and control** are $c_p(t)$ and $u_p(t)$: life events and systems on one hand, and treatment or deliberate self-action on the other.
8. **Developmental/applicability gates** are $g_p(t)$: rules governing which paths or measures are active for age, setting, and person.
9. **Goals and constraints** are $v_p$: the person's preferences, values, refusals, burdens, rights, and clinically required safety constraints. They restrict admissible actions; they are not inferred from symptom data.

The structural graph contains eight dimensions, including therapy. The present dimension-level dynamical simulator contains seven endogenous state channels because therapy is represented as the control input $u(t)$ rather than as another symptom-like state. This is not a missing eighth dimension: the full therapy stratum remains part of the structural model, while delivered treatment becomes an explicit time-varying intervention in the dynamic model. Confusing these resolutions would double-count treatment.

The intended equation remains

$$
x_p(t+1)=\sigma\{\kappa_p B_p x_p(t)+C c_p(t)+G u_p(t)+b_p+\varepsilon_p(t)\},
$$

with measurement model

$$
y_p(t)=H_p x_p(t)+\eta_p(t).
$$

The first equation is about psychological movement. The second prevents observed questionnaire answers from being mistaken for error-free latent states. Every application in this article depends on preserving that distinction.

Only effective coupling $\kappa_p B_p$ is identifiable without an external scale constraint. Consequently, all sites and waves must harmonize scales, and reports must say whether they estimate effective coupling or separately identify $\kappa_p$ and $B_p$. A causal word such as *changes*, *drives*, or *treats* requires design-based identification or replicated perturbation; temporal prediction alone earns *precedes* or *predicts*.

### 1.1 What is already established

The current implementation is internally reproducible. The Great Graph is connected, contains no isolated nodes, has full directed reachability, includes self-influence, and supports signed superposition. Encapsulation has zero violations. The synthetic program establishes that the implemented estimators can recover known properties under their own generative assumptions. These are Layer-1 method claims.

### 1.2 What is not established

No prospective multi-stream cohort has yet shown that the complete eight-dimension state, personalized edges, attractors, or control rankings are valid for real patients. The real archives available here cover personality measurement in a very large cross-section and ME/DIS dynamics in one intensively measured person. They cannot identify all strata or clinical effectiveness. Therefore:

> The UPG may currently organize assessment, generate research hypotheses, and support transparent collaborative formulation; it may not currently claim validated automated diagnosis, prognosis, treatment selection, or outcome improvement.

That sentence is a design boundary, not a disclaimer attached after the analysis.

### 1.3 Diagnosis, treatment, recovery, and cure are different claims

The word *diagnosis* has three uses that must not be collapsed. **Categorical diagnosis** applies established DSM/ICD rules and clinical differential assessment. **Dimensional assessment** estimates severity or traits on validated instruments. **UPG formulation** represents measured state, context, resources, and rival maintaining hypotheses. The first two can be performed now through established practice; the third can be used as a transparent research or collaborative formulation. Calling a heat map or graph topology a new diagnostic test would require target-condition definitions, blinded reference-standard assessment, discrimination and calibration, clinical-utility analysis, external validation, and subgroup error audits. Those studies have not occurred.

Likewise, *response*, *remission*, *recovery*, *relapse prevention*, and *cure* are not synonyms. Batch K uses prespecified outcomes and follow-up horizons. It makes no universal cure claim. A future cure claim would require a disorder- and population-specific definition, durable benefit beyond treatment withdrawal, adverse-effect and functioning outcomes, and replicated comparative trials. Until then, the model may rank **hypotheses for discussion**, never prescribe or promise cure.

### 1.4 Prior art and the defensible novelty claim

No component can honestly be called unprecedented. Categorical and dimensional diagnosis, psychological network theory, person-specific ESM, nonlinear psychotherapy models, computational psychiatry, common-factor and transtheoretical therapy, temperament/personality hierarchies, needs models, lifespan development, and ecological systems all predate the UPG (Borsboom, 2017; Cioffi et al., 2022; Liebovitch et al., 2011; Schiepek et al., 2016). The source audit also found five exact duplicate-file groups and prevents them from being counted as independent support.

| Precedent | What it already contributes | What remains distinct in the current UPG artifact |
|---|---|---|
| DSM/ICD and HiTOP | categorical communication and dimensional psychopathology hierarchy | integration with seven other typed strata and control/context objects |
| symptom-network and person-specific ESM models | interacting symptoms and within-person dynamics | a fixed, sourced, encapsulated cross-stratum registry with explicit priors |
| mathematical/computational psychotherapy | formal learning, nonlinear change, therapist--patient dynamics | shared state/structure/context semantics across therapy and nontherapy strata |
| transtheoretical/common-factor formulation | plural therapies, relationship and fit | machine-checkable provenance, gates, uncertainty, and refusal behavior |
| lifespan, temperament, personality, needs, emotion, and systems theories | domain-specific constructs and mechanisms | one versioned composition with explicit interfaces and formal audits |

The defensible contribution is therefore **the particular versioned composition and application contract**, not invention of graphs, dynamics, personalization, or integrative formulation. Whether that composition adds predictive or clinical value is an empirical question. This is a scholarly prior-art boundary, not a legal patent search or a guarantee that no unpublished or differently named model resembles it.

---

## 2. The Application Axioms and Operational Invariants

The five original axioms remain intact: psychological modules are connected; none is dismissible in a complete formulation; effects may be direct or mediated; nodes may influence themselves; and signed influences combine. Application requires ten additional invariants. These do not add psychological claims. They specify how the axioms may be used without contradiction.

### I1. State is not structure

A high state activation says what is present now. A strong edge says what tends to propagate. A trait or standing condition says what changes slowly. None substitutes for another. A distressed week is not a personality diagnosis; a stable trait is not a symptom; a correlation is not a temporal edge.

### I2. A graph node is not a person

The person owns goals, values, narratives, refusals, and endorsed control inputs. The graph describes measured relations among constructs. It does not exhaust identity or assign human worth.

### I3. Measurement precedes inference

Raw responses are preserved. Items are oriented, normalized, aggregated only above declared completeness thresholds, and passed with uncertainty. Risk items are never silently imputed. Missing treatment is unknown, not zero.

### I4. Resolution follows evidence

Eight dimension activations may be estimated from modest assessment. A full 253-node personalized graph requires much denser and better-validated measurement. The model must remain at the coarsest resolution that the data support.

### I5. Priors remain priors until data move them

The published skeleton and weights initialize inference. Person-specific estimation is anchored to them. Low-excitation or short windows return prior-dominated estimates labeled as such; free edge estimation is never the estimate of record.

### I6. Every result carries uncertainty and provenance

A node score carries item source, count, transform, reliability, missingness rule, and measurement SD. An edge carries its prior, estimate, interval, data volume, movement statistic, and version. A forecast carries horizon, interval, calibration status, and comparator performance.

### I7. Mechanisms do not erase categories; categories do not replace mechanisms

DSM or ICD labels may still be required for communication, billing, and established clinical pathways. In the UPG they are summaries of regions, never complete formulations. Conversely, a graph-derived mechanism cannot displace a validated risk or treatment protocol merely because it is mathematically elegant.

### I8. Treatment has three targets

Interventions may shift **state** ($x$: acute symptom relief), alter **structure** ($B$: consolidated learning and changed propagation), or change **context** ($c$ and SYS: family, school, work, poverty, safety, access). Durable care often needs more than one. A person's difficulty must not be individualized when the dominant lever is environmental.

### I9. Determinism applies to computation, not to human meaning

The same versioned inputs and model state must return the same numerical output. Goals, priorities, cultural meaning, consent, and acceptable trade-offs are supplied through collaborative human judgment. Reproducibility is not omniscience.

### I10. A refusal is a valid output

When measurement quality, duration, excitation, calibration, applicability, or safety is insufficient, the correct output is "not estimable" plus the information needed next. This is how the model avoids fabricating completeness.

### I11. Association and prediction are not intervention effects

Cross-sectional covariance permits *co-occurs*; repeated temporal association permits *predicts within this person and window*; only identified or replicated perturbation permits *changing A changes B*. A large edge estimate does not by itself select a treatment target.

### I12. Safety and rights override optimization

No predicted score gain can override emergency procedures, medical differential assessment, consent, capacity, legal rights, safeguarding, or the person's declared unacceptable burdens. Risk routing is independent of the graph, and human review is mandatory.

### I13. Universality is a test program, not an assumption

The schema can represent every age and population without treating difference as defect. That representational scope does not establish measurement invariance, calibration, or benefit in every group. Transport must be tested across age, language, culture, disability, neurotype, sex/gender, socioeconomic position, setting, and time.

### 2.1 Gödel's theorems are not a clinical tool

Gödel's incompleteness theorems were relevant in Batches I--J to justify choosing consistency and openness over a claim of completeness in a sufficiently expressive self-modeling formal system (Gödel, 1931). They add no patient-level diagnosis, edge, score, or treatment rule in Batch K. Their only operational consequence here is modest: the theory and its registries must remain versioned, revisable, and able to represent "unknown." Invoking Gödel to explain an individual mind would be a category mistake.

---

## 3. The Five W's and H of Application

| Question | Operational answer |
|---|---|
| **What?** | A transparent formulation system that turns measured states, standing conditions, context, and treatment history into a profile, landscape, mechanism list, dynamic classification, ranked levers, and monitoring plan. |
| **Why?** | To connect domains that ordinary formulation often holds in prose; distinguish state relief from structural change; expose environmental causation; quantify uncertainty; and make hypotheses reproducible and falsifiable. |
| **Who?** | Researchers first; trained clinicians as decision-support users after local validation; patients as co-interpreters and owners of goals; community users for non-diagnostic self-mapping; administrators only for aggregated quality improvement, never individual coercion. |
| **When?** | At intake for a provisional map; after 30--60 reliable occasions for state/regime hypotheses; over longer windows for cautiously personalized structure; around treatment or life changes for informative bursts; and at review points to compare predicted with observed change. |
| **Where?** | In therapy and psychiatric visits, between-session EMA, collaborative case conferences, research cohorts, and private self-reflection. It is not suitable for covert surveillance or decontextualized screening. |
| **How?** | Through the fixed pipeline in Section 5: contract the question, measure, quality-gate, estimate state, anchor structure, read topography/mechanics/dynamics, simulate admissible controls, decide collaboratively, and monitor. |

The model's practical contribution is not that it asks eight questions. Clinicians already ask about symptoms, history, personality, needs, emotion, treatment, and context. Its contribution is that the answers become typed quantities in one object, so contradictions become visible. For example, symptom state may fall while the estimated basin becomes more fragile; therapy attendance may rise while family threat holds SYS load constant; a patient may report low motivation not because goals are absent but because need frustration and threat appraisal dominate the approach channel. The graph turns these from narrative possibilities into explicit rival hypotheses.

---

## 4. Inputs, Timescales, and Permitted Outputs

### 4.1 The eight dimensions in practice

| Dimension | Practical question | Primary timescale | Example inputs | Permitted early output |
|---|---|---|---|---|
| TEM | How does this nervous system react and regulate? | slow baseline + state markers | temperament scale, reactivity EMA | prior/load with uncertainty |
| DEV | What history and developmental timing shaped the current system? | history and age gates | developmental interview, adversity/events | standing conditions and gates |
| PER | What patterns, adaptations, and narratives characterize the person? | slow, with repeated states | Big Five facets, goals, self-concept, narrative | five-domain/facet profile; no health scalar |
| NEED | What is satisfied, frustrated, scarce, or protected? | state + weekly | autonomy, competence, relatedness, safety, material, esteem, meaning | separate satisfaction/frustration channels |
| ME | What is wanted, felt, valued, and regulated? | fast EMA | valence, arousal, wanting, avoidance, regulation | current load and trajectory |
| DIS | What symptoms and impairments are active? | fast + validated anchors | presenting-problem EMA, PHQ/GAD/HiTOP-aligned measures | severity state; risk remains separate |
| THER | What help, medication, practice, and alliance are delivered? | event/control | sessions, dose/time, adherence, homework, alliance | verified control stream $u(t)$ |
| SYS | What settings support, threaten, constrain, or exclude? | state + slow context | family/school/work, money, housing, discrimination, services | support/thwart and event channels |

### 4.2 Minimal, intermediate, and full modes

**Minimal collaborative map.** One baseline profile plus interview evidence. Output: eight-dimension problem/resource map, uncertainties, conflicts in evidence, and questions to investigate. No person-specific edges, attractors, or forecasts.

**Monitoring mode.** Reliable EMA with approximately 30--60 usable occasions. Output: filtered state trajectory, missingness-aware uncertainty, provisional regime/attractor hypotheses, treatment-linked change, and short-horizon forecasts only if locally calibrated. This mode is suitable for measurement-based care research.

**Structural mode.** Hundreds to thousands of informative occasions, or an amortized estimator validated on a representative population and realistic simulator. Output: prior-anchored person-specific edges, loop gains, spectral radius, and control simulations. Every result must state how much it moved from the prior and whether the window had enough excitation.

**Full-resolution mode.** Validated item-to-node mappings across the detailed stratum graphs. Output: 253-node analysis. This mode does not yet exist clinically and should not be simulated by filling missing nodes with generic values.

### 4.3 The evidence ladder

| Evidence level | What may be said |
|---|---|
| Self-report or single interview indicator | "Reported/observed activation may be present." |
| Multi-item reliable node score | "This node is estimated at this level with this uncertainty." |
| Repeated within-person association | "These states co-move within this person." |
| Time-directed, prior-anchored estimate with adequate excitation | "This edge is a plausible person-specific temporal influence." |
| Replicated intervention perturbation | "Changing this input appears to change the downstream state." |
| Prospective trial | "Using this model-guided decision improves outcomes relative to the relevant care comparator." |

The language changes with the evidence. The software should enforce that change rather than leaving it to user restraint.

---

## 5. The Operating Protocol

The seven analytical stages of Topographic Network Diagnosis are retained, but Batch K surrounds them with question, safety, and decision stages.

### Stage 0. Contract the question

State the user, decision, horizon, and prohibited uses. Examples: "What appears to maintain distress over the next four weeks?"; "Which measurements should be added before changing treatment?"; "Did the medication change shift state without changing the maintaining loop?" A vague request to "analyze the person" is rejected.

### Stage 1. Instantiate the measurement map

For every scheduled node, declare item source, count, scale, orientation, aggregation, reliability, missingness rule, and uncertainty. Select age-, language-, culture-, disability-, and setting-appropriate measures. Preserve raw items and sentinel risk responses separately.

### Gate A. Measurement sufficiency

Score a node only if its declared completeness threshold is met. The current contract uses at least 60% for most EMA nodes, 70% for PER and DIS, and stronger handling for sentinel developmental or risk items. If the threshold fails, the node is missing.

### Stage 2. Estimate state

Transform admissible observations into $\hat{x}(t)\pm\sigma(t)$. Use a missingness-aware state-space or temporal model; do not mean-impute missing occasions. Display the observation separately from the filtered latent estimate so the user can contest both.

### Gate B. Safety and applicability

Acute risk, delirium, intoxication, medical causes, or other urgent pathways are handled through established clinical procedures. The graph may provide context but never becomes the escalation pathway. Check whether the person and setting are represented in the validation population; otherwise label transport as untested.

### Stage 3. Estimate structure from the prior

Start from $\bar W$ and estimate only published support. Report $\hat W$, intervals, and distance from prior. Compute usable transitions and movement. If the data are quiescent, preserve the prior and say so.

### Gate C. Duration and excitation

Short reliable series may support state and regime hypotheses. They do not support detailed person-specific edges. Structural claims require a predeclared minimum and an excitation statistic above threshold. More quiet data do not solve errors-in-variables bias.

### Stage 4. Read topography and mechanics

Produce the problem-load profile, resource profile, and changes over time. Rank loops by signed gain; identify bridges and bottlenecks. A visual peak is descriptive until a valid temporal or interventional path supports a mechanism claim.

### Stage 5. Read dynamics

Estimate attractors, spectral radius, regime, and forecast distributions. Compare at least persistence, an explicit state-space model, and the learned forecaster. A rising $\rho(J)$ is a hypothesis about decreasing resilience, not a standalone relapse alarm.

### Gate D. Calibration and model agreement

Forecasts are shown only when interval coverage and discrimination meet predeclared held-out criteria in the target setting. Compare structural GAT and temporal-transformer dynamics heads. Material disagreement triggers review, not averaging.

### Stage 6. Generate admissible control options

Each option must name its target and route:

- **State lever:** acute medication, behavioral activation, sleep stabilization, grounding, crisis support.
- **Structure lever:** repeated exposure, schema revision, regulation practice, relationship learning, consolidation.
- **Context lever:** family intervention, school accommodation, workload, financial/housing support, discrimination or safety response.

Simulations rank hypotheses, not commands. Contraindications, preferences, evidence-based guidelines, and feasibility constrain the candidate set before optimization.

### Gate E. Human goals, consent, and rights

The patient chooses goals and acceptable trade-offs. Clinicians remain accountable for clinical judgment. The person can see, contest, annotate, or revoke data streams. No output is the sole determinant of coercive action.

### Stage 7. Decide, document, and monitor

Record the selected hypothesis, expected downstream changes, uncertainty, review date, and falsifier. Monitoring returns to Stage 2. If the predicted intermediate changes do not occur, revise the formulation before escalating intensity.

### Gate F. Stop or revise

Stop structural or predictive output when calibration drifts, data provenance breaks, measures change without harmonization, the person's context leaves the model's scope, or observed outcomes repeatedly contradict the active mechanism.

---

## 6. Role-Specific Use

### 6.1 Psychotherapists

The therapist uses the UPG as a formulation ledger. At intake, they co-create a minimal map: current DIS and ME peaks; NEED satisfaction/frustration; relevant SYS supports and threats; slow TEM, DEV, and PER conditions; current THER inputs. The model then helps separate three questions that therapy notes often merge:

1. What changed this week?
2. What tends to propagate within this person?
3. What conditions keep recreating the same state?

Before a session, the therapist sees deviations from the person's own baseline, not population-normalized red flags alone. During the session, they compare the map with the patient's account. After the session, they record the intervention as a typed control event and specify its expected route. If avoidance decreases but need frustration and family threat do not, the formulation predicts fragile improvement and identifies what needs separate work.

The graph does not choose a school of therapy. It can represent exposure as an intervention on threat/avoidance propagation, behavioral activation as a state and reinforcement intervention, psychodynamic work as revision of recurring relational and narrative structures, systemic therapy as a context and feedback intervention, and common factors as treatment-loop conditions. The shared graph allows approaches to disagree on mechanism in testable terms.

### 6.2 Psychiatrists

Psychiatric use centers on time, dose, adverse effects, and state-versus-structure distinction. Medication exposure is recorded as delivered $u(t)$ with verified dose and time, not inferred from a prescription. Planned changes become known-future inputs; adherence uncertainty remains explicit.

A psychiatrist may ask whether a dose change shifted DIS and ME state, whether sleep or activation mediates the change, whether improvement survives reduction, and whether SYS constraints or psychotherapy inputs alter the trajectory. The model can display symptom benefit alongside costs to arousal, motivation, cognition, autonomy, or daily functioning. It cannot infer causation from an uncontrolled concentration coefficient, prescribe medication, or replace established assessment of side effects, mania, psychosis, withdrawal, or medical risk.

### 6.3 Patients and families

The patient-facing object is a shared map, not a clinical dashboard of hidden scores. It answers:

- Where am I hurting now?
- What resources are still available?
- What loops might keep this going?
- Which parts are inside me, between people, or in my environment?
- What are we trying first, and what change would tell us it is working?

The person can correct meanings: solitude may be restorative rather than withdrawal; high arousal may reflect sensory overload rather than anxiety; family closeness may be support or control depending on context. The model's variables are hypotheses until they survive this semantic check.

For children, the map is simplified and jointly interpreted with assent, caregivers, and developmental context. The child is not treated as the sole location of a family, school, or poverty mechanism. For adolescents, privacy boundaries and identity development must be explicit. For elders, medical, cognitive, bereavement, caregiving, and social-access variables require appropriate measures and differential assessment.

### 6.4 People without a diagnosis

Community self-mapping uses resource-oriented language and the minimal mode. A person may track energy, needs, emotion, habits, relationships, goals, and context to learn patterns. No disorder score, edge estimate, or relapse forecast is generated from casual journaling. The useful outputs are questions, trends, and small self-endorsed experiments such as sleep regularity, social contact, workload boundaries, or values-aligned action.

### 6.5 Teams and researchers

Case conferences receive a compact formulation with provenance, alternative hypotheses, disagreements, and missing information. Researchers receive the full numeric object, preregistered claims, comparators, and falsifiers. Population dashboards may aggregate calibration and outcome quality; they may not expose individual need, personality, or system maps to administrators who do not participate in care.

### 6.6 A practical session rhythm

The protocol can be used without displaying 253 nodes. A research clinic can place the following eight-line card beside the ordinary record; established risk, diagnostic, and treatment procedures remain primary.

| Moment | Question | Recorded object | Stop rule |
|---|---|---|---|
| Before session | Are consent, measures, and safety routing current? | provenance, missingness, risk-protocol status | handle urgent or medical pathways first |
| 0--3 min | What changed, helped, or worsened since last contact? | observed state and events | do not infer an edge from one change |
| 3--6 min | Which current loads and resources matter most to the person? | provisional state/resource profile | display uncertainty and disagreement |
| 6--10 min | What are at least two rival explanations? | path hypotheses and falsifiers | refuse mechanism ranking if data are inadequate |
| 10--13 min | Which evidence-based, acceptable action targets state, structure, or context? | candidate control plus expected route | contraindication, burden, or refusal removes option |
| 13--15 min | What will be measured, when will we review, and when will we stop? | outcome, adverse-effect, and review plan | revise if intermediate change fails |

### 6.7 The formulation packet

Every use returns two synchronized views. The **person-facing page** contains the person's question, plain-language map, strengths/resources, two or more hypotheses, chosen next step, what would count as improvement or harm, and a place to contest the interpretation. The **technical appendix** contains the measurement map, version, raw-to-node transforms, completeness, reliability, measurement error, priors, estimates, intervals, excitation, comparator results, calibration, applicability, alternatives, and prohibited inferences. Nothing visible only to the technical user may silently determine a decision visible to the person.

---

## 7. Real-Life Scenarios

### Scenario 1. Adolescent withdrawal under school threat

A 15-year-old shows elevated DIS and ME, high NEED frustration, and a marked SYS school-threat input after bullying. TEM suggests high sensitivity; DEV gates make peer and identity processes especially relevant. Minimal-mode output identifies a cross-stratum hypothesis: threat raises avoidance and need frustration, which amplify symptoms. The first plan combines safety and school action (context), supportive regulation (state), and gradual reconnection (structure). Treating only the adolescent's anxiety while leaving bullying active violates the model's own causal map.

### Scenario 2. Adult depression after job loss

An adult's state map rises sharply after job loss. SYS financial strain and role loss precede NEED competence/meaning frustration and ME downshift; PER traits remain stable. The formulation prevents a state shock from being rewritten as a fixed personality deficit. Immediate financial and routine support is a context/state intervention; therapy works on the propagating meaning and avoidance loops; medication, if used, is a separate control stream.

### Scenario 3. Neurodivergent overload

A neurodivergent adult reports high arousal, shutdown, and social withdrawal in an inaccessible workplace. The model does not encode neurotypicality as health. Sensory/environmental mismatch enters through SYS and TEM-by-context fit; distress enters DIS only where impairment or suffering is present. The primary lever may be accommodation and demand reduction, not normalization of temperament or personality.

### Scenario 4. Apparent remission during intensive treatment

DIS falls during frequent treatment, but the estimated spectral radius rises and the state returns after missed sessions. The hypothesis is state-shifting without sufficient structural change. The clinical response is not indefinite intensity by default: identify which maintaining edges remain, strengthen consolidation and context supports, taper only with monitoring, and state uncertainty. Batch J's synthetic "fragile remission" example becomes a testable care hypothesis.

### Scenario 5. A nonclinical self-experiment

A person notices low motivation on workdays. Two weeks of simple tracking show that sleep and workload predict ME and NEED frustration, while weekend goals remain intact. The output is a descriptive pattern and a small schedule experiment. It is not "burnout diagnosis" or a person-specific Great Graph.

### Scenario 6. What a correct refusal looks like

A clinician enters one intake interview and asks, "Which causal loop should we break to cure this depression?" The system returns: **state map permitted; personalized temporal edges, causal loop ranking, cure claim, and forecast refused**. It explains that there is no repeated within-person series, no intervention contrast, and no target-setting clinical validation. It offers next information: established diagnostic and medical assessment; validated symptom/function anchors; a collaboratively chosen monitoring window; context and treatment-event logging; and an outcome/adverse-effect plan. This refusal is more clinically useful than a fabricated graph.

| Available evidence | Allowed output | Refused output | What upgrades the claim |
|---|---|---|---|
| one interview or questionnaire | reported problems, resources, context, missing information | personalized edges, attractor, prognosis | repeated reliable measurement |
| repeated observations without adequate movement | trajectory and uncertainty | person-specific coupling | informative change/perturbation and excitation |
| time-directed association | temporal hypothesis | causal treatment target | replicated intervention or identified natural experiment |
| target-setting external validation | calibrated prediction in that setting | outcome-improvement claim | prospective comparative impact trial |
| pragmatic trial with follow-up | incremental clinical effectiveness for defined population/use | universal cure | replication, durability, harms, and transportability |

---

## 8. Data Cleaning, Training, and Empirical Results

### 8.1 Source and artifact audit

The four accepted archives contained 596 files before execution: 219 project files, 139 data files, 190 files in Source Part 1, and 48 in Source Part 2. The source registries contain 223 entries: 222 PDFs and one Transformer Circuits HTML source. The substantive PDFs span 20,253 pages when the four data-documentation PDFs are included. Embedded-text extraction yielded approximately 9.40 million whitespace-delimited words. Two legitimate sources had no embedded text: the 33-page Chess--Thomas scan and the 10-page Rothbart infancy-measurement scan. Page-image Tesseract OCR recovered approximately 24,205 and 6,530 words respectively. The audit records extraction method and failure state per PDF.

Exact hashing identified five substantive duplicate groups: two DSM articles, two motivation--emotion articles, and one temperament article were duplicated under different filenames. They remain in the registry for provenance but count once as evidence. Forty-six `__MACOSX`/AppleDouble stubs in the data archive were metadata, not evidence; four PDF-named stubs failed as expected and were excluded. No substantive registered source remained text-inaccessible after OCR. The audit demonstrates access and provenance, not agreement with every source and not automatic truth of every inherited claim.

### 8.2 Cleaning contract

The retrospective pipelines implement seven frozen rules: (1) preserve raw files read-only; (2) validate ranges and file layout before scoring; (3) orient high values toward the declared construct load and transform to 0--1; (4) apply the documented completeness gate (70% for PER domains, 3/4 for facets, 60% for the ESM ME load); (5) leave missing values missing rather than mean-imputing occasions; (6) estimate reliability and convert it to a reliability-derived measurement standard deviation; and (7) retain hashes, software versions, transforms, item counts, and claim boundaries. The deliverable contains aggregate statistics and the public one-person weekly derived series, not a duplicated 619,150-person response matrix.

### 8.3 Formal and software verification

The full Pytest suite passed 95/95 tests. Independent execution of `reproduce.py` recovered 253 nodes, 522 edges, 35 cross-stratum edges, 20 self-loops, 33 negative edges, and zero encapsulation violations. All five declared structural axioms passed their implemented tests. The dimension graph had algebraic connectivity $\lambda_2=1.568$; PER had the smallest absolute Fiedler coordinate (.015), the strongest amplifying dimension loop was NEED $\rightarrow$ ME $\rightarrow$ NEED (gain +.400), and the strongest regulating loop was DIS $\rightarrow$ THER $\rightarrow$ DIS (gain -.455). These are properties of the current versioned registry, not population estimates.

### 8.4 Layer-1 structure training

The structure-constrained graph-attention estimator was freshly trained with fixed seeds on cached synthetic training populations for `balanced_regimes`, `clinical_realistic`, and `transition_rich`. It starts exactly at the theory prior, attends only over published support, preserves zeros and signs, and returns per-edge uncertainty (Veličković et al., 2018). Across the 12 held-out preset-by-window cells:

- median edge RMSE ranged .078--.098;
- person-specific deviation correlation ranged .129--.341;
- regime accuracy ranged .850--.975;
- 90% edge-interval coverage remained approximately .87--.89;
- it beat the best Step-4 baseline on edge RMSE, deviation correlation, and spectral-radius error in all 12 cells.

These results demonstrate in-family method recovery. They do not show that the synthetic family is an adequate generator of real persons.

### 8.5 Layer-1 temporal training and checkpoint provenance

The causal temporal transformer encodes missingness rather than imputing it. ALiBi supplies relative-time bias; RMSNorm, SwiGLU, residual blocks, and typed heads implement filtering, one-shot multi-horizon forecasting, and a dynamics cross-check (Press et al., 2022; Shazeer, 2020; Vaswani et al., 2017; Zhang & Sennrich, 2019). Checkpoint origin is explicit: `balanced_regimes` was freshly retrained for a fixed 200-epoch budget in this execution and the best validation checkpoint was retained; the versioned uploaded `clinical_realistic` and `transition_rich` checkpoints were hash-verified and reevaluated, not relabeled as fresh. All evaluation persons were held out.

| Preset | Filter RMSE | Forecast RMSE h=1 | Persistence h=1 | Explicit state-space h=1 | Relapse AUC | Recovery AUC |
|---|---:|---:|---:|---:|---:|---:|
| Balanced regimes | .053 | .060 | .092 | .061 | 1.000 | .976 |
| Clinical realistic | .052 | .054 | .104 | .079 | .955 | .983 |
| Transition rich | .110 | .121 | .165 | .157 | .984 | .939 |

The model beat persistence in all three presets and the explicit fitted pipeline in the clinical and transition-rich populations; it was approximately tied with the explicit pipeline in the balanced population. Nominal 90% one-step interval coverage was .879--.904. In the transition-rich population, the coupled model's one-step RMSE (.121) also beat the archived channel-independent null (.139). Early-warning AUCs are high because the event definition and data generator are internal to Layer 1. They do not validate a real clinical alarm.

### 8.6 Large-sample personality measurement

The Johnson IPIP-NEO-120 fixed-width file contained 619,150 153-byte records. Every CRLF terminator and every 0--5 item range passed validation. The source had already reverse-keyed negative items. Zero remained missing, producing 367,593 missing cells in the 74,298,000-cell item matrix. Every record passed the overall 70% item gate; 612,595 passed all 30 facet gates.

Domain reliability was N=.898, E=.889, O=.817, A=.858, and C=.905, reproducing Johnson's published rounded coefficients. Reliability-derived measurement SDs were .055, .053, .060, .053, and .049. The first five facet-correlation eigenvalues were 6.655, 3.745, 2.973, 2.096, and 1.916, jointly 57.95% of variance. A five-component varimax solution recovered the intended primary domain for 25/30 facets; the exceptions were N4 self-consciousness, E3 assertiveness, E4 activity level, O3 emotionality, and C3 dutifulness. The facet-correlation structure was nearly identical in deterministic row-parity halves ($r=.999945$). Median absolute within-domain facet correlation was .323 versus .134 across domains. This supports reliable five-domain PER measurement and a largely, not perfectly, aligned facet structure. It does **not** establish temporal direction, a personality health scalar, person-specific UPG edges, or clinical diagnosis (Johnson, 2014).

### 8.7 Intensive real-person ME/weekly-DIS audit

The Kossakowski archive contained 1,476 rows from one person across medication-reduction phases (Kossakowski et al., 2017). Five explicit aborts were excluded; two missing abort flags were retained but independently item-gated, leaving 1,471 rows and 238 observed days. A declared 20-item ME load combined negative affect/self-evaluation items oriented upward and positive items reverse-oriented, with a 60% gate. All retained rows passed; mean item coverage was .9999. Complete-occasion alpha was .940 and the reliability-derived measurement SD was .0227.

Thirteen weekly SCL-90-R depression items were averaged and normalized to 0--1, producing 28 anchors. The mean ME load over the current seven calendar days correlated with concurrent weekly depression at $\rho=.625$ (circular-block 95% interval [.403,.800]; $n=27$). This is a narrow within-person concurrent-validity result. It is partly expected because affective distress overlaps depression, and it does not identify a complete ME or DIS stratum.

Two preregistration-relevant negative findings matter more for application. The 21-day AR(1) coefficient did not predict next-week depression change ($\rho=-.068$; block interval [-.561,.397]; $n=25$); rolling variance also did not ($\rho=-.124$; [-.397,.173]; $n=25$). A strict expanding-window ridge model using current depression, seven-day ME, and 21-day AR(1) made 15 next-anchor forecasts. It lost to persistence on MAE (.117 vs .088) and RMSE (.135 vs .118). Daily medication concentration correlated weakly and negatively with ME ($\rho=-.165$; $n=238$), but exposure, phase, and time are confounded, so this is not a medication effect.

The archive exercises ME measurement, weekly DIS anchoring, and medication exposure only. It cannot identify all eight strata, detailed edges, dynamic regimes, treatment causality, or population performance. Training a complete UPG on it would manufacture information that is not present; the scientifically correct action was to fit only the bounded analyses and return "not identifiable" for the rest.

### 8.8 Evidence synthesis

The evidence levels must not inherit validity from one another. Formal consistency supports implementation correctness. Synthetic recovery supports the estimator under simulator assumptions. Cross-sectional IPIP data support part of the PER measurement layer. The single-person ESM supports a transparent ME score's concurrent relation and falsifies two candidate warning/prediction claims in that series. None establishes prospective whole-UPG validity. The negative forecast result therefore changes Batch K's permitted behavior: a real-world application must always show a persistence comparator and suppress forecasts that do not improve on it.

---

## 9. The Deterministic Agent Contract

An agent implementing Batch K should not be trained merely on manuscript prose. It should operate against a typed input/output contract.

### 9.1 Required input

```json
{
  "model_version": "semantic_version_plus_registry_hash",
  "question": {"user": "role", "decision": "specific", "horizon": "time"},
  "consent": {"streams_allowed": [], "streams_revoked": [], "expires": "ISO-8601"},
  "goals_constraints": {"goals": [], "refusals": [], "burden_limits": []},
  "observations": [{
    "instrument_item": "versioned_item_id",
    "timestamp": "ISO-8601",
    "raw_value": "preserved",
    "missing_reason": null,
    "provenance": "source_record_id"
  }],
  "measurement_map": {"version": "required", "item_to_node_rules": []},
  "controls": [{"type": "session_or_dose_or_self_action", "status": "planned|delivered|missed|unknown"}],
  "context_events": [],
  "established_assessment": {"diagnoses": [], "medical_differential_status": "documented"},
  "risk_protocol": {"status": "handled_outside_model", "responsible_human": "required"}
}
```

### 9.2 Required output

```json
{
  "admissibility": {"resolution": "minimal", "state": true, "structure": false, "forecast": false, "reason_codes": []},
  "measurement_quality": {"coverage": {}, "reliability": {}, "measurement_sd": {}, "missing": []},
  "state": {"estimate": {}, "interval": {}, "observation_shown_separately": true},
  "structure": {"theory_prior": "hash", "prior_dominance": "high", "edges": []},
  "hypotheses": [{"path": [], "evidence_level": "repeated_association", "uncertainty": {}, "falsifier": "required"}],
  "alternatives": [{"explanation": "required", "discriminating_information": []}],
  "options": [{"target": "state|structure|context", "evidence_basis": [], "expected_route": [], "burdens_harms": [], "not_a_prescription": true}],
  "monitoring": {"outcomes": [], "adverse_effects": [], "review_date": "required", "stop_rules": []},
  "falsifiers": [],
  "next_information": [],
  "prohibited_inferences": ["automated_diagnosis", "causal_treatment_selection", "cure_claim"],
  "patient_contestations": [],
  "human_review_required": true
}
```

### 9.3 Fixed reasoning order

1. Validate schema, version, consent, provenance, goals, and risk-routing status.
2. Route urgent, medical, safeguarding, or established diagnostic tasks through their responsible human procedures.
3. Score measurement quality; preserve observation separately from latent-state inference.
4. Determine admissible resolution and vocabulary from the evidence ladder.
5. Estimate state before structure; preserve priors when duration or excitation is insufficient.
6. Show a forecast only after target-setting calibration and only beside persistence and declared comparators.
7. Generate at least one plausible alternative explanation and the information that discriminates it.
8. Separate state, structure, and context options; filter them through evidence, contraindications, rights, goals, and burden.
9. Attach uncertainty, provenance, falsifier, monitoring, adverse-effect, and stop rules to every active hypothesis.
10. Refuse prohibited or unsupported conclusions and state what information could change the refusal.

This order makes same-input/same-version computation deterministic without pretending that two people with the same questionnaire scores share the same meaning or goals.

---

## 10. Ethics, Equity, and Human Freedom

The UPG maps unusually intimate material: needs, personality, history, family, systems, symptoms, and treatment. Its breadth increases both clinical promise and surveillance risk. The following controls are therefore constitutive.

- Consent is per stream and revocable. Passive sensing is separate from EMA.
- The person can inspect and contest raw data, mappings, and interpretations.
- Data collection is minimized to named nodes and named claims.
- Raw identity is separated from analytic data; retention and deletion are explicit.
- Measurement invariance, calibration, missingness, and error are audited across age, gender, language, disability, neurotype, and socioeconomic position before pooled claims.
- Atypical architecture is not disorder unless suffering, impairment, danger, or the person's own goals make it clinically relevant.
- Contextual oppression must not be translated into individual defect.
- No graph output is the sole basis for involuntary care, legal judgment, benefits, education placement, insurance, employment, or policing.

Human freedom appears in the formalism as endogenous control, but the ethical point is simpler: the map belongs in a relationship where the person can say "that is not what this means" and the model must update.

Representational breadth does not waive subgroup validation. Child use requires age-appropriate instruments, guardian consent and child assent, and explicit family/school system variables. Adolescent use requires negotiated privacy boundaries. Adult and elder use requires relevant medical, reproductive, occupational, cognitive, bereavement, caregiving, and access contexts. Neurodivergence is represented descriptively; pathology is assigned only to distress, impairment, danger, or a person-endorsed target, not deviation from a neurotypical norm. Every pooled model must test measurement invariance or differential item functioning where appropriate, calibration and error by subgroup, missingness mechanisms, accessibility, and the effect of model-assisted decisions.

Translation follows a total-product-lifecycle standard. WHO's health-AI guidance places ethics and human rights at the center of design, deployment, and use. The 2025 IMDRF Good Machine Learning Practice principles require safe, effective, high-quality lifecycle development. FDA's January 2026 clinical-decision-support guidance makes intended user, function, and the user's ability to independently review the basis of recommendations consequential to U.S. regulatory classification; other jurisdictions require their own review. DECIDE-AI governs early live clinical evaluation, TRIPOD+AI prediction-model reporting, and SPIRIT-AI/CONSORT-AI prospective trial protocols and reports. These standards define work still required; citing them does not make the current code compliant, cleared, or clinically deployable (World Health Organization, 2021; U.S. Food and Drug Administration, 2026; Vasey et al., 2022).

---

## 11. Falsifiability and the Route to Clinical Use

### 11.1 Near-term falsifiers

1. **Measurement:** factor/node mappings fail to replicate or show serious non-invariance.
2. **Concurrent:** estimated activations do not track matched validated measures within person.
3. **Temporal:** coupled models do not outperform channel-independent or persistence comparators on held-out real observations.
4. **Dynamic:** rising $\rho(J)$ does not precede adjudicated transitions better than simpler warning rules.
5. **Mechanistic:** high-gain loops do not mark maintenance or response to targeted perturbation.
6. **Incremental:** UPG-guided formulation does not improve decisions or outcomes beyond measurement-based care.
7. **Equity:** error or calibration gaps remain materially different across protected or underserved groups.

Batch K has already encountered falsification rather than waiting for a future paper. The IPIP hierarchy was not exact (five facets had another domain's strongest loading). In the one-person ESM archive, neither early-warning indicator tracked next-week change and the candidate forecast lost to persistence. These results do not falsify the entire UPG, but they falsify the corresponding strong claims for those operationalizations and data. The measurement map or estimator must change, or the claim must remain absent.

### 11.2 Development sequence

1. **Freeze claims and measurement maps.** Turn the supplied mapping into versioned item/node specifications; declare primary outcomes, missingness, estimands, comparators, subgroup checks, and failure thresholds before new data.
2. **Measurement pilot.** Approximately 30 participants for 14 days at three prompts/day, with cognitive interviewing and burden data. Estimate within- and between-person reliability, item functioning, completion decay, and missingness reasons. Do not use this small pilot for edge discovery.
3. **Retrospective external tests.** Analyze additional independent ESM cohorts and registered disorder/therapy datasets. Every prediction must beat persistence and simple clinical baselines out of sample. Recalibrate the simulator to real noise, missingness, and transition frequencies.
4. **Prospective breadth cohort.** Approximately 150--300 people with 45--60 usable occasions, quota-sampled across severity, age, neurotype, language, and context. Test measurement, concurrent validity, forecast calibration, decision-curve utility, subgroup error, and transport.
5. **Prospective depth cohort.** Approximately 20--40 people with hundreds to thousands of occasions and event/treatment bursts. Only this tier may test detailed personalized edges, and only when excitation and measurement error meet preregistered thresholds.
6. **Diagnostic-performance study.** For any claimed diagnostic output, use an independently adjudicated target/reference procedure, blinded assessment where possible, target-setting external validation, calibration, sensitivity/specificity or appropriate dimensional metrics, net benefit, and subgroup analysis. Report prediction models with TRIPOD+AI. Do not let the UPG define both predictor and truth.
7. **Early live evaluation.** Run a small, monitored DECIDE-AI study of workflow, human factors, failure modes, override, time burden, adverse events, and clinician/patient comprehension. Lock the model during evaluation or prespecify change control.
8. **Pragmatic impact trial.** Compare care as usual, measurement-based care, and UPG-assisted measurement-based care. Primary endpoints should be preregistered symptoms/function or goal-attainment plus harms; secondary endpoints may include shared understanding, decision quality, burden, equity, and resource use. Use SPIRIT-AI and CONSORT-AI reporting and follow participants long enough to distinguish acute response from durable recovery.
9. **Lifecycle deployment.** Only a feature that passes target-setting validation, human-factor evaluation, clinical-impact testing, regulatory determination, security/privacy review, and subgroup calibration may enter clinician-facing decision support. Monitor drift, overrides, incidents, and post-deployment performance; maintain rollback and version retirement.

The model earns deployment one claim at a time. A validated state filter does not validate edge surgery; a valid personality measurement layer does not validate relapse prediction; good synthetic AUC does not validate a clinical alarm.

### 11.3 Decision thresholds for release

Release is claim-specific. A state display requires reliable measurement and understandable uncertainty. A forecast requires external calibration, useful net benefit, and superiority to simple comparators. A personalized edge requires dense, informative data and stability across reasonable specifications. A treatment-ranking feature requires intervention evidence and an impact trial. An autonomous diagnosis or prescription is outside the present scope. Failure at a higher level does not erase a lower-level descriptive use, but success at a lower level never licenses a higher claim.

---

## 12. Conclusion

Batch K turns the Great Graph into a disciplined practice. The practical object is not a spectacular 253-node picture. It is a sequence of bounded questions: What can be measured? What is state, what is structure, and what is context? Which claims are admissible at this resolution? What loop is only a hypothesis, what change would falsify it, and which lever respects the person's goals? When should the model refuse to answer?

For therapists, the UPG is a formulation and monitoring ledger. For psychiatrists, it separates dose, state change, structural persistence, and context. For patients and families, it is a contestable shared map that can locate suffering outside the person as well as within. For people without diagnoses, it is a modest framework for noticing patterns, not a machine for producing pathology. For researchers, it is a testable program with fixed comparators, explicit falsifiers, and downloadable models.

The present analyses show that the computational machinery recovers important properties of its own simulated world, that a large real personality dataset supports one measurement layer with five interpretable exceptions, and that a transparent ME score tracks concurrent weekly depression in one intensive series. The same real series rejects the tested early-warning and forecast claims. The work does not validate the complete clinical theory. That boundary is the central result of Batch K. A potentially important model becomes scientific by saying exactly what it can do now, recording what failed, and naming the evidence required before it does more.

---

## References

American Psychological Association Presidential Task Force on Evidence-Based Practice. (2006). Evidence-based practice in psychology. *American Psychologist, 61*(4), 271--285. https://doi.org/10.1037/0003-066X.61.4.271

Borsboom, D. (2017). A network theory of mental disorders. *World Psychiatry, 16*(1), 5--13. https://doi.org/10.1002/wps.20375

Bronfenbrenner, U. (1979). *The ecology of human development: Experiments by nature and design*. Harvard University Press.

Cioffi, V., Mosca, L. L., Moretto, E., Ragozzino, O., Stanzione, R., Bottone, M., Maldonato, N. M., Muzii, B., & Sperandeo, R. (2022). Computational methods in psychotherapy: A scoping review. *International Journal of Environmental Research and Public Health, 19*, 12358. https://doi.org/10.3390/ijerph191912358

Collins, G. S., Moons, K. G. M., Dhiman, P., Riley, R. D., Beam, A. L., et al. (2024). TRIPOD+AI statement: Updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ, 385*, e078378. https://doi.org/10.1136/bmj-2023-078378

Cruz Rivera, S., Liu, X., Chan, A.-W., Denniston, A. K., Calvert, M. J., & SPIRIT-AI and CONSORT-AI Working Group. (2020). Guidelines for clinical trial protocols for interventions involving artificial intelligence: The SPIRIT-AI extension. *Nature Medicine, 26*, 1351--1363. https://doi.org/10.1038/s41591-020-1037-7

Epskamp, S., Borsboom, D., & Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. *Behavior Research Methods, 50*(1), 195--212. https://doi.org/10.3758/s13428-017-0862-1

Gross, J. J. (1998). The emerging field of emotion regulation: An integrative review. *Review of General Psychology, 2*(3), 271--299. https://doi.org/10.1037/1089-2680.2.3.271

Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. *Monatshefte für Mathematik und Physik, 38*, 173--198. https://doi.org/10.1007/BF01700692

Johnson, J. A. (2014). Measuring thirty facets of the Five Factor Model with a 120-item public domain inventory: Development of the IPIP-NEO-120. *Journal of Research in Personality, 51*, 78--89. https://doi.org/10.1016/j.jrp.2014.05.003

International Medical Device Regulators Forum. (2025). *Good machine learning practice for medical device development: Guiding principles*. https://www.imdrf.org/

Kossakowski, J. J., Groot, P. C., Haslbeck, J. M. B., Borsboom, D., & Wichers, M. (2017). Data from "Critical slowing down as a personalized early warning signal for depression." *Journal of Open Psychology Data, 5*(1), Article 1. https://doi.org/10.5334/jopd.29

Kotov, R., Krueger, R. F., Watson, D., Achenbach, T. M., Althoff, R. R., Bagby, R. M., Brown, T. A., Carpenter, W. T., Caspi, A., Clark, L. A., Eaton, N. R., Forbes, M. K., Forbush, K. T., Goldberg, D., Hasin, D., Hyman, S. E., Ivanova, M. Y., Lynam, D. R., Markon, K., ... Zimmerman, M. (2017). The Hierarchical Taxonomy of Psychopathology (HiTOP): A dimensional alternative to traditional nosologies. *Journal of Abnormal Psychology, 126*(4), 454--477. https://doi.org/10.1037/abn0000258

Lim, B., Arik, S. O., Loeff, N., & Pfister, T. (2021). Temporal fusion transformers for interpretable multi-horizon time series forecasting. *International Journal of Forecasting, 37*(4), 1748--1764. https://doi.org/10.1016/j.ijforecast.2021.03.012

Liebovitch, L. S., Peluso, P. R., Norman, M. D., Su, J., & Gottman, J. M. (2011). Mathematical model of the dynamics of psychotherapy. *Cognitive Neurodynamics, 5*, 265--275. https://doi.org/10.1007/s11571-011-9157-x

Liu, X., Cruz Rivera, S., Moher, D., Calvert, M. J., Denniston, A. K., & CONSORT-AI and SPIRIT-AI Working Group. (2020). Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: The CONSORT-AI extension. *Nature Medicine, 26*, 1364--1374. https://doi.org/10.1038/s41591-020-1034-x

Martinez-Martin, N., Greely, H. T., & Cho, M. K. (2021). Ethical development of digital phenotyping tools for mental health applications: Delphi study. *JMIR mHealth and uHealth, 9*(7), Article e27343. https://doi.org/10.2196/27343

Masten, A. S., & Cicchetti, D. (2010). Developmental cascades. *Development and Psychopathology, 22*(3), 491--495. https://doi.org/10.1017/S0954579410000222

Press, O., Smith, N. A., & Lewis, M. (2022). Train short, test long: Attention with linear biases enables input length extrapolation. In *International Conference on Learning Representations*. https://arxiv.org/abs/2108.12409

Rothbart, M. K. (2011). *Becoming who we are: Temperament and personality in development*. Guilford Press.

Ryan, R. M., & Deci, E. L. (2017). *Self-determination theory: Basic psychological needs in motivation, development, and wellness*. Guilford Press.

Schiepek, G., Aas, B., & Viol, K. (2016). The mathematics of psychotherapy: A nonlinear model of change dynamics. *Nonlinear Dynamics, Psychology, and Life Sciences, 20*(3), 369--399.

Shazeer, N. (2020). GLU variants improve transformer. *arXiv*. https://doi.org/10.48550/arXiv.2002.05202

van de Leemput, I. A., Wichers, M., Cramer, A. O. J., Borsboom, D., Tuerlinckx, F., Kuppens, P., van Nes, E. H., Viechtbauer, W., Giltay, E. J., Aggen, S. H., Derom, C., Jacobs, N., Kendler, K. S., van der Maas, H. L. J., Neale, M. C., Peeters, F., Thiery, E., Zachar, P., & Scheffer, M. (2014). Critical slowing down as early warning for the onset and termination of depression. *Proceedings of the National Academy of Sciences, 111*(1), 87--92. https://doi.org/10.1073/pnas.1312114110

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention is all you need. In *Advances in Neural Information Processing Systems* (Vol. 30). https://arxiv.org/abs/1706.03762

Velickovic, P., Cucurull, G., Casanova, A., Romero, A., Lio, P., & Bengio, Y. (2018). Graph attention networks. In *International Conference on Learning Representations*. https://arxiv.org/abs/1710.10903

U.S. Food and Drug Administration. (2026). *Clinical decision support software: Guidance for industry and Food and Drug Administration staff*. https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software

Vasey, B., Nagendran, M., Campbell, B., Clifton, D. A., Collins, G. S., et al. (2022). Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI. *Nature Medicine, 28*, 924--933. https://doi.org/10.1038/s41591-022-01772-9

Wampold, B. E., & Imel, Z. E. (2015). *The great psychotherapy debate: The evidence for what makes psychotherapy work* (2nd ed.). Routledge.

World Health Organization. (2021). *Ethics and governance of artificial intelligence for health*. https://www.who.int/publications/i/item/9789240029200

Zhang, B., & Sennrich, R. (2019). Root mean square layer normalization. In *Advances in Neural Information Processing Systems* (Vol. 32). https://arxiv.org/abs/1910.07467
