# 38 — Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention (Katharopoulos et al., 2020)

**One line:** replace the softmax kernel with a decomposable one and causal
attention becomes an RNN with a matrix-valued hidden state — the exact
mathematical bridge between attention and the state-space/dynamical view.

## The math

Generalized attention with kernel $k(q, s) = \phi(q)^\top\phi(s)$:

$$z_t = \frac{\sum_{s\le t} \phi(q_t)^\top \phi(k_s)\, v_s}{\sum_{s\le t} \phi(q_t)^\top\phi(k_s)}
      = \frac{\phi(q_t)^\top S_t}{\phi(q_t)^\top u_t},$$

where the sums have been *hoisted out of the query*:

$$S_t = \sum_{s \le t} \phi(k_s)\, v_s^\top = S_{t-1} + \phi(k_t)v_t^\top,
\qquad u_t = u_{t-1} + \phi(k_t).$$

That recurrence **is an RNN**: hidden state $(S_t, u_t)$ (a $d\times d$
matrix + vector) updated additively per step, output a state readout keyed
by the current query. Consequences: training parallelizes like a
transformer, inference runs in $\mathcal{O}(1)$ memory/time per step like an
RNN ($\phi(x) = \mathrm{elu}(x)+1$ in the paper keeps features positive).
Softmax attention is the non-decomposable limit — the reason full attention
cannot be compressed into a fixed-size state (its "state" is the entire
past).

## What it means for the UPG

- **This identity settles what kind of object our estimator family is.**
  The linear-attention state update $S_t = S_{t-1} + \phi(k_t)v_t^\top$ is
  an *online sufficient-statistic accumulator* — literally the recursive
  computation of the Gram matrices $\sum \phi(k)\phi(k)^\top$-style
  quantities that recursive least squares / Kalman filtering maintain. Read
  with note 41 (attention implements gradient descent ⇒ regression), the
  picture closes: a causal linear-attention layer *is* an online regression
  estimator, and a transformer over EMA history is running something like
  recursive system identification of the person. "AI as statistical
  instrument" stops being a metaphor at this equation.
- **The taxonomy it induces** (elaborated in note 46): fixed-size-state
  models (RNN, SSM, linear attention) vs. unbounded-state models (softmax
  attention). Our generative process is itself fixed-size-state (Markov in
  $x_t \in \mathbb{R}^7$); a fixed-state estimator is therefore *sufficient
  in principle* for filtering it — the reason S4/Mamba (notes 43–44) are
  natural candidates — while softmax attention buys robustness when the
  state is *mis-specified* (missing dimensions, wrong lag structure), which
  on real data it will be. This trade-off is exactly what the step-6
  benchmark comparison measures.
- Practical: the recurrent form is the deployment mode for continuous
  monitoring (constant memory per new observation, cf. note 07's cache).

## Verdict

Keystone theory note. No direct implementation in Phase 2 (softmax at our
scale), but it supplies the formal argument for the step-6 report's framing
and the criteria for the attention-vs-SSM decision (note 46).
