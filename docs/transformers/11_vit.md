# 11 — An Image is Worth 16×16 Words: Vision Transformers (Dosovitskiy et al., 2021)

**One line:** chop a non-language signal into patches, linearly embed each
patch as a token, and a standard transformer does the rest — tokenization is
a modeling decision, and inductive bias trades off against data volume.

## The math

Image $x \in \mathbb{R}^{H\times W\times C}$ → $N = HW/P^2$ flattened patches
$x_p^{(i)} \in \mathbb{R}^{P^2C}$ → tokens via one linear map $E$:

$$z_0 = [\,x_{\text{cls}};\; x_p^{(1)}E;\; \dots;\; x_p^{(N)}E\,] + E_{pos},$$

then a plain transformer encoder; classify from the `[CLS]` token. The
key finding is a *data-dependence crossover*: with mid-sized data, CNNs
(locality + translation-equivariance baked in) win; with very large
pretraining data, ViT overtakes — learned structure eventually beats built-in
structure, *but only past a data threshold*.

The `[CLS]` token: a learned vector that attends to everything and serves as
a trainable global readout — one designated aggregation point.

## What it means for the UPG

- **The crossover result is a quantitative argument for our priors.** Our
  per-person data ($T \sim 10^2$) sit far below any crossover; the regime
  where built-in structure (skeleton mask, sign constraints, tanh dynamics)
  beats learned-from-scratch flexibility. The recovery study already showed
  this empirically (free estimator RMSE 0.846 vs. anchored 0.364 at $T=30$);
  ViT explains *why* — and predicts the ordering flips only when data grow by
  orders of magnitude, i.e. pooled multi-study corpora in Phase 4+.
- **Patch embedding legitimizes window tokens.** A patch is just a local
  chunk linearly embedded; for time series the same move gives PatchTST
  (note 16), which we adopt for long series. ViT is the reason that move is
  trusted.
- **`[CLS]`-style readout = person token.** Step 6 uses a learned person-level
  token whose final state feeds the dynamical heads ($\hat\rho$, regime,
  $\hat\kappa^\*$) — the person's summary embedding, exactly the `[CLS]`
  pattern.

## Verdict

Background adoption: justifies patch/window tokenization (via note 16) and
the person-summary token in step 6; sharpens the data-threshold argument for
keeping hard theory constraints at current sample sizes.
