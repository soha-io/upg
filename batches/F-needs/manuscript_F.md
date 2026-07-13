# What You Cannot Do Without: A Critical Synthesis of Needs Theories and the Derivation of a Universal Needs Graph

**[Author 1 name], [Author 2 name]**

[Affiliations]

**Author note.** Correspondence concerning this article should be addressed to [corresponding author]. The graph data files and figure-generation code are openly available in the article's supplementary repository. This article is the sixth in a planned series deriving the Unified Person Graph (UPG), an eight-dimensional network model of psychological functioning. The preceding articles derived the Universal Disorder Graph (psychopathology), Universal Therapy Graph (treatment), Universal Developmental Graph (development), Universal Personality Graph (personality), and Universal Temperament Graph (temperament).

---

## Abstract

Needs theories answer the question that gives every other psychological stratum its stakes: what must the person obtain — not merely want — for the system to function? The tradition runs from Murray's catalog and Maslow's pyramid through the organizational content theories of Alderfer, Herzberg, and McClelland to self-determination theory's three basic psychological needs, evolutionary renovations of the hierarchy, and contemporary candidates such as predictability and meaning. A recent meta-theoretical review counts twenty-nine valid theories — a museum, once again, of partially incompatible frameworks. This article critically synthesizes the major needs theories, their philosophies, logics, applications, and documented weaknesses, and reviews what the evidence settled: the necessity criterion that separates needs from desires; a small convergent domain core beneath the taxonomic sprawl; the empirical collapse of the fixed ladder in favor of dynamic, situationally and developmentally gated prioritization; the dual-process finding that need frustration is not the mere absence of satisfaction; and dispositional need-strength differences with demonstrated neural reward-fit signatures. From the synthesis we extract seven principles and formalize them as the **Universal Needs Graph (UNeedG)**: a signed, weighted, gated graph whose seven need domains feed distinct satisfaction and frustration channels with asymmetric outcome edges, whose dynamic-prioritization node replaces the pyramid, and whose interfaces couple environmental supports inward and motivation, personality, and psychopathology outward. Within the Unified Person Graph, needs constitute the input layer of the motivational system: the stratum that converts states of the person and world into the goal pressures the next stratum turns into action. Falsification conditions, a validation pathway, and limitations are specified.

**Keywords:** needs, basic psychological needs, self-determination theory, Maslow, McClelland, need frustration, network model, graph theory

---

## 1. Introduction

The strata of the Unified Person Graph derived so far describe structures — disorders that maintain themselves, therapies that steer, histories that become weights, traits that filter, temperaments that bias. None of them yet says why the person moves at all. Needs theories supply the answer psychology has converged on from five directions at once: the person moves because certain commodities — metabolic, relational, effectance-related, volitional — are *necessities*, and their deficit or active thwarting generates pressure the rest of the system must resolve (Ryan & Deci, 2000; Szalma, 2020). The question of this stratum — *what do you need?* — is thus prior to the question the next stratum will ask (*what do you want?*): wants are negotiable; needs, by definition, are not.

The tradition's plurality is quantified: a systematic meta-theoretical review identified twenty-nine valid theories of basic psychological needs across five fields, most operating at the psychological level of analysis, fewer than a third offering any classification of their own contents (Sohrabi et al., 2021). The famous ones disagree famously: Maslow's (1943)\* five-tier prepotency ladder; Alderfer's (1969)\* three-category compression with a frustration–regression dynamic; Herzberg's two-factor separation of hygiene from motivators (Herzberg et al., 1959\*; Osemeke & Adegboyega, 2017); McClelland's (1961)\* acquired, individually varying need strengths; self-determination theory's exactly three universal psychological needs (Ryan & Deci, 2000); an evolutionary renovation that demolishes the pyramid's apex and rebuilds it as overlapping, life-stage-gated motive systems (Kenrick et al., 2010); and current proposals to admit predictability (Dweck, 2017\*) and meaning (Tønnesvang, 2025) to the basic set.

This article, the sixth in the UPG series, treats the sprawl as the series treats every sprawl: as a representation problem. We review the families critically (Section 3), review what the evidence settled (Section 4), extract the joint requirements as principles (Section 5), and satisfy them with a graph continuous in formalism and axioms with the five strata already derived (Section 6). The review draws on the assembled library, with sources located beyond it marked by an asterisk in the reference list.

