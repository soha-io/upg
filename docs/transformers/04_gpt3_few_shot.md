# 04 — Language Models are Few-Shot Learners (Brown et al., 2020)

**One line:** a large enough autoregressive transformer can adapt to a new
task from examples *placed in its input*, without weight updates — the
phenomenon (in-context learning) that notes 41–42 later explain as implicit
regression.

## The math

Nothing new architecturally (decoder-only, 96 layers, 175B params). The
contribution is an empirical claim about the *conditional*:

$$p_\theta\big(y \mid (x_1,y_1),\dots,(x_k,y_k),\, x\big)$$

improves with $k$ (shots) and with model scale, despite $\theta$ being fixed.
Formally: the model has learned, during pretraining, a mapping from a
*dataset placed in context* to a *predictor* — a learned learning algorithm.
Performance scales smoothly as a power law in parameters (validation loss
$L(N) \propto N^{-\alpha}$, continuing note 35's laws), and few-shot gains
grow with scale, i.e. bigger models are better in-context *estimators*.

The meta-learning reading: pretraining on a mixture of implicit tasks makes
the forward pass approximate a posterior predictive,

$$p(y \mid \mathcal{D}_{\text{context}}, x) = \int p(y \mid x, \tau)\, p(\tau \mid \mathcal{D}_{\text{context}})\, d\tau,$$

where $\tau$ indexes tasks — Bayesian inference *executed by attention*, not
by an explicit algorithm.

## What it means for the UPG

- This is the strongest available evidence for the roadmap's framing of
  "AI as a statistical instrument": a transformer can *behave as* an
  estimator whose "data" arrive at inference time. For us the context window
  is one person's EMA history; the implicit task variable $\tau$ is the
  person's $(B, b, \kappa)$; the posterior-predictive reading says a
  transformer trained across many synthetic persons should *implicitly
  personalize* — infer person parameters in-context and forecast accordingly.
  Step 6 tests exactly this: train on a population, evaluate on unseen
  persons, and check whether forecast error approaches the oracle that knows
  the true $(B,b,\kappa)$.
- The Bayesian-integral reading connects to rule W7: our estimator family is
  posterior-predictive by construction; the transformer version amortizes it.
  Amortized inference = fit once on the population, personalize for free per
  person — clinically important because per-person refitting is what makes
  idiographic methods expensive.
- The caution transfers too: in-context ability emerges with scale and
  pretraining diversity. At our tiny scale we should *not* expect free-form
  few-shot magic; we get amortized personalization only because our task
  distribution (the simulator) is narrow and known.

## Verdict

Conceptual cornerstone for step 6's population-train / person-test protocol
(amortized personalization). No architectural import. Read together with 41
and 42, which turn the phenomenon into math.
