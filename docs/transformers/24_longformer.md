# 24 — Longformer: The Long-Document Transformer (Beltagy et al., 2020)

**One line:** sliding-window local attention for almost all tokens plus
*global* attention for a few designated tokens — a hub-and-spokes attention
graph that is, structurally, our bridge-node result.

## The math

Three patterns replacing full $\mathcal{O}(T^2)$ attention:

1. **Sliding window:** token $t$ attends to $[t-w/2,\, t+w/2]$; cost
   $\mathcal{O}(Tw)$. Stacked $L$ layers give receptive field $Lw$ (same
   depth-locality argument as notes 12/22).
2. **Dilated windows:** gaps of size $d$ multiply reach to $Lwd$ without
   extra cost (analogous to dilated convolutions); different heads can use
   different dilations.
3. **Global tokens:** a small designated set $G$ (e.g. `[CLS]`, question
   tokens) attends to everything and is attended by everything —
   $\mathcal{O}(T|G|)$. The attention graph is then a windowed chain plus a
   few hubs; its diameter is ≤ 2 through any hub.

## What it means for the UPG

- **The attention graph Longformer *chooses* is the graph topology Batch J
  *derived*.** The Great Graph's spectral analysis found global integration
  runs through few bridge nodes (personality, $|v_2| = 0.015$); Longformer
  shows that giving hubs global reach while everything else stays local
  preserves task performance at a fraction of the cost. At full 253-node
  resolution the same design applies with hubs = mother/interface nodes:
  intra-stratum windows + global interface tokens ≈ encapsulation
  (Definition 3) as an attention pattern — third convergent route to this
  conclusion after notes 09 (virtual node) and 12 (windows).
- **Designated global tokens for time:** in step 6, treatment-onset and
  assessment-boundary occasions are natural "global tokens" — rare events
  every occasion should be able to consult regardless of distance (a
  treatment pulse at $t_0$ shapes dynamics long after $w$ occasions). This
  is implementable as a tiny mask change and is registered as a step-6
  variant worth ablating when horizons grow.
- The windowed pattern's justification (most dependence is local) matches
  the Markov argument of note 22 — for us the window width should be set by
  the measurement-noise filter length, a quantity we can compute from the
  simulator rather than tune blindly.

## Verdict

Efficiency machinery unnecessary at Phase-2 scale; the hub-pattern
correspondence (bridge nodes ↔ global tokens) goes into the Phase-3
manuscript, and event-tokens-as-global is a registered step-6 ablation for
long-series work.
