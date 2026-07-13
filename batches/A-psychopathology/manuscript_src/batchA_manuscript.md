# From Categories to Connectivity: A Critical Synthesis of DSM, HiTOP, and ICD and the Derivation of a Universal Disorder Graph

**[Author 1 name], [Author 2 name]**

[Affiliations]

**Author note.** Correspondence concerning this article should be addressed to [corresponding author]. The graph data files, figure-generation code, and all provisional edge weights reported in this article are openly available in the article's supplementary repository. This article is the first in a planned series deriving an integrated, multidimensional network model of psychological functioning.

---

## Abstract

Psychiatric classification currently rests on three partially incompatible foundations. The *Diagnostic and Statistical Manual of Mental Disorders* (DSM-5-TR) offers reliable categorical diagnosis but faces persistent challenges of within-category heterogeneity, between-category comorbidity, and contested validity. The *International Classification of Diseases* (ICD-10/11) prioritizes global clinical utility and public-health applicability, at the cost of formal structure. The Hierarchical Taxonomy of Psychopathology (HiTOP) replaces categories with empirically derived dimensions, yet remains a static architecture of covariation that does not represent the temporal, causal, or self-maintaining dynamics of psychopathology. This article provides a critical synthesis of the philosophy, logic, structure, applications, strengths, and limitations of each system, drawing on the primary literature of each tradition and on their principal critiques. We then argue that the three systems fail in complementary ways, and that their complementary failures specify the design requirements of a successor representation. We derive such a representation: the Universal Disorder Graph (UDG), a hierarchically organized, weighted, signed, dynamic graph in which nodes are dimensional liabilities at four levels of resolution (general factor, superspectra, spectra, subfactors), hierarchical edges carry factor-loading weights, cross-cutting edges carry residual-covariance weights, and self-loops encode the self-maintaining feedback documented in network psychiatry. All structural commitments of the UDG are stated as explicit axioms, all edge weights are published as provisional consensus priors for empirical re-estimation, and a falsification pathway is specified. The UDG is designed as the psychopathology stratum of a broader multidimensional network model of the person, to be developed in subsequent articles in this series.

**Keywords:** psychiatric nosology, DSM-5, HiTOP, ICD-11, network theory, graph theory, dimensional classification, comorbidity

---

## 1. Introduction

The question of how to carve psychological suffering into scientifically defensible and clinically usable units is among the oldest and least settled questions in the mental health field (Boland & Verduin, 2022; Cooper, 2004). It is also among the most consequential. Diagnostic classifications determine who receives treatment and of what kind, what research is funded and how its samples are formed, which conditions insurers reimburse, how courts assign responsibility, how epidemiologists count, and — not least — how millions of people come to understand their own distress (First et al., 2019; Lafrance & McKenzie-Mohr, 2013; Young, 2013). A classification system is never merely a list; it is an implicit theory of what mental disorder *is*, embedded in an institutional apparatus that gives that theory force (Kirschner, 2013; Pickersgill, 2014).

Three systems currently dominate this territory. The American Psychiatric Association's (APA) *Diagnostic and Statistical Manual of Mental Disorders*, in its fifth edition, text revision (DSM-5-TR; American Psychiatric Association [APA], 2022), remains the de facto standard for clinical diagnosis and research operationalization in the United States and much of the research world. The World Health Organization's (WHO) *International Classification of Diseases* (ICD-10 and, progressively, ICD-11) is the legally mandated classification for health statistics in WHO member states and the most widely used system in day-to-day international clinical practice (First et al., 2018; Reed et al., 2019*). The Hierarchical Taxonomy of Psychopathology (HiTOP) is a consortium-built, quantitatively derived dimensional alternative that has, in less than a decade, become the principal scientific challenger to both (Kotov et al., 2017; Kotov et al., 2021).

Each system succeeds at something the others do not. The DSM solved — to a first approximation — the reliability crisis that delegitimized psychiatric diagnosis in the mid-twentieth century (Rief et al., 2013; Regier et al., 2013). The ICD delivers a common statistical language usable by a village health worker and a tertiary research hospital alike (First et al., 2018; Tyrer, 2014). HiTOP recovers, from the covariance structure of symptoms themselves, a hierarchy of dimensions that predicts course, impairment, and treatment response better than the categorical units it replaces (Kotov et al., 2020; Ruggero et al., 2019; Watson et al., 2022). Yet each also fails at something structural. The DSM's categories are heterogeneous within and comorbid between, to a degree that undermines their standing as natural kinds (Cooper, 2004; Forbes, 2023; Wakefield, 1992). The ICD inherits most of these categorical problems while adding few structural innovations of its own (Tyrer, 2014). And HiTOP, for all its empirical rigor, is a *static* architecture: it describes how symptoms covary, not how they cause, maintain, and extinguish one another over time within an individual life (Borsboom, 2017*; Haeffel et al., 2022).

### 1.1 Aim and contribution

This article has two aims. The first is synthetic: to provide an integrated critical review of the theory, philosophy, internal logic, structure, applications, strengths, and weaknesses of the DSM, HiTOP, and the ICD, drawing on the primary documents of each tradition and on four decades of conceptual, empirical, sociological, and clinical critique. Reviews of each system exist separately; what is rarer is a side-by-side analysis oriented by a single design question — namely, *what representational commitments would a classification need in order to keep what each system gets right while discarding what each gets wrong?*

The second aim is constructive. From the comparative analysis we derive a set of design requirements and satisfy them with a formal object we call the **Universal Disorder Graph (UDG)**: a hierarchically organized, weighted, signed, dynamic graph of dimensional liabilities, in which HiTOP's consensus hierarchy supplies the node scaffold, meta-analytic covariance estimates supply provisional edge weights, and the network-theoretic literature supplies the dynamic semantics — directed influence, feedback loops, and self-maintenance — that no current nosology represents (Borsboom, 2017*; Borsboom & Cramer, 2013*; Robinaugh et al., 2020*). The UDG is explicitly axiomatic: its structural commitments are stated as five axioms, its every edge is published with its evidential source, and its weights are declared as provisional priors awaiting re-estimation, so that the object as a whole is reproducible, falsifiable, and free of black-box components.

### 1.2 Novelty and relation to existing programs

Because a central claim of this article is that the UDG occupies unfilled representational territory, we state its relation to neighboring programs at the outset. Network psychiatry models disorders as causal systems of interacting *symptoms*, typically within a single syndrome and a single level of analysis (Borsboom, 2017*; Borsboom & Cramer, 2013*). HiTOP models the *covariance* of symptoms and traits across the full span of psychopathology, but without directionality, feedback, or time (Kotov et al., 2017; Kotov et al., 2021). The National Institute of Mental Health's Research Domain Criteria (RDoC) reorients research toward transdiagnostic neurobehavioral systems but is explicitly a research framework, not a clinical classification, and specifies no formal graph structure (Cuthbert & Insel, 2013*; Insel et al., 2010*). The extended evolutionary meta-model underlying process-based therapy organizes therapeutic change processes across six psychological dimensions but is a conceptual taxonomy — a "periodic table" of processes — without a mathematical object underneath it (Hayes et al., 2020*). Finally, recent proposals to model individual psychopathology as a *dynamic learned graph* equipped with an adjacency matrix, graph Laplacian, and control-theoretic semantics supply exactly the formal machinery the field lacks, but have so far been developed at the level of individual symptom dynamics rather than as a general nosological architecture (Epskamp et al., 2018*; Jones et al., 2021*; Rodebaugh et al., 2018*). To our knowledge, no published system combines (a) a population-level, hierarchical, dimensional node set spanning all major psychopathology, (b) weighted, signed, and directed edges with published evidential provenance, (c) self-loops encoding self-maintenance, and (d) an explicit axiomatization designed for computational implementation. That combination is the contribution of this article, and the psychopathology stratum it yields is the first of eight strata of a broader model of the person developed across this article series.

### 1.3 Method of the review

The synthesis draws on a curated corpus of 64 primary and secondary sources on the DSM (33 items), HiTOP (25 items), and ICD (6 items), assembled to represent each tradition's canonical statements, its major internal reform documents, and its strongest external critiques, supplemented where necessary by literature located through targeted searches (sources so located are marked with an asterisk in the reference list). For each system we ask the same seven questions: What is its history and institutional mandate? What is its philosophy of disorder? What is its formal logic of classification? What is its structure? How is it used? What does the evidence say in its favor? And what are its principal documented failures? Sections 2 through 4 answer these questions for the DSM, HiTOP, and the ICD respectively; Section 5 assembles the comparison; Section 6 derives and formalizes the UDG; Section 7 locates the result in the roadmap of the series.

