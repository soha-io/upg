# Batch K Supplementary Methods, Audit, and Reproducibility Appendix

## S1. Scope and claim classes

Batch K evaluates four different claim classes and prevents evidence from flowing upward by implication:

| Level | Evidence | Permitted inference |
|---|---|---|
| E0 | definitions, registries, proofs, software tests | properties of the versioned formal artifact |
| E1 | held-out synthetic persons | recovery under the declared simulator family |
| E2 | retrospective real data | dataset- and design-bounded measurement or prediction evidence |
| E3 | prospective target-setting cohort | target-setting validity, calibration, transport, and workflow feasibility |
| E4 | prospective comparative impact trial | incremental clinical effectiveness for the tested use and population |
| E5 | independent replication and synthesis | robustness across teams, settings, versions, and time |

E0 consistency cannot validate E1 recovery; E1 recovery cannot validate E2 transport; E2 association cannot establish E3 prospective performance or E4 clinical benefit. No available evidence reaches E3 or E4 for the complete UPG.

## S2. Input audit

The accepted inputs were `psych-lab-main(1).zip`, `Archive(1).zip`, `8-Dimention Model Sources-Part 1.zip`, and `8-Dimention Model Sources-Part 2(1).zip`. The superseded `(2)` project ZIP was not used.

The clean extracted census is 219 project files, 139 archived-data files, 190 Part-1 source files, and 48 Part-2 source files (596 total). Source registries contain 223 entries: 222 PDFs and one HTML source. Including four substantive data-documentation PDFs, the PDF corpus contains 226 readable PDFs, 20,253 pages, and 9,395,322 whitespace-delimited extracted/OCR words. The count is a text-access check, not a bibliometric statistic.

Two sources were image-only. `07. Chess-Thomas-Temperament-and-its-functional-significance.pdf` was rendered at 200 dpi and OCR'd page by page with Tesseract because the PDF/A pipeline rejected the landscape page geometry; 33/33 pages yielded approximately 24,205 words. `12 .Measrmnt_of_temp_in_Infancy.pdf` was processed with OCRmyPDF/Tesseract; 10/10 pages yielded approximately 6,530 words. Forty-six AppleDouble/`__MACOSX` entries were metadata stubs. Five substantive exact-duplicate groups were identified by SHA-256 and must count once in an evidence synthesis.

Per-file page, word, hash, method, status, and error fields are in `pdf_text_audit.csv`; summary counts and duplicate paths are in `source_audit_summary.json`.

## S3. Formal reproduction

The project test suite was executed with Python 3.12 and Pytest through the supplied package. All 95 tests passed. `scripts/reproduce.py` independently returned:

- 253 nodes and 522 edges;
- eight strata with 35 cross-stratum edges;
- 20 self-loops and 33 negative edges;
- full weak connectivity and directed reachability, zero isolated nodes, and zero encapsulation violations;
- dimension-graph algebraic connectivity $\lambda_2=1.568$;
- NEED $\rightarrow$ ME $\rightarrow$ NEED gain +.400;
- DIS $\rightarrow$ THER $\rightarrow$ DIS gain -.455;
- $\lambda_{\max}(B)=2.195$ and the worked-case $\kappa^*=.456$.

These are deterministic properties of the current registry and worked simulation, not empirical population parameters.

## S4. IPIP-NEO-120 analysis

### S4.1 File validation and scoring

`IPIP120.dat` contains 619,150 fixed-width records. Each record was verified as 153 bytes including CRLF. Item bytes 32--151 (one-indexed) were converted from ASCII and constrained to the documented range 0--5. Zero remained missing; values 1--5 were transformed to 0--1 as $(r-1)/4$. The source states that reverse-keyed items were already reversed at collection.

Inventory order cycles N, E, O, A, and C across six facets and repeats the 30-facet block four times. A facet was scored with at least three of four items. A domain required at least 17 of 24 items, the integer ceiling of 70%. No missing item response was replaced.

### S4.2 Reliability

Cronbach's alpha was computed on domain-complete records:

$$
\alpha=\frac{k}{k-1}\left(1-\frac{\sum_j s_j^2}{s_{\sum j}^2}\right).
$$

Reliability-derived measurement error used the project contract:

$$
\sigma_{measurement}=s_{observed}\sqrt{\frac{1-\alpha}{\alpha}}.
$$

