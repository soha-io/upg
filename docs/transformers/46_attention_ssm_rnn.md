# 46 — Understanding the Differences in Foundation Models: Attention, State Space Models, and Recurrent Neural Networks (Sieber et al., 2024)

**One line:** put attention, SSMs, and RNNs into one dynamical-systems
framework and compare them as *systems* — memory structure, state size,
expressivity — giving the decision criteria for which estimator family fits
a given process; the capstone paper for our architecture choice.

## The math

The unifying frame: every sequence model is a map from input history to
output implementable as a (possibly time-varying) dynamical system; compare
via the systems-theoretic reading of each family.

- **Softmax attention:** state = the entire KV cache (grows with $t$);
  output at $t$ is a *nonlinear* (normalized-kernel) readout over all
  stored pairs. Unbounded state ⇒ exact retrieval over arbitrary horizons;
  cost grows with context; no imposed temporal decay (any decay is learned
  via content/position terms — cf. note 30's explicit prior).
- **Linear attention / SSMs:** fixed-size state
  ($S_t \in \mathbb{R}^{d\times d}$ or $x_t \in \mathbb{R}^N$) updated by an
  affine (possibly input-dependent, note 44) recurrence; memory of an event
  decays through repeated application of transition operators — geometric
  in the LTI case, gate-controlled in the selective case (note 45's path
  products). Compression is *lossy by design*; what survives is what the
  learned dynamics choose to encode.
- **Classical RNNs (LSTM/GRU):** fixed-size state with *fully nonlinear*
  recurrence — most expressive per step, hardest to train (no
  parallel-scan form; vanishing-gradient pathologies the gated designs
  patch heuristically rather than structurally as HiPPO does).

The paper's contribution is making these comparisons precise (which
functions of history each family can represent at bounded state; where the
attention↔SSM equivalences of notes 38/45 break — chiefly at the softmax
normalization and content-based exact lookup) and empirical probes of the
theory.

## What it means for the UPG — the decision rule we adopt

Match the estimator's memory structure to the process's memory structure:

1. **Our generative process has a small, fixed, *known-dimension* state**
   ($x_t \in \mathbb{R}^7$, Markov given the state). For *filtering a
   well-specified UPG*, fixed-state models (SSM family) are sufficient in
   principle and matched in structure — the theoretical best-case
   architecture.
2. **Real data guarantee mis-specification** (unmodeled dimensions,
   measurement pathologies, MNAR missingness, rare discrete events).
   Unbounded-state attention buys robustness exactly here: it can retrieve
   raw past evidence at readout time instead of having had to encode it
   correctly at write time — insurance against wrong compression.
3. **Therefore the pipeline's answer is staged, and now principled:**
   attention-first at Phase-2 scale (simplicity, auditability, tiny $T$;
   robustness rehearsal for real data), SSM challenger registered for the
   long-sequence regime (note 43/44), decided by the benchmark — with this
   paper supplying the vocabulary for *why* whichever wins, wins. If the
   SSM matches attention on `transition_rich`, the compression is adequate
   and the cheap model deploys; if attention wins on OOD persons
   (note 42's probes), mis-specification insurance is worth its cost.

One more export: the framework's emphasis that *training dynamics* differ
by family (parallelizability, gradient pathways) reiterates note 06 — the
comparison must tune each family properly or it measures trainability, not
capability.

## Verdict

The architecture-selection framework for step 6 and beyond, turning
"attention vs. Mamba" from fashion into a testable systems question. With
notes 38/43/44/45 it completes the arc: our theory, the estimators, and the
deep architectures are all one subject — dynamical systems — which is
Batch I's isomorphism claim, now extended to the instruments themselves.
