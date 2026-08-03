#!/usr/bin/env python3
"""Frozen CC-101 IPIP-NEO-120 hierarchy-signal development pilot.

This program intentionally accepts one explicit ``IPIP120.dat`` file and one
new output directory.  It never discovers or traverses a data root.  The
analysis is exploratory (E2 ceiling), development-only, and cannot establish
external validity, causality, dynamics, clinical utility, or a UPG-specific
advantage.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import shlex
import shutil
import sys
import tempfile
import time
import traceback
from typing import Iterable, Mapping, Sequence

import numpy as np


STUDY_ID = "CC-101"
PROTOCOL_ID = "K-PER-ORDINAL-001"
SPLIT_SALT = "UPG-K-PER-ORDINAL-v1-SPLIT"
SAMPLE_SALT = "CC-101-PILOT-SAMPLE-v1"
MASK_SEEDS = (2026071501, 2026071502, 2026071503, 2026071504, 2026071505)
BOOTSTRAP_SEED = 2026071699
BOOTSTRAP_RESAMPLES = 2_000
DIRICHLET_PSEUDOCOUNT = 1.0
TRAIN_CAP = 50_000
VALIDATION_CAP = 20_000

EXPECTED_SOURCE_ROWS = 619_150
RECORD_BYTES = 153
ITEM_START = 31
ITEM_COUNT = 120
ITEM_STOP = ITEM_START + ITEM_COUNT
TERMINATOR = (13, 10)

DOMAIN_CODES = ("N", "E", "O", "A", "C")
DOMAIN_NAMES = (
    "Neuroticism",
    "Extraversion",
    "Openness",
    "Agreeableness",
    "Conscientiousness",
)
FACET_NAMES = (
    ("Anxiety", "Anger", "Depression", "Self-Consciousness", "Immoderation", "Vulnerability"),
    ("Friendliness", "Gregariousness", "Assertiveness", "Activity Level", "Excitement-Seeking", "Cheerfulness"),
    ("Imagination", "Artistic Interests", "Emotionality", "Adventurousness", "Intellect", "Liberalism"),
    ("Trust", "Morality", "Altruism", "Cooperation", "Modesty", "Sympathy"),
    ("Self-Efficacy", "Orderliness", "Dutifulness", "Achievement-Striving", "Self-Discipline", "Cautiousness"),
)

MODEL_NAMES = (
    "per_item",
    "domain_conditioned",
    "declared_facet",
    "cyclic_wrong_facet",
)
CONTROL_NAMES = ("per_item", "domain_conditioned", "cyclic_wrong_facet")


def _build_hierarchy() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    facets = np.empty((30, 4), dtype=np.int16)
    facet_domains = np.repeat(np.arange(5, dtype=np.int16), 6)
    wrong_facets = np.empty(30, dtype=np.int16)
    domains = np.empty((5, 24), dtype=np.int16)
    for domain in range(5):
        domain_items: list[int] = []
        for local_facet in range(6):
            facet = domain * 6 + local_facet
            # Frozen legacy audit map: N,E,O,A,C cycle within each 30-item
            # block, with four repeated blocks.
            item_indices = [
                domain + 5 * local_facet + 30 * repeat
                for repeat in range(4)
            ]
            facets[facet] = item_indices
            domain_items.extend(item_indices)
            wrong_facets[facet] = domain * 6 + ((local_facet + 1) % 6)
        domains[domain] = sorted(domain_items)
    return facets, facet_domains, wrong_facets, domains


FACET_ITEMS, FACET_DOMAINS, WRONG_FACETS, DOMAIN_ITEMS = _build_hierarchy()
ITEM_TO_FACET = np.empty(ITEM_COUNT, dtype=np.int16)
for _facet_index, _items in enumerate(FACET_ITEMS):
    ITEM_TO_FACET[_items] = _facet_index
ITEM_IDS = tuple(f"I{index + 1:03d}" for index in range(ITEM_COUNT))
ITEM_ID_BYTES = tuple(item_id.encode("ascii") for item_id in ITEM_IDS)


@dataclass(frozen=True)
class SelectedSample:
    """One hash-ranked split sample of unique complete fingerprints."""

    split: str
    row_indices: np.ndarray
    items: np.ndarray
    fingerprints: tuple[bytes, ...]
    sample_digests: tuple[bytes, ...]


@dataclass(frozen=True)
class ParsedIPIP:
    """Strict parser result without retaining the raw memory map."""

    representatives: Mapping[bytes, int]
    statistics: Mapping[str, int]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def canonical_fingerprint(item_ascii: bytes) -> str:
    """Return the frozen complete-row representation (120 one-byte digits)."""

    if len(item_ascii) != ITEM_COUNT or any(value < 49 or value > 53 for value in item_ascii):
        raise ValueError("canonical fingerprint requires exactly 120 responses in 1..5")
    return item_ascii.decode("ascii")


def fingerprint_split_bucket(fingerprint: bytes) -> int:
    canonical_fingerprint(fingerprint)
    digest = hashlib.sha256(SPLIT_SALT.encode("ascii") + b"|" + fingerprint).hexdigest()
    return int(digest[:8], 16) % 100


def sample_rank_digest(fingerprint: bytes) -> bytes:
    canonical_fingerprint(fingerprint)
    return hashlib.sha256(SAMPLE_SALT.encode("ascii") + b"|" + fingerprint).digest()


def inspect_ipip120(
    path: Path,
    *,
    expected_source_rows: int | None = EXPECTED_SOURCE_ROWS,
) -> ParsedIPIP:
    """Validate the 153-byte layout and retain complete unique fingerprints.

    ``expected_source_rows=None`` exists solely for unit-sized parser fixtures;
    the command-line pilot always enforces the frozen 619,150-row asset size.
    """

    size = path.stat().st_size
    if size % RECORD_BYTES:
        raise ValueError(
            f"fixed-width failure: {size} bytes is not divisible by {RECORD_BYTES}"
        )
    source_rows = size // RECORD_BYTES
    if expected_source_rows is not None and source_rows != expected_source_rows:
        raise ValueError(
            f"dataset-version failure: expected {expected_source_rows} rows, found {source_rows}"
        )
    if source_rows == 0:
        raise ValueError("fixed-width failure: input contains no records")

    raw = np.memmap(path, dtype=np.uint8, mode="r", shape=(size,))
    records = raw.reshape(source_rows, RECORD_BYTES)
    if not (
        np.all(records[:, ITEM_STOP] == TERMINATOR[0])
        and np.all(records[:, ITEM_STOP + 1] == TERMINATOR[1])
    ):
        raise ValueError("fixed-width failure: every record must end in CRLF")

    item_ascii = records[:, ITEM_START:ITEM_STOP]
    byte_min = int(item_ascii.min())
    byte_max = int(item_ascii.max())
    if byte_min < ord("0") or byte_max > ord("5"):
        raise ValueError(
            "response-range failure: item bytes must be ASCII digits 0..5 "
            f"(observed byte range {byte_min}..{byte_max})"
        )
    missing_cells = int(np.count_nonzero(item_ascii == ord("0")))
    complete = np.all(item_ascii != ord("0"), axis=1)
    complete_indices = np.flatnonzero(complete)

    representatives: dict[bytes, int] = {}
    for source_row_index in complete_indices:
        fingerprint = item_ascii[int(source_row_index)].tobytes()
        # Source order is ascending, so first occurrence is the frozen lowest
        # zero-based source-row representative.
        representatives.setdefault(fingerprint, int(source_row_index))

    statistics = {
        "source_rows": int(source_rows),
        "record_bytes": RECORD_BYTES,
        "item_count": ITEM_COUNT,
        "missing_item_cells_zero": missing_cells,
        "complete_source_rows": int(complete.sum()),
        "incomplete_source_rows": int(source_rows - complete.sum()),
        "unique_complete_fingerprints": len(representatives),
        "duplicate_complete_rows_beyond_representatives": int(complete.sum()) - len(representatives),
        "minimum_observed_item_value": byte_min - ord("0"),
        "maximum_observed_item_value": byte_max - ord("0"),
    }
    del item_ascii, records, raw
    return ParsedIPIP(representatives=representatives, statistics=statistics)


def _make_sample(
    split: str,
    selected: Sequence[tuple[bytes, bytes, int]],
) -> SelectedSample:
    fingerprints = tuple(row[1] for row in selected)
    if fingerprints:
        joined = b"".join(fingerprints)
        items = np.frombuffer(joined, dtype=np.uint8).reshape(-1, ITEM_COUNT).copy()
        items -= np.uint8(ord("0"))
    else:
        items = np.empty((0, ITEM_COUNT), dtype=np.uint8)
    return SelectedSample(
        split=split,
        row_indices=np.asarray([row[2] for row in selected], dtype=np.int64),
        items=items,
        fingerprints=fingerprints,
        sample_digests=tuple(row[0] for row in selected),
    )


def select_bounded_samples(
    representatives: Mapping[bytes, int],
    *,
    train_cap: int = TRAIN_CAP,
    validation_cap: int = VALIDATION_CAP,
) -> tuple[SelectedSample, SelectedSample, dict[str, int]]:
    """Split unique fingerprints, hash-rank within split, and apply caps."""

    train_candidates: list[tuple[bytes, bytes, int]] = []
    validation_candidates: list[tuple[bytes, bytes, int]] = []
    for fingerprint, source_row_index in representatives.items():
        candidate = (sample_rank_digest(fingerprint), fingerprint, int(source_row_index))
        if fingerprint_split_bucket(fingerprint) < 80:
            train_candidates.append(candidate)
        else:
            validation_candidates.append(candidate)
    train_candidates.sort(key=lambda value: (value[0], value[1]))
    validation_candidates.sort(key=lambda value: (value[0], value[1]))
    train = _make_sample("train", train_candidates[:train_cap])
    validation = _make_sample("validation", validation_candidates[:validation_cap])
    if not len(train.row_indices) or not len(validation.row_indices):
        raise ValueError("split failure: both train and validation must contain fingerprints")
    overlap = set(train.fingerprints).intersection(validation.fingerprints)
    if overlap:
        raise ValueError("split leakage: a fingerprint appears in train and validation")
    statistics = {
        "unique_train_before_cap": len(train_candidates),
        "unique_validation_before_cap": len(validation_candidates),
        "selected_train": len(train.row_indices),
        "selected_validation": len(validation.row_indices),
        "train_cap": train_cap,
        "validation_cap": validation_cap,
    }
    return train, validation, statistics


def compound_row_id(source_row_index: int) -> str:
    """Dataset-qualified immutable zero-based row identifier for mask hashing."""

    if source_row_index < 0:
        raise ValueError("source row index must be nonnegative")
    return f"DS-IPIP120|source_row_index_0based={source_row_index}"


def mask_target_for_facet(source_row_index: int, seed: int, facet: int) -> int:
    """Apply the frozen protocol rank key to one four-item facet."""

    if seed not in MASK_SEEDS:
        raise ValueError(f"unfrozen mask seed: {seed}")
    if facet < 0 or facet >= 30:
        raise ValueError(f"facet index outside 0..29: {facet}")
    prefix = (
        f"{PROTOCOL_ID}|{seed}|{compound_row_id(source_row_index)}|".encode("ascii")
    )
    base = hashlib.sha256(prefix)
    ranked: list[tuple[bytes, str, int]] = []
    for item in FACET_ITEMS[facet]:
        item_index = int(item)
        item_hash = base.copy()
        item_hash.update(ITEM_ID_BYTES[item_index])
        ranked.append((item_hash.digest(), ITEM_IDS[item_index], item_index))
    return min(ranked)[2]


def generate_masks(
    source_row_indices: np.ndarray,
    *,
    progress_label: str | None = None,
) -> np.ndarray:
    """Generate five masks, each hiding exactly one item in every facet."""

    row_indices = np.asarray(source_row_indices, dtype=np.int64)
    masks = np.empty((len(row_indices), len(MASK_SEEDS), 30), dtype=np.int16)
    for record_index, source_row_index in enumerate(row_indices):
        row_id = compound_row_id(int(source_row_index))
        for seed_index, seed in enumerate(MASK_SEEDS):
            prefix = f"{PROTOCOL_ID}|{seed}|{row_id}|".encode("ascii")
            base = hashlib.sha256(prefix)
            for facet, item_indices in enumerate(FACET_ITEMS):
                ranked: list[tuple[bytes, str, int]] = []
                for item in item_indices:
                    item_index = int(item)
                    item_hash = base.copy()
                    item_hash.update(ITEM_ID_BYTES[item_index])
                    ranked.append((item_hash.digest(), ITEM_IDS[item_index], item_index))
                masks[record_index, seed_index, facet] = min(ranked)[2]
        if progress_label and (record_index + 1) % 5_000 == 0:
            print(
                f"{progress_label}: generated masks for {record_index + 1}/{len(row_indices)} records",
                flush=True,
            )
    validate_masks(masks)
    return masks


def validate_masks(masks: np.ndarray) -> None:
    masks = np.asarray(masks)
    expected_shape = (masks.shape[0], len(MASK_SEEDS), 30)
    if masks.ndim != 3 or masks.shape != expected_shape:
        raise ValueError(
            "mask failure: expected shape (records, 5, 30), found " + str(masks.shape)
        )
    for facet in range(30):
        if not np.all(np.isin(masks[:, :, facet], FACET_ITEMS[facet])):
            raise ValueError(f"mask failure: facet {facet} contains a nonmember item")
    # Disjoint four-item facets imply 30 unique targets and exactly three
    # observed items per facet for every record/seed.
    ordered = np.sort(masks, axis=2)
    if masks.shape[0] and np.any(np.diff(ordered, axis=2) == 0):
        raise ValueError("mask failure: a record/seed target item is repeated")


def _response_totals(items: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(items, dtype=np.uint8)
    if values.ndim != 2 or values.shape[1] != ITEM_COUNT:
        raise ValueError("item matrix must have shape (records, 120)")
    if values.size and (int(values.min()) < 1 or int(values.max()) > 5):
        raise ValueError("eligible item matrix contains a response outside 1..5")
    facet_totals = values[:, FACET_ITEMS].sum(axis=2, dtype=np.int16)
    domain_totals = values[:, DOMAIN_ITEMS].sum(axis=2, dtype=np.int16)
    return facet_totals, domain_totals


def _observed_contexts(
    items: np.ndarray,
    masks_for_seed: np.ndarray,
    facet_totals: np.ndarray,
    domain_totals: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    n_records = len(items)
    rows = np.arange(n_records)[:, None]
    masked_values = items[rows, masks_for_seed]
    observed_facet_sums = facet_totals - masked_values
    observed_domain_sums = domain_totals.copy()
    for domain in range(5):
        domain_facets = slice(domain * 6, (domain + 1) * 6)
        observed_domain_sums[:, domain] -= masked_values[:, domain_facets].sum(
            axis=1, dtype=np.int16
        )
    if n_records:
        if int(observed_facet_sums.min()) < 3 or int(observed_facet_sums.max()) > 15:
            raise ValueError("facet-context failure: expected three observed responses")
        if int(observed_domain_sums.min()) < 18 or int(observed_domain_sums.max()) > 90:
            raise ValueError("domain-context failure: expected 18 observed responses")
    return observed_facet_sums, observed_domain_sums


def fit_empirical_baselines(
    items: np.ndarray,
    masks: np.ndarray,
) -> tuple[dict[str, np.ndarray], dict[str, object]]:
    """Fit all four additive-1 empirical distributions on masked targets.

    Conditional bins are exact integer sums of the observed responses: three
    items for declared/wrong facets and 18 items for the target domain.  Every
    distribution remains target-item-specific.  Unseen bins therefore remain
    the fixed symmetric Dirichlet(1,1,1,1,1) distribution; no fitted backoff or
    bin tuning is used.
    """

    values = np.asarray(items, dtype=np.uint8)
    validate_masks(masks)
    if masks.shape[0] != len(values):
        raise ValueError("training items and masks have different record counts")
    counts = {
        "per_item": np.full((ITEM_COUNT, 5), DIRICHLET_PSEUDOCOUNT, dtype=np.float64),
        "domain_conditioned": np.full(
            (ITEM_COUNT, 91, 5), DIRICHLET_PSEUDOCOUNT, dtype=np.float64
        ),
        "declared_facet": np.full(
            (ITEM_COUNT, 16, 5), DIRICHLET_PSEUDOCOUNT, dtype=np.float64
        ),
        "cyclic_wrong_facet": np.full(
            (ITEM_COUNT, 16, 5), DIRICHLET_PSEUDOCOUNT, dtype=np.float64
        ),
    }
    facet_totals, domain_totals = _response_totals(values)
    rows = np.arange(len(values))
    for seed_index in range(len(MASK_SEEDS)):
        seed_masks = masks[:, seed_index, :]
        observed_facets, observed_domains = _observed_contexts(
            values, seed_masks, facet_totals, domain_totals
        )
        for facet in range(30):
            target_items = seed_masks[:, facet]
            outcomes = values[rows, target_items].astype(np.int16) - 1
            facet_context = observed_facets[:, facet]
            wrong_context = observed_facets[:, int(WRONG_FACETS[facet])]
            domain_context = observed_domains[:, int(FACET_DOMAINS[facet])]
            np.add.at(counts["per_item"], (target_items, outcomes), 1.0)
            np.add.at(
                counts["domain_conditioned"],
                (target_items, domain_context, outcomes),
                1.0,
            )
            np.add.at(
                counts["declared_facet"],
                (target_items, facet_context, outcomes),
                1.0,
            )
            np.add.at(
                counts["cyclic_wrong_facet"],
                (target_items, wrong_context, outcomes),
                1.0,
            )

    expected_targets = len(values) * len(MASK_SEEDS) * 30
    observed_per_item = int(
        np.rint((counts["per_item"] - DIRICHLET_PSEUDOCOUNT).sum())
    )
    if observed_per_item != expected_targets:
        raise ValueError(
            f"estimation failure: expected {expected_targets} training targets, "
            f"counted {observed_per_item}"
        )

    probabilities: dict[str, np.ndarray] = {}
    diagnostics: dict[str, object] = {
        "training_records": len(values),
        "training_mask_seeds": list(MASK_SEEDS),
        "training_targets": expected_targets,
        "dirichlet_pseudocount_per_class": DIRICHLET_PSEUDOCOUNT,
        "conditional_bins": {
            "domain_conditioned": "exact sum of 18 observed target-domain items (18..90)",
            "declared_facet": "exact sum of three observed target-facet items (3..15)",
            "cyclic_wrong_facet": "exact sum of three observed items in the next facet within target domain (3..15)",
        },
        "models": {},
    }
    for name in MODEL_NAMES:
        model_counts = counts[name]
        probabilities[name] = normalize_probabilities(model_counts)
        empirical_totals = (model_counts - DIRICHLET_PSEUDOCOUNT).sum(axis=-1)
        used = empirical_totals > 0
        diagnostics["models"][name] = {
            "count_tensor_shape": list(model_counts.shape),
            "used_target_context_bins": int(used.sum()),
            "all_target_context_bins": int(used.size),
            "minimum_examples_in_used_bin": int(empirical_totals[used].min()) if np.any(used) else 0,
            "maximum_examples_in_used_bin": int(empirical_totals[used].max()) if np.any(used) else 0,
        }
    return counts, diagnostics


def normalize_probabilities(values: np.ndarray) -> np.ndarray:
    """Validate, clip to 1e-15, and renormalize five-class probabilities."""

    probabilities = np.asarray(values, dtype=np.float64)
    if probabilities.shape[-1] != 5:
        raise ValueError("probability failure: final dimension must contain five classes")
    if not np.all(np.isfinite(probabilities)) or np.any(probabilities < 0):
        raise ValueError("probability failure: vectors must be finite and nonnegative")
    totals = probabilities.sum(axis=-1, keepdims=True)
    if not np.all(np.isfinite(totals)) or np.any(totals <= 0):
        raise ValueError("probability failure: vectors must have positive finite sums")
    normalized = probabilities / totals
    normalized = np.maximum(normalized, 1e-15)
    normalized /= normalized.sum(axis=-1, keepdims=True)
    if not np.all(np.isfinite(normalized)):
        raise ValueError("probability failure after clipping and renormalization")
    return normalized


def normalized_ordinal_rps(probabilities: np.ndarray, outcomes: np.ndarray) -> np.ndarray:
    """Five-class normalized ranked probability score from the frozen rule."""

    probs = normalize_probabilities(probabilities)
    observed = np.asarray(outcomes, dtype=np.int16)
    if observed.ndim != 1 or len(observed) != len(probs):
        raise ValueError("RPS outcomes must be a vector matching probability rows")
    if observed.size and (int(observed.min()) < 0 or int(observed.max()) > 4):
        raise ValueError("RPS outcomes must use zero-based classes 0..4")
    cumulative = np.cumsum(probs, axis=1)[:, :4]
    indicators = observed[:, None] <= np.arange(4, dtype=np.int16)[None, :]
    return np.mean((cumulative - indicators) ** 2, axis=1)


def score_empirical_baselines(
    items: np.ndarray,
    masks: np.ndarray,
    counts: Mapping[str, np.ndarray],
) -> tuple[np.ndarray, np.ndarray, dict[str, dict[str, float]]]:
    """Return record x seed x model log loss and normalized RPS."""

    values = np.asarray(items, dtype=np.uint8)
    validate_masks(masks)
    if masks.shape[0] != len(values):
        raise ValueError("validation items and masks have different record counts")
    probabilities = {name: normalize_probabilities(counts[name]) for name in MODEL_NAMES}
    losses = np.zeros((len(values), len(MASK_SEEDS), len(MODEL_NAMES)), dtype=np.float64)
    rps = np.zeros_like(losses)
    diagnostics = {
        name: {
            "minimum_class_probability": 1.0,
            "maximum_probability_sum_abs_error": 0.0,
            "malformed_vectors": 0,
        }
        for name in MODEL_NAMES
    }
    facet_totals, domain_totals = _response_totals(values)
    rows = np.arange(len(values))
    for seed_index in range(len(MASK_SEEDS)):
        seed_masks = masks[:, seed_index, :]
        observed_facets, observed_domains = _observed_contexts(
            values, seed_masks, facet_totals, domain_totals
        )
        for facet in range(30):
            target_items = seed_masks[:, facet]
            outcomes = values[rows, target_items].astype(np.int16) - 1
            contexts = {
                "domain_conditioned": observed_domains[:, int(FACET_DOMAINS[facet])],
                "declared_facet": observed_facets[:, facet],
                "cyclic_wrong_facet": observed_facets[:, int(WRONG_FACETS[facet])],
            }
            for model_index, name in enumerate(MODEL_NAMES):
                if name == "per_item":
                    predicted = probabilities[name][target_items]
                else:
                    predicted = probabilities[name][target_items, contexts[name]]
                predicted = normalize_probabilities(predicted)
                diagnostics[name]["minimum_class_probability"] = min(
                    diagnostics[name]["minimum_class_probability"],
                    float(predicted.min()),
                )
                diagnostics[name]["maximum_probability_sum_abs_error"] = max(
                    diagnostics[name]["maximum_probability_sum_abs_error"],
                    float(np.max(np.abs(predicted.sum(axis=1) - 1.0))),
                )
                chosen = predicted[rows, outcomes]
                losses[:, seed_index, model_index] += -np.log(chosen)
                rps[:, seed_index, model_index] += normalized_ordinal_rps(
                    predicted, outcomes
                )
    losses /= 30.0
    rps /= 30.0
    if not np.all(np.isfinite(losses)) or np.any(losses < 0):
        raise ValueError("metric failure: log loss is malformed")
    if not np.all(np.isfinite(rps)) or np.any(rps < 0) or np.any(rps > 1):
        raise ValueError("metric failure: normalized RPS is malformed")
    return losses, rps, diagnostics


def bootstrap_columns(
    columns: np.ndarray,
    names: Sequence[str],
    *,
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> dict[str, dict[str, float | int]]:
    """Uniform paired record bootstrap for one or more aligned columns."""

    values = np.asarray(columns, dtype=np.float64)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or values.shape[1] != len(names):
        raise ValueError("bootstrap columns and names do not align")
    if not len(values) or not np.all(np.isfinite(values)):
        raise ValueError("bootstrap requires at least one finite record")
    rng = np.random.default_rng(seed)
    sampled_means = np.empty((resamples, values.shape[1]), dtype=np.float64)
    for bootstrap_index in range(resamples):
        indices = rng.integers(0, len(values), size=len(values))
        sampled_means[bootstrap_index] = values[indices].mean(axis=0)
    lower, upper = np.quantile(sampled_means, [0.025, 0.975], axis=0, method="linear")
    points = values.mean(axis=0)
    return {
        name: {
            "mean": float(points[index]),
            "ci_95_percentile_lower": float(lower[index]),
            "ci_95_percentile_upper": float(upper[index]),
            "records": len(values),
            "resamples": resamples,
            "seed": seed,
        }
        for index, name in enumerate(names)
    }


def hierarchy_artifact() -> dict[str, object]:
    facets: list[dict[str, object]] = []
    for facet in range(30):
        domain = int(FACET_DOMAINS[facet])
        local_facet = facet % 6
        wrong = int(WRONG_FACETS[facet])
        facets.append(
            {
                "facet_index_0based": facet,
                "facet_code": f"{DOMAIN_CODES[domain]}{local_facet + 1}",
                "facet_name": FACET_NAMES[domain][local_facet],
                "domain_index_0based": domain,
                "domain_code": DOMAIN_CODES[domain],
                "domain_name": DOMAIN_NAMES[domain],
                "item_ids": [ITEM_IDS[int(item)] for item in FACET_ITEMS[facet]],
                "item_indices_0based": [int(item) for item in FACET_ITEMS[facet]],
                "cyclic_wrong_facet_index_0based": wrong,
                "cyclic_wrong_facet_code": f"{DOMAIN_CODES[domain]}{wrong % 6 + 1}",
            }
        )
    return {
        "study_id": STUDY_ID,
        "map_source": "legacy audit formula domain + 5*facet + 30*repeat",
        "item_id_convention": "I001..I120 in raw file order",
        "wrong_facet_rule": "next facet within the same domain, wrapping facet 6 to facet 1",
        "facets": facets,
    }


def _write_selected_sample(path: Path, samples: Iterable[SelectedSample]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "split",
                "sample_rank_1based",
                "source_row_index_0based",
                "split_bucket",
                "fingerprint_sha256",
                "sample_rank_sha256",
            ]
        )
        for sample in samples:
            for rank, (row_index, fingerprint, sample_digest) in enumerate(
                zip(sample.row_indices, sample.fingerprints, sample.sample_digests), start=1
            ):
                writer.writerow(
                    [
                        sample.split,
                        rank,
                        int(row_index),
                        fingerprint_split_bucket(fingerprint),
                        sha256_bytes(fingerprint),
                        sample_digest.hex(),
                    ]
                )


def _write_record_metrics(
    output_dir: Path,
    validation: SelectedSample,
    losses: np.ndarray,
    rps: np.ndarray,
) -> None:
    record_losses = losses.mean(axis=1)
    record_rps = rps.mean(axis=1)
    with (output_dir / "per_record_metrics.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        header = ["source_row_index_0based", "fingerprint_sha256"]
        for name in MODEL_NAMES:
            header.extend([f"{name}_log_loss", f"{name}_normalized_rps"])
        writer.writerow(header)
        for row in range(len(validation.row_indices)):
            values: list[object] = [
                int(validation.row_indices[row]),
                sha256_bytes(validation.fingerprints[row]),
            ]
            for model_index in range(len(MODEL_NAMES)):
                values.extend(
                    [
                        format(float(record_losses[row, model_index]), ".17g"),
                        format(float(record_rps[row, model_index]), ".17g"),
                    ]
                )
            writer.writerow(values)

    with (output_dir / "per_record_seed_metrics.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        header = ["source_row_index_0based", "fingerprint_sha256", "mask_seed"]
        for name in MODEL_NAMES:
            header.extend([f"{name}_log_loss", f"{name}_normalized_rps"])
        writer.writerow(header)
        for row in range(len(validation.row_indices)):
            fingerprint_hash = sha256_bytes(validation.fingerprints[row])
            for seed_index, seed in enumerate(MASK_SEEDS):
                values = [int(validation.row_indices[row]), fingerprint_hash, seed]
                for model_index in range(len(MODEL_NAMES)):
                    values.extend(
                        [
                            format(float(losses[row, seed_index, model_index]), ".17g"),
                            format(float(rps[row, seed_index, model_index]), ".17g"),
                        ]
                    )
                writer.writerow(values)


def _write_seed_metrics(path: Path, losses: np.ndarray, rps: np.ndarray) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["mask_seed", "model", "mean_log_loss", "mean_normalized_rps"])
        for seed_index, seed in enumerate(MASK_SEEDS):
            for model_index, name in enumerate(MODEL_NAMES):
                writer.writerow(
                    [
                        seed,
                        name,
                        format(float(losses[:, seed_index, model_index].mean()), ".17g"),
                        format(float(rps[:, seed_index, model_index].mean()), ".17g"),
                    ]
                )


def _file_inventory(output_dir: Path, *, exclude: Sequence[str] = ()) -> list[dict[str, object]]:
    excluded = set(exclude)
    inventory: list[dict[str, object]] = []
    for path in sorted(output_dir.iterdir(), key=lambda value: value.name):
        if not path.is_file() or path.name in excluded:
            continue
        inventory.append(
            {
                "path": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return inventory


def _peak_rss_mib() -> float:
    # Linux reports KiB for ru_maxrss.  This study run is frozen on Linux; the
    # platform is retained alongside the value.
    return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024.0


def run_analysis(input_path: Path, output_dir: Path) -> dict[str, object]:
    print("CC-101: validating the IPIP-NEO-120 fixed-width input", flush=True)
    parsed = inspect_ipip120(input_path)
    train, validation, split_statistics = select_bounded_samples(parsed.representatives)
    print(
        f"CC-101: selected {len(train.row_indices)} train and "
        f"{len(validation.row_indices)} validation unique fingerprints",
        flush=True,
    )

    train_masks = generate_masks(train.row_indices, progress_label="CC-101 train")
    validation_masks = generate_masks(
        validation.row_indices, progress_label="CC-101 validation"
    )
    print("CC-101: fitting four frozen empirical baselines", flush=True)
    counts, estimation_diagnostics = fit_empirical_baselines(train.items, train_masks)
    print("CC-101: scoring validation records", flush=True)
    losses, rps, probability_diagnostics = score_empirical_baselines(
        validation.items, validation_masks, counts
    )

    record_losses = losses.mean(axis=1)
    record_rps = rps.mean(axis=1)
    model_mean_losses = {
        name: float(record_losses[:, index].mean())
        for index, name in enumerate(MODEL_NAMES)
    }
    strongest_control = min(CONTROL_NAMES, key=lambda name: model_mean_losses[name])

    bootstrap_names: list[str] = []
    bootstrap_values: list[np.ndarray] = []
    for model_index, name in enumerate(MODEL_NAMES):
        bootstrap_names.extend([f"{name}_log_loss", f"{name}_normalized_rps"])
        bootstrap_values.extend([record_losses[:, model_index], record_rps[:, model_index]])
    for control in CONTROL_NAMES:
        control_index = MODEL_NAMES.index(control)
        facet_index = MODEL_NAMES.index("declared_facet")
        bootstrap_names.extend(
            [
                f"declared_facet_minus_{control}_log_loss",
                f"declared_facet_minus_{control}_normalized_rps",
            ]
        )
        bootstrap_values.extend(
            [
                record_losses[:, facet_index] - record_losses[:, control_index],
                record_rps[:, facet_index] - record_rps[:, control_index],
            ]
        )
    bootstrap = bootstrap_columns(np.column_stack(bootstrap_values), bootstrap_names)
    primary_key = f"declared_facet_minus_{strongest_control}_log_loss"
    primary = bootstrap[primary_key]
    lower = float(primary["ci_95_percentile_lower"])
    upper = float(primary["ci_95_percentile_upper"])
    if upper < 0:
        outcome = "suggestive_hierarchy_signal_in_bounded_development_pilot"
    elif lower > 0:
        outcome = "strongest_control_superior_in_bounded_development_pilot"
    else:
        outcome = "null_or_inconclusive_in_bounded_development_pilot"

    write_json(output_dir / "hierarchy_map.json", hierarchy_artifact())
    _write_selected_sample(output_dir / "selected_sample.csv", (train, validation))
    np.savez_compressed(
        output_dir / "mask_targets.npz",
        mask_seeds=np.asarray(MASK_SEEDS, dtype=np.int64),
        train_source_row_indices_0based=train.row_indices,
        validation_source_row_indices_0based=validation.row_indices,
        train_target_item_indices_0based=train_masks,
        validation_target_item_indices_0based=validation_masks,
    )
    np.savez_compressed(output_dir / "baseline_counts.npz", **counts)
    _write_record_metrics(output_dir, validation, losses, rps)
    _write_seed_metrics(output_dir / "per_seed_metrics.csv", losses, rps)

    model_metrics: dict[str, object] = {}
    for model_index, name in enumerate(MODEL_NAMES):
        model_metrics[name] = {
            "mean_record_log_loss_nats": float(record_losses[:, model_index].mean()),
            "mean_record_normalized_rps": float(record_rps[:, model_index].mean()),
            "record_log_loss_bootstrap": bootstrap[f"{name}_log_loss"],
            "record_normalized_rps_bootstrap": bootstrap[f"{name}_normalized_rps"],
            "mask_seed_means": {
                str(seed): {
                    "log_loss_nats": float(losses[:, seed_index, model_index].mean()),
                    "normalized_rps": float(rps[:, seed_index, model_index].mean()),
                }
                for seed_index, seed in enumerate(MASK_SEEDS)
            },
        }

    contrasts = {
        control: {
            "log_loss": bootstrap[f"declared_facet_minus_{control}_log_loss"],
            "normalized_rps": bootstrap[
                f"declared_facet_minus_{control}_normalized_rps"
            ],
        }
        for control in CONTROL_NAMES
    }
    summary: dict[str, object] = {
        "schema": "upg.cc-101.ipip-hierarchy-pilot-summary.v1",
        "study_id": STUDY_ID,
        "protocol_dependency": PROTOCOL_ID,
        "status": "complete_pending_independent_review",
        "mode": "exploratory_development_only",
        "evidence_ceiling": "E2",
        "question": (
            "Does the declared item-to-facet hierarchy predict deliberately hidden ordinal "
            "responses better than per-item, domain-conditioned, and cyclic wrong-facet controls "
            "on a bounded unique-fingerprint IPIP-NEO-120 validation sample?"
        ),
        "frozen_design": {
            "split_salt": SPLIT_SALT,
            "sample_salt": SAMPLE_SALT,
            "train_cap": TRAIN_CAP,
            "validation_cap": VALIDATION_CAP,
            "mask_seeds": list(MASK_SEEDS),
            "mask_rule": (
                "lowest sha256(K-PER-ORDINAL-001|seed|DS-IPIP120-qualified-zero-based-row|I###) "
                "item in each four-item facet"
            ),
            "dirichlet_pseudocount_per_class": DIRICHLET_PSEUDOCOUNT,
            "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "bootstrap_interval": "two-sided 95% percentile; NumPy linear quantile",
            "primary_contrast_direction": "declared_facet_log_loss_minus_strongest_control_log_loss; negative favors declared facet",
        },
        "input_checks": dict(parsed.statistics),
        "split_and_sample": split_statistics,
        "mask_checks": {
            "train_mask_shape": list(train_masks.shape),
            "validation_mask_shape": list(validation_masks.shape),
            "targets_per_record_seed": 30,
            "observed_items_retained_per_facet": 3,
            "train_mask_array_sha256": sha256_bytes(train_masks.tobytes(order="C")),
            "validation_mask_array_sha256": sha256_bytes(
                validation_masks.tobytes(order="C")
            ),
        },
        "estimation": estimation_diagnostics,
        "probability_checks": probability_diagnostics,
        "model_metrics": model_metrics,
        "strongest_control_by_validation_log_loss": strongest_control,
        "pairwise_declared_facet_minus_control": contrasts,
        "primary_contrast": {
            "key": primary_key,
            **primary,
            "outcome_code": outcome,
        },
        "failures": [],
        "deviations": [],
        "limitations": [
            "Development-only complete-response sample; incomplete records and other populations are not represented.",
            "The empirical exact-sum conditional bins are deliberately simple and do not establish that any signal is uniquely attributable to UPG.",
            "The same archive supports fitting and validation through a deterministic fingerprint split; this is not an external test.",
            "The interval conditions on the prespecified strongest-control selection and does not support causal, temporal, clinical, or whole-UPG inference.",
            "Dataset-local source-row identity is not interpreted as cross-dataset person identity.",
        ],
        "claim_boundary": (
            "At most, this E2 exploratory pilot can describe planned-missing ordinal prediction "
            "signal for the declared IPIP item-to-facet map in a bounded IPIP-NEO-120 development "
            "split. It does not unseal or complete K-PER-ORDINAL-001 and cannot establish external "
            "validity, UPG specificity, dynamics, causality, diagnosis, treatment selection, or "
            "clinical effectiveness."
        ),
    }
    write_json(output_dir / "summary.json", summary)
    return summary


def _commands_payload(input_path: Path, output_path: Path) -> dict[str, object]:
    repo_root = Path(__file__).resolve().parents[1]
    canonical_argv = [
        sys.executable,
        "scripts/ipip_hierarchy_pilot.py",
        "--input",
        str(input_path),
        "--out",
        str(output_path),
    ]
    return {
        "observed_executable": sys.executable,
        "observed_argv": sys.argv,
        "observed_cwd": os.getcwd(),
        "environment": {
            "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED"),
            "PYTHONPATH": os.environ.get("PYTHONPATH"),
        },
        "canonical_run_cwd": str(repo_root),
        "canonical_run_command": "env PYTHONHASHSEED=0 PYTHONPATH=src "
        + shlex.join(canonical_argv),
        "focused_test_cwd": str(repo_root),
        "focused_test_command": (
            "env PYTHONHASHSEED=0 PYTHONPATH=src "
            + shlex.join([sys.executable, "-m", "pytest", "tests/test_ipip_hierarchy_pilot.py", "-q"])
        ),
    }


def execute_frozen_run(input_path: Path, destination: Path) -> Path:
    """Run into a hidden temporary directory and publish once, immutably."""

    if input_path.name != "IPIP120.dat":
        # Reject lexically before any stat/open on a non-authorized input.
        raise ValueError("CC-101 accepts only an explicitly named IPIP120.dat input")
    input_path = input_path.expanduser().resolve(strict=True)
    destination = destination.expanduser().resolve()
    if destination.exists():
        raise FileExistsError(
            f"output destination already exists; choose a new version: {destination}"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    started_utc = datetime.now(timezone.utc).isoformat()
    input_size = input_path.stat().st_size
    input_hash_before = sha256_file(input_path)
    script_path = Path(__file__).resolve()
    test_path = script_path.parents[1] / "tests" / "test_ipip_hierarchy_pilot.py"
    code_inputs = {
        "analysis_script": {
            "path": str(script_path),
            "bytes": script_path.stat().st_size,
            "sha256": sha256_file(script_path),
        },
        "focused_tests": {
            "path": str(test_path),
            "bytes": test_path.stat().st_size,
            "sha256": sha256_file(test_path),
        },
    }
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.tmp-", dir=destination.parent)
    )
    failure: dict[str, object] | None = None
    summary: dict[str, object] | None = None
    try:
        write_json(temporary / "commands.json", _commands_payload(input_path, destination))
        summary = run_analysis(input_path, temporary)
        input_hash_after = sha256_file(input_path)
        if input_hash_before != input_hash_after or input_size != input_path.stat().st_size:
            raise RuntimeError("lineage failure: IPIP120.dat changed during execution")
    except BaseException as exc:  # Retain a quarantine packet for every attempted run.
        input_hash_after = sha256_file(input_path)
        failure = {
            "status": "quarantined",
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
        write_json(temporary / "failure.json", failure)

    resource_payload = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "started_utc": started_utc,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "analysis_and_artifact_wall_seconds": time.perf_counter() - started,
        "peak_process_rss_mib_linux_ru_maxrss": _peak_rss_mib(),
        "rss_limit_mib": 8192,
        "runtime_limit_seconds": 1200,
        "resource_limit_status": "pending_manifest_finalization",
        "measurement_boundary": (
            "Wall time includes pre-run input/code hashing, analysis, and primary artifact writes; "
            "it excludes final output inventory hashing and atomic rename. Peak RSS is whole-process."
        ),
    }
    resource_payload["resource_limit_status"] = (
        "pass"
        if resource_payload["analysis_and_artifact_wall_seconds"] <= 1200
        and resource_payload["peak_process_rss_mib_linux_ru_maxrss"] <= 8192
        else "fail_quarantine_required"
    )
    if resource_payload["resource_limit_status"] != "pass" and failure is None:
        failure = {
            "status": "quarantined",
            "exception_type": "ResourceLimitExceeded",
            "message": "CC-101 exceeded the frozen runtime or RSS limit",
        }
        write_json(temporary / "failure.json", failure)
    write_json(temporary / "resource.json", resource_payload)

    status = "complete" if failure is None else "quarantined"
    manifest = {
        "schema": "upg.cc-101.run-manifest.v1",
        "study_id": STUDY_ID,
        "protocol_dependency": PROTOCOL_ID,
        "status": status,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "destination": str(destination),
        "input": {
            "label": "DS-IPIP120",
            "path": str(input_path),
            "bytes": input_size,
            "sha256_before": input_hash_before,
            "sha256_after": input_hash_after,
            "unchanged": input_hash_before == input_hash_after,
        },
        "code_inputs": code_inputs,
        "frozen_constants": {
            "split_salt": SPLIT_SALT,
            "sample_salt": SAMPLE_SALT,
            "train_cap": TRAIN_CAP,
            "validation_cap": VALIDATION_CAP,
            "mask_seeds": list(MASK_SEEDS),
            "dirichlet_pseudocount": DIRICHLET_PSEUDOCOUNT,
            "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
            "bootstrap_seed": BOOTSTRAP_SEED,
        },
        "outcome_code": (
            summary["primary_contrast"]["outcome_code"] if summary is not None else None
        ),
        "failure": failure,
        "outputs": _file_inventory(temporary, exclude=("manifest.json",)),
        "manifest_hash_scope": "Every regular file in outputs; manifest.json is excluded from its own inventory.",
    }
    write_json(temporary / "manifest.json", manifest)
    if destination.exists():
        shutil.rmtree(temporary)
        raise FileExistsError(f"output appeared during run: {destination}")
    os.rename(temporary, destination)
    print(f"CC-101: published {status} run at {destination}", flush=True)
    if failure is not None:
        raise RuntimeError(f"CC-101 run quarantined: {failure['message']}")
    return destination


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="explicit authorized IPIP120.dat path; no data-root discovery is performed",
    )
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="new, nonexistent versioned output directory",
    )
    args = parser.parse_args(argv)
    try:
        execute_frozen_run(args.input, args.out)
    except (FileExistsError, FileNotFoundError, PermissionError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
