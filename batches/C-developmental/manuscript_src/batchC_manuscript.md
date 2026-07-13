# How History Becomes Structure: A Critical Synthesis of Developmental Theories and the Derivation of a Universal Developmental Graph

**[Author 1 name], [Author 2 name]**

[Affiliations]

**Author note.** Correspondence concerning this article should be addressed to [corresponding author]. The graph data files and figure-generation code are openly available in the article's supplementary repository. This article is the third in a planned series deriving the Unified Person Graph (UPG), an eight-dimensional network model of psychological functioning. The first article derived the Universal Disorder Graph (psychopathology); the second derived the Universal Therapy Graph (treatment).

---

## Abstract

Developmental psychology owns the variable every other psychological subdiscipline holds constant: time. Yet its grand theories — maturational, psychoanalytic, constructivist, sociocultural, learning-theoretic, ethological, ecological, and lifespan — remain a museum of partially incompatible frameworks, each documented, each incomplete, and none formally composable with models of psychopathology, personality, or treatment. This article provides a critical synthesis of the major developmental theories and theorists, their philosophies, logics, applications, strengths, and documented weaknesses. From the synthesis we extract eight principles on which the traditions converge despite their vocabularies: transaction, cascade, plasticity under constraint, sensitive-period gating, domain interdependence, stage-like reorganization, internalization, and equifinality/multifinality. We then formalize these as the **Universal Developmental Graph (UDevG)**: a weighted, signed graph whose nodes are developmental domains and mechanisms, whose directed cascade and reciprocal transactional edges carry the traditions' documented cross-domain effects, and whose defining formal innovation is the *time-gated weight* — edge strengths written as functions of developmental time, $w_{ij}(t) = g_{ij}(t)\,\bar{w}_{ij}$, giving sensitive periods exact representation. The UDevG satisfies the same five axioms as the previous strata of the Unified Person Graph and plays a distinctive role within it: development is modeled not merely as another stratum but as the process by which the person's other graphs acquire their weights — how history becomes structure. Falsification conditions, a validation pathway, and limitations are specified.

**Keywords:** developmental psychology, developmental theory, sensitive periods, developmental cascades, transactional model, network model, graph theory, lifespan development

---

## 1. Introduction

Every psychological fact about a person is a fact about a moment in a trajectory. The anxious adult was an inhibited toddler in a particular caregiving ecology; the therapy client's "presenting problem" is the current state of loops assembled over decades; even the stable traits of personality psychology are stabilities *of* something that had to develop. Developmental psychology is the discipline that studies this assembly directly (Berk, 2018; Crain, 2014). It is therefore, for an integrated model of the person, not one source among eight but the source of the other seven's parameters — a claim we make precise in Section 6.

The difficulty is that developmental psychology's theoretical inheritance is famously plural. Its history reads as a sequence of partially victorious rebellions: nativist maturationism against environmentalism; behaviorist learning theory against both; Piagetian constructivism against behaviorism; Vygotskian socioculturalism against Piaget's solitary child; ethology and attachment theory against drive theory; ecological and lifespan frameworks against everything child-centered and context-free; dynamic systems theory against stages themselves (Crain, 2014). Each rebellion documented real phenomena; none produced a framework the others could be reduced to. Textbook syntheses handle this pluralism by juxtaposition — a chapter per theory — which serves teaching but not model-building (Berk, 2018; Crain, 2014).

This article, the third in the Unified Person Graph (UPG) series, treats the pluralism as the first two articles treated the classification wars and the therapy school wars: as a representation problem. We ask what the traditions *jointly require* of any formal model of development, extract the requirements as principles, and satisfy them with a graph — continuous in formalism and axioms with the Universal Disorder Graph (UDG) and Universal Therapy Graph (UTG) already derived. The reviews' method matches the earlier articles: for each theory family, its philosophy, logic, applications, strengths, and documented weaknesses, drawing on the canonical comparative sources (Berk, 2018; Crain, 2014) and the primary literature, with sources located beyond the assembled library marked by an asterisk in the reference list.

---

## 2. Developmental Psychology in Brief

Developmental psychology studies systematic change and stability in human functioning from conception to death (Berk, 2018). Three of its structural commitments matter for everything that follows. First, *description and explanation diverge*: charting what changes (norms, milestones, trajectories) is separable from explaining why (mechanisms), and the field's theories disagree far more about the second than the first (Crain, 2014). Second, the field's oldest dichotomies — nature versus nurture, continuity versus stages, universal versus context-specific — have all dissolved into interactionist positions in the contemporary literature: development is now near-universally understood as the joint, probabilistic product of genetic activity, neural activity, behavior, and environment in bidirectional traffic (Gottlieb, 2007\*; Sameroff, 2010\*). Third, the lifespan reorientation established that development is lifelong, multidirectional, multidimensional, plastic at every age though declining in efficiency, and embedded in history and culture (Baltes, 1987\*). Any universal representation must therefore span the whole lifespan, encode bidirectionality natively, and treat plasticity as a quantitative parameter rather than a slogan — three requirements the graph of Section 6 satisfies by construction.

