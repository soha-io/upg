"""
upg — the Unified Person Graph toolkit.

A tested, self-contained implementation of the Eight-Dimension model: the
typed graph schema, the composition of the eight strata into the Great Graph,
the axiom/encapsulation audits, and the Batch I mathematical toolbox
(spectral, dynamics, learning).  Every published number in Batches I and J is
reproduced by the accompanying pytest suite.

Quick start
-----------
>>> from upg import build_person_graph, axiom_audit
>>> pg = build_person_graph()
>>> pg.n, len(pg.edges)
(253, 522)
>>> axiom_audit(pg).weakly_connected
True
"""
from __future__ import annotations

from .audit import AxiomReport, axiom_audit
from .compose import build_person_graph, encapsulation_violations
from .schema import Edge, Node, PersonGraph
from .spectral import SpectralReport, dimension_spectral_report
from .casestudy import CaseReport, case_report, build_case_model
from .simulate import (PersonParams, PersonRecord, SimConfig,
                       SyntheticDataset, sample_person, sample_population,
                       simulate_person, simulate_population, dimension_base,
                       characterize, GeneratorPreset, GENERATOR_PRESETS,
                       generator_preset_names, get_generator_preset,
                       preset_config, simulate_preset)
from .recover import (RecoveredPerson, fit_person, recovery_metrics,
                      recover_dataset, known_support)
from .gat import (GATConfig, GATPerson, MaskedGraphAttentionEstimator,
                  build_training_set, gat_recover_dataset, person_features,
                  deviation_rank_spectrum)
from .transformer import (ForecastConfig, TemporalTransformer, make_batches,
                          evaluate_model)

__all__ = [
    "PersonGraph", "Node", "Edge",
    "build_person_graph", "encapsulation_violations",
    "axiom_audit", "AxiomReport",
    "dimension_spectral_report", "SpectralReport",
    "case_report", "CaseReport", "build_case_model",
    # simulation (Step 2)
    "PersonParams", "PersonRecord", "SimConfig", "SyntheticDataset",
    "sample_person", "sample_population", "simulate_person",
    "simulate_population", "dimension_base", "characterize",
    "GeneratorPreset", "GENERATOR_PRESETS", "generator_preset_names",
    "get_generator_preset", "preset_config", "simulate_preset",
    # recovery (Step 3)
    "RecoveredPerson", "fit_person", "recovery_metrics", "recover_dataset",
    "known_support",
    # graph-attention estimator (Step 5)
    "GATConfig", "GATPerson", "MaskedGraphAttentionEstimator",
    "build_training_set", "gat_recover_dataset", "person_features",
    "deviation_rank_spectrum",
    # temporal transformer (Step 6)
    "ForecastConfig", "TemporalTransformer", "make_batches", "evaluate_model",
]

__version__ = "0.1.0"
