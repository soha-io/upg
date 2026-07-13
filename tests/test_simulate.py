"""The synthetic-person simulator (Step 2): correctness and reproducibility."""
import tempfile

import numpy as np

from upg.casestudy import KAPPA, build_case_model
from upg.dynamics import iterate
from upg.registry import ENDO
from upg.simulate import (PersonParams, SimConfig, SyntheticDataset,
                          generator_preset_names,
                          characterize, dimension_base, sample_person,
                          simulate_person, simulate_population, simulate_preset)


def test_reproducible_same_seed():
    cfg = SimConfig(T=40, seed=5)
    a = simulate_population(20, config=cfg, pop_seed=2)
    b = simulate_population(20, config=cfg, pop_seed=2)
    for ra, rb in zip(a.records, b.records):
        assert np.array_equal(ra.states, rb.states)
        assert np.allclose(ra.observations, rb.observations, equal_nan=True)


def test_different_pop_seed_differs():
    cfg = SimConfig(T=40, seed=5)
    a = simulate_population(10, config=cfg, pop_seed=1)
    b = simulate_population(10, config=cfg, pop_seed=99)
    assert not np.array_equal(a.records[0].params.B, b.records[0].params.B)


def test_shapes():
    cfg = SimConfig(T=60)
    ds = simulate_population(8, config=cfg, pop_seed=0)
    n = len(ENDO)
    for r in ds.records:
        assert r.states.shape == (60, n)
        assert r.observations.shape == (60, n)
        assert r.u.shape == (60,)


def test_structure_zeros_preserved():
    B0, _g0, _dims, _k = dimension_base()
    ds = simulate_population(30, config=SimConfig(T=20), pop_seed=4)
    for r in ds.records:
        assert np.all(r.params.B[B0 == 0] == 0.0)      # no invented edges
        assert np.all(r.params.B >= 0.0)


def test_gain_sign_preserved():
    _B0, g0, _dims, _k = dimension_base()
    ds = simulate_population(30, config=SimConfig(T=10), pop_seed=6)
    for r in ds.records:
        nz = g0 != 0
        assert np.all(np.sign(r.params.g[nz]) == np.sign(g0[nz]))


def test_noiseless_full_sampling_obs_equals_states():
    cfg = SimConfig(T=30, process_noise=0.0, meas_noise=0.0,
                    sampling_rate=1.0, dropout_prob=0.0)
    rng = np.random.default_rng(0)
    p = sample_person(np.random.default_rng(1), "X")
    rec = simulate_person(p, cfg, rng)
    assert np.allclose(rec.observations, rec.states)
    assert not np.any(np.isnan(rec.observations))


def test_missingness_matches_sampling_rate():
    cfg = SimConfig(T=200, sampling_rate=0.6, dropout_prob=0.0, item_missing=0.0)
    ds = simulate_population(40, config=cfg, pop_seed=0)
    assert abs(ds.missing_fraction() - 0.4) < 0.03


def test_dropout_makes_trailing_nan():
    cfg = SimConfig(T=100, dropout_prob=1.0, sampling_rate=1.0)
    ds = simulate_population(15, config=cfg, pop_seed=0)
    for r in ds.records:
        assert r.dropout_time is not None
        # everything from dropout onward is missing
        assert np.all(np.isnan(r.observations[r.dropout_time:]))
        # something before dropout is observed
        assert np.any(~np.isnan(r.observations[:r.dropout_time]))


def test_deterministic_limit_matches_attractor():
    # A noiseless simulation of the base person converges to the analytic
    # fixed point of Batch J Section 8 (DIS = 0.774).
    B, g, b, idx = build_case_model()
    xstar = iterate(B, g, b, 0.0, np.ones(7), kappa=KAPPA)
    p = characterize(PersonParams("BASE", list(ENDO), B, g, b, KAPPA))
    cfg = SimConfig(T=3, process_noise=0.0, meas_noise=0.0, sampling_rate=1.0,
                    dropout_prob=0.0, burn_in=400)
    rec = simulate_person(p, cfg, np.random.default_rng(0))
    assert abs(rec.states[-1][idx["DIS"]] - xstar[idx["DIS"]]) < 1e-6
    assert abs(xstar[idx["DIS"]] - 0.774) < 1e-3
    assert p.regime == "pinned_high"


def test_regime_labels_valid_and_varied():
    ds = simulate_population(150, config=SimConfig(T=10), pop_seed=0)
    counts = ds.regime_counts()
    assert set(counts) <= {"quiescent", "pinned_high", "bistable"}
    assert len(counts) >= 2                    # population spans regimes


def test_save_load_roundtrip():
    ds = simulate_population(12, config=SimConfig(T=25, seed=3), pop_seed=1)
    with tempfile.TemporaryDirectory() as d:
        ds.save(d)
        ds2 = SyntheticDataset.load(d)
    assert ds2.dims == ds.dims
    assert len(ds2.records) == len(ds.records)
    for r, r2 in zip(ds.records, ds2.records):
        assert np.array_equal(r.states, r2.states)
        assert np.allclose(r.observations, r2.observations, equal_nan=True)
        assert np.array_equal(r.params.B, r2.params.B)
        assert r.params.regime == r2.params.regime
        assert abs(r.params.kappa - r2.params.kappa) < 1e-12


def test_generator_presets_are_named():
    names = generator_preset_names()
    assert names == ["balanced_regimes", "clinical_realistic", "transition_rich"]


def test_balanced_regime_preset_quota_samples_equal_counts():
    ds = simulate_preset(
        "balanced_regimes", 30, T=8, seed=7,
        config_overrides={"burn_in": 20, "dropout_prob": 0.0},
    )
    assert ds.regime_counts() == {
        "bistable": 10,
        "pinned_high": 10,
        "quiescent": 10,
    }


def test_transition_rich_preset_has_pulsed_treatment():
    ds = simulate_preset(
        "transition_rich", 12, T=60, seed=9,
        config_overrides={"burn_in": 20, "dropout_prob": 0.0},
    )
    u = ds.records[0].u
    assert np.max(u) == 0.85
    assert np.min(u) == 0.0
    assert 0.35 in set(np.round(u, 2))
    assert any(r.params.regime == "bistable" for r in ds.records)
