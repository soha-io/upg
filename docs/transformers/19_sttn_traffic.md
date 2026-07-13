# 19 — Spatial-Temporal Transformer Networks for Traffic Flow Forecasting (Xu et al., 2020)

**One line:** forecast on a sensor network by alternating a *spatial*
transformer (attention over graph nodes, with the road graph as prior) and a
*temporal* transformer (attention over time) — the closest engineering
analogue to "dynamics on a known graph."

## The math

Traffic state $X_t \in \mathbb{R}^{m}$ on $m$ road sensors with adjacency $A$
(the physical road network). The model stacks two attention types:

1. **Spatial transformer:** at each time step, attention across nodes.
   Crucially it *combines* a fixed-graph convolution branch (using the given
   $A$, via GCN-style propagation $\hat A X W$) with a free spatial-attention
   branch, gated together — i.e., prior structure and learned structure
   coexist, with a learned gate deciding how much to trust each:
   $$H = g \odot \mathrm{GCN}_A(X) + (1-g) \odot \mathrm{Attn}_{\text{free}}(X).$$
2. **Temporal transformer:** attention over time steps per node,
   with positional encodings, capturing multi-lag dependencies.

Blocks alternate, so spatial mixing and temporal propagation interleave —
factorized spatiotemporal attention (cf. notes 20–21) on an explicit graph.

## What it means for the UPG

- **Traffic is the friendly isomorph of our problem:** states on named nodes,
  a known physical graph constraining influence, propagation with delays,
  regime shifts (jams = pinned-high attractors), interventions (ramp
  metering = $u_t$). The domain shows that graph-prior + attention hybrids
  are standard practice where the graph is *trusted physics* — exactly our
  W1 posture toward the theory skeleton.
- **The gated two-branch design is the diplomatic version of the tournament:**
  rather than choosing hard mask vs. free attention (note 18), learn a gate
  between them. Tempting — but for *science* the gate is a liability: it
  answers "how much structure to trust" with an uninterpretable mixture
  instead of a model-comparison statistic. We keep the branches separate and
  compare them formally (Bayes factors, step 7) rather than blending. The
  gate value would tell us *that* theory is incomplete but not *where*; the
  tournament tells us where.
- **What transfers directly:** alternate node-attention / time-attention
  layering (adopted in the full-resolution design, cf. note 12); delay-aware
  temporal attention as the analogue of propagation lags along long paths in
  the 253-node graph.

## Verdict

Analogy-level adoption: validates the factorized graph+time architecture and
provides the engineering pattern for full-resolution UPG estimation. Its
learned prior-vs-free gate is explicitly *not* adopted, in favor of formal
model comparison — a decision worth stating in the Phase-3 manuscript.