---

## 2. The DSM: Reliability by Convention

### 2.1 History and philosophical foundations

The DSM's modern history begins not with its first edition (1952) but with its third (1980), which transformed a slim administrative glossary shaped by psychoanalytic assumptions into an operationalized, criterion-based system (Boland & Verduin, 2022; Regier et al., 2013). The immediate provocation was a reliability crisis: studies through the 1960s and 1970s showed that two clinicians assessing the same patient frequently reached different diagnoses, an embarrassment sharpened by demonstrations that diagnostic labels tracked context as much as patient behavior (Rief et al., 2013). DSM-III's solution, associated with the neo-Kraepelinian movement, was to define disorders by explicit inclusion and exclusion criteria, agnostic about etiology — the famous claim to be "atheoretical" (Regier et al., 2013; Widiger & Crego, 2015).

Philosophically, the DSM has always been less atheoretical than advertised. Its architecture presupposes that mental disorders are discrete, syndromal entities — that suffering clusters into kinds that criteria can capture (Cooper, 2004; Kirschner, 2013). Its official definition of mental disorder — a "clinically significant disturbance" reflecting "a dysfunction in the psychological, biological, or developmental processes underlying mental functioning" (APA, 2022) — attempts to naturalize this assumption by anchoring disorder in dysfunction. Wakefield's (1992) harmful dysfunction analysis remains the most influential critique of this anchor: DSM criteria sets operationalize *statistically unexpectable distress or disability*, but distress and disability can arise from perfectly intact response systems facing adverse environments, so the criteria systematically fail to distinguish disorder from non-disordered suffering — the false positives problem (Wakefield, 1992, 2015). Successive definitional revisions from DSM-III to DSM-5-TR have adjusted wording without resolving this core difficulty (Vacca et al., 2025), and the definition plays almost no operative role in the criteria sets themselves, functioning more as a preamble than as an axiom from which the manual's content is derived (Thyer, 2015).

### 2.2 The formal logic: categorical-polythetic classification

Formally, the DSM is a categorical-polythetic system. Each disorder is a category; membership is determined by satisfying *m*-of-*n* criteria (e.g., five of nine symptoms for major depressive episode), plus duration, distress/impairment, and exclusion clauses (APA, 2022). Three structural consequences follow directly from this logic, and all three are extensively documented.

First, *within-category heterogeneity*. Polythetic criteria allow two individuals to share a diagnosis while sharing few or no symptoms; the nine-symptom, five-required structure of major depression alone admits hundreds of distinct symptom profiles, and empirical work confirms that this combinatorial diversity is realized in actual patients (Fried & Nesse, 2015*; Haywood et al., 2024). Second, *artifactual comorbidity*. Because the criteria sets partition a continuous, correlated symptom space with hard boundaries, patients routinely qualify for multiple diagnoses; symptom-level overlap among criteria sets further inflates apparent co-occurrence (Forbes, 2023; Kotov et al., 2017). Third, *boundary arbitrariness*. Thresholds (five of nine rather than four or six; two weeks rather than three) are conventions, defensible pragmatically but not derivable from any theory the manual states (Cooper, 2004; Widiger & Crego, 2015).

### 2.3 Process and content of DSM-5 and DSM-5-TR

The DSM-5 revision (2013) was announced as a potential "paradigm shift" that would align diagnosis with neuroscience and dimensional measurement (Regier et al., 2013). The published manual retreated substantially from that ambition. The planned dimensional reconstruction of personality disorders was relegated to Section III as the Alternative Model for Personality Disorders (AMPD), with the DSM-IV categorical system retained in the main text (Hopwood et al., 2019; Widiger & Crego, 2015). Cross-cutting dimensional measures were included but made optional. Figure 1 (panel A) schematizes the resulting architecture. The revision process itself attracted sustained criticism: confidentiality agreements that limited scholarly scrutiny, inadequate public documentation of evidentiary rationales, missed deadlines and truncated field-trial designs, and reliability results that would once have been considered unacceptable — kappa values around .28 for major depressive disorder and .20 for generalized anxiety disorder in the adult field trials — were defended by relaxed benchmarks (Jones, 2012; Widiger & Crego, 2015). Frances and other insiders warned of diagnostic hyperinflation from lowered thresholds and new categories (Rief et al., 2013; Strong, 2014), and organized opposition — unprecedented in scale — came from the British Psychological Society, APA Division 32, and an international response committee (Kinderman & Cooke, 2017). Audience analysis of the reception shows that critique came not from a single camp but from at least eight distinguishable publics, from reformist scientists to constructivist sociologists (Roy et al., 2019). More balanced retrospectives note that many predicted epidemics of new diagnosis did not materialize and that DSM-5 made real incremental improvements — but they concede the deeper structural critique untouched (Lasalvia, 2015).

The DSM-5-TR (2022) is predominantly a text revision: comprehensively updated descriptive text, one new category (prolonged grief disorder), new symptom codes for suicidal behavior and nonsuicidal self-injury, and a systematic equity and inclusion review (APA, 2022; First et al., 2023). Its most forward-looking element may be institutional rather than scientific: the APA's Future of DSM committee now explicitly discusses elevating functioning and quality of life to essential elements of a complete psychiatric diagnosis — an implicit concession that symptom-count categories under-describe the person (Drexler et al., 2026; Troisi, 2014).

### 2.4 Applications and actual clinical use

Any evaluation of the DSM must reckon with how it is actually used. Survey evidence indicates that clinicians use the manual for far more than billing: as a communication standard among providers, a teaching scaffold for trainees, and an educational instrument for patients and families (First et al., 2019). At the same time, clinicians do not apply the criteria as written: diagnoses assigned in routine practice diverge substantially from those generated by structured interviews, implying that the operational precision that justifies the system scientifically is largely notional at the point of care (First et al., 2014). A global WHO–World Psychiatric Association survey found that most clinicians worldwide prefer flexible diagnostic guidance to strict criteria and routinely use residual ("other/unspecified") categories — behavior that reveals the manual's categories as approximate communicative tools rather than measurement operations (First et al., 2018). This gap between official logic and actual use is itself a finding about the system: the DSM functions socially as a *boundary object* — a shared language that coordinates heterogeneous actors — more than as a scientific instrument (Veldmeijer et al., 2024).

### 2.5 Strengths

The DSM's achievements are real and should be stated without irony. It standardized communication across clinical, research, legal, educational, and administrative settings on a scale no prior psychiatric artifact achieved (First et al., 2019; Regier et al., 2013). It made psychopathology research cumulative by giving investigators common operational targets, underwriting the epidemiology, treatment trials, and measurement literatures on which all successor systems — including HiTOP — are built (Kotov et al., 2017; Rief et al., 2013). Its descriptive texts constitute an encyclopedic clinical reference continuously updated against the literature (APA, 2022; First et al., 2023). And its institutional processes, however criticized, provide something a scientific classification requires and purely academic models lack: a maintained, versioned, accountable standard (Pickersgill, 2014).

### 2.6 Documented weaknesses

The critical literature converges on seven failures. (1) *Validity*: few DSM categories have been validated against etiology, pathophysiology, or even crisp boundaries with adjacent categories or normality; the manual's kinds behave like practical kinds, not natural kinds (Cooper, 2004; Kirschner, 2013). (2) *False positives*: criteria that operationalize distress without dysfunction misclassify normal-range responses to adversity as disorder, inflating epidemiological estimates and pathologizing normality (Wakefield, 1992, 2015). (3) *Heterogeneity and comorbidity*, as derived in Section 2.2 (Forbes, 2023; Fried & Nesse, 2015*; Haywood et al., 2024). (4) *Reification*: categories introduced as conventions harden into entities that patients have and researchers hunt mechanisms for, a category error with clinical and scientific costs (Thyer, 2015; Bradford, 2010). (5) *Medicalization and conflicts of interest*: the manual's expansion has tracked professional and pharmaceutical interests as well as evidence, and its biomedical idiom reshapes how distressed people narrate themselves — offering validation at the price of essentialized identity (Kirschner, 2013; Lafrance & McKenzie-Mohr, 2013; McGuire, 2015; Venkatesan & Suresh, 2022). (6) *Cultural partiality*: despite the DSM-5's cultural formulation interview and the TR's equity review, the system's categories and thresholds remain most valid for the populations on which they were normed (Paniagua, 2018; Roy et al., 2019). (7) *Process opacity*: the DSM-5 development cycle demonstrated that the system's revision machinery can fall short of the transparency expected of a scientific standard (Jones, 2012; Widiger & Crego, 2015). Specific categories illustrate the general points; somatic symptom disorder, for example, was introduced with criteria loose enough to capture large fractions of medically ill and healthy populations, while its differential relations to trauma and dissociation were left unresolved (Ross, 2015).

