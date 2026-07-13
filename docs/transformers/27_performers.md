# 27 — Rethinking Attention with Performers (Choromanski et al., 2021)

**One line:** softmax attention is a kernel; approximate the kernel with
random features and attention becomes a product of two linear maps —
mathematically the deepest of the efficiency papers, and the bridge to the
attention-as-regression theory (notes 38, 41).

## The math

Softmax attention weight $\propto \exp(q^\top k/\sqrt d)$ is a kernel
evaluation $K(q,k)$. If we can write $K(q,k) = \mathbb{E}[\phi(q)^\top\phi(k)]$
for a feature map $\phi$, then

$$\mathrm{Attn}(Q,K,V) = D^{-1}\big(\phi(Q)\,[\phi(K)^\top V]\big),\qquad
D = \mathrm{diag}\big(\phi(Q)[\phi(K)^\top \mathbf{1}]\big),$$

computable left-to-right in $\mathcal{O}(T\,r\,d)$ ($r$ = feature count) —
linear in $T$ because the $T\times T$ matrix is never formed.

**FAVOR+ positive random features** for the softmax kernel: using
$\exp(q^\top k) = \mathbb{E}_{\omega\sim\mathcal N(0,I)}\big[\exp(\omega^\top q - \tfrac{\|q\|^2}{2})\exp(\omega^\top k - \tfrac{\|k\|^2}{2})\big]$,

$$\phi(x) = \frac{1}{\sqrt r}\, e^{-\|x\|^2/2}\big(e^{\omega_1^\top x}, \dots, e^{\omega_r^\top x}\big),$$

with orthogonalized $\omega_i$ to cut variance. Positivity of the features
(unlike trigonometric features) prevents the estimator's relative error from
exploding when true attention weights are near zero — the reason FAVOR+
works where earlier random-feature attention failed.

## What it means for the UPG

- **The kernel view is the statistically legible reading of attention:**
  attention output at query $q_t$ is Nadaraya–Watson kernel regression,
  $$\hat v(q_t) = \frac{\sum_s K(q_t, k_s)\, v_s}{\sum_s K(q_t, k_s)},$$
  i.e. a nonparametric regression estimator over the context. This single
  identification does two things for us: (i) it makes "the transformer is a
  statistical instrument" literal — the forward pass *is* kernel smoothing
  with a learned metric; (ii) it imports the classical bias–variance theory
  of kernel regression for reasoning about what attention can estimate from
  $T$ occasions (bandwidth ↔ temperature $\sqrt d$; effective sample size ↔
  attention entropy). The step-6 report uses attention-entropy as the
  effective-$n$ diagnostic on these grounds.
- The random-feature construction itself is the standard variance-reduction
  toolkit (Monte-Carlo kernel estimates, orthogonal sampling) — good craft,
  not needed at our scale, and stochastic (cf. exactness policy, note 23).

## Verdict

Approximation rejected (scale + exactness policy); the kernel-regression
identity adopted as the interpretive frame for step 6's attention
diagnostics and as the formal link into notes 38/41 (attention ↔ regression
↔ dynamics).
