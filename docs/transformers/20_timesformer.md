# 20 — Is Space-Time Attention All You Need for Video Understanding? (TimeSformer; Bertasius et al., 2021)

**One line:** joint attention over all (patch, frame) pairs is expensive and
unnecessary — *divided* attention (temporal attention, then spatial
attention, in series within each block) works better; factorization is a
regularizer, not just a cost saving.

## The math

Video: $N$ patches per frame × $F$ frames. Candidate attention schemes for
token $(p, t)$:

- **Joint space-time:** attend to all $NF$ tokens: cost
  $\mathcal{O}((NF)^2)$, maximal flexibility.
- **Divided space-time (winner):** within a block, first attend across time
  *at the same patch location* — $\{(p, t') : t' = 1..F\}$ — then attend
  across space *within the same frame* — $\{(p', t) : p' = 1..N\}$, each with
  its own QKV projections and a residual connection between:
  $$z' = z + \mathrm{Attn}_{\text{time}}(z),\qquad
  z'' = z' + \mathrm{Attn}_{\text{space}}(z').$$
  Cost $\mathcal{O}(N F^2 + F N^2)$, and — the empirical surprise — *higher
  accuracy* than joint attention on standard benchmarks.
- Sparse local-global and axis-aligned variants fall in between.

Why divided beats joint at fixed data: joint attention must discover the
factorized structure of the domain (objects persist through time; spatial
layout is per-frame) from data; divided attention *builds it in*, spending
statistical capacity on the residual dependencies instead.

## What it means for the UPG

- Substitute space → graph nodes, frames → EMA occasions: the theorem-shaped
  lesson is that **attention factorized as (within-node across time) +
  (across nodes within time) should beat joint (node, time) attention at our
  sample sizes** — the same conclusion reached from the identifiability
  count in note 18, now supported by direct experiment in a data-rich domain.
  Our step-6 forecaster (time attention per node with shared weights) plus
  step-5 estimator (cross-node attention on the skeleton) *is* the divided
  scheme, split across two models.
- The result also justifies the generative model's own factorization: our
  map applies $B$ (space mixing) and the lag-1 update (time step) as
  separate, composed operators. The deep-learning evidence that this
  factorization is the right inductive bias for spatiotemporal data is
  reassurance the theory didn't have before.

## Verdict

Adopted as the factorization argument (with note 21) for keeping structure
estimation and temporal forecasting as separate attention axes. No direct
implementation import beyond that.
