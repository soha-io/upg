# Wanting and Feeling: A Critical Synthesis of Motivation and Emotion Theories and the Derivation of a Universal Motivation–Emotion Graph

**[Author 1 name], [Author 2 name]**

[Affiliations]

**Author note.** Correspondence concerning this article should be addressed to [corresponding author]. The graph data files and figure-generation code are openly available in the article's supplementary repository. This article is the seventh in a planned series deriving the Unified Person Graph (UPG), an eight-dimensional network model of psychological functioning. The preceding articles derived the Universal Disorder Graph (psychopathology), Universal Therapy Graph (treatment), Universal Developmental Graph (development), Universal Personality Graph (personality), Universal Temperament Graph (temperament), and Universal Needs Graph (needs).

---

## Abstract

The needs stratum left the person under pressure but not yet in motion; motivation and emotion are the stratum that converts pressure into wanting, feeling, and doing. Their literatures have run, for a century, on parallel tracks — drive and incentive on one side, appraisal and affect on the other — and the field's most durable modern insight is that the tracks are one: motivation and emotion are two readouts of a single valuation process. This article critically synthesizes the major theories of motivation and emotion — homeostatic and activation accounts, incentive and reward neuroscience, cognitive-appraisal theories, attributional and expectancy-value models, discrete/basic-emotion and dimensional/constructionist theories, integrative readout theories, and regulation and positive-emotion frameworks — together with their philosophies, logics, applications, and documented weaknesses. We review what the evidence settled: that motivation and emotion co-emerge from one appraisal of reward/punisher value; that "wanting," "liking," and learning are three dissociable components of reward; that appraisal runs on both a fast subcortical route and a slow cognitive route; that discrete and dimensional descriptions are two views of one affective substrate; and that both readouts are regulable. From the synthesis we extract seven principles and formalize them as the **Universal Motivation–Emotion Graph (UMEG)**: a signed, weighted, gated graph whose shared appraisal/valuation core drives two reciprocally coupled readouts — a motivation readout (direction, intensity, persistence) and a componential emotion readout (core affect, discrete emotion, expression, action tendency, feeling) — through approach and avoidance channels, modulated by attribution, incentive salience, reinforcement learning, and regulation, and coupled inward from needs, personality, temperament, and situation and outward to action, psychopathology, and therapy. Within the Unified Person Graph, motivation and emotion constitute the engine that turns need pressure into behavior. Falsification conditions, a validation pathway, and limitations are specified.

**Keywords:** motivation, emotion, appraisal, incentive salience, core affect, reward, emotion regulation, network model, graph theory

---

## 1. Introduction

The preceding stratum ended with a person under pressure. Needs, formalized as the Universal Needs Graph, convert states of the person and world into goal pressure — but pressure is not yet direction, and it is not yet feeling. The question this stratum answers is the one the needs paper deferred: given that the person must obtain certain commodities, *what do they want, how much, and how does it feel?* Motivation supplies the first two answers — the direction and intensity of goal pursuit — and emotion supplies the third — the valenced, aroused, communicable state that accompanies and steers the pursuit (Buck, 1985; Young, 1961).

For most of the twentieth century these two answers were given by two disconnected literatures. Motivation was studied as drive, homeostasis, incentive, and expectancy — a plurality that recent surveys still catalog as a dozen partially overlapping theories, from instinct and arousal accounts to self-determination, expectancy-value, and goal-orientation models (Bandhu et al., 2024); emotion was studied as appraisal, affect program, and feeling; and the textbooks that placed the emotion chapter immediately after the motivation chapter rarely said why (Young, 1961). Turner et al. (2003) documented the cost of the divorce inside a single subfield: the prominent theories of motivation "have mostly ignored emotion," even though emotion turns out to be among the best available indicators of the very goal structures those theories model. The modern correction, arriving from affective neuroscience and integrative theory alike, is radical in its simplicity: motivation and emotion are not two systems to be related but two *readouts* of one system — the brain's valuation of reward and punishment (Berridge, 2018; Buck, 1985; Rolls, 2025).

This article, the seventh in the UPG series, treats the two literatures as the series treats every plurality: as a representation problem whose solution is a graph. We review the families critically (Section 3), review what the evidence settled (Section 4), extract the joint requirements as principles (Section 5), and satisfy them with a single integrated graph continuous in formalism and axioms with the six strata already derived (Section 6). Per the series convention, the review draws on the assembled library, with sources located beyond it — chiefly the canonical emotion theories under-represented in the motivation-weighted library — marked by an asterisk in the reference list.

---