---

## 3. The Theories: A Critical Tour

Table 1 compresses the comparative analysis of the eight theory families that structure the field's history (Berk, 2018; Crain, 2014). The narrative highlights what each family contributes to the extraction of Section 5 and where its documented weaknesses lie.

**Table 1.** *Major developmental theory families: logic, contributions, and documented weaknesses.*

| Family | Exemplary figures | Core logic of development | Chief contribution to the universal architecture | Chief documented weaknesses |
|---|---|---|---|---|
| Maturational / ethological | Gesell; Lorenz; Bowlby | Genetically guided unfolding; evolved behavioral systems expecting species-typical environments | Canalization; sensitive periods; attachment as an evolved regulatory system | Underestimates environmental variation and reversibility; early critical-period claims overstated |
| Psychoanalytic / psychosocial | Freud; Erikson | Personality forged in a staged series of conflicts between inner demands and social requirements | Early experience carried forward as structure; psychosocial epochs spanning the whole lifespan (Erikson) | Core constructs resist measurement; retrospective method; weak falsifiability |
| Learning-theoretic | Pavlov; Watson; Skinner; Bandura | Development as cumulative conditioning, reinforcement history, and observational learning | The precise mechanics of experience-driven change; modeling; self-efficacy | Underplays maturation, stages, and the child's own construction; molecular rather than architectural |
| Constructivist | Piaget; Kohlberg | The child actively constructs successive logical structures through assimilation and accommodation | Stage-like reorganization; invariant sequence; readiness | Underestimated early competence; stages less unitary and more domain-specific than claimed; culture underweighted |
| Sociocultural | Vygotsky | Higher mental functions originate socially and are internalized through interaction within the zone of proximal development | Internalization; scaffolding; culture and tools as constitutive of mind | Mechanism and timing left vague; biology underplayed; constructs hard to operationalize |
| Ecological | Bronfenbrenner | Development is a joint function of proximal processes unfolding within nested contextual systems over time | Multilevel context; the micro-to-macro taxonomy; the interface to the Systems stratum | More framework than theory; nearly untestable as a whole; process claims thin |
| Lifespan | Baltes | Development is lifelong, multidirectional, a gain–loss dynamic, plastic, and historically embedded | Whole-lifespan scope; plasticity as a quantitative parameter; selective optimization with compensation | Propositional rather than mechanistic; few uniquely falsifiable predictions |
| Dynamic systems / transactional | Thelen & Smith; Sameroff; Gottlieb | Development self-organizes in real time from interactions among components; person and environment continuously remake each other | Transaction; probabilistic epigenesis; the formal warrant for time-varying coupling | Abstract; data-hungry; sometimes redescribes phenomena rather than predicting them |

### 3.1 Maturational and ethological theories

The maturational tradition begins with Gesell's normative program: development as the orderly unfolding of a genetic ground plan, with environment supporting but not structuring the sequence (Crain, 2014; Gesell, 1933\*). Its methodological legacy — norms, milestones, developmental quotients — remains the backbone of pediatric surveillance, and its core concept, *maturation as an internally timed sequence*, survives in modern form as canalization: the buffering of species-typical development against a wide band of environmental perturbation (Gottlieb, 2007\*). The philosophy is nativist and the logic is temporal: readiness precedes teachability, so intervention against the internal timetable is wasted or harmful. The documented weakness is symmetric — the tradition systematically underestimated how much environmental variation matters within the canalized band, and its normative samples were narrow (Crain, 2014).

Ethology gave the maturational insight an evolutionary engine. Lorenz's (1935)\* imprinting demonstrated that some learning is possible only inside a bounded developmental window, seeding the critical-period concept, and Bowlby (1969)\* imported the logic into human development: attachment is an evolved behavioral system, expecting a species-typical caregiving environment, whose early output — the *internal working model* — is carried forward as relational structure. Ainsworth's Strange Situation converted the theory into a measurement paradigm and a taxonomy of security (Ainsworth et al., 1978\*). Applications run from hospital visitation policy to attachment-informed psychotherapy. Two corrections are now documented. First, human "critical" periods are almost everywhere *sensitive* periods — windows of heightened, not exclusive, plasticity: even after severe early deprivation, substantial recovery follows environmental enrichment, though with dose- and timing-dependent limits (Nelson et al., 2007\*; Knudsen, 2004\*). Second, attachment distributions vary meaningfully across cultures, complicating universalist readings of the classifications (van IJzendoorn & Kroonenberg, 1988\*). Both corrections are constraints the universal graph must carry: plasticity is real, bounded, and time-varying.

