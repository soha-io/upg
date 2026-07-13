# 18 — Long-Range Transformers for Dynamic Spatiotemporal Forecasting (Spacetimeformer; Grigsby et al., 2021)

**One line:** flatten the whole variable×time grid into one token sequence
(one token per (variable, time) pair) and let attention learn *all*
spatiotemporal dependencies jointly — the maximally free rival to our
theory-constrained approach.

## The math

Given $m$ variables over $T$ steps, form $N = mT$ tokens
$z_{(j,t)} = \mathrm{Embed}(x^{(j)}_t, \mathrm{time}(t), \mathrm{var}(j))$,
each tagged with a *time* embedding and a *variable* embedding. Full
self-attention over all $N$ tokens learns, in one matrix,

$$A \in \mathbb{R}^{mT \times mT}:\qquad
A_{(i,s),(j,t)} = \text{attention of variable } i \text{ at time } s
\text{ to variable } j \text{ at time } t,$$

i.e. simultaneously *which variable* and *which lag* — a learned, dense,
time-varying generalization of every lagged coupling matrix at once
($B^{(1)}, B^{(2)}, \dots$ of a VAR, plus their state dependence). Long-range
efficiency comes from Performer-style linear attention (note 27) because
$N = mT$ explodes quickly.

This is a "spatiotemporal graph learned from data": the paper explicitly
frames attention as inferring a dynamic graph without a predefined adjacency.

## What it means for the UPG

- **This is the named antagonist.** Spacetimeformer answers our estimation
  problem by *refusing structure*: no skeleton, no lag restriction, no sign
  constraints. It therefore defines the top of the flexibility ladder for the
  step-7 tournament: theory-fixed (step 5 hard mask) ⊂ theory-biased
  (Graphormer-style soft bias, note 09) ⊂ free (this). Scoring these three
  against known synthetic truth measures exactly how much our theory buys —
  and at what sample size the free model catches up (cf. ViT crossover,
  note 11).
- **Identifiability accounting:** with our numbers ($m=7$, $T=100$), the free
  attention matrix has $(mT)^2 \approx 5\times10^5$ potential dependencies
  against $mT = 700$ observations — hopeless without the inductive biases we
  possess and it lacks. The comparison isn't rhetorical: the recovery gap is
  measurable and will be reported.
- **What we take even so:** the (variable, time) token *format* with typed
  embeddings is the cleanest way to feed irregular, partially observed grids
  (missing (j,t) pairs are simply absent tokens — same insight as Perceiver,
  note 10); this format is used in the step-6 measurement model.

## Verdict

Adopted as the registered *free rival* for the tournament (implemented at
small scale), and as the token-format donor for irregular data. Rejected as
the estimator of record: it is the architectural embodiment of what rule W1
forbids — and that is precisely what makes it the right thing to beat.