## 2. Motivation and Emotion in Brief

Three commitments organize everything that follows. First, motivation and emotion are *aspects of one process*, not two interacting modules: they share a computational core that evaluates stimuli, relative to the person's needs and goals, as rewarding or punishing, and they diverge only in what is read out of that evaluation — action guidance in the motivational case, state signaling in the emotional case (Buck, 1985; Rolls, 2025). Second, the core is *appraisal*: whether a stimulus matters, and how, is computed rather than given, on routes that range from fast and subcortical to slow and deliberate (Lazarus, 1991; Panksepp, 2011\*; Scherer, 2009\*). Third, the outputs are *plural and componential*: an emotion is not an atom but a bundle — a valence-and-arousal core, a discrete category, an expression, a readiness to act, and a felt quality — and motivation is likewise a bundle of direction, intensity, and persistence (Frijda, 1986\*; Russell, 2003\*; Scherer, 2009\*). The graph of Section 6 carries all three commitments by construction: one core, two readouts, componential subgraphs.

---

## 3. The Theories: A Critical Tour

Table 1 compresses the comparative analysis; Figure G2 maps each theory's constructs onto the components the extraction will formalize. The narrative highlights contributions and documented weaknesses.

**Table 1.** *Major motivation–emotion theory families: logic, contributions, and documented weaknesses.*

| Family | Exemplary figures | Core logic | Chief contribution to the universal architecture | Chief documented weaknesses |
|---|---|---|---|---|
| Drive / homeostatic / activation | Young; Hull; Hebb | Behavior energized by tissue deficits and general arousal seeking equilibrium | Energization and intensity; the motivation–emotion link as a single survey; homeostatic grounding | Cannot explain incentive-driven and anticipatory action; arousal too undifferentiated to specify direction |
| Incentive & reward neuroscience | Berridge; Rolls; Olds | Behavior pulled by anticipated reward/punisher value computed in specific brain systems | "Wanting"/"liking"/learning dissociation; reinforcer value as the common currency; clinical mappings | Animal-model dependence; subjective experience under-specified; valuation detail outruns psychological theory |
| Cognitive appraisal | Lazarus; Scherer; Arnold | Emotion follows from the appraised personal significance (relevance, congruence, coping) of events | Appraisal as the generative core; primary/secondary structure; meaning as cause | Over-cognitive for reflexive affect; appraisal–emotion mapping under-determined; measurement circularity risk |
| Attribution / expectancy–value | Weiner; goal theory | Causal ascriptions (locus, stability, controllability) set expectancy and specific emotions | Cognition→emotion→action loop; expectancy from stability; achievement-emotion catalog | Achievement-domain bias; retrospective self-report; weak for non-attributional affect |
| Discrete / basic emotion | Ekman; Panksepp; Tomkins | A small set of hard-wired, pan-cultural emotion programs with dedicated circuits and signals | Categorical readout; expression and communication; subcortical primary systems | Boundaries and count contested; cultural variation; not all affect is "basic" |
| Dimensional / constructionist | Russell; Barrett | Emotion constructed from a two-dimensional core affect plus categorization and concepts | Core affect (valence × arousal); construction; dimensional continuity | Loss of discrete specificity; construction mechanism still maturing; predictive tests ongoing |
| Integrative readout | Buck (PRIME); Rolls | Motivation and emotion are the readout of hierarchically organized primary systems / reinforcers | The unifying move itself; readout levels (bodily, expressive, subjective); metatheory | Broad and hard to falsify directly; specific predictions must be borrowed from components |
| Regulation & positive emotion | Gross; Fredrickson; Frijda | Emotion is modulable at multiple points; positive affect broadens; emotions are action tendencies | Regulation as a mechanism and therapy lever; broaden-and-build; action readiness | Regulation taxonomy still argued; positive-emotion effects heterogeneous; boundary with coping |