---

## 3. HiTOP: Validity by Covariance

### 3.1 Origins and philosophy

The Hierarchical Taxonomy of Psychopathology emerged in 2015 from a consortium of quantitative psychopathologists explicitly convened to build a classification from the empirical covariation of symptoms, rather than from committee-negotiated categories (Conway et al., 2022; Kotov et al., 2017). Its philosophical stance is structural realism about dimensions: the recurring factor structure recovered across instruments, samples, cultures, and developmental periods is treated as the best current estimate of the true architecture of psychopathological variation (Kotov et al., 2021). Disorders, on this view, are not entities but regions of a continuous liability space; diagnosis is location, not membership (Hopwood et al., 2018; Kotov et al., 2017).

### 3.2 Structure

The HiTOP working model is a hierarchy of increasingly narrow dimensions. At the apex sits a general factor (*p*) capturing the shared variance of all psychopathology (Caspi et al., 2014*; Kotov et al., 2021). Below it, superspectra: an emotional dysfunction superspectrum encompassing internalizing and somatoform variance (Watson et al., 2022), a psychosis superspectrum encompassing thought disorder and detachment (Kotov et al., 2020), and an externalizing superspectrum encompassing disinhibited and antagonistic externalizing (Krueger et al., 2021*). Below these, six consensus spectra — internalizing, somatoform, thought disorder, detachment, disinhibited externalizing, antagonistic externalizing — plus a provisional neurodevelopmental spectrum (Kotov et al., 2017; Kotov et al., 2021; Stevanovic et al., 2024). Spectra resolve into subfactors (e.g., distress, fear, eating pathology within internalizing; substance abuse and antisocial behavior within disinhibition), subfactors into empirical syndromes, and syndromes into homogeneous symptom components and maladaptive traits (Kotov et al., 2017). The same dimensions organize normal-range personality: HiTOP spectra align closely with maladaptive variants of five-factor model domains, with symptoms and traits distinguished principally by time frame rather than by kind (DeYoung et al., 2022; Watson & Clark, 2020; Widiger & Crego, 2019).

### 3.3 Evidence

Three lines of evidence support the architecture. First, structural: the spectra replicate across community and clinical samples, self- and informant report, cross-sectionally and longitudinally, and in youth as well as adults (Kotov et al., 2021; Stevanovic et al., 2024). Second, validity and utility: World Psychiatry's serial reviews document that spectra and subfactors out-predict categorical diagnoses for course, impairment, suicidality, treatment seeking, and family history, across the psychosis and emotional dysfunction domains (Kotov et al., 2020; Watson et al., 2022), with parallel findings for externalizing (Krueger et al., 2021*). Dimensional scores also rescue the information that categorical thresholds discard: eating-disorder dimensions, for example, predict outcome better than DSM eating-disorder categories (Forbush et al., 2018). Third, mechanism-adjacent: reviews of neurobiological substrates find that transdiagnostic dimensions such as internalizing and disinhibition map more cleanly onto neural and genetic correlates than DSM categories do, though the mapping remains coarse (DeYoung et al., 2024; Mullins-Sweatt et al., 2019; Longenecker et al., 2020).

### 3.4 Measurement and clinical translation

A consortium measurement program is constructing dedicated instruments spectrum by spectrum (Simms et al., 2022), with published preliminary scales for detachment (Zimmermann et al., 2022) and the somatoform spectrum and eating disorders (Sellbom et al., 2022). Clinical-translation papers describe how dimensional profiles replace differential diagnosis with a severity-and-configuration readout, how thresholds can be set pragmatically on continuous scores for reimbursement systems that require categories, and how the profile format supports measurement-based care (Ruggero et al., 2019). Treatment-planning agendas link spectra to intervention selection — e.g., internalizing severity to transdiagnostic emotion-focused protocols, disinhibition to contingency-management approaches (Mullins-Sweatt et al., 2020; Hopwood et al., 2018).

### 3.5 Strengths

HiTOP directly repairs the DSM's three structural failures. Heterogeneity is handled by resolution: profiles at the component level individuate presentations that a category collapses. Comorbidity is handled by explanation: co-occurrence becomes the expected signature of shared higher-order liability rather than an embarrassment (Kotov et al., 2017). Boundary arbitrariness is handled by dimensionalization: severity is measured, not legislated (Ruggero et al., 2019). The model is also self-consciously provisional and revision-friendly — its consensus papers publish their own gaps — and its integration of personality and psychopathology into one structure is a unification the DSM never achieved (Kotov et al., 2021; Watson & Clark, 2020; Ringwald et al., 2019).

### 3.6 Documented weaknesses

The critical literature on HiTOP is younger but pointed. Haeffel et al. (2022) argue that the model over-reads factor analysis: covariance structure is not causal structure, simple-structure solutions are underdetermined by the data, and no trial yet demonstrates that HiTOP-guided care improves outcomes — so claims of clinical readiness outrun the evidence. Developmental critics document that the psychosis superspectrum sits uneasily on developmental data: trait-like schizotypy and state-like clinical high-risk phenomena are conflated, and the hierarchy's cross-sectional derivation obscures developmental sequencing (Poletti et al., 2025; Stevanovic et al., 2024). Diversity analyses show the evidence base over-represents Western, English-speaking, majority-population samples, so measurement invariance across cultures, ethnicities, genders, and sexual-minority status remains partly unestablished (Rodriguez-Seijas et al., 2023). Methodologically, symptom-level overlap among the DSM criteria sets from which HiTOP structures are estimated could partially inflate the covariance the model reifies, although current analyses suggest overlap alone cannot explain the dimensions (Forbes, 2023). Finally — and centrally for our purposes — HiTOP is *static*. Its edges are loadings, not processes: it represents that internalizing symptoms travel together, but not that insomnia drives fatigue, that avoidance maintains fear, or that a symptom system can lock into a self-sustaining state (Borsboom, 2017*; Robinaugh et al., 2020*). A hierarchy of liabilities, however well estimated, is a map of variance, not a mechanism of illness.

---

## 4. The ICD: Utility by Mandate

### 4.1 History and institutional position

The ICD descends from nineteenth-century international mortality statistics and has been maintained by WHO since 1948; mental disorders received a dedicated chapter with ICD-6 and their first systematically described treatment in ICD-8 through ICD-10 (Boland & Verduin, 2022; Hirsch et al., 2016). Unlike the DSM, the ICD is a treaty-level instrument: member states are obligated to report health statistics in its terms, making it the world's default administrative and clinical classification, with the United States' delayed and contentious transition to ICD-10-CM illustrating how deeply the system is woven into payment and health-system infrastructure (Hirsch et al., 2016). Also unlike the DSM, the ICD is free, multilingual, and explicitly designed for use across the full range of world health systems and provider types (First et al., 2018; Tyrer, 2014).

### 4.2 Logic and structure

For its mental and behavioural disorders chapter, ICD-10 issued two texts: the Clinical Descriptions and Diagnostic Guidelines (CDDG) for clinical use, built on prototype descriptions with flexible guidance, and the Diagnostic Criteria for Research (DCR), with operational criteria approximating DSM style (Paniagua, 2018; Tyrer, 2014). This dual-text strategy encodes the ICD's core philosophy: clinical utility first. Prototype-based guidance matches how clinicians actually think — global pattern recognition rather than criterion counting — and the global survey evidence confirms clinicians' preference for exactly this format (First et al., 2018). The cost is the mirror image of the benefit: prototype diagnosis is less reliable at the margins, and the CDDG/DCR split institutionalizes a gap between clinical and research diagnosis within the same system (Tyrer, 2014). ICD-11's mental disorders chapter, developed with systematic field studies, retains the clinical-utility-first philosophy while modernizing content — most notably a fully dimensional personality-disorder model organized around severity, an addition of complex PTSD, and closer (though incomplete) harmonization with DSM-5 (Garabiles et al., 2023; Reed et al., 2019*). Comparative psychometric work shows the two lineages' remaining divergences are consequential: DSM-5 and ICD-11 PTSD models, for instance, identify overlapping but non-identical patient groups, with the leaner ICD-11 model showing better fit and the broader DSM-5 model stronger associations with transdiagnostic symptoms (Garabiles et al., 2023).

### 4.3 Cultural scope

