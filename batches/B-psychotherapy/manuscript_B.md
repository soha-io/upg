# The Common Architecture of Healing: A Critical Synthesis of Psychotherapy and Psychiatry and the Derivation of a Universal Therapy Graph

**[Author 1 name], [Author 2 name]**

[Affiliations]

**Author note.** Correspondence concerning this article should be addressed to [corresponding author]. The graph data files, figure-generation code, and all node and edge weights reported in this article are openly available in the article's supplementary repository. This article is the second in a planned series deriving an integrated, multidimensional network model of psychological functioning; the first derived the Universal Disorder Graph from a critical synthesis of the DSM, HiTOP, and ICD.

---

## Abstract

Psychotherapy works: across hundreds of trials and dozens of meta-analyses, bona fide psychological treatments produce reliable, clinically meaningful benefit. Yet the field that produces this benefit remains organized around competing theoretical schools whose outcome differences are small to negligible, whose mechanisms remain unestablished, and whose harms have only recently been measured seriously. This article provides a critical synthesis of the two healing traditions — psychotherapy and psychiatry — covering the philosophy, logic, applications, strengths, and weaknesses of the major systems of psychotherapy; the evidence-based practice movement and its challenges; the emerging literature on negative effects; and the six-decade debate between specific-ingredient and common-factor accounts of therapeutic change. From this synthesis we extract the shared clinical architecture beneath the schools: eleven functions — triage, safety and ethics, alliance, assessment, formulation, goal agreement, change work, practice, monitoring, review, and consolidation — that recur across psychodynamic, behavioral, cognitive, humanistic, systemic, third-wave, and integrative traditions. We then formalize this architecture as the **Universal Therapy Graph (UTG)**: a weighted, signed, directed graph with sequential, feedback, cross-cutting, inhibitory, and self-loop edges, in which each node carries an evidence weight and a process weight with published provenance, and each node owns an encapsulated subgraph for school-sensitive elaboration. The UTG satisfies the same five axioms as the Universal Disorder Graph derived in the first article of this series, and is designed as its control layer: where the disorder graph describes how psychopathology maintains itself, the therapy graph describes the organized process by which that maintenance is detected, mapped, and perturbed. Falsification conditions and a validation pathway are specified.

**Keywords:** psychotherapy, psychiatry, common factors, therapeutic alliance, psychotherapy integration, negative effects, network model, graph theory

---

## 1. Introduction

Two facts jointly define the scientific situation of psychotherapy. The first is that it works. Since the first meta-analytic demonstration that treated clients fare better than roughly 80% of untreated controls (Smith & Glass, 1977*), the efficacy of psychological treatment has been replicated across disorders, formats, and cultures to the point that it is no longer a serious question (Barth et al., 2013; Cook et al., 2017; Wampold & Imel, 2015). The second is that the field which produces this effect cannot agree on why. More than four hundred named therapies now exist (Prochaska & Norcross, 2013), organized into theoretical systems whose explanations of change are mutually incompatible — yet whose measured outcomes are, for most disorders, strikingly similar (Barth et al., 2013; Wampold, 2015; Wampold & Imel, 2015). This "equivalence paradox" has structured sixty years of debate: either the schools' specific ingredients each work through their advertised mechanisms and happen to be equally potent, or the benefit flows substantially through factors the schools share — the relationship, the frame, the expectation of help, the organized activity of healing itself (Cuijpers et al., 2019; Frank & Frank, 1991*; Rosenzweig, 1936*; Wampold, 2015).

The stakes of this debate changed when psychotherapy research began to take its own harms seriously. Roughly one in twenty clients in a representative national sample reported lasting negative effects of treatment, and a substantial minority reported experiences meeting criteria for professional malpractice (Strauss et al., 2021); qualitative meta-analysis of client reports yields a differentiated taxonomy of negative experiences, many of them relational — feeling unheard, judged, abandoned at termination — rather than technical (Vybíral et al., 2024). A field that harms through relationship as much as through technique needs a representation of therapy in which relational and technical processes are the same kind of object, monitored by the same machinery.

### 1.1 Aim and contribution

This article, the second in a series, does for the treatment literature what the first did for the classification literature. The first article synthesized the DSM, HiTOP, and ICD, argued that their failures are complementary, and derived the Universal Disorder Graph (UDG) — a weighted, signed, hierarchical graph of dimensional liabilities satisfying five explicit axioms. The present article synthesizes the psychotherapy and psychiatry literatures with the same design question: *what representational commitments would a model of treatment need in order to keep what every school gets right, discard what the school wars get wrong, and remain computable?* The answer we derive — the **Universal Therapy Graph (UTG)** — formalizes the shared clinical control loop beneath evidence-based and integrative practice as a recursive, weighted graph, satisfying the same axioms as the UDG and designed to couple to it: therapy, in the terms of this series, is organized control input to a person's disorder graph.

