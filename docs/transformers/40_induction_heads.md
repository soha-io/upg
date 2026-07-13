# 40 — In-Context Learning and Induction Heads (Olsson et al., 2022)

**One line:** a specific two-head circuit — find the previous occurrence of
the current token, attend to what followed it, predict that — emerges
abruptly during training and appears to be the mechanical substrate of
in-context learning.

## The math / the mechanism

An **induction head** implements the rule: given context
$\dots A\, B \dots A \to\ \text{predict } B$. Mechanically (using note 39's
machinery): a *previous-token head* in an earlier layer writes "token at
$s{-}1$" information into position $s$'s residual stream (K-composition
fodder); the induction head's QK circuit then matches the current token
$A$ at $t$ against positions whose *predecessor* was $A$, so attention lands
on $s$ (the old $B$); its OV circuit copies $B$ into the prediction.
Prefix-matching + copying = a learned nearest-pattern lookup.

Evidence assembled: (i) induction heads and in-context learning ability
(loss at late context positions minus early positions) appear together in a
sharp *phase change* during training, visible as a bump in the loss curve;
(ii) ablating induction heads selectively destroys in-context learning;
(iii) the same heads do fuzzy versions (match similar-not-identical
patterns), suggesting the mechanism generalizes beyond literal copying.
In small attention-only models the case is airtight; for large models it is
argued as correlational-but-strong.

## What it means for the UPG

- **The microscope result for our amortized estimator.** If step 6's
  transformer personalizes in-context (note 04's protocol: population-train,
  person-test), the mechanistic question is *what circuit does the
  personalizing*. The induction-head recipe predicts a specific, checkable
  pattern for dynamics: heads that attend from the current state-neighborhood
  to *what followed similar states earlier in this person's history* —
  a learned nearest-neighbor forecaster over the person's own past
  (kernel regression again, note 27; "fuzzy induction" over continuous
  states). At our scale we can test this directly: inspect whether trained
  attention concentrates on past occasions with similar $(x, u)$ — and the
  answer is interesting either way (yes ⇒ the model does case-based
  dynamics; no ⇒ it compresses into weights, more SSM-like).
- **Phase changes during training matter for our benchmark discipline:**
  capability can arrive abruptly, so evaluating estimators at one training
  budget can misrank methods (a model stopped pre-phase-change looks
  spuriously bad). Step-6 training curves are therefore logged and reported,
  not just final numbers — the cheap insurance this paper recommends.
- The loss-bump-as-diagnostic transfers: monitoring in-context score
  (late-window minus early-window forecast error) tells us *when* the model
  has learned to use person history as evidence rather than just population
  regularities — the exact capability our clinical use case needs.

## Verdict

Adopted: the in-context score as a step-6 training diagnostic; attention
inspection for fuzzy-induction (similar-state lookup) in the report; full
training curves logged. Together with 39 it defines our audit protocol.