---

## 2. Needs in Brief

A need, in the sense this stratum formalizes, is distinguished from a want by a *necessity criterion*: its satisfaction is required for integrity, growth, and wellbeing, and its deficit or thwarting produces measurable dysfunction — degraded motivation, wellbeing, and health — rather than mere disappointment (Dweck, 2017\*; Ryan & Deci, 2000). Three structural commitments matter for everything that follows. First, needs span levels: the tradition runs continuously from viscerogenic necessities through relational and effectance needs to growth and meaning, and any universal representation must carry the full span without reducing one level to another (Maslow, 1943\*; Sohrabi et al., 2021; Tønnesvang, 2025). Second, needs are *universal in kind but variable in strength and expression*: the same relatedness need that is satisfied in one culture through extended kinship is satisfied elsewhere through chosen intimacy, and individuals differ dispositionally in need intensity — the McClelland tradition's enduring contribution (McClelland, 1961\*; Rybnicek et al., 2019). Third, needs are consequential through two distinct channels: satisfaction predicts flourishing, while active frustration predicts ill-being and psychopathology risk, and the two are not opposite ends of one dial (Vansteenkiste & Ryan, 2013\*; Vansteenkiste et al., 2020\*). The graph of Section 6 carries all three commitments by construction.

---

## 3. The Theories: A Critical Tour

Table 1 compresses the comparative analysis; Figure F2 maps each theory's constructs onto the consensus domains the extraction will formalize. The narrative highlights contributions and documented weaknesses.

**Table 1.** *Major needs-theory families: logic, contributions, and documented weaknesses.*

| Family | Exemplary figures | Core logic of needs | Chief contribution to the universal architecture | Chief documented weaknesses |
|---|---|---|---|---|
| Catalog / personological | Murray; Lewin | Needs as directional intrapsychic forces; tension systems seeking release | The need construct itself; need strength as an individual difference; press (environment) as co-determinant | Catalog unbounded (20+ needs); measurement projective; no priority structure |
| Hierarchy | Maslow | Five prepotent tiers from physiological to self-actualization | Full-span coverage; deficit vs. growth distinction; the intuition of priority | Strict ordering empirically unsupported; apex vague; individual/cultural variation unaccommodated |
| Organizational content | Alderfer; Herzberg; McClelland | Compressed categories (ERG), satisfier/dissatisfier separation, or acquired need strengths driving work behavior | Frustration–regression dynamic; satisfaction ≠ reverse of dissatisfaction; dispositional need strength (nAch, nAff, nPow) | Workplace-bound evidence; Herzberg's method artifacts; McClelland's projective measurement debates |
| Self-determination theory | Deci; Ryan | Exactly three universal psychological needs — autonomy, competence, relatedness — whose satisfaction enables intrinsic motivation and internalization | The necessity criterion; need support vs. thwart; satisfaction/frustration dual process; strongest evidence base | Parsimony contested (candidate fourth needs); physiological needs outside scope; universality-of-expression debates |
| Evolutionary renovation | Kenrick; Griskevicius; Neuberg; Schaller | Overlapping fundamental-motive systems ordered by evolutionary function, developmental sequence, and situational triggers | Dynamic, gated prioritization; life-history staging; the demolition of the fixed ladder | Reproductive apex contested; distal function vs. proximal experience tension; direct tests sparse |
| Contemporary extensions | Dweck; Tønnesvang | Explicit admission criteria for "basic"; meaning as a fourth SDT-grade need; composite needs built from basics | Criteria discipline; meaning/coherence domain; integration scaffolding | Young; competing formulations not yet adjudicated |