![**Figure G2.** Convergence across motivation–emotion theories: each theory's central constructs mapped onto the six UMEG components (appraisal/valuation, motivation, core affect, discrete emotion, wanting/liking, regulation/expression). Grey cells mark constructs that are derivative, implicit, or absent in the source theory.](../figures/figG2_theory_construct_mapping.png)

### 3.1 The drive and activation origins

The classical survey treated motivation and emotion together because both were read as the dynamics of adaptive behavior: tissue deficits energize, affect colors, and the two are best understood by analyzing a specific emotion's underlying motivational dynamics (Young, 1961). The drive tradition's permanent contribution is *energization* — the intensity dimension of motivation, the fact that behavior has magnitude and not only direction — and its insistence, preserved in every later model, that the organism seeks equilibrium. Its documented failure is equally decisive: pure deficit models cannot explain behavior initiated by external incentives or by the anticipation of homeostatic need before it occurs, and general arousal is too undifferentiated to specify *which* behavior (Buck, 1985). The extraction keeps energization as the intensity facet of the motivation readout and discards undifferentiated drive in favor of appraised value.

### 3.2 Incentive and reward neuroscience

The reward tradition replaced deficit with *value*: behavior is pulled by the anticipated reward or punisher value of stimuli, computed in identifiable brain systems (Rolls, 2025). Its two modern contributions are foundational for this stratum. Rolls (2025) offers an operational definition that cuts the century-old knot — emotions are states elicited by instrumental reinforcers (rewards and punishers) — and localizes the computation: the orbitofrontal cortex computes reward value, the anterior cingulate learns the action that obtains it, and reasoning systems can supply alternative goals, while over-learned habits bypass emotion entirely. Berridge (2018) then decomposes reward itself into three dissociable components — "wanting" (incentive salience, a dopamine-dependent motivational pull), "liking" (hedonic impact), and learning — a triple dissociation with immediate clinical yield: excessive "wanting" divorced from "liking" is the signature of addiction, deficient incentive salience is a motivational route into the anhedonia of depression, and a negatively valenced "fearful salience" contributes to paranoia. The documented weaknesses are the tradition's dependence on animal models and its comparative silence on subjective experience. The extraction adopts reinforcer value as the appraisal core's currency and makes wanting, liking, and learning distinct mechanisms rather than one reward node.

### 3.3 Cognitive-appraisal theories

Where reward neuroscience computes value bottom-up, the appraisal tradition computes it top-down: emotion follows from the appraised personal significance of an event, and appraisal is "a necessary as well as sufficient cause of emotion," with knowledge necessary but not sufficient (Lazarus, 1991). Lazarus's primary appraisal (is this relevant to my goals, and congruent or not?) and secondary appraisal (can I cope, and who is accountable?) give the core its internal structure, and his emphasis on *meaning generation* — including automatic, unconscious appraising — pre-empts the objection that appraisal must be slow and deliberate. Scherer's (2009)\* component process model sharpens the machinery into a sequence of stimulus-evaluation checks that drive, and synchronize, the emotion's several components. The documented risks are over-cognitivism for reflexive affect and the under-determination of the appraisal-to-emotion mapping. The extraction takes appraisal as the generative core (with primary and secondary facets) and resolves the over-cognitivism charge through Principle 3's dual route.

### 3.4 Attribution and expectancy

Weiner (1985) supplies the stratum's most explicit cognition→emotion→motivation circuit. Perceived causes of success and failure share three dimensions — locus, stability, and controllability — and these do specifiable work: the *stability* of a cause governs the change in one's expectancy of future success, while all three dimensions generate a catalog of outcome-specific emotions (pride, shame, guilt, anger, gratitude, pity, hopelessness), and expectancy and affect together guide subsequent behavior. The theory thus "relates the structure of thinking to the dynamics of feeling and action" — precisely the relation this stratum must formalize. Its documented weaknesses are its achievement-domain origins and reliance on retrospective report. The extraction renders attribution as a mechanism feeding secondary appraisal, generating discrete emotions, and setting persistence through expectancy — and, when the ascriptions are internal, stable, and global for failure, feeding the hopelessness route into depression (Abramson et al., 1989\*; Weiner, 1985).

### 3.5 Discrete, dimensional, and constructionist emotion

The emotion literature's long argument is about *format*. The discrete tradition holds that a small number of basic emotions — each with a dedicated circuit, expression, and physiology — are the natural kinds: Ekman's (1992)\* argument for basic emotions grounds the categorical readout and its universal facial signals, and Panksepp's (2011)\* affective neuroscience locates seven primary emotional systems (SEEKING, RAGE, FEAR, LUST, CARE, PANIC/GRIEF, PLAY) in homologous subcortical circuits across mammals, establishing that primary-process emotion is subcortical and does not require the neocortex. The dimensional and constructionist tradition holds the opposite pole: Russell's (2003)\* core affect makes valence and arousal the two-dimensional substrate from which discrete emotions are *constructed* by categorization, and Barrett's (2017)\* theory of constructed emotion recasts the whole process as active inference over interoceptive and conceptual predictions. The extraction refuses to adjudicate the format war at the domain level, because the evidence supports both a dimensional substrate and categorical readouts; it encodes core affect and discrete emotion as two coupled facets of the emotion readout (Section 6.3), with construction as the edge between them.

### 3.6 Integrative readout theories

Two theories perform the unification the stratum requires. Buck's (1985) PRIME theory states the thesis outright: motivation and emotion are different aspects of a single process in which emotion is the *readout* of the motivational potential inherent in hierarchically organized primary motivational–emotional systems, with three readout levels — a bodily adaptive-homeostatic readout (Emotion I), an expressive-communicative readout (Emotion II), and a subjectively experienced readout (Emotion III). Rolls (2025) supplies the neuroscientific counterpart, deriving both motivation and emotion from the brain's processing of reinforcers. The value of these theories to the series is structural rather than predictive: they justify a single graph with two readouts, and they supply the readout levels that become the emotion subgraph's expression and feeling facets. Their documented weakness — breadth that resists direct falsification — is exactly what a graph remedies, by attaching the broad thesis to weighted, testable edges borrowed from the component theories.

### 3.7 Regulation, action tendencies, and positive emotion

The final family makes the readouts *dynamic*. Gross's (1998)\* process model shows that emotion is regulable at five points across its generation — situation selection, situation modification, attentional deployment, cognitive reappraisal, and response modulation — a taxonomy that doubles as a map of therapeutic technique. Frijda's (1986)\* laws of emotion recast emotions as *action tendencies* — states of readiness to establish, maintain, or disrupt a relationship with the environment — supplying the missing link by which an emotion becomes a motivation. Fredrickson's (2001)\* broaden-and-build theory adds the asymmetry between positive and negative affect: positive emotions broaden the momentary thought–action repertoire and build enduring resources, whereas negative emotions narrow it. The extraction takes regulation as a mechanism (and the therapy interface), action tendency as an emotion facet feeding action, and the broaden/narrow asymmetry as a signed feedback edge from core affect to appraisal.

---

## 4. What the Evidence Settled

### 4.1 One process, two readouts

The convergence of integrative theory and affective neuroscience is the stratum's central settled result: motivation and emotion are not separable systems but two readouts of one appraisal of reward/punisher value (Berridge, 2018; Buck, 1985; Rolls, 2025). The same genes and brain systems that define primary reinforcers define the states that motivate and the states that are felt. Design consequence: a single shared appraisal core projecting to two readout nodes, not two parallel systems with a bridge — the geometry Figure G3(B) displays.

### 4.2 Wanting is not liking is not learning

Berridge's (2018) triple dissociation is robust and clinically load-bearing: incentive salience ("wanting"), hedonic impact ("liking"), and reward learning are separable, with distinct neural substrates, and they come apart in exactly the disorders the UDG must receive — addiction (wanting without liking), anhedonic depression (deficient wanting), and paranoia (fearful salience). Design consequence: three distinct mechanism/facet nodes, not one reward node, each with its own outward edge to the psychopathology interface (Figure G1).

### 4.3 Appraisal is central, but there are two routes

Appraisal is necessary for the great majority of emotion, and largely sufficient (Lazarus, 1991; Scherer, 2009\*) — but "appraisal" spans a fast, automatic, subcortical route and a slow, deliberate, cognitive one, and the primary-process systems can generate emotion with the neocortex removed (Panksepp, 2011\*). The over-cognitivism objection and the "emotion without cognition" objection dissolve once appraisal is dual-route rather than exclusively deliberate. Design consequence: the appraisal core receives both a low-road input (from temperament and need set-points) and a high-road input (from attribution, learning, and personality), and only the latter is developmentally gated.

### 4.4 Discrete and dimensional are two views of one substrate

The decades-long format war between basic-emotion and dimensional accounts is, on the weight of evidence, not winnable at the level of exclusive truth: there is a two-dimensional affective substrate (valence × arousal) *and* there are categorical, expressed, cross-culturally recognizable emotions, and the most defensible position treats the categories as constructed from, or read out alongside, the substrate (Barrett, 2017\*; Ekman, 1992\*; Russell, 2003\*). Design consequence: core affect and discrete emotion as coupled facets, with a construction edge between them — the structure Figure G4 renders as the affect circumplex.

### 4.5 What follows for design

Jointly the verdicts impose seven requirements: (1) a single appraisal/valuation core rather than separate motivation and emotion engines; (2) two reciprocally coupled readouts — motivation and emotion; (3) a dual-route appraisal, fast and slow; (4) a componential emotion readout carrying core affect, discrete category, expression, action tendency, and feeling; (5) three dissociable reward components — wanting, liking, learning; (6) an attribution/expectancy mechanism closing the cognition→emotion→motivation loop; and (7) regulation as a modulating mechanism that is simultaneously the therapy lever and, when it fails, a disorder pathway. No single theory satisfies all seven; their union does.

---

## 5. Extraction: The Universal Motivation–Emotion Framework

### 5.1 Method of extraction

As in the preceding articles, we triangulated the field's integrative statements (Buck, 1985; Rolls, 2025), its critical and comparative treatments (Berridge, 2018; Turner et al., 2003), the primary statements of each family (Section 3), and the adjudicating empirical and neuroscientific literatures (Section 4). A principle was admitted if (a) it is asserted or presupposed by at least three theory families, and (b) it has empirical support independent of any single family's paradigm. Seven principles survived.

### 5.2 The seven principles

**Table 2.** *The seven universal motivation–emotion principles: ancestry, evidence, and graph translation.*

| # | Principle | Statement | Principal ancestry | Independent evidence | Graph translation |
|---|---|---|---|---|---|
| 1 | Single valuation | Motivation and emotion co-emerge from one appraisal of reward/punisher value | Buck; Rolls; Berridge | Shared neural substrates for reinforcers, motivation, and affect (Rolls, 2025) | One appraisal core projecting to both readouts |
| 2 | Dual readout | The same valuation is read out as action guidance (motivation) and as state signal (emotion), reciprocally | Buck; Frijda; Turner | Emotion indexes goal structure; action tendencies drive behavior (Turner et al., 2003) | MOT and EMO readout nodes with reciprocal edges |
| 3 | Dual-route appraisal | Valuation runs on a fast subcortical route and a slow cognitive route | Lazarus; Panksepp; Scherer | Sub-cortical primary systems; automatic appraisal (Panksepp, 2011\*) | Low-road and high-road inputs to APPR; gated high road |
| 4 | Componential emotion | An emotion is a bundle: core affect, discrete category, expression, action tendency, feeling | Scherer; Russell; Buck; Frijda | Component synchronization; circumplex structure (Scherer, 2009\*) | Emotion subgraph with five facets |
| 5 | Reward is plural | Wanting, liking, and learning are dissociable reward components | Berridge | Neural/behavioral triple dissociation (Berridge, 2018) | Distinct salience, hedonic, and learning nodes |
| 6 | Attributional modulation | Causal ascriptions set expectancy and generate outcome-specific emotions | Weiner | Locus/stability/controllability effects (Weiner, 1985) | Attribution mechanism into appraisal, emotion, persistence |
| 7 | Regulability | Both readouts are modulable — the therapy lever and, when failing, a disorder path | Gross; Lazarus; Fredrickson | Five-point regulation effects (Gross, 1998\*) | Regulation mechanism with signed edges to core and disorder |

The principles are intersection constraints, not a ninth theory. Principle 1 is this stratum's manifestation of the series' non-dismissibility axiom applied to a false dichotomy: one cannot model the person by deleting either motivation or emotion, because they are the same process seen twice. Principle 5 deserves emphasis: it is what lets the UMEG hand the disorder stratum three distinct motivational-emotional priors — dysregulated wanting, deficient liking, and fearful salience — rather than a single undifferentiated "reward problem."

---

## 6. The Universal Motivation–Emotion Graph

### 6.1 Formal definition

Let $V$ be the node set published in the accompanying data files: a superordinate motivation–emotion node $ME$; a shared appraisal/valuation core; two readout nodes — motivation and emotion — with three and six facet subnodes respectively; approach and avoidance channel nodes; four mechanism nodes (causal attribution, incentive salience, regulation, reinforcement learning); an action output node; and six interface nodes (needs, situation/systems, personality, temperament, psychopathology, therapy). Let $W(t) \in \mathbb{R}^{|V| \times |V|}$ be a signed weighted adjacency matrix inheriting the series' gating formalism, $w_{ij}(t) = g_{ij}(t)\,\bar{w}_{ij}$, with gates here carrying *situational triggers* (the appraisal-to-channel edges) and *developmental windows* (the maturation of attribution, learning, and regulation) in addition to the fast/slow route distinction. The UMEG is $G(t) = (V, W(t))$; Figure G1 displays it at domain/channel/mechanism resolution, and every edge carries weight, sign, type, gate class, evidential basis, and primary sources in the data files.

![**Figure G1.** The Universal Motivation–Emotion Graph: one valuation process, two coupled readouts. A shared appraisal/valuation core drives motivation and emotion readouts through approach and avoidance channels, modulated by attribution, incentive salience, reinforcement learning, and regulation, and coupled to six interface nodes. Edge thickness is proportional to provisional consensus weight; diamonds mark gated edges; facet subnodes are shown in Figure G4.](../figures/figG1_universal_motivation_emotion_graph.png)

### 6.2 Axiom compliance

*Axiom 1* (universal connectivity): every input reaches action through the core, a channel, and a readout; no node is islanded. *Axiom 2* (non-dismissibility): neither readout may be deleted — a person modeled without emotion is a decision machine, and a person modeled without motivation is a mood with no behavior; the stratum's whole point is that both are the same process and both are mandatory. *Axiom 3* (mediated and unmediated influence): appraisal reaches action directly (through motivation) and indirectly (through emotion's action tendencies), and situation reaches emotion both directly (low road) and through cognitive appraisal (high road) — all routes are edges. *Axiom 4* (self-influence): the graph carries self-loops on incentive salience (incentive-sensitization: wanting begets wanting), on core affect (affective momentum: mood persists and biases subsequent appraisal), and on motivation (goal engagement builds commitment) — three documented positive-feedback dynamics (Berridge, 2018; Fredrickson, 2001\*). *Axiom 5* (signed superposition): the approach and avoidance channels carry opposite signs into both motivational direction and core-affect valence, so that an approach–avoidance conflict is literally the superposition of a positive and a negative edge, and regulation enters the core with a negative sign that sums against a threat appraisal's positive one — the geometry that lets the model represent ambivalence and reappraisal as arithmetic rather than exception.

