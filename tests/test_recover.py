"""Method recovery (Step 3): the estimator is correct, consistent, and honest."""
import numpy as np

from upg.recover import (fit_person, known_support, recover_dataset,
                         recovery_metrics)
from upg.simulate import SimConfig, sample_person, simulate_person, simulate_population


def _pop(T, meas, samp, procn=0.10, npers=40, seed=0, dropout=0.0):
    cfg = SimConfig(T=T, meas_noise=meas, sampling_rate=samp, dropout_prob=dropout,
                    process_noise=procn, seed=seed)
    return simulate_population(npers, config=cfg, pop_seed=seed,
                              kappa_mean=0.44, kappa_sd=0.09,
                              adversity_mean=0.55, adversity_sd=0.5)


def test_fit_shapes_and_support_preserved():
    p = sample_person(np.random.default_rng(1), "X")
    cfg = SimConfig(T=100, process_noise=0.1, meas_noise=0.0, sampling_rate=1.0,
                    dropout_prob=0.0)
    rec = simulate_person(p, cfg, np.random.default_rng(0))
    r = fit_person(rec.observations, rec.u, p.kappa)
    n = len(p.dims)
    assert r.B_hat.shape == (n, n)
    support = known_support()
    assert np.all(r.B_hat[~support] == 0.0)          # no edges outside the skeleton
    assert r.n_transitions > 0


def test_recovery_improves_with_series_length():
    a_short = recover_dataset(_pop(60, 0.0, 1.0))["aggregate"]
    a_long = recover_dataset(_pop(500, 0.0, 1.0))["aggregate"]
    assert a_long["median_edge_rmse"] < a_short["median_edge_rmse"]
    assert a_long["median_edge_corr"] > a_short["median_edge_corr"]


def test_estimator_is_consistent_beats_prior_with_data():
    # With abundant, well-excited, clean data the personalized estimate beats
    # the consensus prior on absolute edge accuracy (i.e. it converges to truth).
    ds = _pop(3000, 0.0, 1.0, procn=0.25, npers=25)
    agg = recover_dataset(ds, ridge=0.05)["aggregate"]
    assert agg["median_edge_rmse"] < agg["median_prior_rmse"]
    assert agg["median_edge_corr"] > 0.8


def test_prior_anchoring_beats_free_on_short_series():
    ds = _pop(60, 0.0, 1.0)
    anchored = recover_dataset(ds, ridge=0.2, anchor=True)["aggregate"]
    free = recover_dataset(ds, ridge=1e-6, anchor=False)["aggregate"]
    assert anchored["median_edge_rmse"] < free["median_edge_rmse"]


def test_measurement_noise_degrades_edges():
    clean = recover_dataset(_pop(250, 0.0, 1.0))["aggregate"]
    noisy = recover_dataset(_pop(250, 0.20, 1.0))["aggregate"]
    assert noisy["median_edge_rmse"] > clean["median_edge_rmse"]


def test_clinical_quantities_recovered_early():
    # Regime and attractor are recovered well even at modest length + missingness.
    agg = recover_dataset(_pop(120, 0.08, 0.7, dropout=0.2))["aggregate"]
    assert agg["regime_accuracy"] > 0.85
    assert agg["median_attractor_abs_err"] < 0.05


def test_recover_dataset_contract():
    out = recover_dataset(_pop(80, 0.05, 0.8, npers=10))
    assert set(out) == {"per_person", "aggregate"}
    assert len(out["per_person"]) == 10
    for k in ("median_edge_rmse", "median_edge_corr", "regime_accuracy",
              "median_attractor_abs_err", "median_prior_rmse"):
        assert k in out["aggregate"]