The ICD's cultural positioning differs from the DSM's in instructive ways. The DSM-5 provides a cultural formulation interview and disorder-specific cultural notes; ICD-10's core texts are comparatively silent on culture, delegating cultural adaptation to national modifications and clinical judgment (Paniagua, 2018). Neither strategy is fully adequate: explicit cultural apparatus embedded in a fundamentally Western category system risks tokenism, while silence risks unexamined universalism (Paniagua, 2018; Rodriguez-Seijas et al., 2023). The deeper issue — whether the *dimensional structure* of psychopathology, not merely its expression, is invariant across cultures — is an open empirical question for all three systems (Rodriguez-Seijas et al., 2023).

### 4.4 Strengths and weaknesses

The ICD's strengths are its mandate, reach, accessibility, and clinical realism: it is the only classification designed to function in every health system on earth, and the only one whose diagnostic format is empirically matched to clinician cognition (First et al., 2018). Its weaknesses are correspondingly structural. It shares the DSM's categorical logic and therefore the same heterogeneity, comorbidity, and validity problems (Tyrer, 2014). Its clinical-utility-first design trades measurement precision away at exactly the point where science needs it, and its research criteria have historically been under-used relative to DSM criteria, leaving the research base concentrated in the rival system (Tyrer, 2014). Its harmonization with DSM remains partial, so the field's two categorical standards still disagree about the boundaries of major conditions (Garabiles et al., 2023; Regier et al., 2013). And it has, to date, incorporated dimensionality only piecemeal (personality disorders in ICD-11), leaving its overall architecture categorical (Reed et al., 2019*).

---

## 5. Comparative Synthesis: Three Systems, Three Complementary Failures

### 5.1 A design-oriented comparison

Table 1 assembles the comparison developed in Sections 2–4. Read column-wise, it describes three systems; read row-wise, it describes a division of labor that no single system spans.

**Table 1.** *Comparative analysis of DSM-5-TR, ICD-10/11, and HiTOP.*

| Dimension of comparison | DSM-5-TR | ICD-10/11 | HiTOP |
|---|---|---|---|
| Governing institution | American Psychiatric Association | World Health Organization | Research consortium |
| Primary constituency | US/research clinicians, insurers, courts | Global health systems, states | Quantitative psychopathology |
| Unit of classification | Categorical disorder (polythetic criteria) | Categorical disorder (prototype guidance; ICD-11 PD dimensional) | Continuous dimension (hierarchical) |
| Philosophy of disorder | Syndromal realism, officially atheoretical | Pragmatic clinical utility | Structural realism about dimensions |
| Formal logic | m-of-n criterion counting | Prototype matching (CDDG) / criteria (DCR) | Location in factor space |
| Chief virtue | Inter-rater reliability; operational research targets | Global reach, utility, accessibility | Validity; predictive power; parsimony for comorbidity |
| Chief structural failure | Heterogeneity, comorbidity, false positives, reification | Same categorical failures; research under-use | Static; no causal/temporal semantics; unproven clinical benefit |
| Comorbidity treatment | Multiplied diagnoses | Multiplied diagnoses | Explained by shared liability |
| Time and dynamics | Course specifiers only | Course specifiers only | Absent (cross-sectional covariance) |
| Individual formulation | Not represented | Not represented | Profile, but static |

![**Figure 1.** The three classification architectures. (A) DSM-5-TR: discrete categorical disorders defined by polythetic criteria, with no formal between-category structure. (B) ICD-10/11: a clinical-descriptive tree under a global public-health mandate. (C) HiTOP: continuous dimensions organized hierarchically, with comorbidity modeled as shared higher-order liability.](../figures/fig1_three_systems.png)

### 5.2 The complementarity argument

The pattern in Table 1 supports a stronger claim than "each system has pros and cons." The three systems fail *complementarily*: each fails precisely where another succeeds, and one failure is shared by all three.

The DSM and ICD share the categorical failure; HiTOP repairs it. HiTOP lacks an institutional mandate and global clinical apparatus; the DSM and ICD have both. The DSM's operational precision serves research; the ICD's prototype flexibility serves worldwide practice; HiTOP's dimensions serve validity. These strengths are not in conflict — a dimensional structure can be given categorical reporting thresholds (Ruggero et al., 2019) and prototype-style clinical descriptions (First et al., 2018) — which is why the field's actual trajectory is convergent: DSM-5 introduced dimensional cross-cutting measures and the AMPD (Hopwood et al., 2019), ICD-11 dimensionalized personality disorder (Reed et al., 2019*), and HiTOP publishes clinical crosswalks to both (Kotov et al., 2021; Ruggero et al., 2019).

But the shared failure remains: *none of the three represents psychopathology as a process*. All three are, in different idioms, atemporal summaries of symptom aggregation. None can express the clinical commonplaces that motivate treatment: that this patient's insomnia is driving her concentration failure; that his avoidance is maintaining his fear; that her drinking, initiated by distress, now sustains the distress that initiated it; that a system pushed past a tipping point can remain ill after the stressor resolves (Borsboom, 2017*; van de Leemput et al., 2014*). The network-theoretic literature has built exactly these semantics — direct symptom-symptom interaction, feedback, hysteresis, early-warning dynamics — but at the scale of individual syndromes and datasets, without a nosological architecture (Borsboom & Cramer, 2013*; Robinaugh et al., 2020*). The design requirement is therefore explicit: a successor representation must inherit HiTOP's validated node hierarchy, remain crosswalk-compatible with DSM/ICD categories, and equip the whole with the dynamic, causal semantics of network theory — under published, reproducible, falsifiable structural commitments.

Section 6 constructs that object.

---

## 6. The Universal Disorder Graph

### 6.1 Axiomatic foundation

The UDG is defined by five axioms, adopted for the model series as a whole. They are stated here as structural commitments about psychological modules (nodes) and their influences (edges); their satisfaction by the psychopathology stratum is shown in Section 6.2.

- **Axiom 1 (Universal connectivity).** Every psychological module can influence other modules; influences may be unidirectional or reciprocal.
- **Axiom 2 (Non-dismissibility).** No module's role may be set to zero a priori in the formulation of a person; absence of influence is an empirical finding, not a modeling assumption.
- **Axiom 3 (Mediated and unmediated influence).** Any influence between two modules may be direct or may pass through mediating modules; both routes are representable.
- **Axiom 4 (Self-influence).** Every module can influence itself; self-loops are first-class edges.
- **Axiom 5 (Signed superposition).** Influences carry sign and magnitude; concurrent influences on a module combine additively, so that reinforcement and attenuation are both expressible.

These axioms are deliberately weak — they assert representability, not particular causal claims — and jointly they are satisfiable by a weighted, signed, directed graph with self-loops, which is the mathematical object chosen. Consistency is therefore immediate: the axioms are realized by a concrete model, so no contradiction can be derived from them. We note, with care, a humility principle suggested by Gödel's incompleteness theorems (Gödel, 1931*): any formal system rich enough to be interesting cannot certify its own completeness from within. We invoke this not as a mathematical result about the UDG (whose axioms are far weaker than arithmetic) but as a design analogy with a concrete implication: the UDG is constructed as an *open* architecture whose node set and edge set are explicitly revisable from data outside the current model, rather than as a closed system claiming to already contain every psychopathological phenomenon. The formal development of the framework's mathematical substrate — state vectors, Laplacian spectral axes, temporal operators, and control inputs — is the subject of a later article in this series; here we require only the graph itself.

### 6.2 Formal definition

Let $V$ be a finite node set and $W \in \mathbb{R}^{|V| \times |V|}$ a weighted adjacency matrix with signed entries, $w_{ij} \neq 0$ indicating a direct influence of node $j$ on node $i$ with sign and magnitude $w_{ij}$, and $w_{ii} \neq 0$ permitted (Axiom 4). The UDG is the pair $G = (V, W)$ together with (a) a level function $\ell: V \to \{0, 1, 2, 3\}$ assigning each node to a hierarchical stratum, (b) a parent function $\pi$ defining the hierarchy tree, and (c) an edge typology partitioning nonzero entries of $W$ into hierarchical edges (parent–child loadings), cross-cutting edges (residual covariances between non-adjacent nodes), and self-loops (autoregressive maintenance). Axioms 1, 3, and 5 are satisfied by the unrestricted sign structure and the composability of paths in $W$; Axiom 2 is enforced as a modeling discipline: nodes may not be deleted from $V$, only estimated to have small weights.

