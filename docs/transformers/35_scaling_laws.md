# 35 — Scaling Laws for Neural Language Models (Kaplan et al., 2020)

**One line:** test loss falls as a smooth power law in model size, data
size, and compute over many orders of magnitude — performance is
*predictable* from budgets, and architecture details matter far less than
scale.

## The math

With $N$ = non-embedding parameters, $D$ = tokens, $C \approx 6ND$ = compute:

$$L(N) = \Big(\frac{N_c}{N}\Big)^{\alpha_N},\quad
L(D) = \Big(\frac{D_c}{D}\Big)^{\alpha_D},\qquad
\alpha_N \approx 0.076,\ \alpha_D \approx 0.095,$$

and jointly (their Eq. 1.5):

$$L(N, D) = \Big[\Big(\frac{N_c}{N}\Big)^{\alpha_N/\alpha_D} + \frac{D_c}{D}\Big]^{\alpha_D}.$$

Implications derived in the paper: (i) at fixed compute, bigger models
trained shorter beat smaller models trained longer (later corrected by
Chinchilla, note 36); (ii) overfitting is governed by the ratio
$N^{\alpha_N/\alpha_D}/D$ — data requirements grow sublinearly with model
size; (iii) loss depends weakly on shape (depth/width) at fixed $N$ — a
capacity, not architecture, story.

## What it means for the UPG

- **The deep lesson is that estimation error is budgetable.** Our recovery
  study is the same scientific object: recovery-error curves as a function
  of $T$ (data per person). The recovery table behaves like a power law in
  its middle range (edge RMSE 0.364→0.183 for $T$ 30→1000); fitting an
  explicit law $\mathrm{RMSE}(T) \approx (T_c/T)^{\alpha} + \varepsilon_\infty$
  with a *floor* $\varepsilon_\infty$ (the errors-in-variables asymptote
  measurement noise imposes — our analogue of the irreducible entropy term)
  turns "how much data per person?" into a formula with confidence bands
  instead of a table. This fit is added to the step-4 report.
- **Two budget axes, not one:** persons $P$ (population-level, helps the
  amortized/hierarchical estimators) and occasions $T$ (person-level, the
  identifiability constraint). The scaling frame predicts different
  exponents for population-parameter error ($\propto P^{-1/2}$-ish) vs.
  person-parameter error (power law in $T$ with a noise floor) — worth
  measuring once, because the answer dictates study design: recruit more
  people or sample each person longer? That is *the* budget question for
  Phase 4, and the simulator can answer it now.
- Model-sizing corollary for step 6: with $D \sim P \cdot T \cdot n$
  effective observations in the tens of thousands, parameter counts in the
  $10^4$ range are the scaling-consistent choice — our tiny models are not
  a compromise but the correct point on the curve.

## Verdict

Adopted as methodology: fit explicit recovery scaling laws (with noise
floors) in step 4; report the persons-vs-occasions trade-off; size step-6
models by the data budget. High priority, as the registry says.
