# 37 — Attention Is Not All You Need: Pure Attention Loses Rank Doubly Exponentially with Depth (Dong, Cordonnier & Loukas, 2021)

**One line:** stacked self-attention *alone* converges doubly exponentially
to a rank-1 matrix — every token identical — and only skip connections
(chiefly) and MLPs prevent the collapse; a real theorem about what attention
is and isn't.

## The math

Define the residual of a matrix from rank-1 uniformity:
$\mathrm{res}(X) = X - \mathbf{1}x^\top$ where
$x = \arg\min_x \|X - \mathbf{1}x^\top\|$. Main theorem (pure attention,
no skips/MLP): for a depth-$L$ stack of self-attention layers,

$$\|\mathrm{res}(X_L)\|_{1,\infty} \le \Big(\frac{4\gamma H}{\sqrt{d_{qk}}}\Big)^{\!\frac{3^L - 1}{2}} \|\mathrm{res}(X_0)\|_{1,\infty}^{\,3^L},$$

i.e. the distance to rank-1 shrinks with exponent $3^L$ — *doubly
exponential* — whenever the bracketed factor is < 1. Mechanism: each softmax
row is a convex combination; iterated averaging is a (nonlinear) diffusion
that mixes token representations toward consensus. The proof decomposes the
network into *paths* (choices of head per layer) and shows every path output
is close to rank-1; the network is a sum of shallow, weak contributors.

Counteracting forces, analyzed separately: **skip connections** preserve the
identity path (the length-0 path in the decomposition) and provably stop
collapse; **MLPs** slow it (their Lipschitz constants enter the bound);
LayerNorm alone does not help.

## What it means for the UPG

- **This is our own bifurcation mathematics on the architecture side.**
  Iterated averaging → consensus is a contraction-to-attractor result; the
  doubly-exponential rate is the network analogue of $\rho(J) < 1$ dynamics.
  The paper even shares our method: analyze the composed operator's spectrum
  and find the condition under which structure survives iteration. For the
  manuscript, this is the cleanest citation that *deep-learning theory and
  network psychometrics use the same dynamical toolbox* — Batch I's
  isomorphism argument, demonstrated in the other field.
- **Design consequences for steps 5–6 (concrete):** never stack attention
  without residuals (our blocks are pre-norm residual throughout); the
  token-uniformity failure mode is *detectable* — monitor
  $\|\mathrm{res}(X_\ell)\|/\|X_\ell\|$ across layers as a training
  diagnostic (added to the step-6 report). With $n = 7$ variate tokens
  (note 17), collapse would manifest as all dimensions receiving identical
  representations — i.e. the estimator claiming every person is
  psychologically uniform. Worth watching for explicitly.
- **A caution for attention-as-$B$ readouts (step 5):** row-stochastic
  mixing pulls toward uniformity; if our masked-attention corrections
  $\delta_{ij}$ inherit a softmax anywhere, shrinkage-toward-uniform is
  built in and would *bias person heterogeneity downward*. Our unnormalized
  parameterization ($\bar B \odot e^\Delta$, no softmax) dodges this — this
  theorem is the principled reason for that choice, beyond the
  normalization argument of note 08.

## Verdict

High-value theory. Adopted: residual-everywhere policy, rank-residual
training diagnostic, and the no-softmax justification for step 5's edge
parameterization. Cited in Phase 3 as convergent dynamical analysis.