### 3.2 Psychoanalytic and psychosocial theories

Freud's developmental claim — that personality is forged early, in a staged series of conflicts between internal demands and social requirements, and that the residue of each stage is carried forward as structure (Freud, 1905/1953\*) — is, stripped of its specific psychosexual content, the founding statement of the field's most durable idea: *early experience becomes later architecture*. Erikson (1950)\* generalized the logic in two directions the universal model retains: the conflicts became psychosocial rather than psychosexual, and the timetable was extended across the entire lifespan, with each epoch posing a characteristic crisis (trust, autonomy, initiative, industry, identity, intimacy, generativity, integrity) whose resolution parameterizes the next. Applications persist in identity research, life review in gerontology, and the clinical reflex of taking a developmental history at intake. The documented weaknesses are the classical ones: core constructs that resist operationalization, a retrospective evidence base, and predictions too elastic to falsify cleanly (Crain, 2014). The extraction of Section 5 therefore keeps the tradition's *form* — staged epochs whose outcomes feed forward — while requiring that content enter the graph only where measurable.

### 3.3 Learning-theoretic approaches

The learning tradition — Pavlov's (1927)\* conditioned reflexes, Watson's (1913)\* environmentalist manifesto, Skinner's (1953)\* operant analysis, and Bandura's (1977)\* social-cognitive expansion — treats development as cumulative experience-driven change: conditioning histories, reinforcement schedules, observational learning, and, in Bandura's mature statement, self-efficacy beliefs regulating what is attempted at all. Its philosophy is empiricist, its logic mechanistic, and its applied yield unmatched in precision: behavior modification, parent-management training, and token economies are direct exports (Crain, 2014). Its contribution to the universal architecture is exactly that precision — learning is the field's best-specified *mechanism of weight change*, the process by which experience adjusts the strength of connections. Its documented weakness is architectural: it supplies no account of maturational constraint, stage-like reorganization, or the child's own construction, treating the organism's structure as a dependent variable only (Berk, 2018; Crain, 2014). In graph terms: learning theory describes how edges are re-weighted but not which edges exist or when they are open to change.

### 3.4 Constructivist theories

Piaget's (1970)\* theory remains the field's most ambitious single structure: the child actively constructs successive logics — sensorimotor, preoperational, concrete operational, formal operational — through assimilation, accommodation, and equilibration, with each stage an integrated whole and the sequence invariant though its timing varies. Kohlberg (1969)\* extended the constructivist logic to moral judgment. The tradition's applications transformed education: readiness, discovery learning, and developmentally appropriate practice are its vocabulary (Crain, 2014). Three corrections are documented. Infant research revealed far earlier competence than the theory allowed; the stages proved less unitary than claimed — performance is domain- and content-sensitive (horizontal décalage generalized); and culture and schooling shape attainment, with formal operations not universally reached (Berk, 2018; Crain, 2014). Kohlberg inherited parallel critiques on judgment-action gaps and cultural breadth. What survives review, and enters the extraction, is precise: *ordered, qualitative reorganization* — invariant sequence without fixed timetable — and the constructivist mechanism of structure-building through interaction, which the graph will encode as ordered stage-sequence edges whose progression, not whose calendar, is the claim.

### 3.5 Sociocultural theory

Vygotsky's (1978)\* proposal inverts Piaget's solitary constructor: higher mental functions appear first *between* people and only then *within* the child, transferred across the social-to-individual boundary through interaction in the zone of proximal development. Language is the master tool; private speech is thought under construction; culture is not context but constituent. The applied legacy — scaffolding, dynamic assessment, reciprocal teaching, and the broad architecture of collaborative pedagogy — is among the most productive in education (Berk, 2018; Crain, 2014). The documented weaknesses are specification failures: the mechanism and timing of internalization are left vague, biological maturation is underplayed, and core constructs are difficult to operationalize at the precision the rest of the model demands (Crain, 2014). The extraction keeps *internalization* as a distinct mechanism type: a directed transfer of structure from an interpersonal node to an intrapersonal one — an edge whose source lies partly outside the person, which is precisely what makes it the natural interface to the caregiving and systems strata.

### 3.6 Ecological theory