Two structural principles complete the definition. First, the **encapsulation principle**: each level-2 node (spectrum) owns a subgraph — its subfactors, syndromes, and symptom components — and a subgraph communicates with the rest of the graph only through its mother node. This preserves interpretability and modularity: a zoomed-in clinical analysis of, say, internalizing dynamics can proceed within the internalizing subgraph, while cross-spectral effects are carried by the spectrum-level edges. Second, the **provisionality principle**: every edge weight is published with its evidential source and flagged as a prior, $W^{(0)}$, to be re-estimated from data; the graph's identity resides in its node set, level structure, and edge typology, not in the particular numerical values of the priors.

### 6.3 Node set

**Table 2.** *The UDG node set (levels 0–3). The complete machine-readable specification, with per-node source citations, accompanies this article as* udg_nodes.csv.

| Level | Nodes | Evidential basis |
|---|---|---|
| 0 — General factor | *p* | Caspi et al. (2014)\*; Kotov et al. (2021) |
| 1 — Superspectra | Emotional dysfunction; Psychosis; Externalizing | Watson et al. (2022); Kotov et al. (2020); Krueger et al. (2021)\* |
| 2 — Spectra | Internalizing; Somatoform; Thought disorder; Detachment; Disinhibited externalizing; Antagonistic externalizing; Neurodevelopmental (provisional) | Kotov et al. (2017, 2021); Stevanovic et al. (2024) |
| 3 — Subfactors | Distress; Fear; Eating pathology; Sexual problems (provisional); Mania; Substance abuse; Antisocial behavior | Kotov et al. (2017, 2020); Watson et al. (2022); Forbush et al. (2018) |

The node set adopts the HiTOP consensus hierarchy as its scaffold, because it is the only nosological architecture whose structure is itself an empirical result (Kotov et al., 2017; Kotov et al., 2021). Level 0 is the general factor *p* (Caspi et al., 2014*). Level 1 comprises the three superspectra: emotional dysfunction (Watson et al., 2022), psychosis (Kotov et al., 2020), and externalizing (Krueger et al., 2021*). Level 2 comprises the six consensus spectra plus the provisional neurodevelopmental spectrum (Kotov et al., 2021; Stevanovic et al., 2024). Level 3 comprises the replicated subfactors: distress, fear, eating pathology, and (provisionally) sexual problems within internalizing (Forbush et al., 2018; Watson et al., 2022); mania linked to thought disorder (Kotov et al., 2020); substance abuse and antisocial behavior within disinhibited externalizing (Kotov et al., 2017). Below level 3, syndromes and symptom components populate the encapsulated subgraphs; Figure 3 illustrates with the internalizing spectrum. DSM-5-TR and ICD-11 categories are recoverable as regions: a categorical diagnosis corresponds to a characteristic activation profile over subgraph nodes, which preserves crosswalk compatibility with both incumbent systems (Ruggero et al., 2019).

![**Figure 3.** The internalizing spectrum subgraph (zoom-in), illustrating the encapsulation principle: subfactors and representative syndromes communicate with other spectra only through their mother node. The dashed edge marks the distress–fear cross-subfactor association; example bridge symptoms are listed beneath.](../figures/fig3_internalizing_subgraph.png)

### 6.4 Edge set and provisional weights

