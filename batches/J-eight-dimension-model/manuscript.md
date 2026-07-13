# The Great Graph: Composing the Eight-Dimension Network Model of the Person

**[Author 1 name], [Author 2 name]**

[Affiliations]

**Author note.** Correspondence concerning this article should be addressed to [corresponding author]. The graph data files (dimension-level and full-resolution), the composition code, the verification code (which reproduces every numerical claim in the text), and the figure-generation code are openly available in the article's supplementary repository. This article is the tenth in a planned series deriving the Unified Person Graph (UPG), an eight-dimensional network model of psychological functioning. The eight substantive articles derived the Universal Disorder Graph (psychopathology), Universal Therapy Graph (treatment), Universal Developmental Graph (development), Universal Personality Graph (personality), Universal Temperament Graph (temperament), Universal Needs Graph (needs), Universal Motivation–Emotion Graph (motivation and emotion), and Universal Systems Graph (systems); the ninth built and justified the mathematical toolbox. This article is the synthesis: it composes the eight strata into one object, weighs it, reads its topography, and turns it into a diagnostic instrument.

---

## Abstract

Nine articles have prepared one act, and this article performs it. We compose the eight universal strata derived in Batches A–H — psychopathology, therapy, development, personality, temperament, needs, motivation–emotion, and systems — into a single signed, weighted, time-gated network: the Great Graph of the Eight-Dimension model, comprising 253 published nodes and 522 published edges, of which 35 cross stratum boundaries under a strict encapsulation rule (cross-stratum influence passes only through mother and interface nodes; the composition code verifies zero violations). We first generalize the base framework — dynamic learned graphs for individual psychopathology — from a single-domain proposal into a stratified formalism able to host any domain theory that can state itself as a signed, weighted, gated graph, with explicit aggregation and broadcast operators governing how lower-layer subgraphs and the higher-layer dimension graph interact. We answer the five W's and H of why mathematics is the right instrument here, resting on the isomorphism licence issued in the ninth article. We state the weighting method as seven explicit rules, from structure-before-weights through anchored consensus priors to the Bayesian estimation pathway that will replace priors with data. We then read the composed object. Its algebraic connectivity (λ₂ = 1.568) certifies that the person is one graph, not eight; its Fiedler vector splits the dimensions into a dispositional shore (temperament, development, personality) and a transactional shore (needs, motivation–emotion, disorder, therapy, systems), with personality as the near-exact bridge (|v₂| = 0.015); its strongest self-amplifying loop is need frustration feeding negative valuation (gain +0.400), and its strongest regulating loop is the treatment loop (gain −0.455). A fully computed synthetic case demonstrates the model's topographical readout — peaks where the person hurts, valleys where resources lie — and grounds the article's clinical contribution, Topographic Network Diagnosis (TND): a seven-step diagnostic method whose output is a landscape, a mechanism list, and a control plan rather than a category label. The case's dynamics reproduce, at the whole-person level, the loop-gain bifurcation of the ninth article ($\kappa^{*} = 1/\lambda_{\max}(B) = 0.456$), distinguish state-shifting from structure-changing intervention, and quantify fragile remission as rising spectral radius. We close with the validity and reliability analysis the series owes: what the composed model claims, how each claim can fail, and how it compares — property by property — with DSM-5, ICD-11, HiTOP, RDoC, and symptom-network analysis.

**Keywords:** network models, unified theory, diagnosis, graph theory, computational psychiatry, topography, psychopathology, integrative psychology

---

## 1. Introduction

Every article in this series ended with a promissory note. The disorder graph promised that temperament, needs, motivation, and environment would one day arrive as its priors rather than its footnotes. The therapy graph promised a person for its workflow to treat. The developmental graph promised that its time gates would someday gate something. The ninth article sharpened all of these into a single obligation: a toolbox was built and licensed — state vectors, signed weighted matrices, Laplacians, iterated maps, learning rules — "so that the next article picks them up and does the thing they were sharpened for" (Batch I). This is the next article.

Its task is stated in the project's own words: put together the big graphs of the eight dimensions and build the Great Graph; introduce a method to weigh the nodes and direct the edges; introduce the topographical model of the same eight-dimensional object, with peaks and valleys and heat maps; introduce a new diagnostic method based on these; and do all of it without producing a theory soup — everything coherent, corresponsive, and in harmony. The composition must serve all ages (the time gates inherited from the developmental stratum are the mechanism) and all kinds of people, typical and atypical (a person is a location and a trajectory on the graph, not a category member). And the result must be measurable, reproducible, and falsifiable — no black box.

The article proceeds in the order the obligations were incurred. Section 2 generalizes the base framework into a stratified formalism and states, as propositions with computational verification, what survives composition. Section 3 answers the five W's and H of mathematics in this model. Section 4 performs the composition and audits the five axioms on the assembled object. Section 5 states the weighting method. Section 6 reads the composed graph's spectral anatomy. Section 7 defines the topographical model. Section 8 introduces Topographic Network Diagnosis and demonstrates it end-to-end on a synthetic case whose every number is reproduced by the verification code. Section 9 documents the harmonization decisions that keep the model one theory rather than eight stapled ones. Section 10 delivers the validity and reliability analysis, with the comparison to existing systems. Section 11 marks the formal limit, and Section 12 states limitations and the validation roadmap honestly: every weight in this article is a consensus prior awaiting estimation, and the diagnostic method is a research protocol awaiting trials, not a clinic-ready instrument.

---

## 2. The Base Framework, Generalized

### 2.1 What the base framework supplied

The base framework (Dynamic Learned Graphs for Individual Psychopathology) proposed, for one domain, the machinery this series needed for eight. Its central move is the separation of **structure** from **state**: a person's psychology is a graph $G=(V,E,W)$ whose signed, weighted adjacency matrix $W$ is *learned slowly* from repeated observations, while the momentary condition is a fast state vector $x(t) \in \mathbb{R}^{|V|}$. Structure is analyzed spectrally — degree matrix $D$, Laplacian $L = D - W$, eigenpairs $L v_k = \lambda_k v_k$, the Fiedler vector $v_2$ as the deepest learned axis, the embedding $z(t) = V_m^{\top} x(t)$ as the person's location on those axes. State evolves by an iterated map,

$$x(t+1) = \sigma\big(B\,x(t) + C\,c(t) + G\,u(t) + \varepsilon(t)\big),$$

with temporal operator $B$, context $c$, control $u$, and noise $\varepsilon$; attractors, Jacobian stability, and loop gains carry the clinical meaning (self-maintaining disorder, prognosis, sudden change). Structure itself updates by $W_{t+1} = (1-\rho)W_t + \rho \widehat{W}_t$ — psychopathology has both memory and plasticity — and control decomposes as $u = u^{\text{self}} + u^{\text{ext}}$: human will as endogenous control toward endorsed goals, therapy and environment as exogenous input. All of this the series has already used piecewise; Batch I proved each tool sound in isolation.

### 2.2 The stratified generalization

What the base framework did not supply — because its scope was psychopathology alone — is an account of how *several* domain graphs cohere into one person. We generalize it in five definitions. The generalization is deliberately abstract: any future domain theory that can meet the definitions can be added as a stratum, which is what makes this a framework for "other future similar theories" and not only for the present eight.