### 6.3 Subgraphs and encapsulation

The two readouts own encapsulated facet subgraphs. Motivation decomposes into *direction* (goal selection and approach/avoidance orientation), *intensity* (vigor and energization — the drive tradition's surviving contribution), and *persistence* (volitional maintenance, the target of expectancy). Emotion decomposes into *core affect* (valence × arousal — Russell's, 2003\*, substrate), *discrete emotion* (the categorical readout — Ekman's, 1992\*, and Panksepp's, 2011\*, contribution), *expression/communication* (Buck's Emotion II), *action tendency* (Frijda's, 1986\*, readiness), *subjective feeling* (Buck's Emotion III), and *hedonic impact* ("liking"). The subgraphs absorb the tradition's live disputes without destabilizing the readout level: whether emotion is fundamentally discrete or dimensional is a within-EMO question about the edge from core affect to discrete emotion (Figure G4), and whether appraisal is fast or slow is a within-APPR question — neither reaches up to threaten the one-process/two-readout architecture. Figure G4 renders the emotion subgraph's central claim as the affect circumplex: discrete emotions occupy regions of the valence × arousal plane, and the appraisal quadrants (goal-congruence × control) label why each region is reached.

![**Figure G4.** The affect circumplex: discrete emotion as regions of the valence × arousal core-affect plane, integrating the dimensional and categorical accounts, with appraisal quadrants (goal-congruence × control/agency) labeling the regions. After Russell (2003)\*; appraisal structure after Lazarus (1991) and Weiner (1985).](../figures/figG4_affect_circumplex.png)

### 6.4 The two signature dynamics

Figure G3 renders the stratum's two signature dynamics as edge-level claims. Panel A displays the wanting–liking–learning dissociation: across cumulative reward exposure, incentive salience can sensitize upward while hedonic impact habituates and learning saturates — the divergence whose extreme is addiction (Berridge, 2018). Panel B displays the one-process/two-readout claim directly: along a single appraised-value axis from punisher to reward, the motivation readout (approach tendency) and the emotion readout (core-affect valence) rise together while arousal traces its characteristic U — three curves, one underlying variable, which is the whole thesis of the stratum (Buck, 1985; Rolls, 2025). Both dynamics are illustrative shapes, not fitted functions; each corresponds to identified, weighted, testable edges in the data files.

![**Figure G3.** The two signature dynamics the UMEG carries as edges. (A) Wanting ≠ liking ≠ learning: three dissociable reward components (after Berridge, 2018). (B) One process, two readouts: motivation and emotion co-emerge from a single appraised-value axis (after Buck, 1985; Rolls, 2025). Illustrative shapes, not fitted functions.](../figures/figG3_wanting_liking_and_dual_readout.png)

### 6.5 Coupling to the other strata

The UMEG's interfaces define the stratum's systemic role, and they close the loop the needs paper opened. *Inward from needs* (Batch F): the Universal Needs Graph's motivation interface projects into this graph's needs input layer, which feeds the appraisal core — need deficits set the goal-relevance of stimuli, making needs, formally, the input layer of motivation exactly as the needs paper predicted (Buck, 1985; Ryan & Deci, 2000\*). *Inward from temperament* (Batch E): temperament sets the reactivity of the approach and avoidance channels and the baseline of core affect — the initial conditions of the affective system, the low road of Principle 3 (Panksepp, 2011\*). *Inward from personality* (Batch D): traits bias appraisal thresholds and emotional reactivity, the high road's dispositional filter (Barrett, 2017\*). *Inward from situation/systems* (Batch H): the environment enters as appraised stimuli and receives emotional expression as an outward communicative signal (Buck's Emotion II) — the transactional edge the systems stratum will elaborate. *Through development* (Batch C): the maturation of attribution, reinforcement learning, and regulation are developmentally gated edges, and the acquisition of regulation is precisely an internalization the developmental stratum formalized. *Outward to action*: both readouts converge on the action output node, which feeds reinforcement learning back into the core — the model's principal feedback loop. *Toward psychopathology* (Batch A): the UMEG hands the Universal Disorder Graph a rich, differentiated set of person-specific priors — dysregulated wanting (addiction), deficient liking (anhedonic depression), fearful salience (anxiety, paranoia), maladaptive attributional style (hopelessness depression), and emotion dysregulation — the third and most mechanistically detailed disorder-prior source after temperament and need frustration (Abramson et al., 1989\*; Berridge, 2018; Gross, 1998\*). *For therapy* (Batch B): the therapy interface operates through the regulation mechanism, and the UMEG makes explicit why the common therapeutic techniques work — cognitive reappraisal edits appraisal, behavioral activation restores the approach channel and incentive salience, and exposure re-learns reinforcer value — three levers on three identified edges.

