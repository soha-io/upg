# 45 — The Hidden Attention of Mamba Models (Ali, Zimerman & Wolf, 2024)

**One line:** unroll Mamba's selective recurrence and it defines *implicit
attention matrices* — data-dependent weights over past positions — so
Mamba can be analyzed (and audited) with the same attention-map toolkit as
transformers.

## The math

Unrolling $x_t = \bar A_t x_{t-1} + \bar B_t u_t,\ y_t = C_t x_t$ back to
the start:

$$y_t = \sum_{s \le t} \underbrace{C_t \Big(\prod_{r=s+1}^{t} \bar A_r\Big) \bar B_s}_{\tilde\alpha_{ts}}\; u_s,$$

so the output is a weighted sum over all past inputs with weights
$\tilde\alpha_{ts}$ — formally identical to a (causal, unnormalized)
attention matrix, except the "attention" arises from *products of
input-dependent transition operators* along the path from $s$ to $t$ rather
than from query–key similarity. The paper computes these matrices for
trained Mambas, shows they are structured and informative (comparable to
transformer attention maps, usable for explainability — e.g.
attention-rollout-style relevance), and uses the view to compare the two
families' information routing.

The identity also clarifies the difference: transformer attention weights
are pairwise and directly parameterized; Mamba's are *path products* —
influence from $s$ to $t$ is mediated through every intermediate step's
forgetting decisions ($\prod \bar A_r$), i.e. it decays multiplicatively
unless the gates choose to preserve it.

## What it means for the UPG

- **This is our own mathematics again — verbatim.** In the UPG, the
  influence of occasion $s$ on occasion $t$ is the product of Jacobians
  along the trajectory, $\partial x_t/\partial \varepsilon_s =
  \prod_{r=s+1}^{t} J_r$ — exactly the $\prod \bar A_r$ structure — and our
  loop-gain/critical-slowing analysis is the study of when such products
  decay ($\rho < 1$) or persist ($\rho \to 1$). Mamba's hidden attention is
  the estimator-side mirror of the theory's propagator. Practical payoff:
  if we field an SSM forecaster, its $\tilde\alpha_{ts}$ maps are directly
  comparable to the model-implied propagator $\prod J_r$ from the fitted
  graph — *two independent routes to "which past events still act on this
  person now,"* and their agreement is a validation check no black-box
  model could offer.
- **Auditability parity:** the main practical objection to SSMs vs.
  transformers in a no-black-box project — "attention is inspectable,
  recurrences aren't" — is dissolved; both families now expose comparable
  relevance maps. The step-6 architecture decision (note 46) can be made on
  statistical grounds alone.
- The decay structure gives a diagnostic: hidden-attention mass
  concentrating at short lags ⇒ the model sees a strongly contracting
  person ($\rho \ll 1$); slowly-decaying rows ⇒ near-critical dynamics.
  Same early-warning logic as note 26's rank statistic, from the SSM side.

## Verdict

Adopted as the audit method if/when the SSM challenger is implemented, and
— more valuable — as the propagator-correspondence validation experiment
linking deep-model relevance maps to the fitted graph's $\prod J_r$.
A satisfying convergence for the Phase-3 manuscript.