Three commitments distinguish the UTG from prior integrative schemes. First, it is *not a new therapy school*: its nodes are functions every competent treatment already performs, extracted from the transtheoretical, integration, common-factors, and evidence-based practice literatures (Goldfried, 1980; Norcross & Goldfried, 2019; Prochaska & Norcross, 2013; Wampold & Imel, 2015). Second, it is *evidence-weighted with published provenance*: each node carries a rated evidence weight and process weight, each edge a cited basis, so the object is criticizable line by line — no black box. Third, it is *formally continuous with the disorder model*: the same graph mathematics, the same axioms, the same encapsulation principle, so that the two strata can later be joined without translation.

### 1.2 Method of the review

The synthesis draws on a curated corpus of fifteen primary sources on psychotherapy and psychiatry — spanning efficacy, evidence-based practice, negative effects, treatment selection, common factors, and integrative psychiatry — together with the comparative textbook literature on the systems of psychotherapy (Boland & Verduin, 2022; Kress et al., 2021; Prochaska & Norcross, 2013) and the meta-analytic literature on therapeutic relationship elements, supplemented where necessary by literature located through targeted searches (marked with an asterisk in the reference list). Section 2 introduces the two healing traditions. Section 3 reviews the major systems of psychotherapy with their strengths and documented weaknesses. Section 4 reviews the evidence base, its limits, and its harms. Section 5 analyzes the common-factors debate. Section 6 extracts the universal architecture, and Section 7 formalizes it as the UTG. Section 8 locates the result in the series roadmap.

---

## 2. Two Healing Traditions

### 2.1 Psychotherapy

Psychotherapy is the systematic, ethically bounded use of psychological means — conversation, relationship, learning, practice — to relieve suffering and restore functioning (Kress et al., 2021; Prochaska & Norcross, 2013). Its modern history is conventionally dated to Freud, but its scientific history begins with the challenge of Eysenck (1952*), whose claim that neurotic patients improved as often without treatment as with it forced the field to measure itself. The measurement verdict, three decades later, was favorable (Smith & Glass, 1977*), and the ensuing half-century built the efficacy literature summarized above. Contemporary overviews — including those addressed to non-Western professional publics (Abdel-Qawi, 2020) — converge on the same profile: psychotherapy is effective, cost-effective, and preferred by many patients over medication, while facing persistent challenges of access, dissemination, dropout, and quality control (Cook et al., 2017).

### 2.2 Psychiatry

Psychiatry, the medical specialty concerned with mental disorder, brings to treatment the resources and the commitments of medicine: diagnosis, pharmacotherapy, somatic therapies, and stepped systems of care (Boland & Verduin, 2022). Its diagnostic instruments were the subject of the first article in this series; here two points carry forward. First, the prototype-versus-criteria debate in psychiatric diagnosis (Maj, 2011) is the nosological shadow of a treatment question — how much structure clinical judgment needs — that recurs in psychotherapy as the manualization debate (Cook et al., 2017; Wampold & Imel, 2015). Second, psychiatry is itself diversifying: integrative psychiatry programs now formally combine routine pharmacological care with psychotherapeutic, lifestyle, and complementary elements, and are beginning to be evaluated as whole packages (Rezo et al., 2023). The boundary between the traditions is thus increasingly administrative rather than conceptual: both are organized attempts to perturb a self-maintaining psychopathological system toward recovery, differing in the channels they use — a formulation to which we return in Section 7.

---

## 3. The Systems of Psychotherapy

The comparative analysis of therapy systems has a canonical form: for each system, its theory of personality, theory of psychopathology, theory of change, characteristic techniques, and the balance of its evidence (Kress et al., 2021; Prochaska & Norcross, 2013). Table 1 compresses that analysis for the seven system families that dominate practice and research. The narrative below emphasizes what each family contributes to the universal architecture of Section 6 — and what its documented weaknesses are.

**Table 1.** *The major systems of psychotherapy: core logic, contributions, and documented weaknesses.*

| System family | Exemplary figures | Theory of change (compressed) | Chief contribution to the shared architecture | Chief documented weaknesses |
|---|---|---|---|---|
| Psychodynamic | Freud, Klein, Bowlby, Luborsky | Insight into and corrective experience of unconscious relational patterns | The alliance concept itself; formulation of conflict and defense; termination work | Long historical resistance to measurement; efficacy evidence concentrated in short-term variants |
| Behavioral | Pavlov, Skinner, Wolpe | New learning: extinction, reinforcement, skills acquisition | Exposure; behavioral activation; homework; functional analysis | Early neglect of cognition, meaning, and relationship |
| Cognitive / CBT | Beck, Ellis | Modification of dysfunctional beliefs and information processing | Collaborative empiricism; session structure; self-monitoring; the largest trial evidence base | Component analyses often fail to show specific superiority of cognitive elements; heterogeneity of quality |
| Humanistic-experiential | Rogers, Perls, Greenberg | Actualization within an empathic, genuine, accepting relationship | Empathy as measurable, trainable core condition; emotion processing | Weaker trial base historically; vaguer specification of technique |
| Systemic / family | Minuchin, Haley, de Shazer | Change of interactional patterns that maintain the symptom | Context and relationship as intervention targets; reframing | Evidence base uneven across problems; constructs hard to operationalize |
| Third-wave / contextual | Linehan, Hayes, Segal | Change of one's *relation* to inner experience: acceptance, defusion, mindfulness, dialectics | Skills training; values work; explicit treatment hierarchies (DBT); process focus | Some flagship claims outran early evidence; component contributions debated |
| Integrative / eclectic | Frank, Goldfried, Norcross, Beutler, Prochaska | Whatever mechanisms the evidence supports, organized by principles of change and responsiveness | The very idea of transtheoretical principles; systematic treatment selection; stages of change | Risk of unprincipled eclecticism; integration frameworks themselves rarely tested as wholes |