### 6.6 What the UMEG adds

Against a century of parallel literatures, the UMEG replaces the motivation/emotion dichotomy with a computable object in which each family survives as the component it got right: the drive tradition as intensity, reward neuroscience as the valuation currency and the wanting/liking/learning triple, appraisal theory as the generative core, attribution theory as the expectancy-and-emotion mechanism, discrete and dimensional theories as coupled emotion facets, the integrative theories as the one-process architecture itself, and the regulation and positive-emotion frameworks as the modulating mechanism and its feedback asymmetry. Against the reward node of a typical reinforcement-learning model it substitutes a mechanism that distinguishes wanting from liking — the difference between a model that can represent addiction and one that cannot. And against all of them it adds what no motivation or emotion theory currently possesses: formal continuity with needs, temperament, personality, development, disorder, and treatment strata under shared axioms, making an emotional episode a traceable path through a person-model rather than an entry in a separate literature.

### 6.7 Falsifiability, validation pathway, and limitations

The UMEG makes refutable commitments. *Architecture*: the one-process claim predicts that manipulations of appraised value move motivation and emotion together, and that their neural substrates overlap; a clean double dissociation of appraised reward value from both motivation and affect would falsify the shared core (Rolls, 2025). *Dissociation*: Principle 5 predicts that wanting, liking, and learning can be moved independently — already demonstrated pharmacologically and lesion-wise — and that the three map onto distinct disorders; a failure to dissociate them would collapse three nodes into one (Berridge, 2018). *Route*: the dual-route claim predicts emotion under conditions precluding deliberate appraisal (subcortical stimulation, decortication, subliminal induction) and predicts that developmental gates apply only to the high road (Panksepp, 2011\*). *Regulation*: the regulability principle predicts that each of Gross's five points yields measurable, edge-specific modulation, and that therapeutic gains track the targeted edge (Gross, 1998\*). Validation should proceed from reanalysis of existing appraisal-and-affect datasets, through experimental manipulation of the wanting/liking/learning components, to preregistered tests of the developmental gates.