Bronfenbrenner (1979)\* reframed the unit of analysis: development is a joint function of *proximal processes* — progressively more complex reciprocal interactions between the person and the immediate environment — unfolding within nested contextual systems (micro-, meso-, exo-, macro-, chronosystem), each of which moderates the processes below it (Bronfenbrenner & Morris, 2006\*). The framework's fingerprints are on Head Start, two-generation intervention design, and every developmental study that models school, neighborhood, and policy as variables rather than noise (Berk, 2018). Its documented weakness is the mirror of its scope: it is more taxonomy than theory, nearly untestable as a whole, with thin specification of process (Crain, 2014). Its indispensable bequest to the universal architecture is the *interface*: the person-graph must expose named nodes through which contextual systems act — in the present article the caregiving context node; in the full model, the entire Systems stratum of the series (Batch H).

### 3.7 Lifespan theory

Baltes (1987)\* codified the reorientation that dissolved child-centrism: development is lifelong; it is multidirectional (gains and losses co-occur at every age); it is plastic at every age, though plasticity declines in efficiency; it is embedded in history and cohort; and successful aging is managed through selection, optimization, and compensation. The propositions govern modern adult-development and gerontological practice (Berk, 2018). The documented weakness is that they are propositions — orienting commitments rather than a generative mechanism, yielding few uniquely falsifiable predictions (Crain, 2014). For the universal model the bequest is quantitative discipline: plasticity is not a slogan but a *parameter* — in the formalism of Section 6, the magnitude of the time-gated gain g(t), positive at every age, peaked in sensitive periods, declining but never zero.

### 3.8 Dynamic systems and transactional theories

The most recent family supplies the formal warrant for everything the graph does with time. Thelen and Smith (1994)\* demonstrated — first in motor development — that developmental outcomes self-organize in real time from the interaction of components (body, task, context) with no executive program; stages, where they appear, are attractor states, and variability is data rather than noise. Sameroff's (2010)\* transactional model established the field's canonical causal geometry: parent and child continuously remake each other, so unidirectional arrows systematically misestimate effects. Gottlieb's (2007)\* probabilistic epigenesis completed the picture at the biological level: genetic activity, neural activity, behavior, and environment stand in fully bidirectional traffic, making development probabilistic all the way down. The family's documented weaknesses are practical: the accounts are abstract, data-hungry, and sometimes redescribe phenomena rather than predict them (Crain, 2014). But the contribution is foundational — reciprocal, time-varying coupling among components is exactly what a weighted graph with transactional edges and time-gated weights formalizes, which is why this family functions as the mathematical conscience of the extraction rather than one voice among eight.

---

## 4. What the Evidence Settled

Three empirical literatures adjudicate among the theories reviewed above, and their verdicts fix the design requirements for any universal representation.

### 4.1 Stages: reorganization without the grand staircase

The strong Piagetian claim — domain-general structures transforming in lockstep — did not survive; the weaker claim — ordered, qualitative reorganization within domains, with invariant sequence but variable timing and pervasive domain-specificity — did (Berk, 2018; Crain, 2014). The settled position is neither continuous accretion nor a grand staircase but *stage-like reorganization under local constraint*: sequences are real where they are found (sensorimotor progressions, attachment phases, moral-judgment levels), but they are properties of subgraphs, not of the whole child. A universal model must therefore be able to represent ordered sequences *inside* domains without imposing synchrony *across* them.

### 4.2 Sensitive periods: plasticity under constraint

The critical-period concept was tamed rather than discarded. Mechanistic work established that sensitive periods are windows in which experience exerts disproportionate influence on circuit formation, opened and closed by identifiable neurobiological processes, domain-specific in their timing (Knudsen, 2004\*; Werker & Hensch, 2015\*). The Bucharest Early Intervention Project supplied the decisive human evidence: children removed from institutional deprivation showed substantial cognitive recovery, but recovery was graded by the age of placement — plasticity real, timing consequential (Nelson et al., 2007\*). The design requirement is exact: the *strength* of an environmental influence on a developmental outcome must be representable as a function of developmental time — not as a constant, and not as a binary window.

### 4.3 Cascades, equifinality, and multifinality

Longitudinal developmental science converged on the cascade as its central causal object: effects spreading across domains and epochs, as when early emotion-regulation difficulty feeds coercive family cycles, which feed school-entry conduct problems, which feed academic failure and peer rejection, which feed adolescent internalizing (Masten & Cicchetti, 2010\*). Cascades explain why small early differences can compound and why intervention timing matters as much as intervention content. The same literature established the field's twin identifiability results: *equifinality* — different starting points and paths arriving at the same outcome — and *multifinality* — the same starting point diverging to different outcomes depending on the subsequent path (Cicchetti & Rogosch, 1996\*). Any model that maps outcomes to single causes is therefore wrong in form, not merely in detail: the object of study is the path, not the origin.

