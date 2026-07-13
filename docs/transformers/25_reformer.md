# 25 — Reformer: The Efficient Transformer (Kitaev, Kaiser & Levskaya, 2020)

**One line:** two memory tricks — locality-sensitive-hashing attention
(attend only within buckets of similar queries/keys) and reversible layers
(recompute activations instead of storing them) — clever, but both trade
determinism or simplicity for scale we don't need.

## The math

1. **LSH attention.** Softmax attention is dominated by the largest
   $q_i^\top k_j$; nearest keys matter most. Random-projection LSH assigns
   $x$ to bucket $h(x) = \arg\max([xR; -xR])$ (rotations $R$), so similar
   vectors collide with high probability. Attend only within buckets
   (with $Q = K$ tying): expected cost $\mathcal{O}(T\log T)$. Multiple
   hash rounds reduce the probability of missing a large logit; the price is
   *stochastic, approximate* attention whose error depends on hash luck.
2. **Reversible residual layers.** Split channels into $(x_1, x_2)$:
   $$y_1 = x_1 + F(x_2),\qquad y_2 = x_2 + G(y_1),$$
   invertible exactly: $x_2 = y_2 - G(y_1),\ x_1 = y_1 - F(x_2)$. Backprop
   recomputes activations from outputs, so activation memory is
   $\mathcal{O}(1)$ in depth (compute ×~1.5). Also of independent interest:
   an exactly invertible deep map — depth without information loss.

## What it means for the UPG

- **LSH attention violates our reproducibility charter more than it saves:**
  attention support depends on random hashes; two runs see different
  effective graphs unless seeds are fixed and even then the *approximation
  error* is data-dependent and hard to audit. With FlashAttention (note 23)
  providing exact attention at scale, LSH is dominated for our purposes.
- **Reversible layers are the interesting half.** An invertible network is a
  bijection: nothing about the input is discarded — relevant wherever we
  want deep measurement models that provably lose no information before the
  bottleneck (cf. Perceiver latent, note 10). Also a conceptual echo: our
  tanh map with $\rho(J) < 1$ *contracts* (forgets initial conditions —
  that's what an attractor is), so a reversible forecaster is exactly what
  the dynamics say we should *not* need — memory loss is a property of the
  system, not a bug in the model. Worth one line in the manuscript.
- Chunked feed-forward (their third trick) is trivially applicable anywhere.

## Verdict

Rejected for the pipeline (stochastic approximation vs. exactness policy).
Reversible layers filed as a tool for information-preserving measurement
front-ends; the contraction/reversibility contrast is a nice theoretical
footnote for Phase 3.