![**Figure F2.** Convergence across needs theories: each family's constructs mapped onto the seven-domain consensus core (existence and safety displayed as one column; after Sohrabi et al., 2021; Szalma, 2020; Kenrick et al., 2010; Tønnesvang, 2025). Grey cells mark constructs that are derivative, implicit, or absent in the source theory.](../figures/figF2_theory_domain_mapping.png)

### 3.1 Origins: Murray and the need construct

Murray (1938)\* gave psychology the need as a theoretical object: a directional force, with a qualitative aim and an energetic drive component, inferable from behavior and paired with environmental *press* — the field's first person-by-situation formulation (Szalma, 2020). His catalog of twenty-plus psychogenic needs seeded nearly everything after it: achievement, affiliation, dominance, and autonomy all begin here, and the Thematic Apperception Test began the field's long argument about implicit measurement. The documented weaknesses are the catalog's unboundedness and the absence of priority structure (Szalma, 2020). The extraction keeps the construct's two-part anatomy — aim plus energization — and Murray's insistence that need and environment co-determine outcome, which the graph renders as the environmental-supports interface.

### 3.2 Maslow: the hierarchy and its double legacy

Maslow's (1943)\* theory remains psychology's most exported diagram: five tiers — physiological, safety, love/belonging, esteem, self-actualization — with lower needs prepotent over higher ones, later softened by Maslow himself into overlapping salience and famously extended toward growth needs (McLeod, 2025). Its permanent contributions are full-span coverage, the deficit/growth distinction, and the intuition the field still honors in gated form: some needs *can* seize priority. Its documented weaknesses are equally canonical: the strict ordering fails empirically — satisfaction levels across the tiers correlate with traits and emotional systems in patterns incompatible with a fixed staircase (Montag et al., 2020) — the apex is conceptually vague, and cultural and individual variation is unaccommodated (Kenrick et al., 2010; McLeod, 2025). The extraction keeps the span and demotes the ladder to one input among several of a dynamic prioritization mechanism.

### 3.3 The organizational content theories

Alderfer's (1969)\* ERG compression — existence, relatedness, growth — added the tradition's first explicit *frustration dynamic*: blocked growth regresses pressure onto relatedness, blocked relatedness onto existence, anticipating the substitution mechanisms the modern literature documents (Osemeke & Adegboyega, 2017). Herzberg's two-factor theory contributed a structural insight that outlived its method controversies: satisfaction and dissatisfaction are fed by different factor classes — motivators versus hygiene — and are therefore not one bipolar dimension (Herzberg et al., 1959\*; Osemeke & Adegboyega, 2017), a direct ancestor of the dual-channel architecture Section 6 formalizes. McClelland (1961)\* converted needs into acquired, measurable individual differences — need for achievement, affiliation, and power — whose predictive value in work, learning, and leadership contexts remains an active literature (Baptista et al., 2021; Siok et al., 2023), now with neuroscientific support: rewards matched to a person's dominant need produce stronger reward-circuit activation than mismatched rewards (Rybnicek et al., 2019). Documented weaknesses: workplace-bound evidence bases, Herzberg's critical-incident method artifacts, and long-running measurement debates around projective need assessment (Osemeke & Adegboyega, 2017). The extraction keeps the frustration dynamic, the two-factor asymmetry, and need strength as a first-class mechanism.

### 3.4 Self-determination theory: the necessity criterion enforced

Self-determination theory made "basic need" a claim with teeth: autonomy, competence, and relatedness qualify because their satisfaction is required for intrinsic motivation, internalization, and wellbeing across domains and cultures, and their deprivation produces degradation — not merely absence of benefit (Ryan & Deci, 2000). The program's exports dominate the contemporary literature: need-supportive versus need-thwarting environments as the central contextual variable; the satisfaction/frustration dual process, in which frustration predicts ill-being, defensiveness, and need substitutes over and above low satisfaction (Vansteenkiste & Ryan, 2013\*; Vansteenkiste et al., 2020\*); and measurement traditions now extended to state-level ecological assessment (Dunton et al., 2023) and applied educational modeling — where, notably, a recent well-powered structural test found autonomy satisfaction predicting value appraisals but weak overall model fit, a useful reminder that the framework's local predictions do not always assemble (Skues et al., 2025). Documented weaknesses: the exactly-three parsimony is contested from both directions — physiological needs stand outside the theory's scope, and candidate basic needs keep arriving (Dweck, 2017\*; Tønnesvang, 2025). The extraction adopts SDT's necessity criterion as the stratum's admission rule and its dual process as the channel architecture.

### 3.5 The evolutionary renovation

Kenrick et al. (2010) rebuilt the pyramid on three overlays: evolutionary function (motive systems exist because they solved fitness problems — self-protection, affiliation, status, mating, care), developmental sequencing (motives come online with life stage), and situational triggering (current cues, not a ladder, determine which system holds priority now). Self-actualization loses its apex seat, subsumed under status and mating-adjacent display. The renovation's permanent contribution is the *dynamics*: priority as a gated, cue-driven, life-history-staged computation — exactly what a graph can carry and a pyramid cannot. Documented weaknesses: the reproductive reframing of the apex is contested, the distal/proximal levels invite confusion, and direct experimental tests remain sparse (Kenrick et al., 2010). The extraction takes the gating architecture and leaves the apex dispute at the subgraph level, where it belongs.

### 3.6 Contemporary extensions: criteria and candidates

Two developments discipline the tradition's growth. Dweck (2017)\* proposed explicit criteria for basicness — a need's satisfying goals must appear early and its satisfaction must be inherently valued — yielding a set (acceptance, predictability, competence, trust, control, self-esteem/status) in which some classic needs become composites; predictability in particular enters the safety domain with new precision. Tønnesvang (2025) argues meaning satisfies SDT-grade criteria, proposing the MARC quartet — meaning, autonomy, relatedness, competence — with meaning as the vitalizing frame under which the other three are pursued. The meta-theoretical landscape review situates both moves: theory production has slowed, application dominates, and integration is the field's live frontier (Sohrabi et al., 2021). The extraction admits meaning/growth as a domain node — flagged as the consensus core's most revisable member — and adopts criteria discipline in the falsifiability program.

### 3.7 The applied literatures

The applied corpus demonstrates the constructs' reach and their convergence in practice: consumer research maps purchasing onto need surrogates and having/being distinctions (Ward & Lasen, 2009); educational research operationalizes McClelland's triad in online learning (Siok et al., 2023) and SDT in higher-education emotion (Skues et al., 2025); work psychology runs on all three organizational theories (Baptista et al., 2021; Osemeke & Adegboyega, 2017); health research measures thirteen need subscales in physical activity with ecological momentary assessment (Dunton et al., 2023); and complex-problem-solving research connects need pressure to cognition and simulated action, including Dörner's PSI architecture — a rare existing attempt to make needs computational (Güss et al., 2017). Across applications the working skeleton is constant: domains, strengths, supports, and dual outcomes — the skeleton the extraction makes explicit.

---

## 4. What the Evidence Settled

### 4.1 The ladder fell; the span survived

No adequately powered study recovers Maslow's strict prepotency ordering; satisfaction across tiers is simultaneous, trait-correlated, and culturally variable (Kenrick et al., 2010; McLeod, 2025; Montag et al., 2020). What survived is the *span* — from viscerogenic to meaning — and the reality of priority capture: acute deficits and threat cues do seize the motivational system, situationally rather than structurally (Kenrick et al., 2010). Design consequence: domains without a ladder; prioritization as a dynamic mechanism node with deficit, situational, and life-stage gated inputs.

### 4.2 The dual process is real

Need frustration predicts ill-being, defensive functioning, and compensatory substitutes beyond what low satisfaction predicts; satisfaction predicts flourishing beyond what low frustration predicts (Vansteenkiste & Ryan, 2013\*; Vansteenkiste et al., 2020\*) — the modern, general form of Herzberg's two-factor asymmetry (Herzberg et al., 1959\*). Design consequence: two channel nodes with four signed outcome edges of asymmetric weight — the geometry Figure F3(A) displays.

### 4.3 Need strength is dispositional and neurally consequential

Individuals differ reliably in need intensity; the differences are acquired over development, covary with personality traits and primary emotional systems (McClelland, 1961\*; Montag et al., 2020), and carry a neural signature: reward–need fit amplifies reward-circuit response (Rybnicek et al., 2019). Design consequence: a need-strength mechanism fed from the personality interface, modulating prioritization and motivational output.

### 4.4 What follows for design

Jointly the verdicts impose six requirements: (1) a small convergent domain core spanning existence through meaning; (2) no fixed ladder — prioritization as a gated dynamic mechanism; (3) dual satisfaction/frustration channels with asymmetric signed outcome edges; (4) environmental support and thwart as distinct transactional inputs; (5) dispositional need strength as a mechanism coupled to personality; and (6) explicit interfaces — needs feed goals (motivation stratum), frustration feeds risk (disorder stratum), contexts feed support (systems stratum). No single theory satisfies all six; their union does.

---

## 5. Extraction: The Universal Needs Framework

### 5.1 Method of extraction

As in the preceding articles, we triangulated the field's own meta-theory (Sohrabi et al., 2021), its comparative and handbook treatments (Osemeke & Adegboyega, 2017; Szalma, 2020), the primary statements of each family (Section 3), and the adjudicating empirical literatures (Section 4). A principle was admitted if (a) it is asserted or presupposed by at least three theory families, and (b) it has empirical support independent of any single family's paradigm. Seven principles survived.

### 5.2 The seven principles

**Table 2.** *The seven universal needs principles: ancestry, evidence, and graph translation.*

| # | Principle | Statement | Principal ancestry | Independent evidence | Graph translation |
|---|---|---|---|---|---|
| 1 | Necessity criterion | Needs are necessities: thwarting produces dysfunction, not mere disappointment | SDT; Dweck | Deprivation and thwarting effects (Ryan & Deci, 2000; Vansteenkiste et al., 2020\*) | Admission rule for domain nodes; frustration channel |
| 2 | Convergent core | Beneath 29 theories lies a small recurring domain set: existence, safety, relatedness, esteem/status, competence, autonomy, meaning/growth | All families (Figure F2) | Meta-theoretical recurrence (Sohrabi et al., 2021) | Seven level-1 domain nodes with facet subgraphs |
| 3 | Dynamic prioritization | Priority is computed from deficit, situational cues, and life stage — not read off a ladder | Kenrick; Maslow (softened); Alderfer | Situational-trigger and hierarchy-failure evidence (Kenrick et al., 2010; Montag et al., 2020) | Prioritization mechanism node with gated inputs |
| 4 | Dual channels | Satisfaction and frustration are distinct processes with asymmetric outcomes | Herzberg; SDT | Dual-process studies (Vansteenkiste & Ryan, 2013\*) | SAT and FRU nodes; four signed outcome edges |
| 5 | Contextual dependence | Environments support or thwart needs through distinct paths | Murray (press); SDT | Need-support intervention and survey evidence (Ryan & Deci, 2000; Skues et al., 2025) | Transactional edges from the systems interface |
| 6 | Dispositional strength | Individuals differ in acquired need intensity, with reward-fit consequences | Murray; McClelland | Trait covariation and fMRI reward-fit (Montag et al., 2020; Rybnicek et al., 2019) | Need-strength mechanism fed by the personality interface |
| 7 | Needs energize goals | Needs are the input layer of motivation: they convert states into goal pressure | Murray; Lewin; SDT; Dörner | Motivation and problem-solving literatures (Güss et al., 2017; Szalma, 2020) | Cascade edges into the motivation-stratum interface |

The principles are intersection constraints, not a thirtieth theory. Principle 4 deserves emphasis: it is this stratum's manifestation of the series' signed-superposition axiom, and it is what makes need frustration a *distinct causal channel* into the disorder stratum rather than a low score on a wellbeing scale.

---

## 6. The Universal Needs Graph

### 6.1 Formal definition

Let $V$ be the node set published in the accompanying data files: a superordinate needs node $N$; seven domain nodes — physiological/existence, safety/self-protection, relatedness/belonging, esteem/status, competence, autonomy, meaning/growth — with fifteen facet subnodes; satisfaction and frustration channel nodes; three mechanism nodes (dynamic prioritization, need strength, substitution/compensation); and five interface nodes (environmental supports/thwarts, wellbeing, ill-being/defensiveness, motivation/goal layer, personality layer). Let $W(t) \in \mathbb{R}^{|V| \times |V|}$ be a signed weighted adjacency matrix inheriting the series' gating formalism, $w_{ij}(t) = g_{ij}(t)\,\bar{w}_{ij}$, with gates here carrying *situational triggers* and *life-stage* windows in addition to developmental time — the UNeedG's extension of the gate concept from slow developmental clocks to fast contextual ones. The UNeedG is $G(t) = (V, W(t))$; Figure F1 displays it at domain/channel resolution, and every edge carries weight, sign, type, gate class, evidential basis, and primary sources in the data files.

![**Figure F1.** The Universal Needs Graph: seven domains, dual channels, and priority dynamics. Edge thickness is proportional to provisional consensus weight; diamonds mark gated edges; green and red nodes are the satisfaction and frustration channels; grey nodes are interfaces.](../figures/figF1_universal_needs_graph.png)

### 6.2 Axiom compliance

*Axiom 1* (universal connectivity): every domain reaches every outcome through the channels and mechanisms. *Axiom 2* (non-dismissibility): no domain may be deleted in formulating a person — dropping existence needs idealizes the person, dropping meaning truncates the span the tradition spent a century establishing (Maslow, 1943\*; Tønnesvang, 2025). *Axiom 3* (mediated and unmediated influence): relatedness affects wellbeing directly through satisfaction and indirectly through prioritization and goal pursuit — all routes are edges. *Axiom 4* (self-influence): the satisfaction and frustration channels carry self-loops — fulfillment builds the skills and bonds that fulfill further; frustration self-perpetuates through defensive preoccupation (Ryan & Deci, 2000; Vansteenkiste & Ryan, 2013\*). *Axiom 5* (signed superposition): the four channel→outcome edges carry the dual-process asymmetry as signs and weights — satisfaction's negative edge into ill-being is weaker than frustration's positive one, so a person can be simultaneously flourishing and at risk, which is precisely what the dual-process data show (Vansteenkiste et al., 2020\*).

### 6.3 Subgraphs and encapsulation

Each domain owns an encapsulated facet subgraph: homeostatic regulation and rest under existence; physical safety and predictability — Dweck's (2017)\* contribution — under safety; attachment, affiliation, and the life-stage-gated mating/care line — Kenrick et al.'s (2010) contribution — under relatedness; status/prestige and self-esteem under esteem; mastery and achievement striving under competence; volition and self-congruence under autonomy; purpose/coherence and growth under meaning. The subgraphs absorb the tradition's live disputes without destabilizing the domain level: whether self-actualization is an apex, a status display, or a meaning facet is a subgraph question; whether meaning is basic is a domain-membership question the falsifiability program addresses; the channels and mechanisms are indifferent to both.

### 6.4 The two dynamics: dual channels and dynamic prepotency

Figure F3 renders the stratum's two signature dynamics. Panel A displays the dual-channel asymmetry: four outcome edges whose signs and relative weights encode that frustration is not merely low satisfaction — the general form of a finding the tradition discovered twice, once in workplaces (Herzberg et al., 1959\*) and once in basic-needs research (Vansteenkiste & Ryan, 2013\*). Panel B displays dynamic prepotency: need salience as a time-varying priority weight computed from internal deficit cycles, situational triggers, and life-stage gates (Kenrick et al., 2010) — the pyramid's replacement. Both dynamics are edge-level claims: each curve in the figure corresponds to identified, weighted, testable edges in the data files.

![**Figure F3.** The two dynamics the UNeedG carries as edges. (A) Dual-channel asymmetry (after Vansteenkiste & Ryan, 2013; Herzberg et al., 1959). (B) Dynamic prepotency: salience from deficit plus situational triggers — no fixed ladder (after Kenrick et al., 2010). Illustrative shapes, not fitted functions.](../figures/figF3_dual_channel_and_prepotency.png)

### 6.5 Coupling to the other strata

The UNeedG's interfaces define the stratum's systemic role. *Inward from systems* (Batch H): environments enter as need supports and need thwarts on distinct transactional edges — the graph-level home of everything from autonomy-supportive teaching (Skues et al., 2025) to the macro-level deprivations the systems stratum will carry. *Outward to motivation* (Batch G): the satisfaction channel, frustration channel, prioritization mechanism, and strength mechanism all project into the motivation/goal interface — needs are, formally, the input layer of the next stratum, which will convert goal pressure into direction, intensity, and emotion (Güss et al., 2017; Szalma, 2020). *Toward psychopathology*: the frustration channel and substitution mechanism feed the ill-being interface, giving the UDG a second person-specific prior alongside temperament's — chronic need frustration as a documented pathway into defensive and disordered functioning (Vansteenkiste & Ryan, 2013\*). *From personality*: the UPerG's traits and the acquired-needs tradition jointly set dispositional strengths (McClelland, 1961\*; Montag et al., 2020). *Through development*: the life-stage gates are UDevG objects, and the acquired-over-development gate on need strength is precisely the internalization mechanism the developmental stratum formalized. *For therapy*: the UTG's formulation node gains a needs checklist with teeth — assessing which needs are frustrated, by which contexts, under which priorities, is a computable sub-task of case formulation.

### 6.6 What the UNeedG adds

Against the twenty-nine-theory museum, it replaces membership disputes with a computable object in which each family survives as the component it got right: Murray as the construct and its strength, Maslow as the span, Alderfer as substitution, Herzberg as the two-factor asymmetry, McClelland as dispositional strength with neural validation, SDT as the necessity criterion and dual process, the evolutionary renovation as the gating dynamics, and the contemporary extensions as criteria discipline and the meaning domain. Against the pyramid — the tradition's most famous artifact — it substitutes a mechanism that actually computes: priority as a gated function rather than a stacked diagram. And against all of them it adds what no needs theory currently possesses: formal continuity with temperament, personality, development, disorder, and treatment strata under shared axioms, making need frustration a traceable path through a person-model rather than a freestanding literature.

### 6.7 Falsifiability, validation pathway, and limitations

The UNeedG makes refutable commitments. *Membership*: each domain node predicts SDT-grade necessity effects — deprivation dysfunction, satisfaction benefit — and any domain failing both tests in adequately powered designs must be demoted from the core (meaning is the flagged candidate; predictability the flagged promotion). *Channel*: the dual-process asymmetry predicts that frustration measures retain incremental prediction of ill-being controlling for satisfaction, and vice versa for wellbeing; collapse into one bipolar factor would falsify the channel architecture. *Priority*: the prepotency gates predict situational capture — threat and deficit cues reorder goal salience measurably and reversibly — and predict life-stage differences in motive salience of the form the evolutionary renovation specifies (Kenrick et al., 2010). *Fit*: the strength mechanism predicts reward–need fit effects behaviorally and neurally, already supported in fMRI (Rybnicek et al., 2019) and extensible to preregistered designs. Validation should proceed from reanalysis of existing multi-domain satisfaction/frustration datasets, through ecological momentary designs of the kind the library already contains (Dunton et al., 2023), to experimental gate tests.

Four limitations bound the contribution. First, the published weights are consensus priors, and the two dynamics figures are illustrative shapes — the channel asymmetry and prepotency curves await estimation. Second, the domain core is a judgment call over a heterogeneous literature: the meta-theory documents twenty-nine theories, and our seven domains compress them with losses the subgraphs only partially recover (Sohrabi et al., 2021). Third, the evidence base over-represents WEIRD samples, workplaces, and student populations; universality-of-kind versus variability-of-expression remains an open empirical program (Ryan & Deci, 2000). Fourth, physiological needs enter as a domain but their regulatory detail belongs to physiology, not psychology; the node is an interface, and the stratum makes no metabolic claims.

---

## 7. Conclusion

Needs theories began by cataloging what people pursue and matured by discovering what people cannot do without. This article extracted the maturation as seven principles: necessity as the admission rule, a convergent domain core, priority as computation rather than architecture, satisfaction and frustration as distinct channels, environments as supports and thwarts, need strength as acquired disposition, and needs as the input layer of motivation. The Universal Needs Graph formalizes all seven — a signed, gated network in which the pyramid becomes a mechanism, the two-factor insight becomes edge geometry, and a century of catalogs becomes a published, revisable object coupled to every other stratum of the Unified Person Graph. What you need, in this model, is no longer a diagram on a classroom wall: it is the pressure term of a person-level dynamical system — and the next article's task is to show how that pressure becomes wanting, feeling, and doing.

---

## References

*Sources marked with an asterisk (\*) were located by the authors through supplementary literature searches beyond the assembled source library.*

Alderfer, C. P. (1969). An empirical test of a new theory of human needs. *Organizational Behavior and Human Performance, 4*(2), 142–175. https://doi.org/10.1016/0030-5073(69)90004-X \*

Baptista, J. A. de A., Formigoni, A., da Silva, S. A., Stettiner, C. F., & de Novais, R. A. B. (2021). Analysis of the theory of acquired needs from McClelland as a means of work satisfaction. *Timor Leste Journal of Business and Management, 3*(2), 54–59.

Baumeister, R. F., & Leary, M. R. (1995). The need to belong: Desire for interpersonal attachments as a fundamental human motivation. *Psychological Bulletin, 117*(3), 497–529. https://doi.org/10.1037/0033-2909.117.3.497 \*

Dunton, G. F., Do, B., Crosley-Lyons, R., Naya, C. H., Hewus, M., & Kanning, M. (2023). Assessing basic and higher-level psychological needs satisfied through physical activity. *Frontiers in Psychology, 14*, Article 1023556. https://doi.org/10.3389/fpsyg.2023.1023556

Dweck, C. S. (2017). From needs to goals and representations: Foundations for a unified theory of motivation, personality, and development. *Psychological Review, 124*(6), 689–719. https://doi.org/10.1037/rev0000082 \*

Güss, C. D., Burger, M. L., & Dörner, D. (2017). The role of motivation in complex problem solving. *Frontiers in Psychology, 8*, Article 851. https://doi.org/10.3389/fpsyg.2017.00851

Herzberg, F., Mausner, B., & Snyderman, B. B. (1959). *The motivation to work*. Wiley. \*

Kenrick, D. T., Griskevicius, V., Neuberg, S. L., & Schaller, M. (2010). Renovating the pyramid of needs: Contemporary extensions built upon ancient foundations. *Perspectives on Psychological Science, 5*(3), 292–314. https://doi.org/10.1177/1745691610369469

Maslow, A. H. (1943). A theory of human motivation. *Psychological Review, 50*(4), 370–396. https://doi.org/10.1037/h0054346 \*

McClelland, D. C. (1961). *The achieving society*. Van Nostrand. \*

McLeod, S. (2025, March 14). *Maslow's hierarchy of needs*. Simply Psychology. https://www.simplypsychology.org/maslow.html

Montag, C., Sindermann, C., Lester, D., & Davis, K. L. (2020). Linking individual differences in satisfaction with each of Maslow's needs to the Big Five personality traits and Panksepp's primary emotional systems. *Heliyon, 6*(7), Article e04325. https://doi.org/10.1016/j.heliyon.2020.e04325

Murray, H. A. (1938). *Explorations in personality*. Oxford University Press. \*

Osemeke, M., & Adegboyega, S. (2017). Critical review and comparism between Maslow, Herzberg and McClelland's theory of needs. *FUNAI Journal of Accounting, Business and Finance, 1*(1), 161–173.

Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist, 55*(1), 68–78. https://doi.org/10.1037/0003-066X.55.1.68

Rybnicek, R., Bergner, S., & Gutschelhofer, A. (2019). How individual needs influence motivation effects: A neuroscientific study on McClelland's need theory. *Review of Managerial Science, 13*(2), 443–482. https://doi.org/10.1007/s11846-017-0252-1

Siok, T. H., Sim, M. S., & Rahmat, N. H. (2023). Motivation to learn online: An analysis from McClelland's theory of needs. *International Journal of Academic Research in Business and Social Sciences, 13*(3). https://doi.org/10.6007/IJARBSS/v13-i3/16471

Skues, J., Freeman, E., & Allen, K.-A. (2025). Basic psychological needs and achievement emotions: The role of control and value appraisals in higher education. *Australian Journal of Psychology, 77*(1), Article 2500937. https://doi.org/10.1080/00049530.2025.2500937

Sohrabi, B., Yazdani, H., Rajabzadeh, A., & Mahjoub, H. (2021). Analysis of the human basic psychological needs' theories: A meta-theory approach. *Journal of Psychological Science, 20*(103), 979–998. https://doi.org/10.52547/JPS.20.103.979

Szalma, J. L. (2020). Basic needs, goals and motivation. In P. J. Corr & G. Matthews (Eds.), *The Cambridge handbook of personality psychology* (2nd ed., pp. 330–338). Cambridge University Press. https://doi.org/10.1017/9781108264822.030

Tønnesvang, J. (2025). Meaning and psychological needs. *Journal of Theoretical and Philosophical Psychology, 45*(3), 316–332. https://doi.org/10.1037/teo0000269

Vansteenkiste, M., & Ryan, R. M. (2013). On psychological growth and vulnerability: Basic psychological need satisfaction and need frustration as a unifying principle. *Journal of Psychotherapy Integration, 23*(3), 263–280. https://doi.org/10.1037/a0032359 \*

Vansteenkiste, M., Ryan, R. M., & Soenens, B. (2020). Basic psychological need theory: Advancements, critical themes, and future directions. *Motivation and Emotion, 44*(1), 1–31. https://doi.org/10.1007/s11031-019-09818-1 \*

Ward, D., & Lasen, M. (2009). *An overview of needs theories behind consumerism* (MPRA Paper No. 13090). Munich Personal RePEc Archive. https://mpra.ub.uni-muenchen.de/13090/