**Definition 1 (Stratum).** A stratum $S_a = (V_a, W_a, g_a)$ is a signed, weighted graph over a domain's constructs together with its gate functions $w_{ij}(t) = g_{ij}(t)\,\bar{w}_{ij}$, derived from that domain's consensus literature with per-edge provenance. Batches A–H each delivered exactly one stratum (the therapy stratum's graph is a workflow; it joins the formalism identically).

**Definition 2 (Mother node and interfaces).** Each stratum designates one mother node $m_a$ — the aggregate activation of the stratum — and optionally interface nodes that carry specified couplings to named partner strata (e.g., the motivation–emotion stratum's NEEDS_IF, the systems stratum's DEV_IF).

**Definition 3 (Encapsulation constraint).** In the composed graph, $W_{(a\to b)}$ entries are zero except on rows and columns belonging to mother or interface nodes: a stratum's internal nodes never touch another stratum's internal nodes directly. Sub-graphs are zoom-ins of their dimension; they reach the rest of the person only through their mother, and the composition code audits this as a hard constraint (Section 4.3: zero violations).

**Definition 4 (Aggregation and broadcast).** The layers interact in both directions. Upward, each mother's state is a readout of its children: $x_{m_a}(t) = r_a\big(x_{c}(t) : c \in V_a\big)$, with $r_a$ a weighted mean in the present model (the hierarchical edge weights are the aggregation weights). Downward, drive arriving at a mother broadcasts into its subgraph along the same hierarchical edges. This is the formal content of the requirement that "lower-layer and higher-layer graphs (and matrices) interact": the dimension-level matrix is not a separate theory but a *coarse-graining* of the full matrix, exact when within-stratum equilibration is fast relative to between-stratum influence — the standard time-scale-separation assumption of multilevel dynamical models (Érdi et al., 2017).

**Definition 5 (Composition).** The Great Graph is the union of the strata under namespacing, plus the interface bindings and the sourced mother-to-mother couplings, with all signs restated in one algebraic convention (Section 9). Its weight matrix is block-structured: dense diagonal blocks (the strata), sparse off-diagonal entries only in mother/interface rows and columns (Figure J2).

### 2.3 What survives composition: four propositions

**P1 (Consistency).** The five axioms are mutually consistent because a model of them exists: the composed graph itself satisfies all five simultaneously (the Section 4.4 audit is the model-existence proof; a set of axioms with a model cannot be contradictory). This is the appropriate — and appropriately modest — formal sense of the project requirement that the axiom set be consistent.

**P2 (Axiom preservation).** Encapsulated composition preserves the axioms. Connectivity: if each stratum is connected and each stratum's mother is coupled to at least one other mother, the union is connected. Non-dismissibility and mediation: every node reaches every other through its mother chain (verified: reachability fill = 1.000). Self-influence and signed superposition are local properties untouched by composition.

**P3 (Toolbox inheritance).** Every Batch I tool applies unchanged to the composed object, at either resolution: the Laplacian and Fiedler analysis of Section 6 runs on the dimension graph exactly as it ran on Batch I's six-node example; the iterated map of Section 8 runs on the dimension state vector exactly as the base framework ran it on symptoms.

**P4 (Bifurcation inheritance).** The composed system inherits the loop-gain bifurcation of Batch I §5.4 with a computable threshold: for the saturating map $x(t+1) = \tanh(\kappa B x(t))$, the quiescent state loses stability at $\kappa^{*} = 1/\lambda_{\max}(B)$. For the dimension-level matrix of Section 8, $\lambda_{\max}(B) = 2.195$, hence $\kappa^{*} = 0.456$; the verification code confirms quiescence below it and self-sustaining activation above it (Figure J5b). A whole person, not just a symptom cluster, can therefore cross into a self-maintaining configuration — and standing load (constitution, history, adversity) *unfolds* the pitchfork, holding vulnerable systems at elevated activation with no jump required (Section 8).

---

## 3. Why Mathematics: The Five W's and H

**What.** Six objects and no more: a state vector $x(t)$ (where the person is); a signed, weighted, gated matrix $W$ (what influences what, how strongly, in which direction, and when); the Laplacian spectrum (the deep axes and fault lines of the structure); an iterated map with attractors and Jacobians (how the person moves, settles, and resists change); Bayesian/reinforcement updates (how history writes the weights and therapy rewrites them); and measurement/model-selection theory (what keeps the numbers honest). Batch I built each with worked examples; nothing in this article uses any mathematics beyond them.

**Why.** Because the representation is licensed by isomorphism, not convenience: the empirical sciences of the mind independently converged on a subject matter that is many-component, directed, signed, weighted, time-varying, and productive of self-maintaining states, and a signed weighted gated graph is the mathematical object with exactly those properties and no others (Batch I §6.1). A list cannot carry directed influence; a taxonomy cannot carry signed superposition; a narrative cannot be eigendecomposed. The graph can, because the graph is the structural isomorph of what psychology found. That is also why the model represents phenomena rather than forcing reality into itself (project requirement 15): the form was chosen to fit the findings, not the reverse.

**Who.** Three users, one object. Researchers estimate and test it: every claim in Section 10 is falsifiable at a named layer. Clinicians read it: the topography of Section 7 is the case formulation drawn as a landscape, and TND's steps map one-to-one onto intake, testing, formulation, diagnosis, prognosis, and treatment planning (Figure J4). Patients — and any person mapping their own functioning — see themselves in it without translation: the eight dimensions are eight questions anyone can ask (*How were you born? How was your life? Who are you? What do you need? What do you want and feel? What's wrong? How to solve it? Where do you live?*). Batch K develops this third use.

**When.** At every phase, but with different objects. Theory construction fixed $V$ and the structure of $W$ (Batches A–H). Assessment estimates $x(t)$. Formulation personalizes $W$ from repeated states. Monitoring tracks $z(t)$ and $\Delta x(t)$. Treatment planning optimizes $u$. Across the lifespan, the gates $g_{ij}(t)$ carry the model from infancy to old age: the same graph, differently gated, is a child's or an elder's — which is how one model serves all ages without pretending ages are alike.

**Where.** In the model's every layer, and in a specific place in the science: the gap Townsend (2008) lamented — mathematical psychology's failure to colonize clinical, developmental, personality, and social psychology — is exactly the territory the eight strata cover. The series is an existence proof that formal theory construction reaches the whole person.

**How.** By the discipline the weighting method makes explicit (Section 5): structure from theory, magnitudes as anchored consensus priors with provenance, signs algebraic, direction by stated criteria, gates from the developmental stratum, and a declared estimation pathway from priors to data. The *how* is the answer to the black-box prohibition: at no point does a number enter the model without a rule that says where it came from and how it can be revised.

---

## 4. The Composition

### 4.1 The eight dimensions

Table 1 lists the composed dimensions. Each encapsulates the full stratum published in its batch; nothing is re-derived here.

**Table 1.** *The eight dimensions of the model.*

| Dimension | Batch | Stratum graph | Guiding question | Nodes | Mother node |
|---|---|---|---|---|---|
| TEM Temperament | E | UTempG | How were you born? | 30 | T |
| DEV Development | C | UDevG | How was your life? | 21 | D |
| PER Personality | D | UPerG | Who are you? | 54 | P |
| NEED Needs | F | UNeedG | What do you need? | 33 | N |
| ME Motivation–Emotion | G | UMEG | What do you want and feel? | 28 | ME |
| DIS Psychopathology | A | UDG | What's wrong? | 18 | P |
| THER Therapy | B | UTG | How to solve? | 39 | THER (synthesized) |
| SYS Systems | H | USysG | Where do you live? | 30 | SYS |

*Note.* Node counts are the published stratum registries after namespacing (e.g., the two mother nodes named P become DIS.P and PER.P). The therapy stratum was published as an eleven-phase workflow with no single mother; composition adds one (THER.THER) with hierarchical edges to the eleven phases — the only synthesized node in the model.

