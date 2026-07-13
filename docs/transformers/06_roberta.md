# 06 — RoBERTa: A Robustly Optimized BERT Pretraining Approach (Liu et al., 2019)

**One line:** BERT's architecture was fine; its *training recipe* was leaving
most of the performance on the table — data, batch size, masking policy and
training length dominate architectural novelty.

## The math

No new equations; a set of controlled recipe changes to note 02's model:

1. **Dynamic masking** — resample the mask set $\mathcal{M}$ every epoch
   instead of fixing it once, so each sequence is seen under many corruption
   patterns: effectively enlarging the augmentation distribution over
   $(x_{\setminus\mathcal{M}}, \mathcal{M})$ pairs.
2. **More data, longer training, larger batches** — with appropriately scaled
   learning rate (linear-scaling heuristic), bigger batches give lower
   gradient noise $\mathrm{Var}[\hat\nabla] \propto 1/\text{batch}$ and allow
   larger stable steps.
3. **Dropping the next-sentence-prediction loss** — an auxiliary objective
   that ablation showed was not pulling its weight.

Result: same architecture, state-of-the-art results. The quantitative moral:
the gap "recipe vs. architecture" exceeded the gap "BERT vs. its successors."

## What it means for the UPG

- **Direct warning for steps 5–6:** if our GAT underperforms the Bayesian
  baseline, the first suspect is the training recipe (learning rate, epochs,
  masking policy, data volume from the simulator), not the architecture.
  The benchmark protocol therefore fixes a tuning budget for *every*
  estimator, including the classical ones, so comparisons measure the method
  and not the tuning effort.
- **Dynamic masking transfers verbatim:** the step-6 measurement model
  resamples missingness patterns from the simulator each epoch (fresh
  compliance/dropout draws) rather than training on one frozen corrupted
  dataset — cheap for us because the simulator is generative.
- **Auxiliary-loss skepticism:** every extra head we add (regime, $\rho$,
  $\kappa^\*$) must earn its place in ablation, as NSP failed to.

## Verdict

Adopted as discipline, not architecture: dynamic missingness resampling,
per-estimator tuning budgets, ablate every auxiliary loss. This paper is the
reason the Phase-2 reports state the recipe alongside the results.
