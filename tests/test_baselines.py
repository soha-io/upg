"""Step 4 baselines: Student-t utilities, Bayesian anchored VAR, EIV
correction, and the EKF-EM state-space estimator."""
import numpy as np
import pytest

from upg.baselines import (baseline_recover_dataset, betainc_reg,
                           edge_coverage, fit_bayes_person, fit_ev_person,
                           fit_kalman_person, fit_scaling_law, t_cdf, t_ppf)
from upg.recover import fit_person, recovery_metrics
from upg.simulate import SimConfig, dimension_base, simulate_population


@pytest.fixture(scope="module")
def small_dataset():
    config = SimConfig(T=120, meas_noise=0.08, sampling_rate=0.85,
                       dropout_prob=0.0, process_noise=0.06, seed=1)
    return simulate_population(8, config=config, pop_seed=1)


# -------------------------------------------------------------------------
# Student-t machinery (checked against standard table values)
# -------------------------------------------------------------------------

def test_betainc_endpoints():
    assert betainc_reg(2.0, 3.0, 0.0) == 0.0
    assert betainc_reg(2.0, 3.0, 1.0) == 1.0
    # I_x(1,1) = x
    assert abs(betainc_reg(1.0, 1.0, 0.37) - 0.37) < 1e-10


def test_t_cdf_symmetry_and_normal_limit():
    assert abs(t_cdf(0.0, 7.0) - 0.5) < 1e-12
    assert abs(t_cdf(1.5, 9.0) + t_cdf(-1.5, 9.0) - 1.0) < 1e-10
    # large df -> normal: Phi(1.96) ~ 0.975
    assert abs(t_cdf(1.96, 1e6) - 0.975) < 1e-3


def test_t_ppf_table_values():
    # classic two-sided 95% critical values
    assert abs(t_ppf(0.975, 10.0) - 2.228) < 2e-3
    assert abs(t_ppf(0.975, 30.0) - 2.042) < 2e-3
    assert abs(t_ppf(0.95, 5.0) - 2.015) < 2e-3
    # inverse property
    q = t_cdf(t_ppf(0.8, 12.0), 12.0)
    assert abs(q - 0.8) < 1e-8


# -------------------------------------------------------------------------
# Bayesian anchored VAR
# -------------------------------------------------------------------------

def test_bayes_posterior_mean_matches_ridge(small_dataset):
    """With matched prior precision, the NIG posterior mean equals the
    Step 3 anchored ridge estimate (conjugacy check)."""
    r = small_dataset.records[0]
    bp = fit_bayes_person(r.observations, r.u, r.params.kappa, tau=0.2)
    rec = fit_person(r.observations, r.u, r.params.kappa, ridge=0.2,
                     anchor=True)
    assert np.allclose(bp.B_mean, rec.B_hat, atol=1e-8)
    assert np.allclose(bp.g_mean, rec.g_hat, atol=1e-8)


def test_bayes_intervals_contain_mean_and_are_ordered(small_dataset):
    r = small_dataset.records[1]
    bp = fit_bayes_person(r.observations, r.u, r.params.kappa)
    base_B, _g, _d, _k = dimension_base()
    sup = base_B != 0.0
    assert np.all(bp.B_lo[sup] <= bp.B_mean[sup] + 1e-12)
    assert np.all(bp.B_mean[sup] <= bp.B_hi[sup] + 1e-12)
    cov = edge_coverage(bp, r.params.B)
    assert 0.0 <= cov["coverage"] <= 1.0
    assert cov["mean_width"] > 0.0


def test_bayes_width_shrinks_with_data():
    base_cfg = dict(meas_noise=0.05, sampling_rate=1.0, dropout_prob=0.0,
                    process_noise=0.06)
    widths = []
    for T in (30, 250):
        config = SimConfig(T=T, seed=3, **base_cfg)
        ds = simulate_population(3, config=config, pop_seed=3)
        r = ds.records[0]
        bp = fit_bayes_person(r.observations, r.u, r.params.kappa)
        cov = edge_coverage(bp, r.params.B)
        widths.append(cov["mean_width"])
    assert widths[1] < widths[0]


