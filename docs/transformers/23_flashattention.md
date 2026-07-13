# 23 — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (Dao et al., 2022)

**One line:** exact attention computed tile-by-tile in fast on-chip memory —
never materializing the $T\times T$ matrix — because the bottleneck is memory
traffic, not FLOPs. An algorithms lesson, not a modeling one.

## The math

Attention needs $\mathrm{softmax}(QK^\top/\sqrt d)V$ but $QK^\top$ is
$T \times T$; storing/reading it dominates runtime on GPUs (HBM bandwidth ≪
SRAM bandwidth). FlashAttention streams over key/value tiles and maintains a
*running* softmax via the online-softmax recurrence. For each new tile $j$
with logits $S_j$:

$$m^{new} = \max(m, \mathrm{rowmax}(S_j)),\qquad
\ell^{new} = e^{m - m^{new}}\ell + \mathrm{rowsum}(e^{S_j - m^{new}}),$$
$$O^{new} = \frac{e^{m-m^{new}}\,\ell\, O + e^{S_j - m^{new}} V_j}{\ell^{new}},$$

where $m$ (running max) gives numerical stability and $\ell$ (running
normalizer) lets the softmax be assembled incrementally — mathematically
*exact*, $\mathcal{O}(T^2)$ FLOPs but $\mathcal{O}(T)$ extra memory and far
less IO. The backward pass recomputes attention on the fly from saved
$(m,\ell)$ instead of storing the matrix (recomputation < memory traffic).

## What it means for the UPG

- **Exactness is the point.** The efficiency family (notes 24–27) buys speed
  by *approximating* attention; FlashAttention proved the approximations were
  often unnecessary — reorganize the computation instead. For a project whose
  charter is "no black box, every number reproducible," an exact kernel is
  strictly preferable to a stochastic approximation whenever it suffices.
  Adopted as a policy: prefer exact computation reorganized cleverly over
  approximate computation, at every scale we can afford it.
- The **online-softmax recurrence** is independently useful to us: it is the
  standard trick for numerically stable streaming aggregation, applicable to
  any softmax we compute over long horizons (e.g., streaming evaluation of
  attention diagnostics in deployment).
- Practically: at $n=7$, $T \le 200$, on CPU/NumPy, none of this binds. It
  becomes relevant at 253 nodes × long monitoring × batch training (Phase
  4/5, GPU): then FlashAttention is the default kernel and costs us nothing
  scientifically because it is exact.

## Verdict

No Phase-2 action. Recorded as the standing engineering choice for scaled
training, and as the argument that closes the door on approximate-attention
variants (24–27) unless sequence lengths truly explode.