Four limitations bound the contribution. First, the published weights are consensus priors and the two dynamics figures are illustrative shapes; the readout functions and the wanting–liking divergence await estimation. Second, the emotion evidence base over-represents visual facial signals and WEIRD samples, and the discrete/dimensional integration, while defensible, is not settled — the core affect-to-discrete edge is the model's most revisable claim (Barrett, 2017\*; Ekman, 1992\*). Third, the graph draws its neural anchoring from a small number of reviews (Berridge, 2018; Rolls, 2025); the localization claims are imported, not established here, and the psychological graph does not depend on any particular neuroanatomy being correct. Fourth, subjective feeling enters as a facet node but the stratum makes no claim to solve the problem of conscious experience; the feeling node is an interface to a question psychology can measure but not yet explain.

---

## 7. Conclusion

Motivation and emotion were studied apart for a century and turned out to be one thing seen twice — the person's valuation of reward and punishment, read out once as the direction and force of action and once as the valence and arousal of feeling. This article extracted that convergence as seven principles: a single valuation core, two coupled readouts, a dual-route appraisal, a componential emotion, a plural reward, an attributional loop, and a regulable output. The Universal Motivation–Emotion Graph formalizes all seven — a signed, gated network in which wanting and liking are finally distinct, discrete and dimensional emotion are finally reconciled as facets, and the reappraisal that a therapist teaches is finally an identifiable edge. Within the Unified Person Graph it is the engine: the stratum that takes the pressure the needs graph delivers and turns it into wanting, feeling, and doing. The needs paper asked what the person cannot do without; this one shows what the person does about it — and the strata that remain must place that engine in the world it acts on, and in the mathematics that lets the whole assembly be computed.

