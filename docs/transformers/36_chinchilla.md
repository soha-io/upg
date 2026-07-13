# 36 — Training Compute-Optimal Large Language Models (Chinchilla; Hoffmann et al., 2022)

**One line:** Kaplan's compute allocation was wrong — at fixed compute,
model size and data should scale *equally* ($N \propto C^{1/2}$,
$D \propto C^{1/2}$); most large models were oversized and undertrained.
A 4× smaller model on 4× more data won.

## The math

Parametric loss model fitted to hundreds of runs:

$$L(N, D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}},\qquad
\hat\alpha \approx 0.34,\ \hat\beta \approx 0.28,\ E = \text{irreducible loss},$$

minimized subject to $C = 6ND$. Lagrange condition
$\alpha A N^{-\alpha} = \beta B D^{-\beta}$ gives

$$N_{opt} \propto C^{a},\quad D_{opt} \propto C^{b},\qquad
a = \frac{\beta}{\alpha+\beta} \approx 0.46,\ b = \frac{\alpha}{\alpha+\beta} \approx 0.54,$$

i.e. ≈ equal scaling — against Kaplan's $a \approx 0.73$. The discrepancy
traces to methodology (learning-rate schedules not tuned per-duration in the
earlier work): **a fitted scaling law is only as good as the per-point
optimization discipline underneath it.** Chinchilla (70B params, 1.4T
tokens) beat Gopher (280B, 300B tokens) at equal compute.

## What it means for the UPG

- **The additive three-term loss is the right template for our recovery
  laws** (better than note 35's multiplicative form): for person-level
  estimation,
  $$\mathrm{Err}(P, T) \approx E_{\text{meas}} + \frac{A}{P^{\alpha}} + \frac{B}{T^{\beta}},$$
  with $E_{\text{meas}}$ the errors-in-variables floor, a $P$ term for what
  population pooling buys (prior quality / amortization), and a $T$ term for
  person identifiability. Fitting this surface on the simulator gives the
  study-design optimizer directly: for a fixed assessment budget
  $C = P \times T$ (total EMA prompts funded), the Lagrange condition
  hands us the optimal persons-vs-occasions split — the exact question
  every ESM grant application answers by folklore. This is implemented as
  the design-curve analysis in the step-4 report.
- **The correction story is a methods warning we inherit:** our benchmark
  compares estimators across $T$; if per-$T$ hyperparameters (ridge
  strength, training epochs) are not re-tuned at each $T$, we will draw
  Kaplan-style wrong conclusions about how methods scale. The benchmark
  protocol therefore re-tunes per cell, within the fixed budget rule of
  note 06.
- The irreducible term $E$ has a physical identity for us (measurement
  reliability), which real studies can *buy down* (better instruments,
  more items) — an axis LLM training lacks. Worth stating in the
  manuscript: psychology can move its entropy floor.

## Verdict

Adopted: additive scaling-law template, budget-optimizer analysis
($P$ vs. $T$ at fixed prompts), per-cell retuning discipline. Together with
note 35 this turns Phase-4 study design into a computed answer.
