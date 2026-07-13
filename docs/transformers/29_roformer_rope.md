# 29 — RoFormer: Enhanced Transformer with Rotary Position Embedding (Su et al., 2021)

**One line:** encode position by *rotating* query/key vectors, so attention
logits depend on relative offset $t-s$ exactly and by construction — the
mathematically cleanest relative-position scheme.

## The math

Work in 2-D planes: pair up the $d$ dimensions of $q, k$ into $d/2$ planes
and rotate the pair in plane $\ell$ at position $t$ by angle $t\,\theta_\ell$,
$\theta_\ell = 10000^{-2\ell/d}$:

$$f(x, t) = R_t\, x,\qquad R_t = \bigoplus_{\ell} \begin{pmatrix}\cos t\theta_\ell & -\sin t\theta_\ell\\ \sin t\theta_\ell & \cos t\theta_\ell\end{pmatrix}.$$

Because rotations are orthogonal and compose additively,

$$\langle R_t q,\; R_s k\rangle = q^\top R_t^\top R_s\, k = q^\top R_{s-t}\, k,$$

the attention logit depends on positions **only through $s - t$** — the
relative-position property is an algebraic identity, not something learned
(compare Transformer-XL's learned decomposition, note 07). Different
$\theta_\ell$ give a geometric spectrum of wavelengths: fast planes resolve
short offsets, slow planes long offsets — a multi-scale clock. Long-range
decay: the sum over rotated planes exhibits decreasing logit magnitude with
$|s-t|$ under mild conditions on $q,k$.

## What it means for the UPG

- **Time-homogeneity, enforced not hoped for.** Our transition law is
  autonomous (depends on $\Delta t$, never absolute $t$); RoPE gives an
  estimator that provably cannot condition on absolute position through the
  attention logits. That closes off a whole class of overfitting (memorizing
  *where* in the study transitions happened rather than *what precedes*
  them) — important when training data are simulated with fixed-schedule
  treatment pulses (`pulsed_treatment` turns on at 25% of the series —
  an absolute-position confound RoPE neutralizes).
- **Continuous time for free:** $R_t$ is defined for real $t$, so irregular
  EMA sampling (actual timestamps, not indices) slots in directly — rotate
  by *clock time*. This is the principled handling of irregular sampling the
  measurement contract needs, better than index-based encodings that treat a
  3-hour and a 3-day gap as equal.
- The multi-scale wavelength spectrum $\{\theta_\ell\}$ should be *chosen*,
  not defaulted: our known timescales (hours: affect; days: symptoms; weeks:
  treatment response) fix the useful band. Registered as a design rule for
  step 6 with real timestamps.

## Verdict

Adopted in principle for timestamped data (Phase 4). Phase-2 synthetic data
are regularly sampled, so step 6 uses the simpler ALiBi (note 30) — same
relative-time goal, one hyperparameter, and better length extrapolation for
our short-train/long-test protocol.
