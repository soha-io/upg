# 02 — BERT: Pre-training of Deep Bidirectional Transformers (Devlin et al., 2019)

**One line:** train an encoder to reconstruct deliberately masked inputs from
bidirectional context; the resulting representations transfer to every
downstream task — the template for our *measurement model*.

## The math

Masked language modeling (MLM): corrupt a fraction (15%) of tokens, replace
with `[MASK]`, and train the encoder to recover them:

$$\mathcal{L}_{\mathrm{MLM}} = -\mathbb{E}\Big[\sum_{t \in \mathcal{M}} \log p_\theta(x_t \mid x_{\setminus \mathcal{M}})\Big],$$

where $\mathcal{M}$ is the masked index set and $x_{\setminus\mathcal{M}}$ the
visible context. Crucially the conditional uses *both directions* — the
encoder attends to past and future — which is legitimate because the task is
*reconstruction*, not forecasting.

Why this is statistically interesting: MLM is a denoising objective. The
minimizer of the expected loss at a masked position is the conditional
distribution $p(x_t \mid \text{context})$ — i.e. BERT is trained to be an
estimator of the posterior over a missing coordinate given everything
observed. That is *exactly the definition of imputation under missingness*.

Fine-tuning view: pretraining finds $\theta_0$ such that a small
task-specific head $h_\phi$ on top of frozen-ish features solves many tasks;
the claim is that $p(x_t\mid\text{context})$-learning forces general
representations.

## What it means for the UPG

Our measurement problem (docs/measurement_mapping.md) is BERT's problem with
different tokens:

- **EMA items are tokens; skipped items are `[MASK]`.** An occasion with 60%
  of NEED items answered is a partially masked input. A BERT-style encoder
  trained with an MLM loss on synthetic/real EMA learns
  $p(x_{t,i} \mid \text{observed items, other occasions})$ — a principled
  imputation that *respects the dynamics*, unlike mean imputation (which
  measurement rule 4 already forbids).
- **Bidirectionality = smoothing, not filtering.** Statistically, BERT
  computes the analogue of a Kalman *smoother* $p(x_t \mid y_{1:T})$, whereas
  a causal model computes the *filter* $p(x_t \mid y_{1:t})$. For offline case
  formulation (TND) we want the smoother; for real-time early warning we need
  the filter. Step 6 therefore keeps the measurement model bidirectional-
  capable but reports the causal variant for forecasting.
- **The masking rate is a design dial we control.** In EMA the mask is chosen
  by the participant (MNAR risk), not by us. Training on *synthetic* data with
  the simulator's known missingness process lets us verify how far
  MLM-imputation degrades as missingness departs from MCAR — an experiment
  impossible with real data alone.

## Verdict

Adopted as the *pattern* for the step-6 measurement model: mask-token
embeddings for unanswered items, reconstruction loss on synthetic ground
truth, explicit filter/smoother distinction. Not adopted: the 110M-parameter
scale; ours is ~10⁴ parameters because $n=7$ and identifiability, not
capacity, is our binding constraint (notes 35–36).
