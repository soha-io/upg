# 13 — Temporal Fusion Transformers for Interpretable Multi-Horizon Forecasting (Lim et al., 2021)

**One line:** a forecasting transformer engineered for *interpretability and
calibrated uncertainty* — variable-selection weights, gated components, and
quantile outputs — the closest published template for our step-6 forecaster.

## The math

Inputs are typed (the typing matters): static covariates $s$ (per-entity),
known-future inputs (e.g. planned interventions), and observed past inputs.

- **Gated residual network (GRN)**, the basic block:
  $$\mathrm{GRN}(a) = \mathrm{LayerNorm}\big(a + \mathrm{GLU}(W_2\,\mathrm{ELU}(W_1 a))\big),
  \qquad \mathrm{GLU}(x) = \sigma(W_g x)\odot (W_v x).$$
  The GLU gate can shut a component off ($\sigma \to 0$ ⇒ block ≈ identity),
  letting the network use only the machinery the dataset needs.
- **Variable selection:** per time step, softmax weights over the $m$ input
  variables, $v = \mathrm{softmax}(\mathrm{GRN}(\Xi))\in\Delta^{m-1}$, and the
  fused input is $\sum_j v_j\,\tilde\xi_j$. The learned $v_j$ are *reportable
  importances* — which variables the forecast actually used.
- **Temporal processing:** local LSTM encoder → interpretable multi-head
  attention over the horizon (heads share values so attention weights can be
  summed into one readable pattern) → position-wise GRNs.
- **Quantile regression output:** for horizons $h$ and quantiles $q$:
  $$\hat y_{t+h}^{(q)},\qquad
  \mathcal{L} = \sum_{q\in\{.1,.5,.9\}}\sum_h \mathrm{QL}_q\big(y_{t+h},\hat y^{(q)}_{t+h}\big),\quad
  \mathrm{QL}_q(y,\hat y) = \max\big(q(y{-}\hat y),\,(q{-}1)(y{-}\hat y)\big).$$
  Pinball loss is a proper scoring rule for quantiles ⇒ the intervals are
  *trained to be calibrated*, not post-hoc.

## What it means for the UPG

- **Input typing maps one-to-one onto our variables:** static = person
  parameters/traits ($b$, PER baseline, age); known-future = the treatment
  schedule $u_{t+1:t+h}$ (we *know* planned sessions/doses — a genuinely
  known-future input, rare in forecasting and precious here); observed past
  = EMA $y_{1:t}$. Step 6 adopts this three-way typing.
- **Calibration is contractual for us.** The baseline contract demands
  "calibrated intervals or credible intervals." TFT shows the clean way:
  make uncertainty part of the loss (quantile/pinball or Gaussian NLL), then
  *report* empirical coverage. Step 6 uses Gaussian NLL heads (equivalent
  role) and reports 90% interval coverage on held-out synthetic persons.
- **Variable-selection weights are a falsification instrument:** if the
  forecaster's selection weights ignore NEED while the theory says the
  NEED→ME engine drives escalation, either the estimator or the theory is
  wrong — a concrete discrepancy to investigate in the tournament.
- The **early-warning head:** TFT's multi-horizon design (all horizons at
  once, no recursive rollout) avoids compounding rollout error — better for
  detecting *approach to transition* ($\rho \to 1$, van de Leemput) than
  iterated one-step forecasts, so step 6's transition head predicts the full
  horizon vector directly.

## Verdict

Primary template for step 6: typed inputs, gated blocks, direct multi-horizon
heads, loss-integrated uncertainty, reported coverage. We simplify (no LSTM,
smaller GRNs) because $n=7$ and the simulator's dynamics are smooth.
