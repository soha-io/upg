# Corrected calendar-safe Batch K builder baseline

Generated 2026-07-16 from a no-hardlinks clean clone of UPG commit
`1b5676de533b9cf16d7062605c836a5433a94653` with the locked study environment.
The clean-room `upg-preflight --require-data` run passed with 0 failures and 0
skips, including all 123 tests and 10 public-data checksums.

The immutable output is outside Git at:

`/home/ali/UPG-storage/artifacts/batch-k/corrected-v3-calendar-1b5676d`

Its completion manifest SHA-256 is
`a242d83423403b414af5904447280720980c163b9bbdcab0a36271d931661d1e`;
the summary SHA-256 is
`066d10db3889674696fc25b4f519480ec83dc074281c4f8a3d922a08d1bd6c1f`.
The manifest binds eight inputs and all ten result files.

## Bounded result

- Full dates are monotone and every forecast records its source, target, and
  exact 7/14/21-day horizon.
- The transparent seven-day ME load correlates with concurrent weekly
  depression for this one participant: Spearman rho 0.625, n=27, circular
  block interval [0.402, 0.797]. This is concurrent N=1 evidence only.
- Rolling AR(1) versus next-anchor depression change is unsupported: rho
  0.019, n=25, interval [-0.469, 0.402].
- The rolling ridge baseline does not beat persistence: RMSE 0.1354 versus
  0.1204 and MAE 0.1159 versus 0.0923 across 15 forecasts.
- The IPIP audit recovers 25/30 facets by primary varimax loading and remains
  cross-sectional PER measurement evidence, not whole-UPG validation.

This is a builder baseline for study iteration, not an independently accepted
scientific claim and not evidence of causal medication effects, diagnosis,
treatment selection, population transport, or complete-UPG validity.