### 4.4 What follows for design

Jointly, the verdicts impose six requirements. A universal developmental representation must (1) span the lifespan, (2) natively encode bidirectional person–environment traffic, (3) let influence strengths vary with developmental time, (4) represent ordered within-domain sequences without cross-domain synchrony, (5) carry cross-domain, cross-epoch cascade paths as first-class objects, and (6) make equifinality and multifinality structurally possible rather than anomalous. No theory family satisfies all six; Section 5 shows that their union, expressed as principles, does — and Section 6 shows that a signed weighted graph with time-gated edges satisfies all six by construction.

---

## 5. Extraction: The Universal Developmental Framework

### 5.1 Method of extraction

As in the preceding articles of the series, we extracted the shared architecture by triangulating the comparative theoretical literature (Berk, 2018; Crain, 2014) against the primary statements of each family (Section 3) and the adjudicating empirical literatures (Section 4). A principle was admitted as universal if (a) it is asserted or presupposed, under whatever local vocabulary, by at least three of the eight theory families, and (b) it has empirical support independent of any single family's paradigm. Eight principles survived both filters. Their translation into graph primitives is given with each.

### 5.2 The eight principles

**Table 2.** *The eight universal developmental principles: ancestry, evidence, and graph translation.*

| # | Principle | Statement | Principal ancestry | Independent evidence | Graph translation |
|---|---|---|---|---|---|
| 1 | Transaction | Person and environment continuously and reciprocally remake each other | Sameroff; Gottlieb; Bowlby | Longitudinal cross-lagged designs (Sameroff, 2010\*) | Reciprocal (paired directed) edges between person and context nodes |
| 2 | Cascade | Effects propagate across domains and epochs, compounding along paths | Masten & Cicchetti; learning theory | Multi-decade cohort studies (Masten & Cicchetti, 2010\*) | Directed cross-domain edges; dated paths through the graph |
| 3 | Plasticity under constraint | Change is possible at every age, with efficiency that varies by age and domain | Baltes; ethology; Nelson | Deprivation-recovery studies (Nelson et al., 2007\*) | Time-gated gain g(t) > 0 for all t, non-uniform |
| 4 | Sensitive-period gating | Influence strengths are time-dependent, peaking in domain-specific windows | Lorenz; Bowlby; Knudsen | Circuit-level and adoption-timing evidence (Knudsen, 2004\*; Werker & Hensch, 2015\*) | Edge weights as functions of time: w(t) = g(t)·w̄ |
| 5 | Domain interdependence | Physical, cognitive, linguistic, emotional, social, moral, and self development feed one another | All families; explicit in Berk | Cross-domain longitudinal effects (Berk, 2018) | The cross-domain edge set itself (Axioms 1–3) |
| 6 | Stage-like reorganization | Within domains, development passes through ordered qualitative reorganizations with invariant sequence but variable timing | Piaget; Kohlberg; Erikson; Bowlby | Sequence (not timetable) replications (Crain, 2014) | Ordered stage-sequence edges within encapsulated subgraphs |
| 7 | Internalization | Interpersonal structure becomes intrapersonal structure through scaffolded interaction | Vygotsky; Bowlby; Bandura | Scaffolding and observational-learning paradigms (Vygotsky, 1978\*; Bandura, 1977\*) | Directed edges from context nodes to person nodes that *create or re-weight* intra-person edges |
| 8 | Equifinality / multifinality | Many paths to one outcome; many outcomes from one path origin | Cicchetti & Rogosch; dynamic systems | Developmental psychopathology cohorts (Cicchetti & Rogosch, 1996\*) | Multiple directed paths between node pairs; path-dependence of state |

Two remarks prevent misreading. First, the principles are not a ninth theory: they are the *intersection constraints* — what any adequate theory already honors and any formal model must therefore implement. Second, principle 7 is the series' load-bearing wall: internalization is the mechanism by which the developmental stratum writes structure into the person's other strata, and it is what Section 6.4 formalizes as development *setting the weights* of the other graphs.

---

## 6. The Universal Developmental Graph

### 6.1 Formal definition and the time-gated weight

Let $V$ be the node set published in the accompanying data files: a superordinate trajectory node $D$; seven developmental domain nodes (physical/motor, cognitive, language, emotional, social/relational, moral, self/identity); a caregiving-context interface node; five mechanism nodes (maturation, learning, construction, internalization, transaction); and the subgraph nodes of Section 6.3. Let $W(t) \in \mathbb{R}^{|V| \times |V|}$ be a signed weighted adjacency matrix *indexed by developmental time*. The UDevG is

