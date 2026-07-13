# 15 — Autoformer: Decomposition Transformers with Auto-Correlation (Wu et al., 2021)

**One line:** build trend/seasonal decomposition *into* the architecture and
replace point-wise attention with attention over *lagged series segments*
selected by autocorrelation — attention in the frequency/lag domain.

## The math

- **Series decomposition block** (used repeatedly *inside* the network, not
  once as preprocessing):
  $$x_{\text{trend}} = \mathrm{AvgPool}_{k}(x)\ (\text{moving average}),\qquad
  x_{\text{seasonal}} = x - x_{\text{trend}}.$$
  Each layer refines both streams; the decoder accumulates trend separately
  and adds it back at the end.
- **Auto-correlation mechanism.** Instead of query–key similarity between
  time *points*, measure similarity between the series and its *lagged self*:
  $$R_{xx}(\tau) = \lim_{L\to\infty}\frac{1}{L}\sum_t x_t x_{t-\tau},$$
  computed for all lags at once via FFT (Wiener–Khinchin:
  $R_{xx} = \mathcal{F}^{-1}\{|\mathcal{F}(x)|^2\}$), cost
  $\mathcal{O}(L\log L)$. Pick the top-$k$ lags $\tau_1,\dots,\tau_k$
  ($k = c\log L$), softmax their autocorrelations into weights, and aggregate
  the series *rolled* by those lags:
  $$\mathrm{AutoCorr}(x) = \sum_{i=1}^{k} \widehat{R}(\tau_i)\,\mathrm{Roll}(x, \tau_i),
  \quad \widehat R = \mathrm{softmax}(R(\tau_1),\dots,R(\tau_k)).$$
  Aggregating whole lagged segments (not single points) respects that
  periodic processes match *phase-aligned stretches*, not isolated samples.

## What it means for the UPG

- **Psychological series are trend + rhythm + dynamics.** EMA data carry
  circadian and weekly cycles and slow drifts (season/life-phase) *on top of*
  the attractor dynamics we model. Our generative map produces the dynamics
  but real data will add the rhythms. Autoformer's lesson: **decompose
  inside the estimator**, because a fixed preprocessing detrend leaks and
  misses interactions. For Phase 4 real data, the step-6 front end should
  include a decomposition block, with the *residual* stream feeding the
  graph-dynamics heads — else circadian variance will masquerade as coupling
  ($B$ inflation), a known artifact in network psychometrics (detrending
  debates in the mlVAR literature).
- **The lag-domain view suits slow processes.** Our transitions play out
  over many occasions; point-wise attention can waste capacity matching
  noise-level detail. Attention over lags is a structured prior that
  "influence acts at characteristic delays" — a soft, learnable version of
  choosing the VAR lag order.
- **Warning for the simulator:** synthetic data have *no* seasonal component,
  so decomposition machinery would fit nothing in Phase 2 and can only be
  validated once rhythms are added. Action item recorded: add optional
  circadian/weekly components to `SimConfig` before Phase-4 methods are
  finalized, so the decomposition pathway is recovery-tested too.

## Verdict

Deferred adoption: decomposition front-end + a circadian term in the
simulator, scheduled for Phase 4. In Phase 2 (rhythm-free synthetic data) it
is deliberately excluded to keep the comparison clean.
