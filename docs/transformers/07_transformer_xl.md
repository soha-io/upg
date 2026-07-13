# 07 — Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context (Dai et al., 2019)

**One line:** attention over a *cached memory* of previous segments plus
relative position encoding lets effective context grow far beyond the
training window — the mechanism for long person-histories.

## The math

Split a long sequence into segments of length $L$. When processing segment
$\tau+1$, layer $\ell$ attends over its own hidden states *and* a
stop-gradient cache of the previous segment's:

$$\tilde h^{\ell-1}_{\tau+1} = \big[\,\mathrm{SG}(h^{\ell-1}_{\tau}) \,\|\, h^{\ell-1}_{\tau+1}\,\big],\qquad
Q = h^{\ell-1}_{\tau+1}W_Q,\ \ K,V = \tilde h^{\ell-1}_{\tau+1}W_{K,V}.$$

Because layer $\ell$ at segment $\tau+1$ sees layer $\ell-1$ at segment
$\tau$, information propagates one segment per layer: an $L$-layer stack has
effective context $\mathcal{O}(L \times \text{segment length})$.

**Relative position encoding.** Absolute positions break under caching (the
same absolute index recurs in every segment). Decompose the attention logit
between query $i$ and key $j$ so position enters only via $i-j$:

$$A_{ij} = \underbrace{q_i^\top W_{k,E}\, x_j}_{\text{content–content}}
 + \underbrace{q_i^\top W_{k,R}\, R_{i-j}}_{\text{content–position}}
 + \underbrace{u^\top W_{k,E}\, x_j}_{\text{global content bias}}
 + \underbrace{v^\top W_{k,R}\, R_{i-j}}_{\text{global position bias}},$$

with $R_{i-j}$ a sinusoid of the *offset* and $u, v$ learned. This is the
ancestor of RoPE (note 29) and ALiBi (note 30): only *relative time* should
matter to a temporal law.

## What it means for the UPG

- **Relative time is a physical requirement for us, not a trick.** Our
  generative law is time-homogeneous: the transition kernel depends on
  $\Delta t$, never on absolute $t$ (gates $g_{ij}(t)$ modulate slowly, at
  developmental timescales). An estimator whose attention depends on absolute
  index can hallucinate nonstationarity. Step 6 therefore uses relative-time
  encodings exclusively.
- **Segment recurrence is the deployment pattern for continuous monitoring:**
  a patient monitored for a year at 3 EMA/day produces $T\!\sim\!10^3$; the
  cache pattern lets a fixed-window model carry summary state forward instead
  of recomputing over the full history — the engineering shape of a *live*
  early-warning system (Phase 4/5 concern, noted now).
- The stop-gradient cache is also an honest statement of an approximation:
  gradients don't flow into the past beyond one segment. For dynamics as slow
  as ours (attractor residence times ≫ segment length) this truncation is
  benign — same argument as truncated BPTT for stiff systems.

## Verdict

Adopt the principle (relative-time attention; note 30's ALiBi is the simpler
implementation we use). Cache-based recurrence is deferred until real
long-horizon monitoring data exist. High priority as marked in the registry.
