# 21 — ViViT: A Video Vision Transformer (Arnab et al., 2021)

**One line:** a systematic menu of four ways to factorize spatiotemporal
attention, plus *tubelet* embedding (tokens spanning space and a short time
window) — the taxonomy paper for structured attention over grids.

## The math

Tokenization: **tubelets** — 3-D patches of extent $h \times w \times \tau$
(space × time) linearly embedded, so each token already summarizes a short
local clip (compare: patch = spatial only, note 11; patch of a series =
temporal only, note 16).

Four factorization models, decreasing flexibility:

1. **Joint spatio-temporal attention** over all tokens (as note 20's joint).
2. **Factorized encoder:** a spatial transformer per frame produces one
   embedding per frame; a temporal transformer runs over frame embeddings.
   ("Late fusion" of time; cheapest well-performing variant.)
3. **Factorized self-attention:** alternate spatial-only and temporal-only
   attention *layers* inside one encoder (≈ note 20's divided).
4. **Factorized dot-product:** split *heads* — half the heads attend
   spatially, half temporally, fused by concatenation in the same layer.

Findings: 2–4 beat 1 in the regimes tested (data-limited relative to video
complexity); model 2 is a strong accuracy/cost compromise; initialization
from image-pretrained ViT ("inflating" embeddings across time) matters.

## What it means for the UPG

- **Model 2 (factorized encoder) is precisely our two-stage measurement →
  dynamics pipeline:** a per-occasion encoder (items → occasion/node
  embedding; our measurement model) followed by a temporal model over
  occasion embeddings (our forecaster). ViViT's evidence that late-fusion
  factorization is competitive at limited data supports keeping steps 6a and
  6b as separable modules with a clean interface ($\hat x_t$ + uncertainty)
  instead of one end-to-end monolith — which also keeps the interface
  auditable (no-black-box requirement 17).
- **Head-split factorization (model 4)** is the pattern for a future joint
  model: heads assigned to *within-stratum* vs. *cross-stratum* attention
  would encode the encapsulation constraint at head level — a second
  implementation route for the idea in note 12.
- **Tubelet = multi-occasion token:** for 3–5 daily EMA prompts, a one-day
  tubelet (all items × one day) is the natural token for real data —
  consistent with the day-patch conclusion of note 16.

## Verdict

Adopted as the taxonomy that names our design (factorized encoder) and as
independent evidence for modular measurement/dynamics separation. Tubelet
tokenization noted for Phase-4 real EMA.