$$G(t) = \big(V,\, W(t)\big), \qquad w_{ij}(t) = g_{ij}(t)\,\bar{w}_{ij},$$

where $\bar{w}_{ij} \in [-1, 1]$ is the edge's base weight and $g_{ij}(t) \in [g_{\min}, 1]$, with $g_{\min} > 0$, is its *gating function* — the formal innovation this stratum contributes to the series. Constant edges take $g \equiv 1$; sensitive-period edges take unimodal gates peaked in their documented windows; the floor $g_{\min} > 0$ *is* lifelong plasticity (principle 3), and the gates' non-uniformity *is* sensitive-period structure (principle 4). Figure C2 displays illustrative gates for four documented cases — caregiving→attachment (infancy-peaked), input→language (early-childhood sensitive period), motor→cognitive exploration (infancy-peaked), and relational feedback→identity (adolescence-peaked).

![**Figure C2.** Sensitive-period gating: edge weights as functions of developmental time, $w_{ij}(t) = g_{ij}(t)\,\bar{w}_{ij}$. Curve shapes are illustrative of the principle, not fitted functions.](../figures/figC2_sensitive_period_gating.png)

The edge typology partitions nonzero entries into five types, each licensed by a principle: **hierarchical** edges (the global trajectory decomposes into domain trajectories), **cascade** edges (directed cross-domain influence: motor→cognitive, cognitive→language, language→social, emotion→social, social→moral, social→self, and their documented companions; principle 2), **transactional** edges (reciprocal person–context pairs around the caregiving node, including the child-evokes-caregiving return edge; principle 1), **autoregressive** self-loops (canalized momentum, skills-beget-skills, self-confirming working models; Axiom 4), and **stage-sequence** edges (ordered within-subgraph progressions; principle 6). Every edge in the data files carries its provisional consensus weight, sign, type, gate class, evidential basis, and primary sources. Figure C1 displays the domain level.

![**Figure C1.** The Universal Developmental Graph: domains, cascades, transactions, and time-gated weights. Edge thickness is proportional to provisional consensus weight; diamonds mark edges whose weight varies with developmental time; the grey node is the interface to the Systems stratum.](../figures/figC1_universal_developmental_graph.png)

### 6.2 Axiom compliance

The five axioms adopted for the series are satisfied as follows. *Axiom 1* (universal connectivity): every domain reaches every other through the cascade set and the hierarchical spine. *Axiom 2* (non-dismissibility): no domain may be deleted from the formulation of a person — the cascade evidence gives this clinical content, since omitted domains are where cascades hide (Masten & Cicchetti, 2010\*). *Axiom 3* (mediated and unmediated influence): motor development affects language both directly (gesture) and through cognitive exploration — both routes are edges. *Axiom 4* (self-influence): the autoregressive loops encode cumulative advantage and the self-perpetuation of working models by selection of confirming experience (Bowlby, 1969\*; Sameroff, 2010\*). *Axiom 5* (signed superposition): concurrent influences on any node sum; adverse and protective inputs carry opposite signs, which is what makes buffering representable. The time-gating extension is upward-compatible: setting all $g \equiv 1$ recovers a static graph of exactly the form the UDG and UTG employ, so the axioms' semantics are unchanged — the developmental stratum merely reveals that the other strata's matrices are time-slices of gated processes.

### 6.3 Subgraphs and encapsulation

Each domain node owns an encapsulated subgraph, communicating with the rest of the graph only through its mother node — the series' standing encapsulation principle. Two subgraphs are published with this article as canonical demonstrations. The *cognitive* subgraph carries the constructivist sequence — sensorimotor → preoperational → concrete operational → formal operational — as maturation-gated stage-sequence edges, with the final edge deliberately weakened to encode non-universal attainment (Piaget, 1970\*; Crain, 2014). The *social/relational* subgraph carries attachment formation → internal working models → peer competence, with working models additionally projecting to the self/identity domain — the graph's rendering of Bowlby's carried structure and its documented cascade into middle childhood (Ainsworth et al., 1978\*; Masten & Cicchetti, 2010\*). Encapsulation is what lets these subgraphs hold school-specific detail (Piagetian stages, attachment phases) without committing the domain level to any school's timetable.

### 6.4 Development as the parameter-setter of the Unified Person Graph