| Domain | Complete n for alpha | alpha | measurement SD |
|---|---:|---:|---:|
| N | 558,777 | .898459 | .055291 |
| E | 551,341 | .888989 | .052512 |
| O | 554,018 | .816814 | .060208 |
| A | 557,931 | .857988 | .053085 |
| C | 554,765 | .905287 | .049238 |

### S4.3 Facet structure

All 30 facets were available for 612,595 records. A Pearson correlation matrix was eigendecomposed. The first five eigenvalues were 6.6546, 3.7446, 2.9732, 2.0956, and 1.9161 (57.9469% of total variance). Five PCA loadings were rotated using orthogonal varimax. Because factor order and sign are arbitrary, factors were mapped one-to-one to intended domains with the Hungarian algorithm maximizing summed absolute loading over each domain's six facets.

Twenty-five facets had their largest absolute loading on the intended mapped domain. Exceptions were N4 self-consciousness→E, E3 assertiveness→C, E4 activity level→C, O3 emotionality→A, and C3 dutifulness→A. The vector of 435 unique facet correlations correlated $r=.9999446$ across deterministic even/odd row halves. Median absolute correlation was .32326 within intended domains and .13426 across domains.

This is cross-sectional measurement evidence. It does not estimate trait change, temporal edges, treatment effects, disorder, or the complete UPG.

## S5. Kossakowski ESM analysis

### S5.1 Cleaning and measurement map

The public CSV contained 1,476 rows. Five explicit aborted questionnaires were removed. Two missing abort flags were retained but item-gated rather than assumed valid or aborted. All 1,471 retained rows passed the 12-of-20 item gate; mean item coverage was .999898.

The 20-item ME load used the contiguous momentary affect/pattern/self-evaluation block from `mood_relaxed` through `se_handle`. Items documented on -3--3 were mapped with $(r+3)/6$; items on 1--7 with $(r-1)/6$. Relaxed, satisfied, enthusiastic, cheerful, strong, concentration, self-liking, and ability-to-handle were reverse-oriented so higher values represent greater load. The other 12 items were oriented upward. The occasion score was the available-item mean. Complete-occasion alpha was .940207 ($n=1,470$); observed SD was .090161 and reliability-derived measurement SD .022737.

Thirteen weekly SCL-90-R depression items were averaged when at least ten were present and divided by four. This yielded 28 weekly anchors. Daily ME was the within-day occasion mean.

### S5.2 Concurrent and early-warning analyses

For each weekly anchor, current seven-calendar-day ME was computed when at least three observed days were present. Spearman correlation with concurrent depression used 27 anchors. A circular moving-block percentile interval (block length 4; 5,000 deterministic resamples; seed 20260712) preserves short local order but is not a population-generalization interval for this N=1 archive.

For each anchor, AR(1) was the lag coefficient from OLS with intercept over the current 21-calendar-day daily-ME window when at least eight observed values were present. Rolling variance used the same window and threshold. Each was correlated with the following anchor's change in depression. The preregistration-relevant results were:

| Analysis | rho | n | circular-block 95% interval |
|---|---:|---:|---:|
| seven-day ME vs concurrent depression | .6249 | 27 | [.4034, .8001] |
| 21-day AR(1) vs next depression change | -.0678 | 25 | [-.5606, .3969] |
| 21-day variance vs next depression change | -.1244 | 25 | [-.3974, .1731] |

P-values in the JSON are descriptive only. The analysis is exploratory, has one person, multiple related tests, temporal dependence, and no population sample.

### S5.3 Strict rolling-origin forecast

The candidate feature vector contained current weekly depression, current seven-day ME, and current 21-day AR(1). After complete transition construction, the first ten transitions formed the initial training history. Each of the remaining 15 targets was predicted once using only earlier transitions. Standardization was fitted inside each historical training window. Ridge alpha was chosen inside that training history by expanding-window error over {0.01, 0.1, 1, 10, 100}. Persistence carried current depression forward.

| Metric | Ridge | Persistence |
|---|---:|---:|
| MAE | .11663 | .08846 |
| RMSE | .13532 | .11782 |

The candidate model failed both comparator criteria. No tuning on the 15 held-out targets was performed. The result is retained as a falsifier.

