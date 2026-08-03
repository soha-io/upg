"""Focused contract tests for the frozen CC-101 development pilot."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ipip_hierarchy_pilot.py"
SPEC = importlib.util.spec_from_file_location("ipip_hierarchy_pilot", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
pilot = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = pilot
SPEC.loader.exec_module(pilot)


def _record(source_index: int, responses: bytes, terminator: bytes = b"\r\n") -> bytes:
    assert len(responses) == 120
    prefix = f"{source_index:031d}".encode("ascii")
    assert len(prefix) == 31
    return prefix + responses + terminator


def _fingerprint(number: int) -> bytes:
    """Unique fixed-width base-five response vector with values 1..5."""

    digits = bytearray(b"1" * 120)
    cursor = 119
    value = number
    while value:
        digits[cursor] = ord("1") + value % 5
        value //= 5
        cursor -= 1
    return bytes(digits)


def test_frozen_constants_are_exact() -> None:
    assert pilot.PROTOCOL_ID == "K-PER-ORDINAL-001"
    assert pilot.SPLIT_SALT == "UPG-K-PER-ORDINAL-v1-SPLIT"
    assert pilot.SAMPLE_SALT == "CC-101-PILOT-SAMPLE-v1"
    assert pilot.TRAIN_CAP == 50_000
    assert pilot.VALIDATION_CAP == 20_000
    assert pilot.MASK_SEEDS == (
        2026071501,
        2026071502,
        2026071503,
        2026071504,
        2026071505,
    )
    assert pilot.DIRICHLET_PSEUDOCOUNT == 1.0
    assert pilot.BOOTSTRAP_RESAMPLES == 2_000
    assert pilot.BOOTSTRAP_SEED == 2026071699
    assert pilot.MODEL_NAMES == (
        "per_item",
        "domain_conditioned",
        "declared_facet",
        "cyclic_wrong_facet",
    )


def test_legacy_hierarchy_is_a_partition_with_cyclic_wrong_facets() -> None:
    assert pilot.FACET_ITEMS.shape == (30, 4)
    assert sorted(pilot.FACET_ITEMS.ravel().tolist()) == list(range(120))
    for domain in range(5):
        for local_facet in range(6):
            facet = domain * 6 + local_facet
            expected = [
                domain + 5 * local_facet + 30 * repeat for repeat in range(4)
            ]
            assert pilot.FACET_ITEMS[facet].tolist() == expected
            assert pilot.FACET_DOMAINS[facet] == domain
            assert pilot.WRONG_FACETS[facet] == domain * 6 + ((local_facet + 1) % 6)
            assert set(pilot.FACET_ITEMS[facet]).isdisjoint(
                set(pilot.FACET_ITEMS[pilot.WRONG_FACETS[facet]])
            )


def test_fixed_width_parser_range_eligibility_and_lowest_representative(tmp_path: Path) -> None:
    complete_one = b"1" * 120
    incomplete = b"1" * 40 + b"0" + b"2" * 79
    complete_five = b"5" * 120
    path = tmp_path / "IPIP120.dat"
    path.write_bytes(
        _record(0, complete_one)
        + _record(1, incomplete)
        + _record(2, complete_one)
        + _record(3, complete_five)
    )

    parsed = pilot.inspect_ipip120(path, expected_source_rows=None)

    assert parsed.statistics == {
        "source_rows": 4,
        "record_bytes": 153,
        "item_count": 120,
        "missing_item_cells_zero": 1,
        "complete_source_rows": 3,
        "incomplete_source_rows": 1,
        "unique_complete_fingerprints": 2,
        "duplicate_complete_rows_beyond_representatives": 1,
        "minimum_observed_item_value": 0,
        "maximum_observed_item_value": 5,
    }
    assert parsed.representatives[complete_one] == 0
    assert parsed.representatives[complete_five] == 3


@pytest.mark.parametrize(
    ("responses", "terminator", "message"),
    [
        (b"1" * 119 + b"6", b"\r\n", "response-range failure"),
        (b"1" * 120, b"\n\n", "every record must end in CRLF"),
    ],
)
def test_fixed_width_parser_fails_closed(
    tmp_path: Path, responses: bytes, terminator: bytes, message: str
) -> None:
    path = tmp_path / "IPIP120.dat"
    path.write_bytes(_record(0, responses, terminator))
    with pytest.raises(ValueError, match=message):
        pilot.inspect_ipip120(path, expected_source_rows=None)


def test_fixed_width_parser_rejects_wrong_dataset_row_count(tmp_path: Path) -> None:
    path = tmp_path / "IPIP120.dat"
    path.write_bytes(_record(0, b"1" * 120))
    with pytest.raises(ValueError, match="dataset-version failure"):
        pilot.inspect_ipip120(path)


def test_split_formula_caps_and_fingerprint_containment() -> None:
    representatives = {_fingerprint(index): 1_000 + index for index in range(100)}
    train, validation, statistics = pilot.select_bounded_samples(
        representatives, train_cap=7, validation_cap=5
    )

    assert len(train.fingerprints) == 7
    assert len(validation.fingerprints) == 5
    assert set(train.fingerprints).isdisjoint(validation.fingerprints)
    assert all(pilot.fingerprint_split_bucket(value) < 80 for value in train.fingerprints)
    assert all(
        pilot.fingerprint_split_bucket(value) >= 80 for value in validation.fingerprints
    )
    expected_train = sorted(
        (
            pilot.sample_rank_digest(fingerprint),
            fingerprint,
            row_index,
        )
        for fingerprint, row_index in representatives.items()
        if pilot.fingerprint_split_bucket(fingerprint) < 80
    )[:7]
    expected_validation = sorted(
        (
            pilot.sample_rank_digest(fingerprint),
            fingerprint,
            row_index,
        )
        for fingerprint, row_index in representatives.items()
        if pilot.fingerprint_split_bucket(fingerprint) >= 80
    )[:5]
    assert train.fingerprints == tuple(row[1] for row in expected_train)
    assert validation.fingerprints == tuple(row[1] for row in expected_validation)
    assert statistics["unique_train_before_cap"] + statistics[
        "unique_validation_before_cap"
    ] == 100


def test_split_bucket_matches_declared_sha256_text_formula() -> None:
    fingerprint = _fingerprint(981_271)
    expected = int(
        hashlib.sha256(
            b"UPG-K-PER-ORDINAL-v1-SPLIT|" + fingerprint
        ).hexdigest()[:8],
        16,
    ) % 100
    assert pilot.fingerprint_split_bucket(fingerprint) == expected


def test_masks_follow_rank_key_and_preserve_three_observed_items_per_facet() -> None:
    row_indices = np.asarray([0, 42], dtype=np.int64)
    masks = pilot.generate_masks(row_indices)

    assert masks.shape == (2, 5, 30)
    for row in range(2):
        for seed_index, seed in enumerate(pilot.MASK_SEEDS):
            assert len(set(masks[row, seed_index].tolist())) == 30
            for facet in range(30):
                target = int(masks[row, seed_index, facet])
                assert target in pilot.FACET_ITEMS[facet]
                prefix = (
                    f"K-PER-ORDINAL-001|{seed}|"
                    f"DS-IPIP120|source_row_index_0based={int(row_indices[row])}|"
                ).encode("ascii")
                ranked = [
                    (
                        hashlib.sha256(prefix + f"I{int(item) + 1:03d}".encode("ascii")).digest(),
                        f"I{int(item) + 1:03d}",
                        int(item),
                    )
                    for item in pilot.FACET_ITEMS[facet]
                ]
                assert target == min(ranked)[2]
                assert len(set(pilot.FACET_ITEMS[facet]) - {target}) == 3
    assert hashlib.sha256(masks.tobytes(order="C")).hexdigest() == (
        "5c0212ab478b1b493ee7154fdefdfa4371d030edefc3af5a45d05096ecdfa1b1"
    )


def test_empirical_baselines_are_additive_one_normalized_and_finite() -> None:
    records = 25
    items = np.empty((records, 120), dtype=np.uint8)
    for row in range(records):
        items[row] = np.asarray(
            [1 + ((row * 3 + item * 2 + row * item) % 5) for item in range(120)],
            dtype=np.uint8,
        )
    masks = pilot.generate_masks(np.arange(100, 100 + records, dtype=np.int64))
    counts, diagnostics = pilot.fit_empirical_baselines(items, masks)
    losses, rps, probability_diagnostics = pilot.score_empirical_baselines(
        items, masks, counts
    )

    assert diagnostics["training_targets"] == records * 5 * 30
    assert np.isclose(
        (counts["per_item"] - 1.0).sum(), records * 5 * 30
    )
    assert losses.shape == (records, 5, 4)
    assert rps.shape == (records, 5, 4)
    assert np.all(np.isfinite(losses)) and np.all(losses >= 0)
    assert np.all(np.isfinite(rps)) and np.all((rps >= 0) & (rps <= 1))
    for name in pilot.MODEL_NAMES:
        probabilities = pilot.normalize_probabilities(counts[name])
        assert np.all(np.isfinite(probabilities))
        assert np.all(probabilities > 0)
        assert np.allclose(probabilities.sum(axis=-1), 1.0)
        assert probability_diagnostics[name]["malformed_vectors"] == 0


def test_observed_contexts_exclude_all_targets() -> None:
    items = np.ones((1, 120), dtype=np.uint8)
    masks = pilot.generate_masks(np.asarray([7], dtype=np.int64))
    facet_totals, domain_totals = pilot._response_totals(items)
    observed_facets, observed_domains = pilot._observed_contexts(
        items, masks[:, 0, :], facet_totals, domain_totals
    )
    assert observed_facets.tolist() == [[3] * 30]
    assert observed_domains.tolist() == [[18] * 5]


def test_probability_rule_and_normalized_rps_fixture() -> None:
    uniform = np.full((2, 5), 0.2)
    scores = pilot.normalized_ordinal_rps(uniform, np.asarray([0, 2]))
    assert scores == pytest.approx([0.3, 0.1])
    clipped = pilot.normalize_probabilities(np.asarray([[1.0, 0.0, 0.0, 0.0, 0.0]]))
    assert np.all(clipped > 0)
    assert clipped.sum() == pytest.approx(1.0)
    with pytest.raises(ValueError, match="finite and nonnegative"):
        pilot.normalize_probabilities(np.asarray([[1.0, -1.0, 1.0, 1.0, 1.0]]))
    with pytest.raises(ValueError, match="positive finite sums"):
        pilot.normalize_probabilities(np.zeros((1, 5)))


def test_paired_bootstrap_is_deterministic_and_uses_record_mean() -> None:
    values = np.asarray(
        [
            [-1.0, 1.0],
            [0.0, 2.0],
            [1.0, 3.0],
            [2.0, 4.0],
        ]
    )
    first = pilot.bootstrap_columns(values, ("a", "b"), resamples=100, seed=123)
    second = pilot.bootstrap_columns(values, ("a", "b"), resamples=100, seed=123)
    assert first == second
    assert first["a"]["mean"] == pytest.approx(0.5)
    assert first["b"]["mean"] == pytest.approx(2.5)
    assert first["a"]["records"] == 4
    assert first["a"]["resamples"] == 100
    assert first["a"]["seed"] == 123


def test_non_authorized_input_name_is_rejected_before_file_access(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="only an explicitly named IPIP120.dat"):
        pilot.execute_frozen_run(
            tmp_path / "not-authorized.dat", tmp_path / "new-output"
        )