Hierarchical edges carry loading-magnitude weights taken from the consensus structural literature; cross-cutting edges carry residual-covariance weights for the documented spectrum-level associations (e.g., the strong disinhibited–antagonistic association; the internalizing–somatoform association; mania's bridge position between internalizing distress and thought disorder); self-loops encode the self-maintenance phenomena documented in network psychiatry (Borsboom, 2017*). Figure 2 displays the full graph; Figure 4 displays the spectrum-level adjacency matrix $W^{(0)}$.

![**Figure 2.** The Universal Disorder Graph. Node color encodes hierarchical level; solid edges are hierarchical loadings; dashed red edges are cross-cutting residual covariances; dotted orange edges are cross-subfactor associations; red arcs are self-loops (Axiom 4). Edge thickness is proportional to the provisional consensus weight.](../figures/fig2_universal_disorder_graph.png)

![**Figure 4.** The provisional spectrum-level adjacency matrix W(0). All values are consensus priors with published provenance, intended for empirical re-estimation.](../figures/fig4_adjacency_heatmap.png) Three properties of the published weights must be stated plainly. First, they are *consensus priors*: rationally synthesized from published meta-analytic and structural estimates, cited edge by edge in the data files, and rounded to reflect their precision honestly. Second, they are *not* claims of measurement: no reader should cite this article as having estimated, e.g., the internalizing–detachment association at .50; the value encodes the literature's qualitative consensus (moderate, positive, robust) in numerical form for computational use. Third, they are *replaceable without loss of identity*: the falsification conditions of Section 6.6 attach to the structure, and improved weights strengthen rather than threaten the model.

### 6.5 What the UDG adds

Against the DSM and ICD, the UDG adds what HiTOP adds — dimensionality, hierarchy, explained comorbidity — while retaining categorical crosswalks (Section 6.3). Against HiTOP, it adds four things. (1) *Edge semantics*: HiTOP's structure is a pattern of loadings; the UDG's edges are influence-bearing, signed, and directional in principle, so that the clinical commonplaces of Section 5.2 become expressible. (2) *Self-maintenance*: self-loops give formal standing to the network-theoretic insight that disorder can be a self-sustaining state of a symptom system rather than the expression of a latent liability (Borsboom, 2017*; van de Leemput et al., 2014*). (3) *Encapsulated multiscale structure*: the mother-node principle lets the same object serve population-level nosology (upper strata) and individual-level formulation (subgraph dynamics), which no incumbent system does. (4) *Computability*: the graph is published as machine-readable node and edge lists with full provenance, so any research group can re-derive, re-estimate, perturb, or extend it — the no-black-box requirement realized. Against single-syndrome network psychiatry, conversely, the UDG contributes the missing *architecture*: a principled, hierarchical node set spanning all psychopathology, into which idiographic symptom networks plug as subgraph instantiations (Epskamp et al., 2018*; Robinaugh et al., 2020*).

### 6.6 Falsifiability, reliability, and validation pathway

The UDG makes refutable commitments at three levels. *Structural*: if confirmatory modeling in adequately powered, demographically diverse samples reliably rejects the four-level hierarchy — for instance, if bifactor or network models systematically outperform the hierarchical arrangement, or if the spectra fail measurement invariance across cultures — the node scaffold is falsified in part or whole (Ringwald et al., 2019; Rodriguez-Seijas et al., 2023). *Relational*: each cross-cutting edge predicts a nonzero conditional association after accounting for the hierarchy; estimated near-zero edges are pruned, and stable unmodeled associations force new edges — both events are recorded revisions, not silent adjustments. *Dynamic*: the self-loop and influence semantics predict that intensive longitudinal data will show autoregressive symptom maintenance and directed cross-lagged effects concentrated along UDG edges rather than distributed arbitrarily; systematic failure of that concentration falsifies the edge typology (Epskamp et al., 2018*; Rodebaugh et al., 2018*). Reliability, in turn, is inherited from measurement: the UDG prescribes no new instruments at the upper strata, deferring to the HiTOP measurement program (Simms et al., 2022) and existing validated scales, so its scores are exactly as reliable as the best available dimensional measurement — and improve as that program matures.

### 6.7 Limitations

Five limitations bound the present contribution. First, the provisional weights, however honestly flagged, will be quoted; we mitigate by publishing provenance per edge and versioning the graph. Second, the UDG at this stage represents influence *capacity*, not estimated within-person causality; the dynamic semantics become empirical only with the temporal machinery of the later mathematical article, and cross-sectional covariance remains an imperfect guide to intervention targets (Rodebaugh et al., 2018*). Third, the node scaffold inherits HiTOP's evidentiary skews — Western samples, self-report dominance, cross-sectional derivation (Poletti et al., 2025; Rodriguez-Seijas et al., 2023) — and therefore also inherits every caveat of Section 3.6. Fourth, coverage at the lower strata is uneven: well-studied spectra contribute richer subgraphs than under-studied ones (somatoform; neurodevelopmental), an imbalance the graph makes visible rather than hides. Fifth, the UDG is one stratum of a person, not a person: psychopathology interacts with development, personality, temperament, needs, motivation and emotion, therapeutic process, and the social systems a person inhabits, and the present graph reserves — but does not yet populate — the interfaces to those strata. Populating them is the work of the remainder of this series.

---

## 7. Conclusion

Sixty-five years separate the DSM's first edition from HiTOP's first consensus paper, and the arc of that history is legible: reliability first (DSM-III), reach next (ICD-10's global mandate), validity most recently (HiTOP) — with dynamics still missing. This article's synthesis located each system's contribution and each system's structural failure, argued that the failures are complementary, and converted that complementarity into design requirements for a successor representation. The Universal Disorder Graph satisfies those requirements in a deliberately minimal way: a hierarchically organized, weighted, signed graph with self-loops, whose node set is the field's best-validated dimensional architecture, whose edges carry published provenance, whose weights are declared priors, and whose axioms are few, weak, and jointly realizable. It is offered not as a finished nosology but as a reproducible starting object — the psychopathology stratum of a multidimensional model of the person whose remaining strata, and whose full mathematical and clinical development, occupy the subsequent articles of this series.

---

## References

*Sources marked with an asterisk (\*) were located by the authors through supplementary literature searches beyond the assembled source library.*

American Psychiatric Association. (2013). *Diagnostic and statistical manual of mental disorders* (5th ed.). https://doi.org/10.1176/appi.books.9780890425596

American Psychiatric Association. (2022). *Diagnostic and statistical manual of mental disorders* (5th ed., text rev.). https://doi.org/10.1176/appi.books.9780890425787

Boland, R. J., & Verduin, M. L. (2022). *Kaplan & Sadock's synopsis of psychiatry* (12th ed.). Wolters Kluwer.

Borsboom, D. (2017). A network theory of mental disorders. *World Psychiatry, 16*(1), 5–13. https://doi.org/10.1002/wps.20375 \*

Borsboom, D., & Cramer, A. O. J. (2013). Network analysis: An integrative approach to the structure of psychopathology. *Annual Review of Clinical Psychology, 9*, 91–121. https://doi.org/10.1146/annurev-clinpsy-050212-185608 \*

Bradford, G. K. (2010). Fundamental flaws of the DSM: Re-envisioning diagnosis. *Journal of Humanistic Psychology, 50*(3), 335–350. https://doi.org/10.1177/0022167809352007

Caspi, A., Houts, R. M., Belsky, D. W., Goldman-Mellor, S. J., Harrington, H., Israel, S., Meier, M. H., Ramrakha, S., Shalev, I., Poulton, R., & Moffitt, T. E. (2014). The p factor: One general psychopathology factor in the structure of psychiatric disorders? *Clinical Psychological Science, 2*(2), 119–137. https://doi.org/10.1177/2167702613497473 \*

Conway, C. C., Forbes, M. K., South, S. C., & the HiTOP Consortium. (2022). A Hierarchical Taxonomy of Psychopathology (HiTOP) primer for mental health researchers. *Clinical Psychological Science, 10*(2), 236–258. https://doi.org/10.1177/21677026211017834

Cooper, R. (2004). What is wrong with the DSM? *History of Psychiatry, 15*(1), 5–25. https://doi.org/10.1177/0957154X04039343

Cuthbert, B. N., & Insel, T. R. (2013). Toward the future of psychiatric diagnosis: The seven pillars of RDoC. *BMC Medicine, 11*, Article 126. https://doi.org/10.1186/1741-7015-11-126 \*

DeYoung, C. G., Blain, S. D., Latzman, R. D., Grazioplene, R. G., Haltigan, J. D., Kotov, R., Michelini, G., Venables, N. C., Docherty, A. R., Goghari, V. M., Kallen, A. M., Martin, E. A., Palumbo, I. M., Patrick, C. J., Perkins, E. R., Shackman, A. J., Snyder, M. E., Tobin, K. E., & the HiTOP Neurobiological Foundations Workgroup. (2024). The Hierarchical Taxonomy of Psychopathology (HiTOP) and the search for neurobiological substrates of mental illness: A systematic review and roadmap for future research. *Journal of Psychopathology and Clinical Science, 133*(8), 697–715. https://doi.org/10.1037/abn0000903

DeYoung, C. G., Chmielewski, M., Clark, L. A., Condon, D. M., Kotov, R., Krueger, R. F., Lynam, D. R., Markon, K. E., Miller, J. D., Mullins-Sweatt, S. N., Samuel, D. B., Sellbom, M., South, S. C., Thomas, K. M., Watson, D., Watts, A. L., Widiger, T. A., Wright, A. G. C., & the HiTOP Normal Personality Workgroup. (2022). The distinction between symptoms and traits in the Hierarchical Taxonomy of Psychopathology (HiTOP). *Journal of Personality, 90*(1), 20–33. https://doi.org/10.1111/jopy.12593

Drexler, K., Alpert, J. E., Benton, T. D., Fung, K. P., Gogtay, N., Malaspina, D., O'Keefe, V. M., Oquendo, M. A., Wainberg, M. L., Yonkers, K. A., Yousif, L., & Clarke, D. E. (2026). The future of DSM: Are functioning and quality of life essential elements of a complete psychiatric diagnosis? *American Journal of Psychiatry, 183*(5).

Epskamp, S., Borsboom, D., & Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. *Behavior Research Methods, 50*(1), 195–212. https://doi.org/10.3758/s13428-017-0862-1 \*

First, M. B., Bhat, V., Adler, D., Dixon, L., Goldman, B., Koh, S., Levine, B., Oslin, D., & Siris, S. (2014). How do clinicians actually use the Diagnostic and Statistical Manual of Mental Disorders in clinical practice and why we need to know more. *Journal of Nervous and Mental Disease, 202*(12), 841–844. https://doi.org/10.1097/NMD.0000000000000210

First, M. B., Clarke, D. E., Yousif, L., Eng, A. M., Gogtay, N., & Appelbaum, P. S. (2023). DSM-5-TR: Rationale, process, and overview of changes. *Psychiatric Services, 74*(8), 869–875. https://doi.org/10.1176/appi.ps.20220334

First, M. B., Erlich, M. D., Adler, D. A., Leong, S., Dixon, L. B., Oslin, D. W., Goldman, B., Koh, S., Levine, B., Berlant, J. L., & Siris, S. G. (2019). How the DSM is used in clinical practice. *Journal of Nervous and Mental Disease, 207*(3), 157–161. https://doi.org/10.1097/NMD.0000000000000953

First, M. B., Rebello, T. J., Keeley, J. W., Bhargava, R., Dai, Y., Kulygina, M., Matsumoto, C., Robles, R., Stona, A.-C., & Reed, G. M. (2018). Do mental health professionals use diagnostic classifications the way we think they do? A global survey. *World Psychiatry, 17*(2), 187–195. https://doi.org/10.1002/wps.20525

Forbes, M. K. (2023). Implications of the symptom-level overlap among DSM diagnoses for dimensions of psychopathology. *Journal of Emotion and Psychopathology, 1*(1), 104–112. https://doi.org/10.55913/joep.v1i1.6

Forbush, K. T., Chen, P.-Y., Hagan, K. E., Chapa, D. A. N., Gould, S. R., Eaton, N. R., & Krueger, R. F. (2018). A new approach to eating-disorder classification: Using empirical methods to delineate diagnostic dimensions and inform care. *International Journal of Eating Disorders, 51*(7), 710–721. https://doi.org/10.1002/eat.22891

Fried, E. I., & Nesse, R. M. (2015). Depression is not a consistent syndrome: An investigation of unique symptom patterns in the STAR*D study. *Journal of Affective Disorders, 172*, 96–102. https://doi.org/10.1016/j.jad.2014.10.010 \*

Garabiles, M. R., Mordeno, I. G., & Nalipay, M. J. N. (2023). A comparison of DSM-5 and ICD-11 models of PTSD: Measurement invariance and psychometric validation in Filipino trauma samples. *Journal of Psychiatric Research, 163*, 24–31. https://doi.org/10.1016/j.jpsychires.2023.05.021

Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. *Monatshefte für Mathematik und Physik, 38*, 173–198. https://doi.org/10.1007/BF01700692 \*

Haeffel, G. J., Jeronimus, B. F., Fisher, A. J., Kaiser, B. N., Weaver, L. J., Vargas, I., Goodson, J. T., Soyster, P. D., & Lu, W. (2022). The Hierarchical Taxonomy of Psychopathology (HiTOP) is not an improvement over the DSM. *Clinical Psychological Science, 10*(2), 285–290. https://doi.org/10.1177/21677026211068873

Hayes, S. C., Hofmann, S. G., & Ciarrochi, J. (2020). A process-based approach to psychological diagnosis and treatment: The conceptual and treatment utility of an extended evolutionary meta model. *Clinical Psychology Review, 82*, Article 101908. https://doi.org/10.1016/j.cpr.2020.101908 \*

Haywood, D., Castle, D. J., & Hart, N. H. (2024). Avoiding the pitfalls of the DSM-5: A primer for health professionals. *General Hospital Psychiatry, 90*, 88–90. https://doi.org/10.1016/j.genhosppsych.2024.07.008

Hirsch, J. A., Nicola, G., McGinty, G., Liu, R. W., Barr, R. M., Chittle, M. D., & Manchikanti, L. (2016). ICD-10: History and context. *American Journal of Neuroradiology, 37*(4), 596–599. https://doi.org/10.3174/ajnr.A4696

Hopwood, C. J., Kotov, R., Krueger, R. F., Watson, D., Widiger, T. A., Althoff, R. R., Ansell, E. B., Bach, B., Bagby, R. M., Blais, M. A., Bornovalova, M. A., Chmielewski, M., Cicero, D. C., Conway, C., De Clercq, B., De Fruyt, F., Docherty, A. R., Eaton, N. R., Edens, J. F., ... Zimmermann, J. (2018). The time has come for dimensional personality disorder diagnosis. *Personality and Mental Health, 12*(1), 82–86. https://doi.org/10.1002/pmh.1408

Hopwood, C. J., Mulay, A. L., & Waugh, M. H. (Eds.). (2019). *The DSM-5 alternative model for personality disorders: Integrating multiple paradigms of personality assessment*. Routledge. https://doi.org/10.4324/9781315205076

Insel, T., Cuthbert, B., Garvey, M., Heinssen, R., Pine, D. S., Quinn, K., Sanislow, C., & Wang, P. (2010). Research Domain Criteria (RDoC): Toward a new classification framework for research on mental disorders. *American Journal of Psychiatry, 167*(7), 748–751. https://doi.org/10.1176/appi.ajp.2010.09091379 \*

Jones, K. D. (2012). A critique of the DSM-5 field trials. *Journal of Nervous and Mental Disease, 200*(6), 517–519. https://doi.org/10.1097/NMD.0b013e318257c699

Jones, P. J., Ma, R., & McNally, R. J. (2021). Bridge centrality: A network approach to understanding comorbidity. *Multivariate Behavioral Research, 56*(2), 353–367. https://doi.org/10.1080/00273171.2019.1614898 \*

Kinderman, P., & Cooke, A. (2017). Responses to the publication of the American Psychiatric Association's DSM-5. *Journal of Humanistic Psychology*. Advance online publication. https://doi.org/10.1177/0022167817698262

Kirschner, S. R. (2013). Diagnosis and its discontents: Critical perspectives on psychiatric nosology and the DSM. *Feminism & Psychology, 23*(1), 10–28. https://doi.org/10.1177/0959353512467963

Kotov, R., Jonas, K. G., Carpenter, W. T., Dretsch, M. N., Eaton, N. R., Forbes, M. K., Forbush, K. T., Hobbs, K., Reininghaus, U., Slade, T., South, S. C., Sunderland, M., Waszczuk, M. A., Widiger, T. A., Wright, A. G. C., Zald, D. H., Krueger, R. F., Watson, D., & the HiTOP Utility Workgroup. (2020). Validity and utility of Hierarchical Taxonomy of Psychopathology (HiTOP): I. Psychosis superspectrum. *World Psychiatry, 19*(2), 151–172. https://doi.org/10.1002/wps.20730

Kotov, R., Krueger, R. F., Watson, D., Achenbach, T. M., Althoff, R. R., Bagby, R. M., Brown, T. A., Carpenter, W. T., Caspi, A., Clark, L. A., Eaton, N. R., Forbes, M. K., Forbush, K. T., Goldberg, D., Hasin, D., Hyman, S. E., Ivanova, M. Y., Lynam, D. R., Markon, K., ... Zimmerman, M. (2017). The Hierarchical Taxonomy of Psychopathology (HiTOP): A dimensional alternative to traditional nosologies. *Journal of Abnormal Psychology, 126*(4), 454–477. https://doi.org/10.1037/abn0000258

Kotov, R., Krueger, R. F., Watson, D., Cicero, D. C., Conway, C. C., DeYoung, C. G., Eaton, N. R., Forbes, M. K., Hallquist, M. N., Latzman, R. D., Mullins-Sweatt, S. N., Ruggero, C. J., Simms, L. J., Waldman, I. D., Waszczuk, M. A., & Wright, A. G. C. (2021). The Hierarchical Taxonomy of Psychopathology (HiTOP): A quantitative nosology based on consensus of evidence. *Annual Review of Clinical Psychology, 17*, 83–108. https://doi.org/10.1146/annurev-clinpsy-081219-093304

Krueger, R. F., Hobbs, K. A., Conway, C. C., Dick, D. M., Dretsch, M. N., Eaton, N. R., Forbes, M. K., Forbush, K. T., Keyes, K. M., Latzman, R. D., Michelini, G., Patrick, C. J., Sellbom, M., Slade, T., South, S. C., Sunderland, M., Tackett, J., Waldman, I., Waszczuk, M. A., ... Kotov, R. (2021). Validity and utility of Hierarchical Taxonomy of Psychopathology (HiTOP): II. Externalizing superspectrum. *World Psychiatry, 20*(2), 171–193. https://doi.org/10.1002/wps.20844 \*

Lafrance, M. N., & McKenzie-Mohr, S. (2013). The DSM and its lure of legitimacy. *Feminism & Psychology, 23*(1), 119–140. https://doi.org/10.1177/0959353512467974

Lasalvia, A. (2015). DSM-5 two years later: Facts, myths and some key open issues. *Epidemiology and Psychiatric Sciences, 24*(3), 185–187. https://doi.org/10.1017/S2045796015000256

Longenecker, J. M., Krueger, R. F., & Sponheim, S. R. (2020). Personality traits across the psychosis spectrum: A Hierarchical Taxonomy of Psychopathology conceptualization of clinical symptomatology. *Personality and Mental Health, 14*(1), 88–105. https://doi.org/10.1002/pmh.1448

McGuire, A. (2015). Diagnosing the Diagnostic and Statistical Manual of Mental Disorders [Review of the book *Diagnosing the Diagnostic and Statistical Manual of Mental Disorders*, by R. Cooper]. *Disability & Society, 30*(10), 1582–1585. https://doi.org/10.1080/09687599.2015.1062233

Mullins-Sweatt, S. N., DeShong, H. L., Lengel, G. J., Helle, A. C., & Krueger, R. F. (2019). Disinhibition as a unifying construct in understanding how personality dispositions undergird psychopathology. *Journal of Research in Personality, 80*, 55–61. https://doi.org/10.1016/j.jrp.2019.04.006

Mullins-Sweatt, S. N., Hopwood, C. J., Chmielewski, M., Meyer, N. A., Min, J., Helle, A. C., & Walgren, M. D. (2020). Treatment of personality pathology through the lens of the hierarchical taxonomy of psychopathology: Developing a research agenda. *Personality and Mental Health, 14*(1), 123–141. https://doi.org/10.1002/pmh.1464

Paniagua, F. A. (2018). ICD-10 versus DSM-5 on cultural issues. *SAGE Open, 8*(1). https://doi.org/10.1177/2158244018756165

Pickersgill, M. D. (2014). Debating DSM-5: Diagnosis and the sociology of critique. *Journal of Medical Ethics, 40*(8), 521–525. https://doi.org/10.1136/medethics-2013-101762

Poletti, M., Preti, A., & Raballo, A. (2025). Developmental perspectives on HiTOP psychosis superspectrum: Unveiling pitfalls and theoretical fallacies. *Frontiers in Psychiatry, 16*, Article 1523025. https://doi.org/10.3389/fpsyt.2025.1523025

Reed, G. M., First, M. B., Kogan, C. S., Hyman, S. E., Gureje, O., Gaebel, W., Maj, M., Stein, D. J., Maercker, A., Tyrer, P., Claudino, A., Garralda, E., Salvador-Carulla, L., Ray, R., Saunders, J. B., Dua, T., Poznyak, V., Medina-Mora, M. E., Pike, K. M., ... Saxena, S. (2019). Innovations and changes in the ICD-11 classification of mental, behavioural and neurodevelopmental disorders. *World Psychiatry, 18*(1), 3–19. https://doi.org/10.1002/wps.20611 \*

Regier, D. A., Kuhl, E. A., & Kupfer, D. J. (2013). The DSM-5: Classification and criteria changes. *World Psychiatry, 12*(2), 92–98. https://doi.org/10.1002/wps.20050

Rief, W., Frances, A., & Wittchen, H.-U. (2013). DSM-5 – Pros and cons. *Verhaltenstherapie, 23*(4), 280–285. https://doi.org/10.1159/000356572

Ringwald, W. R., Beeney, J. E., Pilkonis, P. A., & Wright, A. G. C. (2019). Comparing hierarchical models of personality pathology. *Journal of Research in Personality, 81*, 98–107. https://doi.org/10.1016/j.jrp.2019.05.011

Robinaugh, D. J., Hoekstra, R. H. A., Toner, E. R., & Borsboom, D. (2020). The network approach to psychopathology: A review of the literature 2008–2018 and an agenda for future research. *Psychological Medicine, 50*(3), 353–366. https://doi.org/10.1017/S0033291719003404 \*

Rodebaugh, T. L., Tonge, N. A., Piccirillo, M. L., Fried, E., Horenstein, A., Morrison, A. S., Goldin, P., Gross, J. J., Lim, M. H., Fernandez, K. C., Blanco, C., Schneier, F. R., Bogdan, R., Thompson, R. J., & Heimberg, R. G. (2018). Does centrality in a cross-sectional network suggest intervention targets for social anxiety disorder? *Journal of Consulting and Clinical Psychology, 86*(10), 831–844. https://doi.org/10.1037/ccp0000336 \*

Rodriguez-Seijas, C., Li, J. J., Balling, C., Brandes, C., Bernat, E., Boness, C. L., Forbes, M. K., Forbush, K. T., Joyner, K. J., Krueger, R. F., Levin-Aspenson, H. F., Michelini, G., Ro, E., Rutter, L., Stanton, K., Tackett, J. L., Waszczuk, M., & Eaton, N. R. (2023). Diversity and the Hierarchical Taxonomy of Psychopathology (HiTOP). *Nature Reviews Psychology, 2*(8), 483–495. https://doi.org/10.1038/s44159-023-00200-0

Ross, C. A. (2015). Problems with DSM-5 somatic symptom disorder. *Journal of Trauma & Dissociation, 16*(4), 341–348. https://doi.org/10.1080/15299732.2014.989558

Roy, M., Rivest, M.-P., Namian, D., & Moreau, N. (2019). The critical reception of the DSM-5: Towards a typology of audiences. *Public Understanding of Science, 28*(8), 932–948. https://doi.org/10.1177/0963662519868969

Ruggero, C. J., Kotov, R., Hopwood, C. J., First, M., Clark, L. A., Skodol, A. E., Mullins-Sweatt, S. N., Patrick, C. J., Bach, B., Cicero, D. C., Docherty, A., Simms, L. J., Bagby, R. M., Krueger, R. F., Callahan, J., Chmielewski, M., Conway, C. C., De Clercq, B., Dornbach-Bender, A., ... Zimmermann, J. (2019). Integrating the Hierarchical Taxonomy of Psychopathology (HiTOP) into clinical practice. *Journal of Consulting and Clinical Psychology, 87*(12), 1069–1084. https://doi.org/10.1037/ccp0000452

Sellbom, M., Forbush, K. T., Gould, S. R., Markon, K. E., Watson, D., & Witthöft, M. (2022). HiTOP assessment of the somatoform spectrum and eating disorders. *Assessment, 29*(1), 62–74. https://doi.org/10.1177/10731911211020825

Simms, L. J., Wright, A. G. C., Cicero, D., Kotov, R., Mullins-Sweatt, S. N., Sellbom, M., Watson, D., Widiger, T. A., & Zimmermann, J. (2022). Development of measures for the Hierarchical Taxonomy of Psychopathology (HiTOP): A collaborative scale development project. *Assessment, 29*(1), 3–16. https://doi.org/10.1177/10731911211015309

Stevanovic, D., Cirovic, N., & Knez, R. (2024). Hierarchical structuring of psychopathological dimensions in youth: Current progress and future steps with the Hierarchical Taxonomy of Psychopathology (HiTOP). *Middle East Current Psychiatry, 31*, Article 80. https://doi.org/10.1186/s43045-024-00471-0

Strong, T. (2014). DSM-5 and two insider critiques [Review of the books *Saving normal*, by A. Frances, and *The book of woe*, by G. Greenberg]. *Asia Pacific Journal of Counselling and Psychotherapy, 5*(1), 106–109. https://doi.org/10.1080/21507686.2013.854818

Thyer, B. A. (2015). The DSM-5 definition of mental disorder: Critique and alternatives. In B. Probst (Ed.), *Critical thinking in clinical assessment and diagnosis* (pp. 45–68). Springer. https://doi.org/10.1007/978-3-319-17774-8_3

Troisi, A. (2014). Functional classification of psychiatric disorders: A luminous future? *Psychological Inquiry, 25*(3–4), 336–341. https://doi.org/10.1080/1047840X.2014.926201

Tyrer, P. (2014). A comparison of DSM and ICD classifications of mental disorder. *Advances in Psychiatric Treatment, 20*(4), 280–285. https://doi.org/10.1192/apt.bp.113.011296

Vacca, M., Mura, A., Carrogu, G. P., Gaviano, L., Atzori, R., & Petretto, D. R. (2025). Definitions of "mental disorder" from DSM-III to DSM-5. *Behavioral Sciences, 15*(6), Article 830. https://doi.org/10.3390/bs15060830

van de Leemput, I. A., Wichers, M., Cramer, A. O. J., Borsboom, D., Tuerlinckx, F., Kuppens, P., van Nes, E. H., Viechtbauer, W., Giltay, E. J., Aggen, S. H., Derom, C., Jacobs, N., Kendler, K. S., van der Maas, H. L. J., Neale, M. C., Peeters, F., Thiery, E., Zachar, P., & Scheffer, M. (2014). Critical slowing down as early warning for the onset and termination of depression. *Proceedings of the National Academy of Sciences, 111*(1), 87–92. https://doi.org/10.1073/pnas.1312114110 \*

Veldmeijer, L., Terlouw, G., van Os, J., te Meerman, S., van 't Veer, J., & Boonstra, N. (2024). From diagnosis to dialogue – reconsidering the DSM as a conversation piece in mental health care: A hypothesis and theory. *Frontiers in Psychiatry, 15*, Article 1426475. https://doi.org/10.3389/fpsyt.2024.1426475

Venkatesan, S., & Suresh, A. (2022). Critique of DSM, medicalisation and graphic medicine. *Journal of Graphic Novels and Comics*. Advance online publication. https://doi.org/10.1080/21504857.2022.2053558

Wakefield, J. C. (1992). Disorder as harmful dysfunction: A conceptual critique of DSM-III-R's definition of mental disorder. *Psychological Review, 99*(2), 232–247. https://doi.org/10.1037/0033-295X.99.2.232

Wakefield, J. C. (2015). DSM-5, psychiatric epidemiology and the false positives problem. *Epidemiology and Psychiatric Sciences, 24*(3), 188–196. https://doi.org/10.1017/S2045796015000116

Watson, D., & Clark, L. A. (2020). Personality traits as an organizing framework for personality pathology. *Personality and Mental Health, 14*(1), 51–75. https://doi.org/10.1002/pmh.1458

Watson, D., Levin-Aspenson, H. F., Waszczuk, M. A., Conway, C. C., Dalgleish, T., Dretsch, M. N., Eaton, N. R., Forbes, M. K., Forbush, K. T., Hobbs, K. A., Michelini, G., Nelson, B. D., Sellbom, M., Slade, T., South, S. C., Sunderland, M., Waldman, I., Witthöft, M., Wright, A. G. C., ... Krueger, R. F. (2022). Validity and utility of Hierarchical Taxonomy of Psychopathology (HiTOP): III. Emotional dysfunction superspectrum. *World Psychiatry, 21*(1), 26–54. https://doi.org/10.1002/wps.20943

Widiger, T. A., & Crego, C. (2015). Process and content of DSM-5. *Psychopathology Review, 2*(1), 162–176. https://doi.org/10.5127/pr.035314

Widiger, T. A., & Crego, C. (2019). HiTOP thought disorder, DSM-5 psychoticism, and five factor model openness. *Journal of Research in Personality, 80*, 72–77. https://doi.org/10.1016/j.jrp.2019.04.008

Young, G. (2013). Breaking bad: DSM-5 description, criticisms, and recommendations. *Psychological Injury and Law, 6*(4), 345–348. https://doi.org/10.1007/s12207-013-9181-8

Zimmermann, J., Widiger, T. A., Oeltjen, L., Conway, C. C., & Morey, L. C. (2022). Developing preliminary scales for assessing the HiTOP detachment spectrum. *Assessment, 29*(1), 75–87. https://doi.org/10.1177/10731911211015313
