# Unified Person Graph — Batch K Model Card

## Model identity

- **Name:** Unified Person Graph (UPG), Batch K application release
- **Release:** 2026-07-12
- **Graph:** 253 nodes, 522 edges, eight strata
- **Software status:** research code; current pre-study suite 123/123 passing (original frozen release reported 95/95)
- **Clinical status:** not a validated diagnostic, prognostic, prescribing, treatment-selection, or cure system
- **Data correction status:** legacy Kossakowski chronology/results quarantined; corrected pipeline not yet rerun

## Intended uses now

1. Reproducible research on the supplied formal graph, simulator, estimators, and falsifiers.
2. Transparent, collaborative, non-diagnostic case-formulation research at the coarsest resolution supported by the data.
3. Measurement mapping, data-quality reporting, uncertainty display, hypothesis generation, alternative-explanation tracking, and monitoring-plan design.
4. Resource-oriented private self-mapping that reports descriptions and questions, not disorders or person-specific causal graphs.

## Uses not authorized by current evidence

- autonomous or graph-only diagnosis;
- suicide, violence, relapse, or emergency triage;
- medication or psychotherapy prescription;
- causal treatment ranking from observational edges;
- claim that UPG-guided care improves outcomes or cures a disorder;
- sole input to involuntary care, legal, benefits, insurance, education, employment, or policing decisions;
- covert monitoring or secondary use outside specific consent.

## Architecture

The theory object is a fixed, sourced, signed, gated graph prior. The dimension-level dynamic implementation has seven endogenous channels because THER is represented as a delivered control stream rather than double-counted as a symptom-like state. The application contract distinguishes raw observations $y$, latent state $x$, standing load/resources $b$, theory prior $\bar W$, personalized temporal estimate $B_p$, context $c$, controls $u$, developmental/applicability gates $g$, uncertainty $q$, and person-supplied goals and constraints $v$.

The structure estimator is a masked graph-attention model constrained to published support and signs. The temporal model is a causal, missingness-aware transformer with ALiBi, RMSNorm, SwiGLU, multi-horizon forecast heads, and a dynamics cross-check. Neither architecture makes its learned quantities causal by construction.

## Training and evaluation data

- **Structure models:** freshly trained on three uploaded UPG-simulator populations (`balanced_regimes`, `clinical_realistic`, `transition_rich`). Training generated an independent population at each T rather than matched shorter/longer windows of the same persons. Evaluation used 40 held-out simulated persons per preset at T=30, 60, 120, and 250.
- **Temporal balanced model:** freshly trained for a fixed 200-epoch budget; best validation checkpoint retained.
- **Temporal clinical and transition models:** uploaded versioned checkpoints, hash-verified and reevaluated; not misrepresented as fresh training.
- **Real retrospective data:** IPIP-NEO-120 cross-sectional records (619,150) and one public intensive ESM depression archive (1,476 raw rows). These real datasets do not contain all eight strata and were not used to train a full UPG.

## Performance summary

- GAT median edge RMSE .0775--.0976; person-deviation correlation .1286--.3415; nominal-90% coverage .8727--.8930. Edge RMSE, deviation correlation, and spectral-radius error beat the best Step-4 baseline in 12/12 synthetic cells.
- Temporal h=1 RMSE .0596/.0537/.1209 versus persistence .0922/.1041/.1647 on the three synthetic presets.
- IPIP domain alpha .8168--.9053; 25/30 facet primary loadings mapped to their intended domain.
- No current Kossakowski performance claim. Previously reported one-person ME, early-warning, and forecast numbers are frozen chronology-invalid fixtures, not evidence. See `../CHRONOLOGY_QUARANTINE.md`.

## Limitations and known failure modes

1. Synthetic success can be inflated by simulator-model alignment.
2. Current graph weights are sourced consensus priors, not population causal effects.
3. Fine person-specific edges require much denser, more informative data than a state map.
4. Errors-in-variables, irregular missingness, low excitation, dataset shift, and instrument changes can invalidate structure or forecasts.
5. The real archive has one person and confounds medication exposure, phase, and time; the legacy analysis additionally sorted day-of-year across two years and is quarantined.
6. Cross-sectional personality reliability does not establish temporal validity or diagnosis.
7. Five IPIP facets did not recover their intended primary domain.
8. The legacy real rolling forecast is chronology-invalid. Future applications must suppress forecasts that do not beat declared simple comparators on a valid calendar-ordered evaluation.
9. All-age and all-population scope remains a transportability program requiring measurement-invariance, calibration, accessibility, and subgroup-error testing.
10. GAT inference rejects non-finite standardized features, heads,
    exponential inputs/outputs, interval endpoints, and gains. It does not
    clip or silently repair them. This is an arithmetic safety boundary, not
    an OOD-validity result: a numerically finite but extreme estimate may still
    be scientifically inapplicable. Any applicability detector, parameter
    bound, or clipping policy must be preregistered and independently evaluated
    before use; none is implied by the current guard.

## Required human controls

- established risk, medical differential, diagnosis, and treatment procedures remain primary;
- consent is stream-specific and revocable;
- every hypothesis includes provenance, uncertainty, an alternative, a falsifier, and next information;
- every intervention option includes target (state/structure/context), evidence basis, burdens/harms, monitoring, and stop rules;
- the person can inspect and contest data and interpretation;
- safety, rights, contraindications, and goals override numerical optimization;
- a refusal with reason codes is a successful output.

## Validation required before clinical decision support

Complete item/node measurement studies; independent retrospective replication; prospective breadth and depth cohorts; target-setting diagnostic/forecast validation; subgroup calibration and decision-curve analysis; DECIDE-AI human-factor and early-live evaluation; a SPIRIT-AI/CONSORT-AI comparative impact trial against care as usual and measurement-based care; jurisdiction-specific regulatory, privacy, security, and quality review; and postdeployment monitoring with rollback.

## Provenance

Use `batch_k_claim_ledger.csv` as the authoritative claim boundary, `batch_k_source_cards.csv` for evidence roles and limitations, `training_provenance.json` for checkpoint origins and hashes, and the supplementary methods for exact transformations and commands.
