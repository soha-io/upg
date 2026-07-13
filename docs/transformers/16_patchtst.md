# 16 — A Time Series is Worth 64 Words: PatchTST (Nie et al., 2023)

**One line:** two design choices — tokenize time series as *patches* of
consecutive steps, and process channels *independently* with shared weights —
give simple transformers state-of-the-art long-horizon accuracy.

## The math

- **Patching.** Split each univariate channel into (possibly overlapping)
  patches of length $P$ with stride $S$: token count drops from $L$ to
  $N \approx L/S$; each token is $x_{i:i+P}$ linearly embedded. Effects:
  (i) attention cost falls by $S^2$; (ii) each token carries *local semantic
  content* (a windowed shape, not a single noisy sample); (iii) with the
  receptive field per token = $P$, longer lookbacks become usable.
- **Channel independence.** Each of the $m$ channels is forecast by the
  *same* transformer applied separately — no cross-channel attention at all:
  $\hat y^{(j)} = f_\theta(x^{(j)}),\ j = 1..m$, shared $\theta$. Empirically
  this *beats* channel-mixing on standard benchmarks: cross-channel
  dependence is apparently often weak/noisy there, and mixing mostly adds
  variance.
- Self-supervised variant: mask random patches, reconstruct (BERT for
  patches), then fine-tune.

## What it means for the UPG

- **Channel independence is a direct challenge to our core claim.** The UPG
  says cross-dimension coupling ($B$) is the disease mechanism; PatchTST
  says forecasting often doesn't need cross-channel structure. Both can be
  true: forecasting benchmarks reward marginal accuracy, not mechanism.
  **This makes PatchTST the perfect strong null model for step 7:** if a
  channel-independent forecaster matches the graph-coupled forecaster on our
  synthetic data — where we *know* coupling exists — then forecast accuracy
  is simply not the metric that detects coupling ✱ and structural claims
  must be tested on structural metrics (edge recovery, loop gains,
  intervention response), not on RMSE. That conclusion, either way, sharpens
  the whole tournament design.
- **Patching fits EMA burst structure:** a day of 3–5 prompts is a natural
  patch; patch tokens = day summaries with intraday shape preserved. For
  Phase-2 lengths ($T \le 200$) we can afford per-occasion tokens, so
  patching is optional; it becomes valuable for year-long monitoring.
- The masked-patch pretraining objective doubles as our measurement-model
  training (mask whole occasions/days, reconstruct) — consistent with the
  burst-masking conclusion from note 05.

## Verdict

Adopted: PatchTST-style *channel-independent* forecaster is implemented as
the named null model for step 6/7 comparisons (its defeat, or survival, is
itself a finding). Patching deferred until long real series. ✱ = the key
methodological insight this paper contributes to the project.
