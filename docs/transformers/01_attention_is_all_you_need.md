# 01 — Attention Is All You Need (Vaswani et al., 2017)

**One line:** replaces recurrence with a learned, data-dependent weighted
average over the whole sequence; every later paper in this folder is a
footnote to this mechanism.

## The math

Given a sequence of token vectors stacked as $X \in \mathbb{R}^{T \times d}$,
one attention head computes

$$Q = XW_Q,\quad K = XW_K,\quad V = XW_V,\qquad
\mathrm{Attn}(X) = \mathrm{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)V .$$

Row $t$ of the output is a convex combination of value vectors:

$$z_t = \sum_{s=1}^{T} \alpha_{ts}\, v_s,\qquad
\alpha_{ts} = \frac{\exp(q_t^\top k_s/\sqrt{d_k})}{\sum_{s'}\exp(q_t^\top k_{s'}/\sqrt{d_k})},\qquad
\sum_s \alpha_{ts} = 1,\ \alpha_{ts}\ge 0.$$

Three facts that matter more than the architecture diagram:

1. **Attention is a state-dependent adjacency matrix.** $A(X) = [\alpha_{ts}]$
   is a row-stochastic $T\times T$ matrix *computed from the data*. The layer
   output is $A(X)\,XW_V$ — structurally the same operation as our
   $B x_t$ drive, except $B$ is fixed and $A(X)$ is recomputed per input.
2. **The $\sqrt{d_k}$ scaling controls gradient variance.** If
   $q,k \sim \mathcal{N}(0, I_{d_k})$, then $q^\top k$ has variance $d_k$;
   dividing by $\sqrt{d_k}$ keeps softmax inputs $\mathcal{O}(1)$ so the
   softmax doesn't saturate (saturated softmax ⇒ one-hot weights ⇒ vanishing
   gradients).
3. **Multi-head = multiple relation types.** $H$ heads run the same machinery
   with separate projections and are concatenated:
   $\mathrm{MHA}(X) = [\,\mathrm{head}_1 \| \cdots \| \mathrm{head}_H\,]W_O$.
   Each head can realize a *different* graph over tokens — the analogue of our
   edge *types* (unmediated influence, gating, treatment).

A full block adds the parts that make deep stacks trainable:

$$X' = X + \mathrm{MHA}(\mathrm{LN}(X)),\qquad
X'' = X' + \mathrm{FFN}(\mathrm{LN}(X')),\quad
\mathrm{FFN}(x) = W_2\,\phi(W_1 x).$$

Residual paths keep an identity map through the network (gradient highway);
paper 37 proves attention *without* them collapses. Position information must
be injected separately (sinusoidal PE here; RoPE/ALiBi in notes 29–30) because
attention itself is permutation-equivariant:
$\mathrm{Attn}(PX) = P\,\mathrm{Attn}(X)$ for any permutation $P$.

Causal (decoder) attention imposes $\alpha_{ts} = 0$ for $s > t$ via an
additive $-\infty$ mask before softmax — the same masking mechanism we reuse
with a *graph* mask in step 5.

## What it means for the UPG

- Our generative map $x_{t+1} = \tanh(\kappa(Bx_t + gu_t) + b)$ is a
  *one-hop, fixed-weight* message pass. Attention generalizes exactly the two
  assumptions we might want to relax at estimation time: (i) weights constant
  in time, (ii) influence limited to lag 1. A causal transformer over EMA
  history can represent lag-$k$ and state-dependent influence without us
  hand-specifying it.
- Permutation equivariance is a *feature* for us: our 7 dimensions have no
  natural order, so attention over variables (note 17) respects that; any
  ordering-based model (RNN over variables) would not.
- The additive-mask trick is the whole of step 5 in embryo: replace the
  causal mask with the skeleton mask $M$ and attention weights become
  constrained edge estimates.

## Verdict

Foundation. Adopted directly: the step-6 forecaster is a small causal
encoder of exactly this form; step 5's masked attention is this equation
with $M$ in place of the causal mask.