Three observations organize this landscape. First, the families' *theories* conflict, but their *practices* converge: every family builds a bond, agrees on tasks, maps the problem, intervenes, assigns or evokes between-session experience, and handles endings (Goldfried, 1980; Norcross & Goldfried, 2019; Prochaska & Norcross, 2013). Convergence is clearest at the level Goldfried (1980) identified as *clinical strategies* — corrective experience and ongoing reality testing — situated between abstract theory and concrete technique. Second, the outcome literature rewards none of the families decisively: network meta-analysis of seven interventions for depression found all bona fide treatments effective with small between-treatment differences (Barth et al., 2013), the pattern that generalizes across most (not all) disorders (Wampold, 2015; Wampold & Imel, 2015). Third, each family's documented weaknesses are largely *absences* — dimensions of the shared work it underweights — which is precisely why an architecture extracted from all of them is more complete than any of them (Norcross & Goldfried, 2019).

The transtheoretical tradition adds one further element the school map lacks: *readiness*. Clients enter treatment at different stages of change, and interventions mismatched to stage underperform (Prochaska & Norcross, 2013). Any universal architecture must therefore make triage, goal negotiation, and adaptation first-class functions rather than assuming an always-ready client — a requirement the graph of Section 7 encodes structurally.

---

## 4. Evidence, Limits, and Harms

### 4.1 Evidence-based practice and its challenges

The evidence-based practice (EBP) framework defines good care as the integration of best research evidence with clinical expertise and patient characteristics, culture, and preferences (APA Presidential Task Force on Evidence-Based Practice, 2006). Its achievements are substantial: efficacious, cost-effective protocols exist across the anxiety, mood, trauma, eating, and psychotic disorders; dissemination initiatives have carried them into large care systems; and the framework has professionalized training and accountability (Cook et al., 2017). Its challenges are equally documented: efficacy-effectiveness gaps, exclusion of complex comorbid patients from trials, clinician misperceptions that manuals preclude flexibility, slow and partial implementation, and the persistent finding that adherence and competence measured within protocols predict outcome weakly (Cook et al., 2017; Wampold, 2015). EBP, in other words, specifies *what* should inform treatment but underdetermines *how* treatment is organized in time — a gap the UTG addresses.

### 4.2 Treatment selection and responsiveness

If treatments tie on average, matching may still matter for individuals. The systematic treatment selection tradition demonstrates that patient dimensions that cannot be randomized — reactance level, coping style, subjective distress, stage of change — moderate which therapeutic *style* helps whom: directive approaches for low-reactance clients, skill-building for externalizing copers, insight-oriented work for internalizing copers (Beutler et al., 2016). Meta-analytic work on relationship responsiveness reaches the same conclusion from the other side: tailoring the relationship to the particular patient improves outcomes beyond either technique or relationship alone (Norcross & Wampold, 2019). Treatment fitting, not treatment branding, is where individual differences earn their keep (Beutler et al., 2016) — which is why the UTG carries adaptation as a permanent node rather than a one-time selection.

### 4.3 Negative effects

The harms literature has matured from anecdote to measurement. In a random national sample, 4.9% of former psychotherapy patients reported lasting negative effects, with additional respondents reporting boundary violations or treatment experiences consistent with malpractice (Strauss et al., 2021). Reviews of adverse experiences distinguish side effects of properly delivered treatment, effects of unethical conduct, and deterioration independent of treatment — categories with different prevention logics — and document that assessment instruments, reporting standards, and trial-level monitoring all remain underdeveloped (Strauss et al., 2026). The client's-eye view adds content the instruments miss: qualitative meta-analysis across 51 studies identifies negative experiences clustering around the therapist (feeling judged, not listened to, pathologized), the treatment (mismatch, pace, endings), and the frame (costs, discontinuity), many invisible to symptom scales (Vybíral et al., 2024). Client decisional-balance research shows that anticipated harms and burdens weigh directly in treatment engagement among high-risk groups (Alonzo, 2020). Format changes add further asymmetries: online delivery expands access while introducing distinct disadvantages and adoption dynamics of its own (Furmańska et al., 2025). The design implication is unambiguous: monitoring for deterioration, adverse experience, and alliance strain must be architecturally central — not an optional add-on (Lambert et al., 2018; Strauss et al., 2026).

### 4.4 What follows for design

