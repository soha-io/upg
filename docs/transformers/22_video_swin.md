# 22 — Video Swin Transformer (Liu et al., 2022)

**One line:** extend shifted-window attention (note 12) into time — attend
within local 3-D windows (space × a few frames), shift the partition across
layers — locality as the dominant inductive bias even for dynamics.

## The math

Tokens from 3-D patches; attention restricted to non-overlapping 3-D windows
of size $P \times M \times M$ (time × height × width); alternating layers
shift the window partition by half in every axis, so cross-window (including
cross-*time-window*) information flows with depth. Relative position bias is
3-D: $b_{\Delta t, \Delta h, \Delta w}$. Hierarchy via spatial patch merging
per stage (time resolution kept).

The modeling claim: spatiotemporal correlation in video is dominated by
*local* neighborhoods — most of what predicts a pixel-patch is nearby in
space and time — so spending attention capacity globally is wasteful; global
integration emerges through depth.

## What it means for the UPG

- **Locality holds for our data too, in a specific sense:** the generative
  map is Markov (lag-1), so given $x_t$, occasion $t+1$ is conditionally
  independent of the deeper past; temporal influence *is* local, and only
  latent-state uncertainty (measurement noise, missingness) makes longer
  context useful (the filter integrates evidence). This predicts the step-6
  transformer's useful attention span should be short — dictated by
  measurement noise, not by long mechanistic memory — and we can *verify*
  this on synthetic data by ablating context length: forecast skill should
  saturate once the filter has enough occasions to pin down $x_t$. A crisp,
  checkable prediction linking architecture to the known generator.
- **Where locality fails is informative:** developmental gates $g_{ij}(t)$
  and slow trait drift are the UPG's genuinely long-range temporal
  structure. If long-context attention beats the saturation prediction on
  *real* data, that surplus predictability is evidence of slow
  components/gates — an estimator-side detector for Batch C's mechanism.
- The 3-D relative-bias table transfers as the general recipe: biases
  indexed by (time offset, graph distance) rather than (Δt, Δh, Δw) — the
  graph-native version combining note 09's spatial encoding with note 30's
  temporal bias, reserved for full-resolution work.

## Verdict

No direct Phase-2 use. Contributes the context-length saturation experiment
(adopted in the step-6 report) and the (Δt × graph-distance) bias design for
the 253-node estimator.