### 4.2 The dimension-level Great Graph

The dimension-level graph (Figure J1) contains the 8 mother nodes and 41 published edge rows: 34 inter-dimension couplings and 7 self-loops, of which 5 rows are negative-signed. Every row carries weight, sign, type, gate, provenance (which batch established it, via which interface or edge), evidence basis, and primary sources; the file `upg_dimension_edges.csv` is the authoritative registry. Three points deserve emphasis.

First, almost nothing here is new. Of the 34 inter-dimension couplings, 29 were established one at a time by Batches A–H (temperament as the initial conditions of personality; needs as the input layer of motivation; the four classes of disorder prior — temperamental, need-based, motivational–emotional, environmental; the therapy levers into regulation, fit, and systems; the developmental gates over everything). Composition mostly consisted of *collecting debts*, and the provenance column is the ledger. Five edges are new at composition and are flagged as such: the feedback edges by which disorder erodes needs and settings (Vansteenkiste & Ryan, 2013\*; Dohrenwend et al., 1992\*), the action-to-needs closure of the F→G loop (Hull, 1943\*; Ryan & Deci, 2017\*), and therapy's slow edges into personality and needs (Roberts et al., 2017\*; Ryan & Deci, 2017\*).

Second, the edge *types* sort the couplings into five mechanism classes, and the classes are doing theoretical work: **cascades** (dispositions flowing forward: temperament → personality → appraisal), **parametric edges** (development writing other strata's weights and gates — influence on *edges*, not only on nodes: the second-order structure the time-gated formalism was built for), **transactional edges** (person and environment selecting, evoking, and answering each other), **disorder priors** (the four classes converging on DIS), and **treatment edges** (the six THER levers plus the symptom-driven entry edge DIS→THER, which together make treatment an endogenous *loop*, not an outside intervention).

Third, two couplings are dual-channel (SYS→NEED and SYS→ME carry a positive support channel and a negative social-determinant channel). At dimension level both channels are published; which dominates for a given person is a fact about their environment's state, and the net drive is their signed sum — Axiom 5 operating *between* dimensions exactly as it operates between symptoms.

![**Figure J1.** The Great Graph at dimension level: eight mother nodes, 34 sourced inter-dimension couplings, and 7 self-loops. Green edges reinforce; red edges weaken; width is the consensus prior; each node encapsulates its stratum's full subgraph, and cross-dimension influence passes only through these mother nodes.](../figures/figJ1_great_graph.png)

### 4.3 The full-resolution Great Graph

The full object is produced by the composition code (`compose_greatgraph.py`), which (i) namespaces all published nodes and edges of the eight strata; (ii) synthesizes the THER mother; (iii) materializes hierarchical edges that three strata had encoded only in their registries' parent field; (iv) adds binding edges connecting each published interface node to its partner's mother in the direction the interface specifies; and (v) adds mother-to-mother edges for the couplings that have no interface node, drawn from the dimension registry. The result: **253 nodes and 522 edges, of which 35 cross stratum boundaries, with 20 explicit self-loops and 33 negative edges — and zero encapsulation violations** (every cross-stratum edge touches a mother or interface node; the code audits the constraint and fails loudly if any future edit breaks it). Figure J2 shows the block structure: the strata as dense diagonal blocks, the whole person held together by a sparse lattice of interface entries.

![**Figure J2.** The weight matrix of the full Great Graph (253 × 253), nodes ordered by stratum. Encapsulation is visible as block structure: dense within-stratum blocks, sparse cross-stratum entries confined to mother and interface rows and columns. Green entries are positive (reinforcing), red negative (weakening).](../figures/figJ2_block_matrix.png)

### 4.4 The axiom audit

The five axioms were commitments; on a composed object they become computable properties. The verification code checks each on the full 253-node graph. **Axiom 1** (every module affects others): the graph is weakly connected — 253 of 253 nodes in one component. **Axiom 2** (no module dismissible): zero isolated nodes; every node participates in at least one influence relation. **Axiom 3** (influence with or without mediators): with decomposition edges carrying aggregation upward as Definition 4 provides, the directed reachability fill is 1.000 — every node can influence every other through some directed path. **Axiom 4** (self-influence): 20 explicit self-loops, distributed across all seven person-side strata and the environment. **Axiom 5** (signed superposition): 33 negative edges coexist with 489 positive ones, and every node's net drive is computed as the signed sum $(Wx)_i$ of Batch I §5.2. The audit is the model-existence proof behind Proposition P1: the axioms are jointly satisfiable because this object jointly satisfies them.

---

## 5. Weighing the Nodes and Directing the Edges

The project requires "a method to weigh the nodes of the graph and the direction of the edges." The method exists — the series has been applying it for eight batches — but it has never been stated as a method. It is seven rules.

**W1 — Structure before weights.** The node set and edge skeleton come from consensus theory, never from free estimation. A model that can fit anything explains nothing (Batch I §5.6); fixing structure from theory is the series' overfitting control, and it is why every stratum began with the domain's consensus architecture rather than with data mining.

**W2 — Anchored magnitudes.** Edge weights are consensus priors on a $[0,1]$ magnitude scale with verbal anchors: ~0.9 definitional or decompositional (a hierarchy loading), ~0.7 strong replicated dependence (meta-analytic), ~0.5 moderate established dependence, ~0.3 weak or provisional. Weights are set by the anchor the evidence supports and recorded with the evidence; they are deliberately coarse, because false precision in a prior is a lie about uncertainty.

**W3 — Algebraic signs.** An edge is positive if greater source activation raises target activation, negative if it lowers it — always with respect to activation, never with respect to desirability. (Section 9 documents the one harmonization this forced.) Protective factors are therefore negative edges *into* problem nodes, and Axiom 5 does the rest.

**W4 — Direction by stated criteria.** An edge $j \to i$ requires at least one of: temporal precedence (longitudinally, $j$ leads $i$: temperament precedes traits), demonstrated mechanism (an experiment or intervention moves $i$ by moving $j$: scarcity captures appraisal), or intervention response (treatment applied at $j$ changes $i$: regulation training lowers symptoms). Mutual influence is two edges with independent justifications, not one "association."

**W5 — Gates.** Every edge may carry a gate $g_{ij}(t)$ inherited from the developmental stratum: sensitive periods, life-stage windows, situational triggers, age-rising stability. Gates are how one matrix serves all ages: the child's and the adult's graphs differ in $g(t)$, not in kind.

**W6 — Provenance and the asterisk.** Every weight ships with its sources; sources found beyond the provided library are asterisk-marked. A reader who disputes an edge disputes a row of a CSV file — a specific, falsifiable, revisable claim — not a paragraph of prose.

**W7 — The estimation pathway.** Priors are starting values, not conclusions. The base framework's fusion scheme $W = \sum_m \alpha_m \mathcal{N}(W^{(m)})$ combines evidence channels (panel co-occurrence, intensive-longitudinal transitions, semantic relations, clinical priors), and the update $W_{t+1} = (1-\rho)W_t + \rho\widehat{W}_t$ personalizes structure from a person's own repeated states. The consensus prior is $W^{(\text{clin})}$ in that fusion — the channel that keeps estimates interpretable — and the declared endpoint is a posterior, person-specific $W$ whose distance from the consensus prior is itself diagnostic information.

Node weight, finally, is not one number but three, and conflating them is a category error the method forbids. A node's **structural importance** is a property of $W$ (weighted degree, eigenvector centrality: how much of the graph routes through it). Its **activation** is a property of $x(t)$ (how loaded it is now). Its **elevation** in the topographic readout (Section 7) composes the two. On the composed graph, structural importance behaves as the architecture predicts: the mother nodes dominate (NEED.N 17.9, SYS.SYS 17.4, PER.P 16.1, ME.ME 15.9 weighted degree) because everything routes through them — that is what encapsulation *means* — and the highest-ranking internal nodes are the trait layer (PER.LAYER_TRT 10.7) and the therapy workflow's change-work and alliance phases (THER.N07 11.6, THER.N03 10.7), which is where domain theory itself locates the leverage.

---

## 6. The Spectral Anatomy of the Composed Person

With the object built, the Batch I tools can finally be pointed at the whole person. Three results follow from the dimension-level matrix alone, and each is a substantive psychological claim produced by arithmetic — none was put in by hand.

**One person, one graph.** The Laplacian spectrum of the (symmetrized-magnitude) dimension graph is $(0, 1.568, 1.929, 2.436, 2.510, 2.930, 3.189, 3.562)$. Algebraic connectivity $\lambda_2 = 1.568$ is *large* — compare the 0.119 of Batch I's deliberately loose two-community example. The composed person is nowhere near separable into independent subsystems: there is no cut through this graph that costs little. That is the arithmetic content of holism, and the formal rebuke to any assessment that measures one dimension and ignores the rest.

**The two shores and the bridge.** The Fiedler vector signs split the dimensions into $\{TEM, DEV, PER\}$ — the dispositional shore: what the person brings — and $\{NEED, ME, DIS, THER, SYS\}$ — the transactional shore: what the person is currently doing with the world. The smallest magnitude by far belongs to personality ($|v_2| = 0.015$, against 0.140 for the next-nearest): **personality is the bridge between constitution and current life**, sitting almost exactly on the graph's principal fault line. The model thus *derives* what personality theory has long asserted of itself — that traits are where biography and biology meet transaction (McAdams & Pals, 2006\*; Hampson, 2012) — as a spectral coordinate.

**The engine and the brake.** Signed cycle analysis on the case-effective matrix (Section 8) ranks the loops. The strongest self-amplifying loops are need frustration feeding negative valuation and back (NEED→ME→NEED, gain +0.400), negative expression eroding the environment that then re-thwarts (ME→SYS→ME, +0.330), and niche-building (PER→SYS→PER, +0.300; DEV→PER→SYS→DEV, +0.294). The strongest regulating loops all pass through treatment: DIS→THER→DIS (−0.455), ME→DIS→THER→ME (−0.273), DIS→THER→SYS→DIS (−0.252). The composed model says, from structure alone: the engine of deterioration is the needs–valuation loop amplified by environmental transaction, and the only strong brake in the architecture is the treatment loop — which exists *because the model includes help-seeking as an edge*, not as an afterthought.

---

## 7. The Topographical Model

The project asks for a topographical representation — peaks and valleys, heat maps — "to diagnose precisely and have a topological view of the patient." The formal construction is a direct composition of the two node quantities distinguished in Section 5.

**Definition (state landscape).** Give each node $i$ a position $p_i$ in the plane (the published layout of Figure J1 at dimension level; any fixed layout at full resolution) and define the elevation field

$$h(p) = \sum_{i} x_i(t)\, K(\lVert p - p_i \rVert),$$

with $K$ a smoothing kernel. Peaks are regions of concentrated activation — *where the person hurts*, when $x$ is encoded as problem load. Valleys are low-activation regions — *where resources and slack lie*. Plateaus are diffuse load; a landscape's total volume is overall burden; and the *same* person under different conditions is the same terrain differently flooded (Figure J3a–b). The complementary flat view is the heat-map profile — dimensions × conditions, each cell an activation (Figure J3c) — which is the landscape's table form and the natural monitoring display.

**Definition (dynamic landscape).** Where the state landscape shows the present, the attractor landscape shows the possible: fixed points of the iterated map are the basins the terrain funnels into, their spectral radii are the basin walls' steepness, and a bifurcation diagram (Figure J5b) is a cross-section through the landscape as a parameter varies. Peaks and valleys in the *state* landscape say where the person is loaded; attractors in the *dynamic* landscape say where the person is headed and how hard it will be to leave. TND uses both.

Two properties make the topographic readout more than a visualization. It is **lossless with respect to the profile** (the landscape is computed from $x$, and $x$ is recoverable from node elevations), so nothing diagnostic is hidden in the picture; and it is **comparable across persons and occasions** (same layout, same kernel, same scale), so landscapes can be differenced, averaged, and tracked. A person's course through treatment is literally the erosion of their peaks (compare Figure J3a with J3b); relapse risk is literally a deepening basin.

![**Figure J3.** The topographical readout of the worked case. (a) Untreated landscape: peaks at disorder, motivation–emotion, and needs, on a high plateau extending to the environment. (b) The same terrain after structure-changing intervention plus maintenance: peaks eroded, valleys restored. (c) The heat-map profile of the same four conditions (fixed-point activations from the verification code).](../figures/figJ3_topography.png)

---

## 8. Topographic Network Diagnosis, With a Worked Case

### 8.1 The case

To demonstrate the diagnostic method end-to-end with no hidden steps, we construct a synthetic case at dimension resolution. *Sara, 16, presents with social withdrawal and persistent distress. Constitutionally high negative affectivity (TEM standing input 0.35); a developmental history of instability (DEV 0.30); ongoing family conflict and economic strain (SYS 0.30). No current treatment.* In the model: a standing-condition vector $b$ with those three entries, dynamics $x(t+1) = \tanh(\kappa(Bx(t) + g\,u(t)) + b)$ over the seven endogenous dimensions, where $B$ is the dimension-level coupling matrix in the problem-load frame, $g$ the treatment gain vector (the six THER edges), $u$ the treatment intensity, and $\kappa = 0.42$ the global coupling. Every number below is printed by `verify_math.py`.

**Where she is.** The untreated system settles, from any starting state, into a single fixed point: TEM 0.51, DEV 0.63, PER 0.57, NEED 0.70, ME 0.72, **DIS 0.77**, SYS 0.72 — the landscape of Figure J3a, with spectral radius $\rho(J) = 0.486$: a *stable* configuration. The diagnosis is not "Sara has social anxiety disorder"; it is "Sara's system is settled in a high-load configuration whose peaks are disorder, valuation, and needs, held there by her standing conditions."

**Why she is there.** The loop ranking (Section 6) names the mechanism: the frustration–valuation engine (+0.400) running on top of environmental thwart, with no treatment loop yet engaged. The bifurcation analysis adds the deeper structural fact: $\lambda_{\max}(B) = 2.195$, so the critical coupling is $\kappa^{*} = 0.456$, and Sara's $\kappa = 0.42 = 0.92\,\kappa^{*}$. A person with her coupling but *no standing load* ($b=0$) would sit quietly at baseline — below threshold, perturbations decay; the same person coupled 30% more tightly would sustain activation with no adversity at all (at $\kappa = 0.592$, self-sustained activation of 0.89 from near-zero starts; Figure J5b). Sara's standing load *unfolds* the pitchfork: her system is monostable-high — pinned, not trapped. The distinction is diagnostic gold, because the two conditions respond to different levers.

**What moves her.** Treatment as state-shifting control: at $u = 0.5$, DIS falls to 0.58; at $u = 0.8$, to 0.25, with the whole profile decompressing (Figure J3c, row 2). But $\rho(J)$ *rises* toward the healthy state — 0.486 → 0.664 → 0.839 — the treated configuration is nearer its basin boundary, formally capturing **fragile remission** and the critical-slowing-down signature that predicts transition risk (van de Leemput et al., 2014\*). And indeed, withdraw treatment and the system returns exactly to DIS 0.77 (Figure J5a): in a monostable-high system, state-shifting alone cannot hold. Durable change must rewrite structure: after edge surgery — the consolidated learning that therapy aims at (regulation acquired: ME→DIS 0.60→0.35; frustration–appraisal coupling softened: NEED→ME 0.80→0.50; symptom self-maintenance broken: DIS self-loop 0.30→0.20; family intervention: the SYS channels and standing input reduced) — the *untreated* fixed point drops to DIS 0.68, and with a maintenance dose ($u = 0.3$) to **0.53**, the landscape of Figure J3b. Honestly: residual load persists. Constitution and history are not erased, and the model refuses to pretend otherwise.

![**Figure J5.** (a) State-shifting versus structure-changing intervention: treatment drives the state down; withdrawal returns it; edge surgery plus maintenance holds it. (b) The composed system inherits the loop-gain bifurcation: with no standing load the quiescent state destabilizes at $\kappa^{*} = 1/\lambda_{\max}(B) = 0.456$; standing load unfolds the pitchfork into a monostable-high regime — pinned, not trapped.](../figures/figJ5_control_bifurcation.png)

### 8.2 The method

Topographic Network Diagnosis (TND) is the generalization of what Section 8.1 just did (Figure J4). Its seven steps: **(1) Instantiate** — select measures for the model's published nodes (interview, standard scales, EMA where available); at minimum the eight dimension activations, at best the full 253. **(2) State** — estimate $x(t)$; repeat to obtain trajectories. **(3) Structure** — begin from the consensus $\bar{W}$ (all persons) and personalize edges from repeated states via W7. **(4) Topography** — compute the landscape and profile; read peaks, valleys, plateaus. **(5) Mechanics** — rank loops by signed gain, find bridges by $|v_2|$, locate the person on the learned axes $z(t)$. **(6) Dynamics** — find the attractor, its $\rho(J)$, the distance to basin boundaries; forecast. **(7) Control** — rank interventions by expected effect: drive $x$ (acute treatment, $u$), rewrite $W$ (skills, consolidation, edge surgery), or change context ($c$ and the SYS channels); output a monitoring plan that re-enters at step 2. Diagnosis, on this method, is a loop with the same shape as care itself.

![**Figure J4.** Topographic Network Diagnosis: the seven-step workflow, with each step's nearest analogue in existing practice. Outcome monitoring re-enters at step 2.](../figures/figJ4_tnd_workflow.png)

The output is a **topographic formulation**: a landscape (where the load is), a mechanism list (which loops hold it there, with gains), a dynamic classification (settled/pinned/trapped/fragile, by attractor structure and $\rho$), and a ranked control plan (state, structure, or context levers). A categorical label, where needed for communication or administration, is recoverable as a *region* of the landscape — "internalizing peak with needs-plateau" contains DSM social anxiety and much of its comorbidity — but the label is a summary of the formulation, never its substitute. Because every step is a fixed function of the inputs, two assessors with the same measurements produce the same formulation up to measurement error (Section 10 develops this as inter-rater reliability by construction); because the gates travel with the edges, the same protocol serves a child (heavily gated caregiving and maturation edges), an adult, and an elder; and because neurodivergence enters as a *different weight topology* rather than a deviation score, the method describes rather than pathologizes atypical architectures — disorder is a landscape region and a dynamic regime, not a departure from a single norm.

---

## 9. One Theory, Not Eight: The Harmonization Ledger

A composition of eight literatures invites soup. The defense is a short list of hard rules, applied everywhere, with the one conflict they surfaced documented rather than hidden. (i) **One formalism**: every stratum is a signed weighted gated graph and nothing else; theories that would not state themselves in that form contributed content to nodes and edges, never a second formalism. (ii) **One axiom set**: the five axioms hold in every stratum and in the composed object (Section 4.4 is the proof by audit). (iii) **One weight scale and one sign convention**: Section 5's anchors and algebraic signs. Harmonization surfaced exactly one inconsistency worth reporting: the systems stratum had signed several social-determinant edges by *wellbeing valence* (adversity marked negative) where the motivation–emotion stratum signed by *activation algebra* (adversity into a disorder interface marked positive, since it raises disorder activation). Composition restates all dimension-level signs algebraically (W3), and the dimension registry's provenance column records each restatement. (iv) **One hierarchy discipline**: encapsulation with mother/interface routing, audited in code. (v) **One provenance regime**: every edge sourced, asterisks for beyond-library sources, priors never silently promoted to estimates. Coherence here is not an aesthetic judgment; it is the conjunction of five checkable properties, and all five are checked.

---

## 10. Reliability and Validity

The series's claim is not that the Eight-Dimension model is finished; it is that the model is *more testable* than its rivals, and already passes the tests that can be run before data collection. We take reliability first, then validity, then the comparison.

### 10.1 Reliability

**Inter-rater reliability by construction.** Given the same measurements, TND's formulation is the output of a fixed, published function — the same $W$, the same equations, the same code. Disagreement between assessors reduces to disagreement in measurement, which is where a century of psychometrics already works. This is the deterministic property the project's trainable-agent requirement demands (an agent instantiated on the model returns the same formulation for the same case), and it is a property *no* verbal diagnostic culture possesses: DSM field trials' categorical reliability was famously poor for common diagnoses (test–retest κ around .28 for major depressive disorder and .20 for generalized anxiety disorder in DSM-5 field trials; Regier et al., 2013\*), precisely because verbal criteria leave the combination function inside the clinician's head.

**Test–retest reliability by design.** The model *separates* what should be stable from what should move: $W$ is slow (structure; its stability is an empirical prediction, W7's update bounds its drift), $x(t)$ is fast (state; its movement is signal, not error), and the gates say which changes with age are expected. A framework that predicts *which of its own quantities should replicate* converts test–retest reliability from a hope into a hypothesis.

**Internal consistency.** The axiom audit (Section 4.4) and the encapsulation audit (zero violations) are internal-consistency checks that run in seconds and re-run on every future revision. The verification code reproduces every number in this article; the figures are generated from the same functions.

### 10.2 Validity

**Content validity.** The node set descends from the consensus documents of eight literatures — HiTOP's hierarchy for disorder (Kotov et al., 2017, 2021), the common-factors and workflow evidence for therapy (Frank & Frank, 1991\*; Wampold & Imel, 2015; APA Presidential Task Force, 2006), the shared core of developmental theory (Berk, 2018; Masten & Cicchetti, 2010\*), the Big Five with facets plus adaptations and narrative (McCrae & Costa, 2008\*; McAdams & Pals, 2006\*), the reactivity/regulation consensus in temperament (Rothbart, 2011; Chess & Thomas, 1989), the seven-domain needs core with dual channels (Ryan & Deci, 2000\*; Sohrabi et al., 2021), the one-process-two-readouts synthesis in motivation–emotion (Buck, 1985; Rolls, 2025; Berridge, 2018), and the nested-systems consensus with state and economy included (Bronfenbrenner, 1977; Mani et al., 2013; Siegel, 2008). Domain coverage is the widest of any formal model we know of; the comparison table makes this concrete.

**Structural validity.** Within strata, the hierarchies mirror the quantitative consensus (the disorder stratum *is* the HiTOP architecture as a graph). Across strata, Section 6's derivations function as structural checks the model could have failed: had the Fiedler partition cut through the middle of a stratum, or $\lambda_2$ come out near zero (a person separable into independent modules), the composition would have contradicted the holism it assumes. It did neither.

**Convergent validity.** The composed couplings recover, without being asked, the field's replicated cross-domain findings: temperament dimensions as developmental cores of neuroticism, extraversion, and conscientiousness (Rothbart, 2011; Caspi et al., 2005\*); trait liabilities for internalizing and externalizing (Kotov et al., 2010\*); need frustration as a transdiagnostic vulnerability (Vansteenkiste & Ryan, 2013\*); scarcity's capture of appraisal (Mani et al., 2013; Shah et al., 2018); therapy's common-factor efficacy and its regulation pathway (Wampold & Imel, 2015; Gross, 1998\*; Moutoussis et al., 2017).

**Discriminant validity.** Encapsulation enforces it architecturally: strata remain distinct subsystems with published boundaries, so the model cannot quietly collapse needs into personality or temperament into disorder — the off-diagonal blocks of Figure J2 are sparse *by theory*, and the audit keeps them so.

**Criterion validity — concurrent and predictive.** Untested as yet, and stated as predictions: dimension activations estimated by TND should track validated instruments concurrently (DIS with p-factor indicators, NEED frustration with need-satisfaction scales, and so on); prospectively, $\rho(J)$ rising toward 1 should predict transition and relapse (the critical-slowing prediction; van de Leemput et al., 2014\*), loop-gain rankings should predict which mechanisms mark maintenance versus recovery, and TND-guided target selection should beat monitoring-as-usual in outcome trials. Each is a falsifier: stable $\rho$ before relapse, or loops that rank high but never mark maintenance, or no incremental benefit over measurement-based care, would break the model where it claims the most.

**Incremental and ecological validity.** Incremental: what the model adds over each rival is exactly the column set of Table 2 — no rival offers mechanism, dynamics, environment, treatment, and development in one formal object. Ecological: the systems stratum places the person's actual settings — family, school, work, services, state policy, economy — *inside* the model with signed edges, rather than as "context" acknowledged in prose; assessment can therefore represent a person whose main problem is their environment without locating the pathology in the person, which no purely intrapsychic nosology can do.

### 10.3 Comparison with existing systems

**Table 2.** *The Eight-Dimension model against existing diagnostic and research frameworks.*

| Property | DSM-5 | ICD-11 | HiTOP | RDoC | Symptom networks | Eight-Dimension / TND |
|---|---|---|---|---|---|---|
| Basic unit | category | category | dimension | construct × unit of analysis | symptom node | node in stratified graph |
| Structure between units | comorbidity (unmodeled) | comorbidity (unmodeled) | hierarchy (loadings) | matrix (unweighted) | weighted edges, one domain | signed weighted gated edges, eight domains |
| Person-specific? | no | no | profile only | no | yes (idiographic networks) | yes (state + personalized W) |
| Mechanism of maintenance | none | none | none | implicit | loops (within symptoms) | loops across all strata, signed gains |
| Dynamics / prognosis formal? | no | no | no | no | emerging | attractors, ρ(J), bifurcations |
| Environment in the model? | axis notes | contextual codes | no | environmental unit, unweighted | rarely | full stratum with signed edges |
| Treatment in the model? | no | no | no | no | no | full stratum; six levers + entry loop |
| Development / all ages? | age variants | age variants | provisional | developmental unit | no | time gates on every edge |
| Reliability locus | clinician judgment (κ ≈ .2–.6) | clinician judgment | instrument | instrument | estimation | fixed function of measurements |
| Falsifiable at edge level? | no | no | loadings | partially | yes | yes, every edge published |
| Openly recomputable? | no | no | partially | no | per-study | fully (code + registries) |

The table's point is not triumphalism — the three rightmost properties of the last column are exactly the ones with the least empirical support behind them today — but *location*: the model is the only entry that is simultaneously a nosology (via landscape regions), a formulation method (via loops and topography), a prognostic model (via dynamics), and a treatment planner (via control), and it purchases that unification with assumptions (priors, time-scale separation, dimension-level coarse-graining) that are all published and all revisable.

### 10.4 The validation roadmap

Inherited from the base framework and now concrete: **Layer 1, method recovery** — simulate persons from known $W$, $B$, gates; verify that TND's pipeline recovers structure, loops, attractors, and control rankings under realistic noise, sampling, and missingness. **Layer 2, retrospective validation** — fit the model to existing intensive-longitudinal and cohort data (experience-sampling depression datasets; ABCD for developmental gates; RADAR-MDD for relapse dynamics); test the concurrent and predictive claims of Section 10.2. **Layer 3, prospective validation** — three-arm pragmatic trials (care as usual / measurement-based care / TND-guided care), because structured measurement alone already improves outcomes and the model must beat that bar, not merely the unaided clinician. Until Layer 2 returns, every weight in this article is a prior and every clinical statement a hypothesis; the model's virtue is that this sentence can be written precisely.

---

## 11. The Formal Limit, Kept

Batch I fixed the precise sense in which Gödel's theorems bear on this project, and composition does not weaken it — it strengthens its relevance, because the Great Graph now explicitly contains a self-modeling agent: the person's endogenous control $u^{\text{self}}$ is generated *about* the very system the model describes, and the therapy stratum models the modeling of the person. A formal system expressive enough to represent such self-reference cannot be simultaneously consistent and complete (Gödel, 1931\*; Batch I §6.3). The design response is unchanged and now fully instantiated: the model prioritizes **consistency** (one axiom set, audited on the composed object) and **openness** (every edge versioned, revisable, and awaiting estimation; a stated procedure for adding strata) over completeness, and its outputs are decision support under uncertainty, never oracular. The practical corollary reaches the trainable-agent requirement: an agent trained on the model is deterministic *given the model's current state* — same case, same formulation — while the model itself remains an open system that revises under evidence. Determinism of application, openness of theory: that pair, not omniscience, is what consistency buys, and it is also the pair that protects the human authenticity and freedom the project requires — the model formalizes will as the person's own control signal (base framework), and a formalism that includes the person's agency as an input cannot, on pain of violating its own equations, treat the person as a mere output.

---

## 12. Limitations, Ethics, and What Remains

The limitations are the honest core of the contribution. **Priors, not estimates**: all 522 weights are consensus priors; the model's numerical results (fixed points, gains, thresholds) demonstrate the machinery, not measured persons; Layer-2 estimation may revise edges substantially, and the framework is built so that it can. **Coarse-graining**: the dimension-level dynamics assume within-stratum equilibration is fast; where it is not (e.g., slow personality change interacting with fast affect), full-resolution simulation is required, and the composed data files support it. **Identification**: person-specific $W$ estimation is unstable in realistic clinical sampling (base framework; Epskamp et al., 2018\*), which is why TND personalizes *from* a strong prior rather than estimating freely, and why centrality-style results are never treated as automatic intervention targets (Rodebaugh et al., 2018\*). **Measurement**: the 253 nodes are unevenly instrumented; several (esp. systems-stratum constructs) lack good idiographic measures, and building them is unglamorous, necessary work. **Ethics**: a model that maps a person's needs, environment, and control capacity can serve care or surveillance; the digital-phenotyping consensus applies in full — data minimization, per-stream consent, reviewable outputs, fairness audits, and a hard prohibition on graph-derived outputs as sole determinants of coercive action (Martinez-Martin et al., 2021\*). The model's own systems stratum, which contains the state's power over the person as signed edges, should be read as the theory warning about its own misuse.

What remains is use. Batch K addresses the five W's and H of application — for the therapist and psychiatrist in the room, for the patient reading their own landscape, and for the person with no diagnosis who wants a map of their own functioning.

---

## 13. Conclusion

Ten articles ago this project promised a grand theory that would not be a metaphor. The promise is now an object: 253 nodes, 522 edges, five axioms audited true, one axiom set, one formalism, every number derivable from files any reader can open. The eight dimensions answer the eight questions a person can be asked; the composition holds them together exactly as tightly as the evidence warrants and no tighter; the topography turns the state of a whole person into a landscape a clinician can read at a glance and a patient can recognize as themselves; the diagnosis it supports outputs mechanisms and levers instead of labels; and the whole construction is falsifiable edge by edge, which is the only kind of grand theory worth introducing to the world. The Great Graph is not the end of the series' work — it is the beginning of the model's: estimation, trial, revision, and use. The last article shows how to use it.

---

## References

American Psychological Association Presidential Task Force on Evidence-Based Practice. (2006). Evidence-based practice in psychology. *American Psychologist, 61*(4), 271–285. https://doi.org/10.1037/0003-066X.61.4.271

Berk, L. E. (2018). *Development through the lifespan* (7th ed.). Pearson.

Berridge, K. C. (2018). Evolving concepts of emotion and motivation. *Frontiers in Psychology, 9*, Article 1647. https://doi.org/10.3389/fpsyg.2018.01647

Borsboom, D. (2017). A network theory of mental disorders. *World Psychiatry, 16*(1), 5–13. https://doi.org/10.1002/wps.20375 \*

Bronfenbrenner, U. (1977). Toward an experimental ecology of human development. *American Psychologist, 32*(7), 513–531. https://doi.org/10.1037/0003-066X.32.7.513

Buck, R. (1985). Prime theory: An integrated view of motivation and emotion. *Psychological Review, 92*(3), 389–413. https://doi.org/10.1037/0033-295X.92.3.389

Buss, D. M. (1987). Selection, evocation, and manipulation. *Journal of Personality and Social Psychology, 53*(6), 1214–1221. https://doi.org/10.1037/0022-3514.53.6.1214 \*

Caspi, A., Roberts, B. W., & Shiner, R. L. (2005). Personality development: Stability and change. *Annual Review of Psychology, 56*, 453–484. https://doi.org/10.1146/annurev.psych.55.090902.141913 \*

Chess, S., & Thomas, A. (1989). Temperament and its functional significance. In S. I. Greenspan & G. H. Pollock (Eds.), *The course of life: Vol. 2. Early childhood* (pp. 163–227). International Universities Press.

Dickerson, A., & Popli, G. K. (2016). Persistent poverty and children's cognitive development: Evidence from the UK Millennium Cohort Study. *Journal of the Royal Statistical Society: Series A (Statistics in Society), 179*(2), 535–558. https://doi.org/10.1111/rssa.12128

Dohrenwend, B. P., Levav, I., Shrout, P. E., Schwartz, S., Naveh, G., Link, B. G., Skodol, A. E., & Stueve, A. (1992). Socioeconomic status and psychiatric disorders: The causation–selection issue. *Science, 255*(5047), 946–952. https://doi.org/10.1126/science.1546291 \*

Eells, T. D. (Ed.). (2022). *Handbook of psychotherapy case formulation* (3rd ed.). Guilford Press.

Epskamp, S., Borsboom, D., & Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. *Behavior Research Methods, 50*(1), 195–212. https://doi.org/10.3758/s13428-017-0862-1 \*

Érdi, P., Sen Bhattacharya, B., & Cochran, A. L. (Eds.). (2017). *Computational neurology and psychiatry*. Springer.

Fiedler, M. (1973). Algebraic connectivity of graphs. *Czechoslovak Mathematical Journal, 23*(2), 298–305. \*

Frank, J. D., & Frank, J. B. (1991). *Persuasion and healing: A comparative study of psychotherapy* (3rd ed.). Johns Hopkins University Press. \*

Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. *Monatshefte für Mathematik und Physik, 38*, 173–198. https://doi.org/10.1007/BF01700692 \*

Gross, J. J. (1998). The emerging field of emotion regulation: An integrative review. *Review of General Psychology, 2*(3), 271–299. https://doi.org/10.1037/1089-2680.2.3.271 \*

Hampson, S. E. (2012). Personality processes: Mechanisms by which personality traits "get outside the skin." *Annual Review of Psychology, 63*, 315–339. https://doi.org/10.1146/annurev-psych-120710-100419

Hull, C. L. (1943). *Principles of behavior: An introduction to behavior theory*. Appleton-Century-Crofts. \*

Jordans, M. J. D. (2025). Applying systems theory to global mental health. *Cambridge Prisms: Global Mental Health, 12*, e2. https://doi.org/10.1017/gmh.2024.147

Kenrick, D. T., Griskevicius, V., Neuberg, S. L., & Schaller, M. (2010). Renovating the pyramid of needs: Contemporary extensions built upon ancient foundations. *Perspectives on Psychological Science, 5*(3), 292–314. https://doi.org/10.1177/1745691610369469

Kotov, R., Gamez, W., Schmidt, F., & Watson, D. (2010). Linking "big" personality traits to anxiety, depressive, and substance use disorders: A meta-analysis. *Psychological Bulletin, 136*(5), 768–821. https://doi.org/10.1037/a0020327 \*

Kotov, R., Krueger, R. F., Watson, D., Achenbach, T. M., Althoff, R. R., Bagby, R. M., Brown, T. A., Carpenter, W. T., Caspi, A., Clark, L. A., Eaton, N. R., Forbes, M. K., Forbush, K. T., Goldberg, D., Hasin, D., Hyman, S. E., Ivanova, M. Y., Lynam, D. R., Markon, K., ... Zimmerman, M. (2017). The Hierarchical Taxonomy of Psychopathology (HiTOP): A dimensional alternative to traditional nosologies. *Journal of Abnormal Psychology, 126*(4), 454–477. https://doi.org/10.1037/abn0000258

Kotov, R., Krueger, R. F., Watson, D., Cicero, D. C., Conway, C. C., DeYoung, C. G., Eaton, N. R., Forbes, M. K., Hallquist, M. N., Latzman, R. D., Mullins-Sweatt, S. N., Ruggero, C. J., Simms, L. J., Waldman, I. D., Waszczuk, M. A., & Wright, A. G. C. (2021). The Hierarchical Taxonomy of Psychopathology (HiTOP): A quantitative nosology based on consensus of evidence. *Annual Review of Clinical Psychology, 17*, 83–108. https://doi.org/10.1146/annurev-clinpsy-081219-093304

Kuppens, P., Allen, N. B., & Sheeber, L. B. (2010). Emotional inertia and psychological maladjustment. *Psychological Science, 21*(7), 984–991. https://doi.org/10.1177/0956797610372634 \*

Laszlo, A., & Krippner, S. (1998). Systems theories: Their origins, foundations, and development. In J. S. Jordan (Ed.), *Systems theories and a priori aspects of perception* (pp. 47–74). Elsevier Science.

Lazarus, R. S. (1991). Cognition and motivation in emotion. *American Psychologist, 46*(4), 352–367. https://doi.org/10.1037/0003-066X.46.4.352

Mani, A., Mullainathan, S., Shafir, E., & Zhao, J. (2013). Poverty impedes cognitive function. *Science, 341*(6149), 976–980. https://doi.org/10.1126/science.1238041

Martinez-Martin, N., Greely, H. T., & Cho, M. K. (2021). Ethical development of digital phenotyping tools for mental health applications: Delphi study. *JMIR mHealth and uHealth, 9*(7), Article e27343. https://doi.org/10.2196/27343 \*

Masten, A. S., & Cicchetti, D. (2010). Developmental cascades. *Development and Psychopathology, 22*(3), 491–495. https://doi.org/10.1017/S0954579410000222 \*

Maturana, H. R., Varela, F. G., & Uribe, R. (1974). Autopoiesis: The organization of living systems, its characterization and a model. *BioSystems, 5*(4), 187–196. https://doi.org/10.1016/0303-2647(74)90031-8

McAdams, D. P., & Pals, J. L. (2006). A new Big Five: Fundamental principles for an integrative science of personality. *American Psychologist, 61*(3), 204–217. https://doi.org/10.1037/0003-066X.61.3.204 \*

McClelland, D. C. (1961). *The achieving society*. Van Nostrand. \*

McClowry, S. G., Rodriguez, E. T., & Koslowitz, R. (2008). Temperament-based intervention: Re-examining goodness of fit. *European Journal of Developmental Science, 2*(1–2), 120–135.

McCrae, R. R., & Costa, P. T., Jr. (2008). The five-factor theory of personality. In O. P. John, R. W. Robins, & L. A. Pervin (Eds.), *Handbook of personality: Theory and research* (3rd ed., pp. 159–181). Guilford Press. \*

Mischel, W., & Shoda, Y. (1995). A cognitive-affective system theory of personality: Reconceptualizing situations, dispositions, dynamics, and invariance in personality structure. *Psychological Review, 102*(2), 246–268. https://doi.org/10.1037/0033-295X.102.2.246 \*

Montag, C., Sindermann, C., Lester, D., & Davis, K. L. (2020). Linking individual differences in satisfaction with each of Maslow's needs to the Big Five personality traits and Panksepp's primary emotional systems. *Heliyon, 6*(7), Article e04325. https://doi.org/10.1016/j.heliyon.2020.e04325

Moutoussis, M., Shahar, N., Hauser, T. U., & Dolan, R. J. (2017). Computation in psychotherapy, or how computational psychiatry can aid learning-based psychological therapies. *Computational Psychiatry, 2*, 50–73.

Nagpaul, T., Sidhu, D., & Chen, J. (2021). Food insecurity mediates the relationship between poverty and mental health. *Journal of Poverty, 26*(3), 233–249. https://doi.org/10.1080/10875549.2021.1910102

Regier, D. A., Narrow, W. E., Clarke, D. E., Kraemer, H. C., Kuramoto, S. J., Kuhl, E. A., & Kupfer, D. J. (2013). DSM-5 field trials in the United States and Canada, Part II: Test–retest reliability of selected categorical diagnoses. *American Journal of Psychiatry, 170*(1), 59–70. https://doi.org/10.1176/appi.ajp.2012.12070999 \*

Retzlaff, R., von Sydow, K., Beher, S., Haun, M. W., & Schweitzer, J. (2013). The efficacy of systemic therapy for internalizing and other disorders of childhood and adolescence: A systematic review of 38 randomized trials. *Family Process, 52*(4), 619–652. https://doi.org/10.1111/famp.12041

Roberts, B. W., & DelVecchio, W. F. (2000). The rank-order consistency of personality traits from childhood to old age: A quantitative review of longitudinal studies. *Psychological Bulletin, 126*(1), 3–25. https://doi.org/10.1037/0033-2909.126.1.3 \*

Roberts, B. W., Luo, J., Briley, D. A., Chow, P. I., Su, R., & Hill, P. L. (2017). A systematic review of personality trait change through intervention. *Psychological Bulletin, 143*(2), 117–141. https://doi.org/10.1037/bul0000088 \*

Roberts, B. W., Walton, K. E., & Viechtbauer, W. (2006). Patterns of mean-level change in personality traits across the life course: A meta-analysis of longitudinal studies. *Psychological Bulletin, 132*(1), 1–25. https://doi.org/10.1037/0033-2909.132.1.1 \*

Rodebaugh, T. L., Tonge, N. A., Piccirillo, M. L., Fried, E., Horenstein, A., Morrison, A. S., Goldin, P., Gross, J. J., Lim, M. H., Fernandez, K. C., Blanco, C., Schneier, F. R., Bogdan, R., Thompson, R. J., & Heimberg, R. G. (2018). Does centrality in a cross-sectional network suggest intervention targets for social anxiety disorder? *Journal of Consulting and Clinical Psychology, 86*(10), 831–844. https://doi.org/10.1037/ccp0000336 \*

Rolls, E. T. (2025). Emotion, motivation, reasoning, and how their brain systems are related. *Brain Sciences, 15*(5), Article 507. https://doi.org/10.3390/brainsci15050507

Rothbart, M. K. (2011). *Becoming who we are: Temperament and personality in development*. Guilford Press.

Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist, 55*(1), 68–78. https://doi.org/10.1037/0003-066X.55.1.68 \*

Ryan, R. M., & Deci, E. L. (2017). *Self-determination theory: Basic psychological needs in motivation, development, and wellness*. Guilford Press. \*

Shah, A. K., Zhao, J., Mullainathan, S., & Shafir, E. (2018). Money in the mental lives of the poor. *Social Cognition, 36*(1), 4–19. https://doi.org/10.1521/soco.2018.36.1.4

Siegel, A. W. (2008). Inequality, privacy, and mental health. *International Journal of Law and Psychiatry, 31*(2), 150–157. https://doi.org/10.1016/j.ijlp.2008.02.008

Sohrabi, B., Yazdani, H., Rajabzadeh, A., & Mahjoub, H. (2021). Analysis of the human basic psychological needs' theories: A meta-theory approach. *Journal of Psychological Science, 20*(103), 979–998. https://doi.org/10.52547/JPS.20.103.979

Szapocznik, J., Schwartz, S. J., Muir, J. A., & Brown, C. H. (2012). Brief strategic family therapy: An intervention to reduce adolescent risk behavior. *Couple and Family Psychology: Research and Practice, 1*(2), 134–145. https://doi.org/10.1037/a0029002

Townsend, J. T. (2008). Mathematical psychology: Prospects for the 21st century: A guest editorial. *Journal of Mathematical Psychology, 52*(5), 269–280.

van de Leemput, I. A., Wichers, M., Cramer, A. O. J., Borsboom, D., Tuerlinckx, F., Kuppens, P., van Nes, E. H., Viechtbauer, W., Giltay, E. J., Aggen, S. H., Derom, C., Jacobs, N., Kendler, K. S., van der Maas, H. L. J., Neale, M. C., Peeters, F., Thiery, E., Zachar, P., & Scheffer, M. (2014). Critical slowing down as early warning for the onset and termination of depression. *Proceedings of the National Academy of Sciences, 111*(1), 87–92. https://doi.org/10.1073/pnas.1312114110 \*

Vansteenkiste, M., & Ryan, R. M. (2013). On psychological growth and vulnerability: Basic psychological need satisfaction and need frustration as a unifying principle. *Journal of Psychotherapy Integration, 23*(3), 263–280. https://doi.org/10.1037/a0032359 \*

von Luxburg, U. (2007). A tutorial on spectral clustering. *Statistics and Computing, 17*(4), 395–416. \*

Wampold, B. E., & Imel, Z. E. (2015). *The great psychotherapy debate: The evidence for what makes psychotherapy work* (2nd ed.). Routledge.

Weiner, B. (1985). An attributional theory of achievement motivation and emotion. *Psychological Review, 92*(4), 548–573. https://doi.org/10.1037/0033-295X.92.4.548
