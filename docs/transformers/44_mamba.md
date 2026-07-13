# 44 — Mamba: Linear-Time Sequence Modeling with Selective State Spaces (Gu & Dao, 2023)

**One line:** make the state-space parameters *input-dependent* — the model
chooses, per token, what to store and what to forget — recovering the
content-based selectivity that made attention win, while keeping
$\mathcal{O}(L)$ time and $\mathcal{O}(1)$ inference state.

## The math

S4's limitation: LTI systems ($A, B, C, \Delta$ constant) treat every input
identically — they cannot, e.g., selectively remember one token and ignore
another (the selective-copying and induction-head tasks isolate this).
Mamba's S6 layer makes the system time-varying as a function of the input:

$$B_t = W_B\, u_t,\qquad C_t = W_C\, u_t,\qquad
\Delta_t = \mathrm{softplus}(W_\Delta u_t),$$
$$\bar A_t = \exp(\Delta_t A),\qquad
x_t = \bar A_t\, x_{t-1} + \bar B_t\, u_t,\qquad y_t = C_t\, x_t.$$

$\Delta_t$ is the crux: large $\Delta_t$ ⇒ $\bar A_t \to 0$ ⇒ *reset state,
absorb current input* (attend); small $\Delta_t$ ⇒ $\bar A_t \to I$ ⇒
*ignore input, preserve memory* (skip). A learned, continuous
gate between remembering and forgetting — which is also exactly a learned,
per-step re-discretization of continuous time.

Input dependence breaks the convolution trick (no fixed kernel), so Mamba
computes the recurrence with a **parallel associative scan** (prefix-scan
over the affine maps $(\bar A_t, \bar B_t u_t)$), fused in SRAM
(FlashAttention-style IO awareness, note 23). Architecture: the S6 layer
inside a gated block (SiLU gate, cf. note 32), homogeneous stack. Matches
same-size transformers on language; linear scaling to million-length
sequences.

## What it means for the UPG

- **Selectivity is state-dependent dynamics — the thing our model has and
  LTI lacks.** Our tanh map's effective dynamics change with state
  ($J$ depends on $x^\*$): near saturation the person is rigid (small
  effective gain), near the middle responsive. Mamba is the first deep
  sequence family whose *mechanism* mirrors this: $\Delta_t$ as
  state/input-conditioned gain control. For step 6 this predicts Mamba-type
  models should excel precisely on *regime-switching* persons
  (`transition_rich` preset) where LTI-ish summaries blur across the
  switch — a concrete, falsifiable benchmark prediction, registered.
- **$\Delta_t$ has a psychological reading worth exploring:** a learned
  forgetting rate per occasion is an *arousal/salience gate* — events that
  reset state vs. events that bounce off. If a trained Mamba's $\Delta_t$
  spikes align with treatment pulses and transitions on synthetic persons
  (checkable — we know where those are), the gate is recovering event
  salience, and on real data becomes an interpretable signal of which
  life-occasions "got in."
- **Irregular sampling, solved natively:** feeding the *actual* inter-prompt
  gap into $\Delta_t$ (rather than learning it) is the formally correct
  continuous-time treatment of EMA spacing — the cleanest solution yet to
  the problem notes 29/30/43 circle around. Adopted as the design of record
  for Phase-4 irregular data, whichever architecture hosts it.

## Verdict

Co-challenger with S4 for the step-6 forecaster; the regime-switching
prediction and the $\Delta_t$-salience probe are registered experiments.
At Phase-2 scale we implement the attention version first (simpler to
hand-differentiate), with the selective-SSM comparison as the follow-on.