Sections 4.1–4.3 convert into three requirements for any universal treatment representation. It must be *organized in time* (EBP's gap); it must carry *permanent adaptation machinery* keyed to monitoring (the responsiveness finding); and it must treat *safety and adverse-effect detection as first-class structure* (the harms literature). These join the convergence findings of Section 3 as the design brief for Section 6.

---

## 5. The Common-Factors Debate

### 5.1 The contextual model and its evidence

The common-factors tradition — from Rosenzweig's (1936*) original "implicit common factors" through Frank's demoralization framework (Frank & Frank, 1991*) and the classic taxonomies of proposed commonalities (Grencavage & Norcross, 1990*) to Wampold's contextual model — holds that psychotherapy works substantially through pathways all bona fide treatments share: a real relationship, the creation of positive expectations through a credible explanation and ritual, and the enactment of health-promoting actions (Wampold, 2015; Wampold & Imel, 2015). Its meta-analytic evidence is strong at the level of association: alliance correlates with outcome robustly across treatments, disorders, and raters (Flückiger et al., 2018); empathy shows effects of comparable size (Elliott et al., 2018); goal consensus and collaboration predict outcome (Tryon & Winograd, 2011); therapist differences exceed treatment differences; and treatment differences themselves hover near zero for most comparisons (Barth et al., 2013; Wampold, 2015). Routine outcome monitoring with feedback — arguably a common factor manufactured by research — improves outcomes, particularly for cases going off track (Lambert et al., 2018). Clinical writing in this tradition goes further, arguing that a small set of relational-ethical moves — building trust under maximal transparency, validating without endorsing, siding with the patient's dilemma rather than one of its horns — may be close to globally applicable across presentations, including the complex and chronic cases that protocols fit worst (Howe, 2024).

### 5.2 The critical position

The strongest critical review concedes the associations and contests the causality: virtually no common factor has been shown to *cause* outcome by the standards required of a mechanism — temporal precedence, dose-response, experimental manipulation, ruled-out reverse causation (alliance may follow early symptom relief rather than produce it) — and the same standards convict the specific-ingredient side equally, since component studies and adherence-competence correlations also fail to establish mechanisms (Cuijpers et al., 2019). The honest state of the science is that psychotherapy's benefit is established while its causal pathways are not — for either camp (Cuijpers et al., 2019; Wampold, 2015).

### 5.3 Theoretical repairs

Two recent lines attempt to give the common factors what they lack — a unifying theory and a formal model. The self-determination account proposes that the heterogeneous common factors cohere as supports for three basic psychological needs (autonomy, competence, relatedness), distinguishing need-supportive *processes* from need-satisfying *techniques* and yielding testable predictions about when alliance, goal agreement, and expectations should carry outcome (Baier-Mosch et al., 2025). The dynamical-systems account formalizes alliance as an emergent order parameter of two coupled self-organizing systems — therapist and client — using synergetics: alliance is neither technique nor ingredient but a *state* the dyad enters, which then constrains ("enslaves," in synergetic vocabulary) the micro-dynamics of both parties (Tschacher et al., 2015). This formalization matters for the present series: it demonstrates that core therapy constructs can be given non-metaphorical mathematical form — and it anticipates the self-loop with which the UTG endows its alliance node.

### 5.4 Resolution by architecture

The debate's apparent deadlock dissolves under a change of representation. "Common factors versus specific ingredients" presumes that therapy is a *list* of components whose independent contributions sum. Every result reviewed above resists that presumption: alliance potentiates technique, technique feeds alliance, monitoring reshapes both, and none operates outside an ethical frame. Therapy behaves like a *system* — a set of coupled functions with feedback — and the correct scientific object for a coupled system is not a component list but a graph (Tschacher et al., 2015). On this view the common factors are the *high-connectivity nodes* of a shared clinical architecture, and the specific ingredients are school-specific *instantiations of one node* (change work). That is the object Section 6 extracts.

---

## 6. Extraction: The Universal Therapy Framework

### 6.1 Method of extraction

We extracted the shared architecture by triangulating four literatures that describe therapy at the level of function rather than school: the transtheoretical comparative analysis of therapy systems (Prochaska & Norcross, 2013), the psychotherapy integration corpus (Goldfried, 1980; Norcross & Goldfried, 2019), the evidence-based practice and case-formulation traditions (APA Presidential Task Force on Evidence-Based Practice, 2006; Eells, 2022), and the meta-analytic literature on relationship elements and monitoring (Elliott et al., 2018; Flückiger et al., 2018; Lambert et al., 2018; Norcross & Lambert, 2019; Tryon & Winograd, 2011). A function was admitted as universal if (a) it appears, under whatever local vocabulary, in every major system family of Table 1, and (b) at least one evidence stream supports its association with outcome or its necessity for safe practice. Eleven functions survived both filters.

### 6.2 The eleven nodes and their weights

Table 2 presents the eleven nodes. Each carries two ratings on a 1–5 scale: an **evidence weight** (how directly and strongly the literature supports the node's contribution) and a **process weight** (how architecturally central the node is to the organized flow of treatment). The two dimensions deliberately diverge: case formulation, for example, has maximal architectural centrality but more indirect isolated evidence than alliance or feedback (Eells, 2022; Norcross & Goldfried, 2019), and consolidation/termination is clinically indispensable but thinly studied in isolation (Norcross & Goldfried, 2019; Wampold & Imel, 2015). Figure B3 visualizes the profile.

![**Figure B3.** Evidence and process weights of the eleven universal nodes (1–5 scale; complete provenance in the accompanying data files).](../figures/figB3_evidence_process_weights.png)

**Table 2.** *The eleven universal nodes: function, ancestry, and weights (E = evidence, P = process; complete provenance in* utg_nodes.csv*).*

| # | Node | Core function | E | P | Principal evidential anchor |
|---|---|---|---|---|---|
| 1 | Entry / Triage | Problem, urgency, fit, care level, immediate risk | 4 | 5 | APA Presidential Task Force (2006) |
| 2 | Safety + Ethical Frame | Consent, confidentiality, risk procedures, boundaries | 5 | 5 | APA (2017); Linehan (2015) |
| 3 | Engagement / Alliance | Bond, task and goal agreement, empathy, rupture-repair | 5 | 5 | Bordin (1979); Flückiger et al. (2018); Elliott et al. (2018) |
| 4 | Assessment | Symptoms, functioning, history, context, strengths, preferences | 4 | 5 | Eells (2022); APA Presidential Task Force (2006) |
| 5 | Case Formulation | Living causal-functional map with maintaining loops | 4 | 5 | Eells (2022); Norcross & Goldfried (2019) |
| 6 | Goal Agreement | Shared, value-aligned, measurable targets | 5 | 5 | Tryon & Winograd (2011); Bordin (1979) |
| 7 | Change Work / Intervention | Targeted methods across cognition, behavior, emotion, relations, skills, meaning, context | 5 | 5 | Wampold & Imel (2015); Barth et al. (2013); Hayes & Hofmann (2018) |
| 8 | Practice + Generalization | Homework, experiments, exposure, life transfer | 4 | 4 | Kazantzis et al. (2010) |
| 9 | Outcome Monitoring | Symptoms, functioning, alliance, risk, adverse effects, not-on-track detection | 5 | 5 | Lambert et al. (2018); Strauss et al. (2026) |
| 10 | Review + Adaptation | Repair, reformulate, switch, step care, renegotiate | 4 | 5 | Hayes & Hofmann (2018); Lambert et al. (2018); Norcross & Wampold (2019) |
| 11 | Consolidation / Termination / Maintenance | Gains review, relapse prevention, agency transfer, booster routes | 3 | 4 | Norcross & Goldfried (2019); Wampold & Imel (2015) |

Two features distinguish this extraction from a stage model. First, the functions are *concurrent, not serial*: alliance work does not end when assessment begins, and monitoring runs from the first contact. The sequential spine is a default flow, not a fixed order. Second, the architecture is *recursive*: its central loop — formulate, agree, intervene, practice, monitor, review, reformulate — repeats until review routes to consolidation. Recursion is what makes the architecture a control system rather than a protocol (Hayes & Hofmann, 2018; Lambert et al., 2018).

---

## 7. The Universal Therapy Graph

### 7.1 Formal definition and axiom compliance

Let $V$ be the node set of Table 2 together with the subgraph nodes specified in the data files, and let $W \in \mathbb{R}^{|V| \times |V|}$ be a signed weighted adjacency matrix. The UTG is $G = (V, W)$ with an edge typology partitioning nonzero entries into **sequential** edges (the default workflow spine), **feedback** edges (recursion: review→formulation, monitoring→alliance, consolidation→entry), **cross-cutting** edges (concurrent influence: alliance⇄change work), **inhibitory** edges (negative entries: the safety frame *bounds* admissible interventions; protective factors *dampen* consequences), and **self-loops** (alliance self-stabilization; skill compounding). Figure B1 displays the graph.

![**Figure B1.** The Universal Therapy Graph: the recursive clinical control loop. Solid edges form the sequential spine; dashed red edges are feedback (recursion); dotted orange edges are cross-cutting concurrent influences; the teal edge is inhibitory (Axiom 5); purple arcs are self-loops (Axiom 4). Dark nodes are Evidence-5/Process-5 core architecture.](../figures/figB1_universal_therapy_graph.png)

The five axioms adopted for this series are satisfied as follows. *Axiom 1* (universal connectivity): every node reaches every other through the spine and feedback edges. *Axiom 2* (non-dismissibility): no node may be deleted in the formulation of a treatment — a commitment with clinical content, since the harms literature shows that omitted monitoring and mishandled endings are precisely where damage concentrates (Strauss et al., 2026; Vybíral et al., 2024). *Axiom 3* (mediated and unmediated influence): alliance affects outcome both directly and through intervention uptake — both routes are edges (Flückiger et al., 2018; Wampold, 2015). *Axiom 4* (self-influence): the alliance self-loop encodes the dynamical-systems finding that alliance, once formed, stabilizes itself as an emergent state of the dyad (Tschacher et al., 2015). *Axiom 5* (signed superposition): the safety→change-work edge is negative — ethical constraints subtract from the admissible intervention space — and concurrent influences on any node sum (American Psychological Association, 2017).

### 7.2 Subgraphs and encapsulation

Each workflow node owns an encapsulated subgraph elaborating it in school-sensitive detail, communicating with the rest of the graph only through its mother node — the same encapsulation principle as the UDG. The alliance subgraph carries Bordin's (1979) bond, task, and goal facets plus empathy, collaboration, and rupture-repair (Elliott et al., 2018; Norcross & Wampold, 2019). The monitoring subgraph carries symptom, functioning, alliance, risk, *adverse-effect*, and not-on-track channels — giving the negative-effects literature permanent structural residence (Lambert et al., 2018; Strauss et al., 2021, 2026). The formulation subgraph (Figure B2) is the clinically richest: a maintaining loop — presenting problem → triggers → emotion/body state → meaning → action/avoidance → consequences → back to the problem — with contextual inputs and an inhibitory protective-factors node (Eells, 2022; Hayes & Hofmann, 2018). Its loop structure is not decorative: it is the same formal object as the self-sustaining symptom dynamics of the disorder stratum, which is what makes formulation the natural *interface* between the two graphs.

![**Figure B2.** The Case Formulation subgraph (zoom-in): a maintaining loop with contextual inputs and protective inhibition. The subgraph communicates with the workflow level only through its mother node (encapsulation principle).](../figures/figB2_formulation_subgraph.png)

### 7.3 Coupling to the Universal Disorder Graph

The first article in this series modeled psychopathology as a weighted graph whose states can become self-maintaining. In control-theoretic terms, treatment is then an organized source of control input: interventions perturb node states, alter edge weights (new learning), and support the person's own control capacity. The UTG specifies *where that input comes from and how it is regulated*: assessment and formulation estimate the person's disorder subgraph; goal agreement selects target states; change work applies input; practice extends it into the person's environment; monitoring measures the response; review adjusts the policy. The two graphs are thus not analogues but complements — one models the system to be moved, the other models the mover — and their formal continuity (same axioms, same edge semantics, same encapsulation) is what will later allow them to be composed into a single model, with the full state-space and control machinery developed in the mathematical article of this series. This coupling also honors a constraint stated in the series' axioms of origin: the model must not override human authenticity and freedom. In the coupled system, the client's own goal-directed effort is a control input *from within* — therapy augments it rather than replacing it, a formulation consistent with the self-determination account of why need-supportive processes carry outcome (Baier-Mosch et al., 2025).

### 7.4 What the UTG adds

Against school-based organization, the UTG replaces brand identity with functional identity: any school's treatment is a particular weighting and instantiation of the same eleven nodes, which makes school comparison a measurement question rather than a tribal one (Goldfried, 1980; Prochaska & Norcross, 2013). Against stage and protocol models, it adds feedback structure: recursion and monitoring are edges, not appendices (Lambert et al., 2018). Against the common-factors list, it adds coupling: the factors' documented interdependencies become explicit signed edges rather than covariates in separate meta-analyses (Cuijpers et al., 2019; Wampold, 2015). Against prior integrative frameworks — which supply principles but no computable object (Norcross & Goldfried, 2019) — it adds machine-readability with provenance: every node and edge is published with its evidential basis, re-derivable and revisable by any research group. And against all of them it adds continuity with a disorder model, which no treatment framework currently possesses.

### 7.5 Falsifiability, validation pathway, and limitations

The UTG makes refutable commitments. *Structural*: if a major treatment system is found whose effective practice omits one of the eleven functions entirely, the universality claim fails for that node; conversely, if a function outside the eleven is shown to be both universal and outcome-relevant, the node set must be revised — both are recorded revisions. *Relational*: the cross-cutting alliance⇄change-work edges predict that alliance and technique effects will be non-additive in adequately instrumented studies; clean additivity would falsify the coupling. *Dynamic*: the feedback edges predict that monitoring-informed adaptation improves outcomes over identical treatment without it — a prediction already supported for feedback systems (Lambert et al., 2018) — and the alliance self-loop predicts alliance stability dynamics of the kind synergetic models describe (Tschacher et al., 2015). Validation should proceed from instrumented routine care (the nodes map directly onto measurement-based care data streams) to prospective comparison of UTG-organized versus conventionally organized treatment.

Four limitations bound the contribution. First, the node and edge weights are consensus priors — rated, sourced, and versioned, but not yet estimated from process data; they inherit the causal-inference caveats of the common-factors evidence they summarize (Cuijpers et al., 2019). Second, the extraction privileges the Western, English-language treatment literature; the architecture's universality across cultural healing frames is an empirical question, though its function-level (rather than technique-level) formulation is designed to travel (Wampold, 2015). Third, the UTG models the treatment *process*, not the treatment *system*: workforce, financing, and access — decisive for real-world outcomes (Cook et al., 2017) — belong to the systems stratum of this series, not to this graph. Fourth, psychiatry enters here as process (integrative care, measurement, prescription as change work) rather than as pharmacology; the biological channel receives fuller treatment when the temperament and systems strata are developed.

---

## 8. Conclusion

The psychotherapy literature presents a paradox — treatments that work equally while explaining themselves incompatibly — and a newer obligation: to take harms as seriously as benefits. This article argued that both are representation problems. Schools are lists of commitments; common-factor and specific-ingredient accounts are lists of components; and lists cannot carry feedback, coupling, inhibition, or self-maintenance — the properties that every strand of evidence reviewed here exhibits. The Universal Therapy Graph replaces the lists with a system: eleven evidence-weighted functions, coupled by signed edges, recursively organized, encapsulating school-sensitive subgraphs, satisfying the same five axioms as the Universal Disorder Graph it is built to steer. It is offered, like its companion, not as a finished theory but as a reproducible object — the treatment stratum of a multidimensional model of the person whose remaining strata occupy the articles to come.

---

## References

*Sources marked with an asterisk (\*) were located by the authors through supplementary literature searches beyond the assembled source library.*

Abdel-Qawi, R. E. A. (2020). Psychotherapy: Its pros and cons in terms of definition, benefits, types, and challenges [in Arabic]. *Nafssaniat, 65*.

Alonzo, D. (2020). Pros and cons of mental health treatment: Reports from depressed clients with suicidal ideation. *Journal of Mental Health*. Advance online publication. https://doi.org/10.1080/09638237.2020.1793121

American Psychological Association. (2017). *Ethical principles of psychologists and code of conduct*. https://www.apa.org/ethics/code

American Psychological Association Presidential Task Force on Evidence-Based Practice. (2006). Evidence-based practice in psychology. *American Psychologist, 61*(4), 271–285. https://doi.org/10.1037/0003-066X.61.4.271

Baier-Mosch, F., Weiher, G. M., & Kananian, S. (2025). Determining what is common: A theoretical account of common factors in psychotherapy through the lens of self-determination theory. *Journal of Contemporary Psychotherapy, 55*(3), 269–281. https://doi.org/10.1007/s10879-025-09664-y

Barth, J., Munder, T., Gerger, H., Nüesch, E., Trelle, S., Znoj, H., Jüni, P., & Cuijpers, P. (2013). Comparative efficacy of seven psychotherapeutic interventions for patients with depression: A network meta-analysis. *PLOS Medicine, 10*(5), Article e1001454. https://doi.org/10.1371/journal.pmed.1001454

Beutler, L. E., Someah, K., Kimpara, S., & Miller, K. (2016). Selecting the most appropriate treatment for each patient. *International Journal of Clinical and Health Psychology, 16*(1), 99–108. https://doi.org/10.1016/j.ijchp.2015.08.001

Boland, R. J., & Verduin, M. L. (2022). *Kaplan & Sadock's synopsis of psychiatry* (12th ed.). Wolters Kluwer.

Bordin, E. S. (1979). The generalizability of the psychoanalytic concept of the working alliance. *Psychotherapy: Theory, Research & Practice, 16*(3), 252–260. https://doi.org/10.1037/h0085885

Cook, S. C., Schwartz, A. C., & Kaslow, N. J. (2017). Evidence-based psychotherapy: Advantages and challenges. *Neurotherapeutics, 14*(3), 537–545. https://doi.org/10.1007/s13311-017-0549-4

Cuijpers, P., Reijnders, M., & Huibers, M. J. H. (2019). The role of common factors in psychotherapy outcomes. *Annual Review of Clinical Psychology, 15*, 207–231. https://doi.org/10.1146/annurev-clinpsy-050718-095424

Eells, T. D. (Ed.). (2022). *Handbook of psychotherapy case formulation* (3rd ed.). Guilford Press.

Elliott, R., Bohart, A. C., Watson, J. C., & Murphy, D. (2018). Therapist empathy and client outcome: An updated meta-analysis. *Psychotherapy, 55*(4), 399–410. https://doi.org/10.1037/pst0000175

Eysenck, H. J. (1952). The effects of psychotherapy: An evaluation. *Journal of Consulting Psychology, 16*(5), 319–324. https://doi.org/10.1037/h0063633 \*

Flückiger, C., Del Re, A. C., Wampold, B. E., & Horvath, A. O. (2018). The alliance in adult psychotherapy: A meta-analytic synthesis. *Psychotherapy, 55*(4), 316–340. https://doi.org/10.1037/pst0000172

Frank, J. D., & Frank, J. B. (1991). *Persuasion and healing: A comparative study of psychotherapy* (3rd ed.). Johns Hopkins University Press. \*

Furmańska, J., Rutkowska, E., Lane, H., Meixner, J., Marques, C. C., & Martins, M. J. (2025). Advantages and disadvantages of online psychotherapy and decisions to use it in the era of the COVID-19 pandemic — analysis of mediation variables. *Frontiers in Psychiatry, 16*, Article 1679186. https://doi.org/10.3389/fpsyt.2025.1679186

Goldfried, M. R. (1980). Toward the delineation of therapeutic change principles. *American Psychologist, 35*(11), 991–999. https://doi.org/10.1037/0003-066X.35.11.991

Grencavage, L. M., & Norcross, J. C. (1990). Where are the commonalities among the therapeutic common factors? *Professional Psychology: Research and Practice, 21*(5), 372–378. https://doi.org/10.1037/0735-7028.21.5.372 \*

Hayes, S. C., & Hofmann, S. G. (Eds.). (2018). *Process-based CBT: The science and core clinical competencies of cognitive behavioral therapy*. New Harbinger Publications.

Howe, E. (2024). Psychotherapeutic approaches: Hopefully, globally effective. *Frontiers in Psychiatry, 15*, Article 1322184. https://doi.org/10.3389/fpsyt.2024.1322184

Kazantzis, N., Whittington, C., & Dattilio, F. (2010). Meta-analysis of homework effects in cognitive and behavioral therapy: A replication and extension. *Clinical Psychology: Science and Practice, 17*(2), 144–156. https://doi.org/10.1111/j.1468-2850.2010.01204.x

Kress, V. E., Seligman, L., & Reichenberg, L. W. (2021). *Theories of counseling and psychotherapy: Systems, strategies, and skills* (5th ed.). Pearson.

Lambert, M. J., Whipple, J. L., & Kleinstäuber, M. (2018). Collecting and delivering progress feedback: A meta-analysis of routine outcome monitoring. *Psychotherapy, 55*(4), 520–537. https://doi.org/10.1037/pst0000167

Linehan, M. M. (2015). *DBT skills training manual* (2nd ed.). Guilford Press.

Maj, M. (2011). Psychiatric diagnosis: Pros and cons of prototypes vs. operational criteria. *World Psychiatry, 10*(2), 81–82. https://doi.org/10.1002/j.2051-5545.2011.tb00019.x

Norcross, J. C., & Goldfried, M. R. (Eds.). (2019). *Handbook of psychotherapy integration* (3rd ed.). Oxford University Press.

Norcross, J. C., & Lambert, M. J. (Eds.). (2019). *Psychotherapy relationships that work: Vol. 1. Evidence-based therapist contributions* (3rd ed.). Oxford University Press.

Norcross, J. C., & Wampold, B. E. (Eds.). (2019). *Psychotherapy relationships that work: Vol. 2. Evidence-based therapist responsiveness* (3rd ed.). Oxford University Press.

Prochaska, J. O., & Norcross, J. C. (2013). *Systems of psychotherapy: A transtheoretical analysis* (8th ed.). Cengage Learning.

Rezo, A., Wagner, P., Sanchez, A., Brunnhuber, S., Pedrosa Gil, F., & Rapp, M. A. (2023). Comparing psychiatric routine care and integrative psychiatry — A study protocol for a prospective observational study (INTEGRAL). *Advances in Integrative Medicine*. Advance online publication. https://doi.org/10.1016/j.aimed.2023.02.003

Rosenzweig, S. (1936). Some implicit common factors in diverse methods of psychotherapy. *American Journal of Orthopsychiatry, 6*(3), 412–415. https://doi.org/10.1111/j.1939-0025.1936.tb05248.x \*

Smith, M. L., & Glass, G. V. (1977). Meta-analysis of psychotherapy outcome studies. *American Psychologist, 32*(9), 752–760. https://doi.org/10.1037/0003-066X.32.9.752 \*

Strauss, B., Gawlytta, R., Schleu, A., & Frenzl, D. (2021). Negative effects of psychotherapy: Estimating the prevalence in a random national sample. *BJPsych Open, 7*(6), Article e186. https://doi.org/10.1192/bjo.2021.1025

Strauss, B., Rosendahl, J., & Klatte, R. (2026). Adverse experiences in psychological treatments: Where do we stand? *Current Opinion in Psychology, 67*, Article 102161. https://doi.org/10.1016/j.copsyc.2025.102161

Tryon, G. S., & Winograd, G. (2011). Goal consensus and collaboration. *Psychotherapy, 48*(1), 50–57. https://doi.org/10.1037/a0022061

Tschacher, W., Haken, H., & Kyselo, M. (2015). Alliance: A common factor of psychotherapy modeled by structural theory. *Frontiers in Psychology, 6*, Article 421. https://doi.org/10.3389/fpsyg.2015.00421

Vybíral, Z., Ogles, B. M., Řiháček, T., Urbancová, B., & Gocieková, V. (2024). Negative experiences in psychotherapy from clients' perspective: A qualitative meta-analysis. *Psychotherapy Research, 34*(3), 279–292. https://doi.org/10.1080/10503307.2023.2226813

Wampold, B. E. (2015). How important are the common factors in psychotherapy? An update. *World Psychiatry, 14*(3), 270–277. https://doi.org/10.1002/wps.20238

Wampold, B. E., & Imel, Z. E. (2015). *The great psychotherapy debate: The evidence for what makes psychotherapy work* (2nd ed.). Routledge.