# -------------------------------------------------------------------------
# Errors-in-variables correction
# -------------------------------------------------------------------------

def test_ev_beats_free_ls_at_high_noise():
    """At heavy measurement noise the subspace-truncated EIV estimator must
    beat the uncorrected free estimator on edge RMSE (it corrects the
    attenuation bias in identified directions and refuses to invert
    noise-dominated ones)."""
    config = SimConfig(T=500, meas_noise=0.15, sampling_rate=1.0,
                       dropout_prob=0.0, process_noise=0.08, seed=5)
    ds = simulate_population(6, config=config, pop_seed=5)
    base_B, _g, _d, _k = dimension_base()
    sup = base_B != 0.0
    rmse_plain, rmse_ev = [], []
    for r in ds.records:
        rec0 = fit_person(r.observations, r.u, r.params.kappa, ridge=1e-6,
                          anchor=False)
        rec1 = fit_ev_person(r.observations, r.u, r.params.kappa,
                             meas_sd=0.15, ridge=1e-6, anchor=False)
        bt = r.params.B[sup]
        rmse_plain.append(np.sqrt(np.mean((rec0.B_hat[sup] - bt) ** 2)))
        rmse_ev.append(np.sqrt(np.mean((rec1.B_hat[sup] - bt) ** 2)))
    assert np.median(rmse_ev) < np.median(rmse_plain)


# -------------------------------------------------------------------------
# EKF-EM state-space estimator
# -------------------------------------------------------------------------

def test_kalman_runs_with_missingness(small_dataset):
    r = small_dataset.records[2]
    rec = fit_kalman_person(r.observations, r.u, r.params.kappa,
                            meas_sd=0.08, process_sd=0.06, n_em=2)
    assert np.all(np.isfinite(rec.B_hat))
    m = recovery_metrics(r.params, rec)
    assert np.isfinite(m["edge_rmse"])
    # uses every consecutive smoothed pair, not just complete cases
    assert rec.n_transitions == r.observations.shape[0] - 1


def test_kalman_beats_step3_under_heavy_noise():
    """Smoothed states should mitigate the errors-in-variables floor."""
    config = SimConfig(T=250, meas_noise=0.20, sampling_rate=0.9,
                       dropout_prob=0.0, process_noise=0.08, seed=7)
    ds = simulate_population(6, config=config, pop_seed=7)
    rmse3, rmse_k = [], []
    for r in ds.records:
        m3 = recovery_metrics(
            r.params, fit_person(r.observations, r.u, r.params.kappa))
        mk = recovery_metrics(
            r.params, fit_kalman_person(r.observations, r.u, r.params.kappa,
                                        meas_sd=0.20, process_sd=0.08,
                                        n_em=3))
        rmse3.append(m3["edge_rmse"])
        rmse_k.append(mk["edge_rmse"])
    assert np.median(rmse_k) < np.median(rmse3)


# -------------------------------------------------------------------------
# Dataset runner + scaling law
# -------------------------------------------------------------------------

def test_baseline_recover_dataset_all_methods(small_dataset):
    for method in ("bayes", "ev", "kalman"):
        out = baseline_recover_dataset(small_dataset, method)
        agg = out["aggregate"]
        assert agg["n_persons"] == 8
        assert np.isfinite(agg["median_edge_rmse"])
    bayes = baseline_recover_dataset(small_dataset, "bayes")["aggregate"]
    assert "mean_coverage" in bayes


def test_scaling_law_recovers_known_curve():
    T = np.array([30, 60, 120, 250, 500, 1000], float)
    E_true, A_true, beta_true = 0.08, 2.0, 0.55
    y = E_true + A_true * T ** (-beta_true)
    fit = fit_scaling_law(T, y)
    assert abs(fit["beta"] - beta_true) < 0.05
    assert abs(fit["E"] - E_true) < 0.02