The preceding articles derived a disorder graph (states that can become self-maintaining) and a therapy graph (an organized controller that perturbs states and re-weights edges). The UDevG stands to both in a relation no mere third stratum would: **it is the process model of where their parameters come from.** The adult's disorder-stratum weights — how strongly rumination couples to insomnia *in this person* — are outputs of a developmental path: temperamental starting values transacted with caregiving, gated through sensitive periods, compounded along cascades, consolidated by internalization. Formally, where the other strata are graphs of the person at time $t$, the UDevG is the equation of motion for their weight matrices: history becoming structure. This is also the model's rendering of equifinality and multifinality (principle 8): because outcomes are path-dependent states of a network rather than readouts of origins, different dated paths can converge on the same adult configuration, and identical origins can diverge (Cicchetti & Rogosch, 1996\*). Figure C3 renders a documented cascade family — externalizing-to-internalizing across four epochs — as a dated path in the UDevG: each arrow is a time-stamped, testable prediction, and each is a candidate site for the therapy graph's control input, which is how the timing of intervention acquires formal representation.

![**Figure C3.** A developmental cascade rendered as a dated path in the UDevG (illustrative composite of documented externalizing-to-internalizing cascades; Masten & Cicchetti, 2010\*). Each edge is a time-stamped, testable prediction.](../figures/figC3_cascade_example.png)

### 6.5 What the UDevG adds

Against textbook juxtaposition, the UDevG replaces a chapter-per-theory museum with a single computable object in which each family survives as the component it got right: maturational theory as gates and canalized loops, learning theory as the weight-change mechanism, constructivism as ordered subgraph sequences, socioculturalism as internalization edges, ecology as interface nodes, lifespan theory as the plasticity floor, and dynamic systems as the licence for the whole time-varying construction. Against stage models, it adds cross-domain asynchrony and cascade structure. Against static network models — including this series' own earlier strata — it adds the time-gated weight, without which sensitive periods, cascades, and plasticity decline are representable only as prose. And against all of them it adds machine-readable provenance: every node and edge published with its evidential basis, re-derivable and revisable by any research group.

### 6.6 Falsifiability, validation pathway, and limitations

The UDevG makes refutable commitments. *Structural*: if a developmental domain is shown to develop independently of all others — no incoming or outgoing cross-domain effects in adequately powered longitudinal data — Axioms 1–2 fail for that node; if a major theory family is found whose documented phenomena the edge typology cannot express, the typology must be revised on record. *Temporal*: every gated edge predicts an interaction between input timing and outcome — caregiving quality, language input, and identity-relevant feedback should show age-dependent effect sizes of the shapes their gates assert; flat effect-size-by-age curves falsify the gate. *Path-dependent*: the cascade edges predict that intervening on an upstream node inside its window outperforms the same intervention outside it — a prediction with existing partial support (Nelson et al., 2007\*) and direct policy consequences. Validation should proceed from published-cohort reanalysis (the gates map onto age-moderated cross-lagged effects) to prospective tests of gate shapes in intervention-timing designs.

Four limitations bound the contribution. First, the published weights are consensus priors — rated, sourced, and versioned, not estimated from data — and the gating curves are illustrative shapes, not fitted functions; both are stated as such in the data files and await longitudinal estimation. Second, the domain taxonomy, though standard (Berk, 2018), is one defensible partition among several; the formalism is indifferent to re-partitioning, and the taxonomy is offered as revisable. Third, the extraction privileges the Western developmental literature; cross-cultural work already documents variation in the *content* flowing along the edges and plausibly in gate timing, though the architecture is formulated at a level designed to travel (van IJzendoorn & Kroonenberg, 1988\*). Fourth, biology enters here as gates and canalization rather than as mechanism; genetic and temperamental starting values receive their own stratum later in the series (Batch E), where the UDevG's initial conditions are supplied.

---

## 7. Conclusion

Developmental psychology's theoretical inheritance is not a scandal to be resolved by choosing a winner; it is a division of labor that was never given a common ledger. Each family recorded a real property of human development — timetables, carried early structure, weight change through experience, ordered reorganization, internalization, nested context, lifelong bounded plasticity, transactional self-organization — in a notation the others could not read. This article extracted the eight properties as principles and gave them the common ledger: a signed, weighted, encapsulated graph whose edges carry their strength as functions of developmental time. The Universal Developmental Graph satisfies the series' five axioms, remains continuous with the disorder and therapy strata already derived, and adds the one thing a model of persons cannot do without: an account of how the person's structure got there, and of when it can still be changed. Within the Unified Person Graph it therefore plays a double role — one stratum among eight, and the process by which the other seven acquire their weights. How history becomes structure is no longer a metaphor in this model; it is a matrix-valued function of time, published with its provenance, and offered for correction.

---

## References

*Sources marked with an asterisk (\*) were located by the authors through supplementary literature searches beyond the assembled source library.*

Ainsworth, M. D. S., Blehar, M. C., Waters, E., & Wall, S. (1978). *Patterns of attachment: A psychological study of the Strange Situation*. Erlbaum. \*