---

## References

*Sources marked with an asterisk (\*) were located by the authors through supplementary literature searches beyond the assembled source library.*

Abramson, L. Y., Metalsky, G. I., & Alloy, L. B. (1989). Hopelessness depression: A theory-based subtype of depression. *Psychological Review, 96*(2), 358–372. https://doi.org/10.1037/0033-295X.96.2.358 \*

Bandhu, D., Mohan, M. M., Nittala, N. A. P., Jadhav, P., Bhadauria, A., & Saxena, K. K. (2024). Theories of motivation: A comprehensive analysis of human behavior drivers. *Acta Psychologica, 244*, Article 104177. https://doi.org/10.1016/j.actpsy.2024.104177

Barrett, L. F. (2017). The theory of constructed emotion: An active inference account of interoception and categorization. *Social Cognitive and Affective Neuroscience, 12*(1), 1–23. https://doi.org/10.1093/scan/nsw154 \*

Berridge, K. C. (2018). Evolving concepts of emotion and motivation. *Frontiers in Psychology, 9*, Article 1647. https://doi.org/10.3389/fpsyg.2018.01647

Buck, R. (1985). Prime theory: An integrated view of motivation and emotion. *Psychological Review, 92*(3), 389–413. https://doi.org/10.1037/0033-295X.92.3.389

