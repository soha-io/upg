# 33 — LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2022)

**One line:** adapt a pretrained model by learning only a low-rank *update*
$\Delta W = BA$ while freezing $W_0$ — adaptation lives in a tiny subspace —
which is, almost verbatim, our rule W7.

## The math

For a frozen pretrained weight $W_0 \in \mathbb{R}^{d\times k}$, parameterize
the adapted weight as

$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r}\,B A,\qquad
B \in \mathbb{R}^{d\times r},\ A \in \mathbb{R}^{r\times k},\ r \ll \min(d,k),$$

with $A \sim \mathcal{N}(0,\sigma^2)$, $B = 0$ at init (so adaptation starts
exactly at the pretrained model), scale $\alpha/r$ decoupling step size from
rank. Only $A, B$ train: parameter count drops by orders of magnitude, no
inference latency (merge $BA$ into $W$ after training), and the empirical
finding: **very small $r$ (1–4) suffices** — the intrinsic dimension of the
adaptation is tiny even when the model is enormous.

## What it means for the UPG

- **W7 is LoRA for people.** Rule W7 personalizes as
  $W_{t+1} = (1-\rho)W_t + \rho \hat W_t$ starting from the consensus
  $\bar W$; step 5 parameterizes $\hat B = \bar B \odot e^\Delta$ with the
  *correction* $\Delta$ learned and zero-initialized. Same design logic as
  LoRA: freeze the knowledge (theory prior / pretrained weights), learn a
  small structured deviation, start at the prior. The LoRA evidence — that
  adaptations are intrinsically low-dimensional — is a transferable
  hypothesis about persons: **individual deviations from the consensus graph
  may be low-rank** (a person differs along a few coherent axes, not 522
  independent edges). Testable on our simulator immediately: SVD the
  population of true $B^{(p)} - \bar B$; if the spectrum concentrates, a
  rank-$r$ person model is justified and the per-person parameter count
  collapses from |edges| to $r(2n)$ — a substantial identifiability win at
  small $T$. Registered as a step-5 experiment.
- (Honest caveat, recorded: our simulator generates i.i.d. multiplicative
  edge noise, which is *full-rank* by construction — so on synthetic data
  the test measures what estimation *loses* by assuming low rank, while the
  truth of low-rankness is a real-data question for Phase 4. Both directions
  are informative.)
- **For the amortized estimators:** once a population-level step-6 model
  exists, per-person adaptation should be LoRA-style (small $r$ adapters per
  person) rather than full fine-tuning — cheap, reversible, auditable
  (a person's model = population model + inspectable $\Delta$).

## Verdict

Adopted conceptually everywhere (it *is* W7), adopted concretely as: (i) the
zero-initialized correction parameterization in step 5; (ii) the person-
deviation rank experiment; (iii) the Phase-4 per-person adapter design.
