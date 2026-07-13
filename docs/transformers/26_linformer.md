# 26 — Linformer: Self-Attention with Linear Complexity (Wang et al., 2020)

**One line:** the attention matrix is empirically low-rank, so project keys
and values to a fixed small dimension $k$ before attending — linear cost —
justified by Johnson–Lindenstrauss; for us, the interesting part is the
low-rank claim itself.

## The math

Empirical observation: the spectrum of
$P = \mathrm{softmax}(QK^\top/\sqrt d)$ decays fast — most of its action lies
in a low-dimensional subspace (checked by cumulative eigenvalue mass across
layers/heads of trained models).

Mechanism: insert learned projections $E, F \in \mathbb{R}^{k \times T}$ on
keys and values:

$$\mathrm{Attn}(Q, K, V) \approx \mathrm{softmax}\!\Big(\frac{Q\,(EK)^\top}{\sqrt d}\Big)(F V),$$

cost $\mathcal{O}(Tk)$ instead of $\mathcal{O}(T^2)$. The JL argument: random
(hence also learned) projections to $k = \mathcal{O}(\log T / \varepsilon^2)$
preserve inner products within $(1\pm\varepsilon)$, so attention scores
survive projection; the theorem's $k$ is dimension-free in $T$ up to the log.

## What it means for the UPG

- **The low-rank observation is a statement about the world, and ours
  agrees.** Psychological dynamics being effectively low-dimensional is the
  UPG's founding bet (8 dimensions carrying a 253-node graph; Batch J's
  spectral gap). Linformer finds trained attention discovers low rank in
  language; our attractor dynamics live near low-dimensional manifolds
  (near a fixed point, activity concentrates along the slow eigenvectors of
  $J$ — dimension = number of $|\lambda_i(J)|$ near 1, typically 1–2). The
  agreement suggests: (i) small $d_{\text{model}}$ suffices for step 6
  (we use 16–32); (ii) the *measured rank* of learned attention over our
  data is an estimate of the dynamical dimension — a statistic worth
  reporting, connecting the deep model back to $\rho(J)$.
- **Rank as diagnostic:** compute the effective rank
  $r_{\text{eff}} = \exp(H(\sigma_i^2/\sum\sigma_j^2))$ (entropy of
  normalized squared singular values) of step-6 attention matrices on
  synthetic persons: near transitions the slow subspace grows —
  rank statistics may themselves carry early-warning signal (critical
  slowing = one eigenvalue approaching 1 = rank-1 dominance). Registered as
  an exploratory analysis, not a claim.
- The projection trick itself: unnecessary at our $T$.

## Verdict

Mechanism rejected (scale), observation adopted: low-rank attention supports
small model width, and attention effective-rank is added to the step-6
diagnostics as an exploratory early-warning statistic.
