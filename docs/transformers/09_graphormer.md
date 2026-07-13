# 09 — Do Transformers Really Perform Badly for Graph Representation? (Ying et al., 2021)

**One line:** a *full* transformer beats specialized GNNs on graphs — but only
after graph structure is injected into attention as explicit bias terms;
structure must be told, not discovered.

## The math

Graphormer runs unmasked all-pairs attention over nodes, then adds three
structural encodings:

1. **Centrality encoding** — degree embeddings added to node inputs:
   $h_i^{(0)} = x_i + z^{-}_{\deg^-(i)} + z^{+}_{\deg^+(i)}$. Attention gets
   told which nodes are hubs (for us: which dimensions have many couplings —
   DIS in-degree, SYS out-degree).
2. **Spatial encoding** — a learned scalar bias indexed by shortest-path
   distance $\phi(i,j)$ added to every attention logit:
   $$A_{ij} = \frac{(h_iW_Q)(h_jW_K)^\top}{\sqrt{d}} + b_{\phi(i,j)}.$$
   With $b_{\phi}$ decreasing in $\phi$, attention decays with graph distance
   — a soft version of GAT's hard mask.
3. **Edge encoding** — features of the edges along the path from $i$ to $j$
   enter as an additional logit bias $c_{ij} = \frac{1}{\phi}\sum_k
   x_{e_k}^\top w_k$, so edge *types* (our gates, signs) modulate attention.

The theoretical remark worth keeping: with these encodings, Graphormer can
express mean/sum GNN aggregation as special cases (attention simulates the
message pass), so the transformer is strictly more expressive — *given* the
structural information.

## What it means for the UPG

- **The central empirical lesson supports rule W1 from the deep-learning
  side:** even with huge data, transformers win on graphs only when
  structure enters as explicit bias. Our data regimes ($T \le 200$ per
  person) are far below "huge," so the case for hard structural constraints
  is stronger still. Step 5's hard mask is the small-data limit of
  Graphormer's soft spatial bias.
- **Soft vs. hard structure is a testable dial.** The spatial-encoding option
  defines the natural *relaxation* of step 5 for the theory tournament
  (step 7): hard mask (edges only) vs. distance-biased soft attention (allows
  2-hop shortcuts, i.e. mediated influence per Axiom 3) vs. free attention
  (no theory). Comparing these three *is* a test of whether the published
  skeleton is complete — a falsifier for the theory delivered by the
  estimator family itself.
- **Centrality encoding maps to node structural importance** (Batch J's
  weight disambiguation: structural importance ≠ activation). Feeding
  degree/strength embeddings gives the estimator the same information the
  Fiedler/bridge analysis uses, without letting it rewrite the graph.
- The **virtual node** Graphormer adds (connected to all nodes, aggregating
  graph-level readout) is architecturally identical to our *mother node* /
  interface construction — encapsulated strata communicating through one
  hub. Deep-learning practice independently reinvented Batch J's Definition 2.

## Verdict

Adopt as the *upgrade path* for step 5: keep the hard mask now; register the
soft spatial-bias variant as a named rival for the step-7 tournament. The
virtual-node ≅ mother-node correspondence goes in the Phase-3 manuscript as
convergent validation of the encapsulation formalism.
