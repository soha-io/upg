# 05 — Exploring the Limits of Transfer Learning with T5 (Raffel et al., 2020)

**One line:** every task can be cast as the *same* sequence-to-sequence
interface, and a single model + objective handles all of them — the argument
for one unified prediction interface across UPG tasks.

## The math

Encoder–decoder transformer; all tasks serialized as text-to-text:
translation, classification, regression all become
$p_\theta(\text{output tokens} \mid \text{input tokens})$. The paper's real
contribution is a controlled *ablation program* over objectives (span
corruption beats prefix LM for transfer), architectures, and data scale —
i.e., it is a methods paper about how to compare model variants fairly:
same data, same compute, one axis varied at a time.

Span corruption objective: mask contiguous spans, predict them
autoregressively — a middle point between BERT's token masking and GPT's
full autoregression:

$$\mathcal{L} = -\log p_\theta(\text{masked spans} \mid \text{corrupted sequence}).$$

## What it means for the UPG

- **Unified interface.** Our pipeline has heterogeneous outputs: imputed
  states $\hat x_t$, forecasts $\hat x_{t+h}$, dynamical scalars
  $\hat\rho,\ \hat\kappa^\*$, regime labels, edge weights $\hat B$. The T5
  lesson is to give them one interface — in our case not text but a shared
  encoder trunk with typed heads, trained multi-task. Step 6 implements this:
  one trunk, three heads (reconstruction, forecast, dynamics).
- **Span corruption ≈ EMA dropout.** Our missingness is *bursty* (dropout,
  skipped days) — contiguous spans, not independent tokens. T5's result that
  span-masking transfers better than token-masking predicts that training the
  measurement model with realistic *burst* missingness (which our simulator
  already generates via `dropout_time` and compliance) beats i.i.d. masking.
  This is a concrete, testable design choice we adopt.
- **The ablation discipline** is the real import: when we compare estimator
  variants in the benchmark, one axis at a time on identical presets — the
  scorecard exists precisely so Phase 2 models are compared T5-style, not
  anecdotally.

## Verdict

Adopted: multi-task trunk-plus-heads design; burst-masking during training;
ablation discipline. Rejected: text serialization (our variables are already
numeric graph nodes; flattening them to text would discard the structure that
rule W1 exists to protect).
