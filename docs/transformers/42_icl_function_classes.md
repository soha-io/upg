# 42 — What Can Transformers Learn In-Context? A Case Study of Simple Function Classes (Garg et al., 2022)

**One line:** train a transformer from scratch on prompts of $(x, f(x))$
pairs with $f$ drawn from a known function class, and it learns to *be* an
estimator for that class — matching least squares on linear functions and
holding up on sparse-linear, decision-tree, and small-network classes.

## The math

Formal definition: a model $M$ learns function class $\mathcal{F}$
in-context if for $f \sim \mathcal{F}$, inputs $x_i \sim D_x$,

$$\mathbb{E}\big[\,\ell\big(M(P), f(x_{q})\big)\,\big] \le \varepsilon,\qquad
P = (x_1, f(x_1), \dots, x_N, f(x_N), x_{q}),$$

i.e. average prediction error over fresh prompts is small. Training:
minimize $\sum_i \ell(M(P_{1:i}), f(x_{i+1}))$ over random draws of $f$ and
inputs — the model is literally optimized to be a *learning algorithm*
scored at every prompt length.

Results that matter:

- **Linear class:** error tracks *optimal least squares* as a function of
  the number of in-context examples, including the classical error curves
  around $N \approx d$ — the transformer behaves like the Bayes-optimal
  estimator for the class, not a lookup heuristic.
- **Sparse linear ($s$-sparse $w$):** error beats OLS and tracks **Lasso**
  sample efficiency — the model *discovers regularization appropriate to
  the task prior* from the task distribution alone.
- **Robustness/OOD:** performance degrades gracefully under covariate
  shift, out-of-range queries, and prompt-composition shifts (with
  documented failure directions).
- Curriculum (growing $d$ and $N$ during training) needed for the larger
  settings to train reliably.

## What it means for the UPG

- **The sparse-linear result is the pivotal one for us.** The task prior
  (sparsity) got *baked into the learned estimator* without anyone writing
  down an $\ell_1$ penalty. Translate: train the step-6 transformer on
  prompts generated from persons drawn around $\bar B$ with our simulator's
  perturbation law, and the learned in-context estimator should incorporate
  *our theory prior* — support, signs, magnitude ranges — implicitly,
  with sample-efficiency gains over unregularized fitting mirroring
  Lasso-over-OLS. This is rule W7 emerging from population training, and
  it is directly measurable: compare in-context error curves vs. context
  length $T$ against the explicit prior-anchored estimator's recovery
  curves from step 3/4 — same axes, same truth, on the same plots.
- **The experimental *design* transfers wholesale:** "function class" =
  our generative person family; "prompt" = an EMA window; "query" = next
  occasions; error-vs-$N$ curves = our recovery-vs-$T$ curves. Their
  protocol is the deep-learning mirror of our method-recovery study, which
  lets us report both estimator families in one framework — the concrete
  format adopted for the step-6 study.
- **The OOD probes define our robustness section:** persons outside the
  training family (heavier-tailed edge noise, regime mixtures not seen in
  training, $\kappa$ beyond the sampled range) are the covariate-shift
  analogue; the graceful-degradation-or-not answer decides how far the
  amortized estimator can be trusted on real patients, before real patients.

## Verdict

Adopted as the experimental blueprint for step 6's estimator evaluation
(error-vs-context-length against explicit baselines + OOD person probes).
With 41 it forms the two-paper theoretical core of "the transformer as a
trainable statistical instrument."
