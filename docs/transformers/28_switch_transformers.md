# 28 — Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity (Fedus, Zoph & Shazeer, 2022)

**One line:** replace each feed-forward block with many expert FFNs and route
each token to exactly one — parameters scale without compute scaling; for
us, a formal template for *regime-specific* or *theory-specific* components.

## The math

Mixture-of-experts layer with $E$ experts $\{FFN_e\}$ and a router
$W_r$:

$$p(x) = \mathrm{softmax}(W_r x) \in \Delta^{E-1},\qquad
y = p_{e^\*}(x)\cdot FFN_{e^\*}(x),\quad e^\* = \arg\max_e p_e(x).$$

Top-1 routing (the "switch") means each token activates $1/E$ of the layer's
parameters: sparse activation, dense parameter count. Two stabilizers:

- **Load-balancing loss:** with $f_e$ = fraction of tokens routed to $e$ and
  $P_e$ = mean router probability, add
  $\mathcal{L}_{\text{aux}} = \alpha E \sum_e f_e P_e$, minimized by uniform
  routing — prevents expert collapse (all tokens to one expert).
- **Capacity factor:** cap tokens per expert; overflow is passed through the
  residual (dropped from expert computation).

Selective precision and small init keep top-1 training stable where earlier
MoE needed top-2.

## What it means for the UPG

- **Routing is a discrete latent-class model inside a network:** the router
  is estimating $p(\text{class} \mid x)$ and experts are class-conditional
  models. Our dynamics have genuine discrete structure — regimes (quiescent /
  pinned-high / bistable) with qualitatively different local dynamics. A
  regime-routed forecaster (small expert per regime) is therefore *matched*
  to the generative truth in a way monolithic models are not; expert
  assignment would even be checkable against true regime labels on synthetic
  persons. Registered as a step-6 extension: measurable question — does
  routing recover the regime partition unsupervised?
- **Experts as theories:** for the step-7 tournament there is a tempting
  variant — one expert per rival theory, router learns which theory explains
  which person. We *reject* this for scoring (it blends theories instead of
  comparing them; same reasoning as note 19's gate), but note it as a
  *hypothesis generator*: persons routed away from the UPG expert are the
  cases our theory fits worst — a principled way to find falsifying persons.
- Expert collapse ↔ our quota sampling: the load-balancing problem is the
  same imbalance issue `sample_population` solves with regime quotas;
  training any regime-aware model needs the balanced preset for the same
  reason the aux loss exists.

## Verdict

Not in Phase 2 (adds capacity we can't identify at current data). Registered:
regime-routed forecaster as a step-6 extension with a checkable routing
target; "expert-per-theory" rejected for scoring but kept as a
falsifier-finding heuristic.
