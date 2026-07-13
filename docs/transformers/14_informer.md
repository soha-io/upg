# 14 — Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting (Zhou et al., 2021)

**One line:** most attention rows are nearly uniform (uninformative); keep
only the queries whose attention distribution deviates most from uniform —
sparsity by information content, plus one-shot decoding for long horizons.

## The math

- **ProbSparse attention.** Measure how far query $i$'s attention
  distribution is from uniform with a max-mean surrogate of KL divergence:
  $$\bar M(q_i, K) = \max_j \frac{q_i k_j^\top}{\sqrt d} - \frac{1}{L_K}\sum_j \frac{q_i k_j^\top}{\sqrt d}.$$
  Keep the top-$u$ queries by $\bar M$ ($u = c\ln L_Q$); the rest output the
  mean of values (their attention was ~uniform anyway). Cost drops to
  $\mathcal{O}(L \ln L)$. The bound justifying the surrogate: for the true
  sparsity measure $M$, $\bar M$ brackets it within constants under mild
  conditions (their Lemma 1).
- **Self-attention distilling:** between encoder layers, conv + max-pool
  halves the sequence, focusing deeper layers on dominant features.
- **Generative-style decoder:** feed the decoder a start token (a recent
  slice of the series) plus zero placeholders for the whole horizon; predict
  *all* $h$ future steps in one forward pass — no recursive rollout, so no
  error compounding across the horizon.

## What it means for the UPG

- **The sparsity diagnostic transfers even where the efficiency doesn't.**
  At $T \le 200$, full attention is trivial and ProbSparse is unnecessary.
  But $\bar M(q_i, K)$ — "how far from uniform is this row's attention" — is
  a useful *interpretability statistic* for step 6: occasions whose queries
  are high-$\bar M$ are the informative ones (transitions, treatment onsets),
  and we can report *which occasions the forecaster looked at* when issuing a
  warning. Attention near-uniform everywhere would mean the model found no
  temporal structure — a red flag against the dynamics claim.
- **One-shot horizon decoding** (shared with TFT, note 13) is adopted: the
  step-6 forecaster emits $\hat x_{t+1:t+h}$ jointly. For early warning this
  matters: recursive rollout through a nonlinearity near a bifurcation is
  exactly where iterated forecasts explode; direct decoding sidesteps it.
- The **uniform-attention baseline** gives a cheap null: replace learned
  attention with uniform averaging and re-score. If forecasting barely
  degrades, the attention isn't doing temporal work — a null test in the
  spirit of step 8's permutation tests, applied to the deep model.

## Verdict

Efficiency machinery: not needed at Phase-2 scale. Adopted: one-shot
multi-horizon decoding; the $\bar M$ sparsity score as an attention
diagnostic and the uniform-attention null for the step-6 report.
