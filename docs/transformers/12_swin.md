# 12 — Swin Transformer: Hierarchical Vision Transformer Using Shifted Windows (Liu et al., 2021)

**One line:** attend locally within windows, shift the windows between layers
so information crosses boundaries, and merge tokens hierarchically — how to
get global context from local operations, cheaply.

## The math

- **Windowed attention:** partition tokens into non-overlapping windows of
  $M\times M$; run self-attention within each window only. Cost per layer
  falls from $\mathcal{O}((hw)^2 d)$ to $\mathcal{O}(hw\, M^2 d)$ — linear in
  image size.
- **Shifted windows:** alternate layers displace the partition by
  $\lfloor M/2 \rfloor$, so tokens split by a boundary in layer $\ell$ share
  a window in layer $\ell+1$. Two layers suffice for cross-window flow;
  receptive fields grow with depth like stacked convolutions.
- **Patch merging:** every stage concatenates $2\times2$ neighboring tokens
  and projects down — resolution halves, channels grow, producing a pyramid
  of representations at multiple scales.
- **Relative position bias** $B_{ij} = b_{\Delta(i,j)}$ added to logits
  within windows (same family as notes 07/29/30).

## What it means for the UPG

- **The shifted-window theorem in graph terms:** local attention + partition
  shifts = global reachability in $\mathcal{O}(\text{depth})$ hops. Our
  Axiom 3 (mediated influence) makes the same claim about the person graph:
  everything reaches everything, but through paths. In estimation this
  licenses *local* estimators (per-stratum, per-neighborhood) stacked in
  depth, rather than one global monolith — important at 253-node resolution
  where full attention over nodes×time gets heavy.
- **Patch merging is the aggregation operator of Batch J Definition 4**
  (facets → mother node = tokens merged into a coarser token with richer
  channels). The Swin pyramid is a worked example that hierarchical
  coarsening preserves task-relevant information while cutting cost — the
  same bet the UPG makes by running dynamics at dimension level with
  stratum subgraphs underneath.
- Phase-2 relevance is limited (at $n=7$, windows are pointless), but the
  253-node Great-Graph estimator should use stratum-windows (attend within
  stratum) + interface-shifts (cross-stratum layers touching only interface
  nodes) — which would make the *encapsulation constraint itself* an
  attention pattern. That design falls out of this paper directly.

## Verdict

No Phase-2 use at dimension resolution. Reserved as the architectural
blueprint for full-resolution (253-node) estimation: stratum-windowed
attention with interface-restricted cross-layers = encapsulation as
architecture.