Ekman, P. (1992). An argument for basic emotions. *Cognition and Emotion, 6*(3–4), 169–200. https://doi.org/10.1080/02699939208411068 \*

Fredrickson, B. L. (2001). The role of positive emotions in positive psychology: The broaden-and-build theory of positive emotions. *American Psychologist, 56*(3), 218–226. https://doi.org/10.1037/0003-066X.56.3.218 \*

Frijda, N. H. (1986). *The emotions*. Cambridge University Press. \*

Gross, J. J. (1998). The emerging field of emotion regulation: An integrative review. *Review of General Psychology, 2*(3), 271–299. https://doi.org/10.1037/1089-2680.2.3.271 \*

Lazarus, R. S. (1991). Cognition and motivation in emotion. *American Psychologist, 46*(4), 352–367. https://doi.org/10.1037/0003-066X.46.4.352

Panksepp, J. (2011). Cross-species affective neuroscience decoding of the primal affective experiences of humans and related animals. *PLoS ONE, 6*(9), Article e21236. https://doi.org/10.1371/journal.pone.0021236 \*

Rolls, E. T. (2025). Emotion, motivation, reasoning, and how their brain systems are related. *Brain Sciences, 15*(5), Article 507. https://doi.org/10.3390/brainsci15050507

Russell, J. A. (2003). Core affect and the psychological construction of emotion. *Psychological Review, 110*(1), 145–172. https://doi.org/10.1037/0033-295X.110.1.145 \*

Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist, 55*(1), 68–78. https://doi.org/10.1037/0003-066X.55.1.68 \*

Scherer, K. R. (2009). The dynamic architecture of emotion: Evidence for the component process model. *Cognition and Emotion, 23*(7), 1307–1351. https://doi.org/10.1080/02699930902928969 \*

Turner, J. C., Meyer, D. K., & Schweinle, A. (2003). The importance of emotion in theories of motivation: Empirical, methodological, and theoretical considerations from a goal theory perspective. *International Journal of Educational Research, 39*(4–5), 375–393. https://doi.org/10.1016/j.ijer.2004.06.005

Weiner, B. (1985). An attributional theory of achievement motivation and emotion. *Psychological Review, 92*(4), 548–573. https://doi.org/10.1037/0033-295X.92.4.548

Young, P. T. (1961). *Motivation and emotion: A survey of the determinants of human and animal activity*. Wiley.
