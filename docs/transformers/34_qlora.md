# 34 — QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023)

**One line:** freeze the base model in 4-bit precision and train LoRA
adapters in 16-bit on top — full-quality finetuning at a fraction of the
memory; the compute-frugality paper.

## The math

Three components:

1. **NF4 (NormalFloat-4):** a 4-bit data type whose quantization levels are
   the quantiles of a standard normal — information-theoretically optimal
   for normally distributed weights (equal probability mass per bin
   minimizes expected distortion for $w \sim \mathcal{N}$). Weights are
   normalized per block, quantized to the nearest of 16 quantile levels.
2. **Double quantization:** the per-block scale constants (32-bit each) are
   themselves quantized (8-bit), saving ~0.37 bits/parameter.
3. **Paged optimizers:** optimizer states page between GPU/CPU on demand to
   survive memory spikes.

Backprop flows *through* the frozen 4-bit weights (dequantized on the fly)
*into* the 16-bit LoRA adapters; gradients never update the quantized base.
Empirically matches 16-bit full finetuning on the benchmarks tested.

## What it means for the UPG

- **The quantile-quantization idea is independently useful to us.** NF4's
  principle — allocate representation levels by the *distribution* of the
  quantity, not uniformly — is exactly how ordinal EMA response scales
  should be treated: a 0–4 symptom item is a quantile code of an underlying
  continuum (the graded-response view in IRT). The measurement layer already
  normalizes to 0–1; the NF4 lens says the *spacing* should follow the
  empirical distribution, i.e. thresholds estimated, not assumed equal —
  aligning our measurement model with psychometric practice through an
  information-theoretic argument.
- **Precision-vs-fidelity discipline:** QLoRA demonstrates that most bits in
  a trained model are redundant *given* an adapter that can compensate. Our
  numbers policy inherits the lesson in reverse: for reproducibility we keep
  float64 in the scientific pipeline (exactness > memory at our scale), and
  quantization becomes relevant only if models ever ship on-device
  (Batch K's patient-facing tools — where a phone-resident forecaster would
  quantize honestly, with the recovery benchmark re-run at each precision).
- Otherwise: an engineering paper for a compute regime (33B–65B params) five
  orders of magnitude above ours.

## Verdict

No Phase-2 action. Two exports: quantile-coded ordinal measurement (aligns
with IRT; Phase-4 measurement model) and the precision-audit policy for any
future on-device deployment.
