# 39 — A Mathematical Framework for Transformer Circuits (Elhage et al., 2021)

**One line:** decompose small attention-only transformers *exactly* into
interpretable algebraic pieces — the residual stream as a shared
communication bus, attention heads as independent read/write operations
factored into QK ("where to look") and OV ("what to copy") circuits — the
founding document of mechanistic interpretability.

## The math

Key reframings (all exact, not approximations):

- **Residual stream as bus.** Every layer reads from and additively writes
  to a shared vector space; the network output is the sum over *paths*
  through these read/write operations ("path expansion"). A one-layer
  attention-only model expands as
  $$T = \underbrace{W_U W_E}_{\text{direct path}} + \sum_h A^{(h)} \otimes W_U W_{OV}^{(h)} W_E,$$
  where $A^{(h)}$ is the attention pattern of head $h$.
- **QK / OV factorization.** Each head is fully described by two low-rank
  matrices: $W_{QK} = W_Q^\top W_K$ (which source positions a destination
  attends to — bilinear form scoring token pairs) and
  $W_{OV} = W_O W_V$ (how an attended token's content transforms the
  output). Attention pattern and information movement are *separable*
  analyses.
- **Composition.** In two-layer models, heads compose three ways — Q-, K-,
  and V-composition (a head's output feeding a later head's query, key, or
  value) — and this composition is what creates algorithms beyond skip-gram
  statistics, notably **induction heads** (note 40). Virtual heads:
  products $W_{OV}^{(h_2)}W_{OV}^{(h_1)}$ act as effective composed heads.

The method throughout: treat the trained network as a linear-algebraic
object and *expand it into a sum of interpretable terms* — eigendecompose
$W_{OV}$ (copying = positive eigenvalues), inspect $W_{QK}$ bilinear forms.

## What it means for the UPG

- **This is requirement 17 ("no black box") holding at the frontier.** The
  deep models we add in steps 5–6 do not exempt themselves from the
  project's transparency charter, and this paper shows the charter is
  *achievable*: at our scale (1–2 layers, $d\le 32$, $n=7$ tokens) the
  path expansion is not merely possible but easy — we can write our trained
  forecaster as prior-path + head contributions and *print every term*.
  The step-6 report includes exactly this decomposition (direct/residual
  path vs. attention-path contributions to each forecast).
- **QK/OV maps onto our estimation semantics:** in the step-5 estimator, the
  QK circuit is "which source dimensions modulate edge $i{\leftarrow}j$"
  (evidence selection) and OV is "how strongly the modulation moves
  $\hat B_{ij}$" (effect size) — auditing them separately is how we verify
  the estimator uses theory-sanctioned evidence and not artifacts.
- **The residual stream = signed superposition.** A shared additive bus that
  every module reads/writes, with interference when many things superpose,
  is Axiom 5's algebra realized in silicon; even their "superposition"
  vocabulary matches. For Phase 3 this is the strongest available
  demonstration that interpretable decomposition of learned dynamical
  operators is a mature methodology we can import wholesale.

## Verdict

Adopted as the *audit methodology* for every deep component we train: path
expansion + QK/OV inspection at our (tiny) scale, reported alongside
accuracy. This paper is why our deep estimators can claim to stay inside
the project's transparency rules.
