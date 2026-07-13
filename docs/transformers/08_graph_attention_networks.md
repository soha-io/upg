# 08 — Graph Attention Networks (Veličković et al., 2018)

**One line:** compute attention only over a node's *given* graph
neighborhood, so learned attention coefficients are weights *on known edges*
— the mathematical core of step 5.

## The math

Node features $h_i \in \mathbb{R}^{F}$, shared projection $W$, and a graph
whose neighborhoods $\mathcal{N}(i)$ are **fixed in advance**. One GAT layer:

$$e_{ij} = \mathrm{LeakyReLU}\big(a^\top [\,Wh_i \,\|\, Wh_j\,]\big),
\qquad j \in \mathcal{N}(i),$$

$$\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k \in \mathcal{N}(i)} \exp(e_{ik})},
\qquad
h_i' = \sigma\Big(\sum_{j \in \mathcal{N}(i)} \alpha_{ij}\, W h_j\Big).$$

Multi-head: concatenate (hidden layers) or average (output layer) $K$
independent $\{\alpha^{(k)}_{ij}\}$.

Contrast with note 01: full self-attention has $\mathcal{N}(i) = $ all
tokens; GAT restricts the softmax support to the adjacency structure. The
masking is implemented exactly as in causal attention — add $-\infty$ to
logits of non-edges — so GAT ⊂ masked transformer.

Two properties the paper stresses:

1. **Inductive:** weights $(W, a)$ are shared across nodes and graphs, so the
   trained layer applies to unseen graphs/nodes. (For us: unseen *persons*.)
2. **Data-dependent weights:** unlike GCN's fixed
   $\hat A = D^{-1/2}(A+I)D^{-1/2}$ propagation, $\alpha_{ij}$ depends on the
   *features* of $i$ and $j$ — different persons get different effective edge
   strengths on the same skeleton.

## What it means for the UPG — the step-5 license

Read $\mathcal{N}(i) = \{j : \bar B_{ij} \ne 0\}$: the consensus skeleton
(rule W1) *is* the GAT neighborhood structure. Then:

- The attention coefficient $\alpha_{ij}$ is a **person-specific, learned
  weight on a theory-sanctioned edge** — precisely "attention learns only the
  strengths and state-dependence of edges that already exist" (roadmap
  step 5). A free GNN/transformer would relearn structure and violate W1;
  GAT's mask makes the constraint architectural, hence unbreakable by
  optimization.
- **Normalization mismatch, and our fix.** GAT's softmax makes each row of
  $[\alpha_{ij}]$ sum to 1, but rows of our $B$ are *not* normalized — total
  incoming drive is a meaningful, person-varying quantity (it sets
  $\kappa^\*$). So step 5 keeps GAT's *scoring* function but replaces the
  softmax with an unnormalized positive link:
  $$\hat B_{ij} = \bar B_{ij}\, \exp(\delta_{ij}),\qquad
  \delta_{ij} = \text{attention score from person features},$$
  which preserves sign and support by construction ($\bar B_{ij}=0 \Rightarrow
  \hat B_{ij}=0$) and reduces to the prior at $\delta = 0$ — rule W7 as an
  architecture. This mirrors the simulator's own generative family
  ($B = \bar B \odot e^{\text{noise}}$), so the estimator is well-specified.
- **Node features for a *person* graph** are not word embeddings but
  sufficient statistics of that person's series: means, variances, lag-1
  auto-/cross-correlations of $y$, treatment covariances. The GAT then maps
  observation-window statistics → personalized $\hat B$ — an amortized
  estimator (cf. note 04).

## Verdict

Core adoption. Step 5 implements: skeleton-masked attention scores over
pairwise series statistics → multiplicative log-corrections on $\bar B$.
Softmax row-normalization is deliberately dropped (documented above), which
is the one place we deviate from the paper and must say so.
