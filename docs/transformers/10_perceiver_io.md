# 10 — Perceiver IO: A General Architecture for Structured Inputs and Outputs (Jaegle et al., 2021)

**One line:** cross-attend arbitrary, heterogeneous inputs into a small
latent array, compute there, then cross-attend out to arbitrary outputs —
the shape of a universal measurement layer.

## The math

Three stages, all attention:

1. **Encode.** A learned latent array $Z_0 \in \mathbb{R}^{N \times d}$
   (with $N$ small, independent of input size $M$) queries the inputs
   $X \in \mathbb{R}^{M \times c}$:
   $$Z_1 = \mathrm{CrossAttn}(Q{=}Z_0,\ K,V{=}X)\qquad \mathcal{O}(NM).$$
2. **Process.** $L$ self-attention blocks on the latent only:
   $\mathcal{O}(LN^2)$ — the expensive part never touches $M$.
3. **Decode.** Output *queries* $O \in \mathbb{R}^{P \times d}$ — one per
   desired output element, built from output-position encodings — attend to
   the latent: $Y = \mathrm{CrossAttn}(Q{=}O,\ K,V{=}Z_L)$, $\mathcal{O}(PN)$.

Total cost linear in input and output sizes; the latent is an information
bottleneck of fixed width. Different modalities are handled by tagging each
input element with modality/position embeddings — inputs are just a *set* of
(value, metadata) pairs.

## What it means for the UPG

- **Our measurement layer is a set problem, not a sequence problem.** An
  occasion delivers an unordered, variable-length bag: some PHQ items, some
  affect sliders, an actigraphy summary, maybe nothing (missing). Perceiver's
  input format — elements tagged with (instrument, item, node, time)
  embeddings — accepts exactly this, with missingness handled by *absence*
  (the element simply isn't in the set) instead of imputation tokens. That is
  cleaner than the BERT masking route (note 02) when item sets differ across
  occasions and studies.
- **Output queries = graph nodes.** Decoding with one query per dimension
  (TEM…SYS) yields $\hat x_t \in \mathbb{R}^7$ regardless of what was
  observed: the architecture *is* the items→nodes bridge that
  `measurement_mapping.md` specifies by hand. The hand-specified mapping
  stays as the interpretable baseline; the Perceiver route is its learned
  generalization for Phase 4, when heterogeneous real instruments arrive.
- **The latent bottleneck ($N \ll M$) is our friend:** psychological state is
  low-dimensional by hypothesis (8 dimensions); forcing all items through a
  narrow latent enforces that hypothesis architecturally and can be
  checked — if reconstruction needs $N \gg 8$ latents, the eight-dimension
  claim loses support. A falsifiable architecture choice.

## Verdict

Not needed for Phase 2 (single simulated instrument, fixed item sets); the
step-6 measurement model uses the simpler per-node masking scheme. Adopted as
the *design* for the Phase-4 real-data measurement front-end, and noted for
the manuscript: latent-width ablation as an architectural test of
dimensionality.
