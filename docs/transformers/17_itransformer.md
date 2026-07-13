# 17 — iTransformer: Inverted Transformers for Time Series Forecasting (Liu et al., 2024)

**One line:** transpose the token dimension — embed each *variable's whole
series* as one token and let attention act *across variables* — so the
attention matrix becomes a variable-dependency matrix. For us: attention
rows over tokens = rows of $B$.

## The math

Standard temporal transformer: tokens = time steps, embedding mixes variables
at each step. iTransformer inverts:

$$h^{(j)} = \mathrm{Embed}\big(x^{(j)}_{1:T}\big) \in \mathbb{R}^{d},\qquad j = 1..m\ \text{(variables)},$$

then plain self-attention over the $m$ variate tokens:

$$A = \mathrm{softmax}\!\Big(\frac{QK^\top}{\sqrt d}\Big) \in \mathbb{R}^{m\times m},$$

with the feed-forward network applied per variate token (it learns the
*temporal* representation), and LayerNorm across the token (reducing
variate-scale artifacts). Forecast head projects each token back to the
horizon. Attention now models **multivariate correlation explicitly**: entry
$A_{ij}$ is how much variable $i$'s representation draws on variable $j$.

Why this helps where token-per-timestep struggles: a timestep token glues
together simultaneous values of physically different quantities with
misaligned scales and delays; a variate token keeps each series' identity
intact and moves the interaction question to attention, where it is readable.

## What it means for the UPG

- **This is the architecture whose attention matrix has the same *type* as
  our $B$.** $A \in \mathbb{R}^{m \times m}$, rows = targets, columns =
  sources, entries = dependency strengths between *named psychological
  dimensions*. Masked to the skeleton (note 08) and unnormalized (our
  $\bar B\odot e^\Delta$ parameterization), the iTransformer attention block
  *is* the step-5 estimator's natural deep extension: variate tokens built
  from each dimension's observed series, attention constrained to theory
  edges, attention scores read out as personalized couplings.
- It also resolves the step-5/step-6 division of labor cleanly:
  **variate-token attention (this paper) estimates *structure***;
  **time-token attention (notes 01/13) estimates *dynamics/forecasts***.
  The two factorized attentions over the same data are the video-transformer
  factorization (notes 20–21) with space = graph.
- **Caution it inherits:** attention is correlational; an $A_{ij}$ readout
  conflates direct and mediated influence (common-cause SYS drives
  everything). The skeleton mask mitigates by restricting candidates, and
  ground-truth checks on synthetic persons quantify the residual confounding
  — which free iTransformer cannot do.

## Verdict

High adoption. The step-5 GAT is implemented in exactly this spirit (variate
summaries → masked cross-variable attention → edge corrections), and the
step-6 report cites this paper as the reason variables, not time steps, are
the right tokens for *structural* questions.
