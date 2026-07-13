# 30 — Train Short, Test Long: Attention with Linear Biases (ALiBi; Press, Smith & Lewis, 2022)

**One line:** skip position embeddings entirely; subtract a head-specific
penalty proportional to distance from every attention logit — and the model
extrapolates to sequences far longer than it trained on.

## The math

For head $h$ with slope $m_h$, the causal attention logits become

$$A_{ts} = \frac{q_t^\top k_s}{\sqrt d} - m_h\,(t - s),\qquad s \le t,$$

with slopes fixed (not learned) as a geometric sequence
$m_h = 2^{-8h/H}$ for $H$ heads: some heads see only the recent past (large
$m_h$), others reach far back (small $m_h$). That is the entire method.

Why it extrapolates: the bias is defined for *every* distance, and its
linear form means longer test sequences merely extend a penalty ramp the
model already understands; learned absolute embeddings, by contrast, are
undefined (or untrained) beyond the training length, and sinusoidal/rotary
schemes extrapolate only partially. Empirically: train at 1024, test at
2048+ with *no* perplexity degradation, where sinusoidal and rotary degrade.

Interpretation: ALiBi is a fixed recency prior over the attention graph —
an exponential-ish decay kernel per head after softmax — with the
QK content term modulating it.

## What it means for the UPG

- **Our deployment reality is exactly "train short, test long":** simulator
  training series are $T = 100\text{–}200$; a monitored patient produces
  thousands of occasions. An estimator that silently degrades past its
  training length is a clinical hazard; ALiBi is the one positional scheme
  with demonstrated graceful extension, so **step 6 adopts ALiBi** as its
  temporal encoding.
- **The recency prior is dynamically correct for us.** Near a stable
  attractor, dependence on the past decays geometrically at rate
  $\rho(J)^k$ — the true influence kernel *is* an exponential decay. ALiBi's
  per-head slopes are therefore a correctly-shaped prior family, and the
  head slopes bracket plausible $\rho$ values. (Where this breaks —
  near-critical persons with $\rho \to 1$, long memory — the small-slope
  heads carry the load; the geometric slope spectrum covers both.)
- Free bonus: no positional parameters to train = fewer parameters at our
  tiny scale, and one less thing to gradient-check in the NumPy
  implementation.

## Verdict

Adopted as the step-6 positional scheme (with the $\rho$-matching argument
stated in the report). RoPE (note 29) supersedes it when real timestamps and
irregular gaps arrive, unless timestamp-aware ALiBi ($m_h\,\Delta\text{time}$
— the natural generalization) proves sufficient; that comparison is
registered for Phase 4.
