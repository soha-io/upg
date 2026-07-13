# 31 — Root Mean Square Layer Normalization (Zhang & Sennrich, 2019)

**One line:** LayerNorm's benefit comes from re-scaling, not re-centering —
drop the mean subtraction, normalize by the RMS alone, keep the quality,
save the compute.

## The math

LayerNorm: $\ \mathrm{LN}(x) = \frac{x - \mu}{\sigma}\odot\gamma + \beta$,
with $\mu, \sigma$ the per-vector mean/SD. RMSNorm:

$$\mathrm{RMSNorm}(x) = \frac{x}{\mathrm{RMS}(x)}\odot\gamma,\qquad
\mathrm{RMS}(x) = \sqrt{\tfrac{1}{d}\sum_{i=1}^{d} x_i^2 + \epsilon}.$$

Properties: (i) invariance to input *scaling* ($x \to \alpha x$ gives the
same output), which is the property that stabilizes gradient magnitudes
across depth — $\partial\mathrm{RMSNorm}/\partial x$ has norm
$\mathcal{O}(1/\mathrm{RMS}(x))$, so upstream blow-ups are damped; (ii) *no*
invariance to shifts, which LayerNorm has and — per the ablations — barely
uses; (iii) ~10–30% cheaper normalization and one fewer learned parameter
vector ($\beta$ dropped).

The projection view: LayerNorm maps onto the sphere within the
mean-zero hyperplane; RMSNorm maps onto the sphere in the full space.
Empirically the hyperplane constraint contributes nothing reliable.

## What it means for the UPG

- Directly practical: our from-scratch NumPy transformer implements one
  normalization; RMSNorm is chosen because it is (a) the modern default,
  (b) *simpler to differentiate by hand* — the Jacobian is
  $$\frac{\partial y}{\partial x} = \frac{\gamma}{\mathrm{RMS}(x)}\Big(I - \frac{x x^\top}{d\,\mathrm{RMS}(x)^2}\Big),$$
  one projection term instead of LayerNorm's two — which reduces the surface
  for gradient bugs in `autodiff.py` (every hand-derived gradient is a
  liability under requirement 21: double-check everything).
- Conceptual rhyme worth one sentence in the manuscript: normalization as
  homeostatic self-regulation — a fixed operator holding activation scale in
  range — is the network-architecture analogue of the negative self-loops /
  regulation mechanisms the UPG models psychologically (Gross regulation in
  UMEG; the brake loops). Architecture needs its homeostats for the same
  reason persons do: uncontrolled positive feedback diverges.

## Verdict

Adopted: RMSNorm (pre-norm placement) in all step-6 blocks, with the
hand-derived Jacobian above gradient-checked in the test suite.