Medication concentration and daily ME correlated $\rho=-.1652$ over 238 days. Phase and exposure co-evolve with time, and there is one participant; no medication-effect claim is permitted.

## S6. Synthetic model training and evaluation

### S6.1 Masked graph-attention estimator

The uploaded `train_*` and `val_*` NPZ sets were copied without modification. Fresh models were trained with the supplied code and fixed preset seeds. Best validation epochs/objects were 79/-1.344898 (`balanced_regimes`), 88/-1.363646 (`clinical_realistic`), and 141/-1.192276 (`transition_rich`). Evaluation used the supplied simulator with 40 held-out persons per preset, window lengths 30, 60, 120, and 250, and seed 0.

Across 12 cells, median edge RMSE was .0775--.0976, person-deviation correlation .1286--.3415, regime accuracy .850--.975, and mean nominal-90% interval coverage .8727--.8930. The GAT beat the best Step-4 comparator for edge RMSE, deviation correlation, and spectral-radius absolute error in 12/12 cells. Regime and attractor wins were mixed and are not summarized as universal wins.

### S6.2 Temporal transformer

The balanced model was freshly retrained in one fixed 200-epoch budget; the best validation checkpoint was saved even though the stopping flag remained false. The clinical and transition checkpoints were versioned artifacts in the uploaded archive and were reevaluated, not relabeled as fresh. Their SHA-256 values and origins are recorded in `training_provenance.json`. Evaluation used 40 held-out persons per preset.

| Preset | checkpoint origin | filter RMSE | h=1 RMSE | persistence | explicit Kalman fit | nominal-90% coverage |
|---|---|---:|---:|---:|---:|---:|
| balanced | fresh 200-epoch run | .05299 | .05955 | .09221 | .06066 | .89217 |
| clinical | uploaded/reevaluated | .05235 | .05367 | .10407 | .07915 | .87857 |
| transition | uploaded/reevaluated | .11040 | .12088 | .16466 | .15657 | .90417 |

The transition model also beat the uploaded channel-independent null at horizon 1 (.12088 vs .13883). Synthetic early-warning AUCs were .955--1.000 for relapse and .939--.983 for recovery. Because targets and events come from the same simulator family, these are implementation results, not clinical alarms.

## S7. Reproduction commands

Run from `/workspace/batch-k-run` after placing the extracted inputs in the paths used by the scripts:

```bash
python3 work/analysis/audit_sources.py
MPLCONFIGDIR=/tmp/matplotlib python3 work/analysis/run_real_data_analysis.py

cd work/project/upg
UV_CACHE_DIR=/tmp/uv-cache MPLCONFIGDIR=/tmp/matplotlib uv run --with pytest pytest -q
PYTHONPATH=src python3 scripts/reproduce.py

PYTHONPATH=src python3 scripts/gat_study.py --stage train --force \
  --out /workspace/batch-k-run/work/results/retrained/gat_v1
PYTHONPATH=src python3 scripts/gat_study.py --stage eval \
  --out /workspace/batch-k-run/work/results/retrained/gat_v1 \
  --baselines /workspace/batch-k-run/work/data/baselines_v1

PYTHONPATH=src python3 scripts/forecast_study.py --stage eval \
  --out /workspace/batch-k-run/work/results/retrained/forecast_v1
```

The GAT command above trains all three presets sequentially if `--preset` is omitted. The temporal directory must contain the checkpoint files described by its provenance JSON. Raw archives are never overwritten.

## S8. Files and audit trail

- `batch_k_claim_ledger.csv`: every consequential claim, evidence level, status, permitted wording, and prohibited inference.
- `batch_k_source_cards.csv`: local/external source roles and limits.
- `source_audit_summary.json` and `pdf_text_audit.csv`: corpus access, OCR, duplicates, and hashes.
- `real_data_summary.json`, `ipip_domain_metrics.csv`, `ipip_facet_loadings.csv`, `kossakowski_weekly_derived.csv`, and `kossakowski_rolling_forecasts.csv`: exact retrospective outputs.
- `gat_results.json`, `forecast_results.json`, and `training_provenance.json`: synthetic evaluations and checkpoint provenance.
- `run_real_data_analysis.py` and `audit_sources.py`: executable retrospective/audit code.

The claim ledger, not the prose alone, is the authoritative boundary for downstream agent training.