Baltes, P. B. (1987). Theoretical propositions of life-span developmental psychology: On the dynamics between growth and decline. *Developmental Psychology, 23*(5), 611–626. https://doi.org/10.1037/0012-1649.23.5.611 \*

Bandura, A. (1977). *Social learning theory*. Prentice-Hall. \*

Berk, L. E. (2018). *Development through the lifespan* (7th ed.). Pearson.

Bowlby, J. (1969). *Attachment and loss: Vol. 1. Attachment*. Basic Books. \*

Bronfenbrenner, U. (1979). *The ecology of human development: Experiments by nature and design*. Harvard University Press. \*

Bronfenbrenner, U., & Morris, P. A. (2006). The bioecological model of human development. In R. M. Lerner & W. Damon (Eds.), *Handbook of child psychology: Vol. 1. Theoretical models of human development* (6th ed., pp. 793–828). Wiley. \*

Cicchetti, D., & Rogosch, F. A. (1996). Equifinality and multifinality in developmental psychopathology. *Development and Psychopathology, 8*(4), 597–600. https://doi.org/10.1017/S0954579400007318 \*

Crain, W. (2014). *Theories of development: Concepts and applications* (6th ed.). Pearson.

Erikson, E. H. (1950). *Childhood and society*. Norton. \*

Freud, S. (1953). Three essays on the theory of sexuality. In J. Strachey (Ed. & Trans.), *The standard edition of the complete psychological works of Sigmund Freud* (Vol. 7, pp. 123–246). Hogarth Press. (Original work published 1905) \*

Gesell, A. (1933). Maturation and the patterning of behavior. In C. Murchison (Ed.), *A handbook of child psychology* (2nd ed., pp. 209–235). Clark University Press. \*

Gottlieb, G. (2007). Probabilistic epigenesis. *Developmental Science, 10*(1), 1–11. https://doi.org/10.1111/j.1467-7687.2007.00556.x \*

Knudsen, E. I. (2004). Sensitive periods in the development of the brain and behavior. *Journal of Cognitive Neuroscience, 16*(8), 1412–1425. https://doi.org/10.1162/0898929042304796 \*

Kohlberg, L. (1969). Stage and sequence: The cognitive-developmental approach to socialization. In D. A. Goslin (Ed.), *Handbook of socialization theory and research* (pp. 347–480). Rand McNally. \*

Lorenz, K. (1935). Der Kumpan in der Umwelt des Vogels [The companion in the bird's world]. *Journal für Ornithologie, 83*, 137–213. https://doi.org/10.1007/BF01905355 \*

Masten, A. S., & Cicchetti, D. (2010). Developmental cascades. *Development and Psychopathology, 22*(3), 491–495. https://doi.org/10.1017/S0954579410000222 \*

Nelson, C. A., III, Zeanah, C. H., Fox, N. A., Marshall, P. J., Smyke, A. T., & Guthrie, D. (2007). Cognitive recovery in socially deprived young children: The Bucharest Early Intervention Project. *Science, 318*(5858), 1937–1940. https://doi.org/10.1126/science.1143921 \*

Pavlov, I. P. (1927). *Conditioned reflexes: An investigation of the physiological activity of the cerebral cortex* (G. V. Anrep, Trans.). Oxford University Press. \*

Piaget, J. (1970). Piaget's theory. In P. H. Mussen (Ed.), *Carmichael's manual of child psychology* (3rd ed., Vol. 1, pp. 703–732). Wiley. \*

Sameroff, A. (2010). A unified theory of development: A dialectic integration of nature and nurture. *Child Development, 81*(1), 6–22. https://doi.org/10.1111/j.1467-8624.2009.01378.x \*

Skinner, B. F. (1953). *Science and human behavior*. Macmillan. \*

Thelen, E., & Smith, L. B. (1994). *A dynamic systems approach to the development of cognition and action*. MIT Press. \*

van IJzendoorn, M. H., & Kroonenberg, P. M. (1988). Cross-cultural patterns of attachment: A meta-analysis of the Strange Situation. *Child Development, 59*(1), 147–156. https://doi.org/10.2307/1130396 \*

Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes* (M. Cole, V. John-Steiner, S. Scribner, & E. Souberman, Eds.). Harvard University Press. \*

Watson, J. B. (1913). Psychology as the behaviorist views it. *Psychological Review, 20*(2), 158–177. https://doi.org/10.1037/h0074428 \*

Werker, J. F., & Hensch, T. K. (2015). Critical periods in speech perception: New directions. *Annual Review of Psychology, 66*, 173–196. https://doi.org/10.1146/annurev-psych-010814-015104 \*
