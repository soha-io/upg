# 32 — GLU Variants Improve Transformer (Shazeer, 2020)

**One line:** replace the FFN's first layer with a *gated* product of two
projections — GEGLU/SwiGLU — a one-line change that reliably improves
transformer blocks ("We offer no explanation… we attribute their success,
as all else, to divine benevolence").

## The math

Standard FFN: $\ \mathrm{FFN}(x) = W_2\,\phi(W_1 x)$, $\phi \in$
{ReLU, GELU}. GLU family replaces the first stage with an element-wise
product of a *gate* path and a *value* path:

$$\mathrm{GLU}_\phi(x) = \phi(W_g x) \odot (W_v x),\qquad
\mathrm{FFN}_{\mathrm{GLU}}(x) = W_2\,[\phi(W_g x)\odot(W_v x)].$$

Variants by gate nonlinearity: bilinear ($\phi = $ identity), GEGLU
($\phi = $ GELU), SwiGLU ($\phi(z) = z\,\sigma(\beta z)$, Swish). To keep
parameter count constant against a plain FFN, shrink the hidden width by
2/3 (three matrices instead of two). Empirically GEGLU/SwiGLU dominate on
transfer benchmarks; the mechanism is usually glossed as multiplicative
interactions: the block computes data-dependent, input-conditional linear
maps — second-order terms a plain FFN must simulate with depth.

## What it means for the UPG

- **Multiplicative gating is our own formalism.** Time-gated weights
  $w_{ij}(t) = g_{ij}(t)\cdot \bar w_{ij}$ (Batch C) and the situational
  triggers of Batch F are multiplicative gates on couplings; the UMEG
  regulation mechanism multiplies drives down. A network block whose basic
  operation is "one pathway modulates the gain of another" is *the matched
  functional form* for learning gated dynamics — if step 6 has to
  approximate $g(t)\,\bar w$ interactions, SwiGLU gives it the product
  structure natively instead of forcing an additive approximation through
  depth. This is the difference between representing the theory's algebra
  and imitating it.
- Practical adoption: step-6 blocks use SwiGLU FFNs (with the 2/3-width
  correction so comparisons stay parameter-matched — the paper's own
  discipline). Backward pass is product-rule simple; one extra matmul.
- The famous non-explanation is worth keeping in mind culturally: even at
  the field's center, *why* remains open while *that* is solid. Our project
  holds itself to a higher explanatory bar (mechanism first), which is
  exactly why the gated form is chosen here for a *reason* (matched algebra)
  and that reason is falsifiable: ablate SwiGLU → plain GELU FFN and check
  whether gated-dynamics recovery specifically degrades.

## Verdict

Adopted (SwiGLU in step-6 FFNs) with the matched-algebra rationale and a
registered ablation. The gate-recovers-gates hypothesis becomes testable
once developmental gates enter the simulator.
