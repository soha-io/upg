"""Step 5: the structure-constrained graph-attention estimator."""
import numpy as np
import pytest

from upg.gat import (GATConfig, MaskedGraphAttentionEstimator,
                     build_training_set, deviation_rank_spectrum, edge_list,
                     gat_recover_dataset, person_features)
from upg.simulate import SimConfig, dimension_base, simulate_population


@pytest.fixture(scope="module")
def tiny_sets():
    train = build_training_set("clinical_realistic", n_persons=12, seed=1234,
                               T_grid=(30, 60))
    val = build_training_set("clinical_realistic", n_persons=6, seed=5678,
                             T_grid=(30, 60))
    return train, val


def test_features_shapes_and_finiteness():
    base_B, _g, dims, _k = dimension_base()
    config = SimConfig(T=40, sampling_rate=0.6, dropout_prob=0.5, seed=9)
    ds = simulate_population(3, config=config, pop_seed=9)
    for r in ds.records:
        node, edge, glob = person_features(r.observations, r.u,
                                           r.params.kappa, base_B)
        assert node.shape == (len(dims), 6)
        assert edge.shape == (int((base_B != 0).sum()), 5)
        assert glob.shape == (6,)
        assert np.all(np.isfinite(node))
        assert np.all(np.isfinite(edge))
        assert np.all(np.isfinite(glob))


def test_zero_init_returns_prior_exactly():
    """LoRA-style zero-init (rule W7 as architecture): before training the
    estimator's point estimate IS the consensus prior, for any input."""
    model = MaskedGraphAttentionEstimator(GATConfig(seed=3))
    config = SimConfig(T=50, seed=4)
    ds = simulate_population(2, config=config, pop_seed=4)
    r = ds.records[0]
    gp = model.estimate(r.observations, r.u, r.params.kappa)
    assert np.allclose(gp.B_hat, model.B0, atol=1e-12)
    assert np.allclose(gp.g_hat, model.g0, atol=1e-12)
    # intervals: prior-centred with the configured initial width
    sup = model.B0 != 0.0
    assert np.all(gp.B_lo[sup] < gp.B_hat[sup])
    assert np.all(gp.B_hi[sup] > gp.B_hat[sup])


def test_support_and_sign_inherited():
    """B_hat is exactly zero off the published skeleton and keeps the
    skeleton's signs — the architectural W1 guarantee."""
    model = MaskedGraphAttentionEstimator(GATConfig(seed=0))
    for k in model.params:                       # scramble all weights
        model.params[k].data += np.random.default_rng(1).normal(
            0.0, 0.3, model.params[k].data.shape)
    config = SimConfig(T=60, seed=5)
    ds = simulate_population(2, config=config, pop_seed=5)
    r = ds.records[1]
    gp = model.estimate(r.observations, r.u, r.params.kappa)
    sup = model.B0 != 0.0
    assert np.all(gp.B_hat[~sup] == 0.0)
    assert np.all(gp.B_hat[sup] > 0.0)           # problem-frame prior is positive
    assert np.all(gp.g_hat * model.g0 >= 0.0)    # gain signs preserved
    assert np.all(gp.b_hat >= 0.0)               # standing conditions nonneg
    # b support = the generative family's TEM/DEV/SYS only, exact zeros off it
    assert np.all(gp.b_hat[model.b_mask == 0.0] == 0.0)


def test_training_never_ends_worse_than_prior(tiny_sets):
    """fit() seeds early stopping with the init (= prior) state, so the
    returned model is never worse than the prior on validation."""
    train, val = tiny_sets
    cfg = GATConfig(seed=0, epochs=120, patience=120, lr=5e-3)
    model = MaskedGraphAttentionEstimator(cfg)
    model._fit_standardizer([e[0] for e in train])
    batch = model._make_batch(val)
    loss0 = float(model._loss(batch).data)       # loss at the prior (zero-init)
    out = model.fit(train, val, verbose=False)
    loss1 = float(model._loss(batch).data)
    assert loss1 <= loss0 + 1e-9
    assert out["best_val"] <= out["history"][0]["val"] + 1e-9


def test_determinism_same_seed(tiny_sets):
    train, val = tiny_sets
    cfg = GATConfig(seed=7, epochs=10, patience=10)
    m1 = MaskedGraphAttentionEstimator(cfg)
    m1.fit(train, val, verbose=False)
    m2 = MaskedGraphAttentionEstimator(cfg)
    m2.fit(train, val, verbose=False)
    for k in m1.params:
        assert np.array_equal(m1.params[k].data, m2.params[k].data)


def test_save_load_roundtrip(tmp_path, tiny_sets):
    train, val = tiny_sets
    cfg = GATConfig(seed=2, epochs=5, patience=5)
    model = MaskedGraphAttentionEstimator(cfg)
    model.fit(train, val, verbose=False)
    path = str(tmp_path / "gat.npz")
    model.save(path)
    loaded = MaskedGraphAttentionEstimator.load(path)
    config = SimConfig(T=45, seed=11)
    ds = simulate_population(2, config=config, pop_seed=11)
    r = ds.records[0]
    a = model.estimate(r.observations, r.u, r.params.kappa)
    b = loaded.estimate(r.observations, r.u, r.params.kappa)
    assert np.allclose(a.B_hat, b.B_hat, atol=1e-12)
    assert np.allclose(a.B_sd, b.B_sd, atol=1e-12)


def test_dataset_runner_reports_contract_metrics(tiny_sets):
    train, val = tiny_sets
    cfg = GATConfig(seed=1, epochs=30, patience=30)
    model = MaskedGraphAttentionEstimator(cfg)
    model.fit(train, val, verbose=False)
    config = SimConfig(T=60, seed=21)
    ds = simulate_population(5, config=config, pop_seed=21)
    out = gat_recover_dataset(ds, model)
    agg = out["aggregate"]
    for key in ("median_edge_rmse", "median_edge_dev_corr", "regime_accuracy",
                "mean_coverage", "median_ci_width", "median_rho_abs_err"):
        assert np.isfinite(agg[key])
    assert 0.0 <= agg["mean_coverage"] <= 1.0


def test_deviation_rank_spectrum(tiny_sets):
    train, _ = tiny_sets
    spec = deviation_rank_spectrum(train)
    base_B = dimension_base()[0]
    E = int((base_B != 0).sum())
    assert spec["n_edges"] == E
    assert 1.0 <= spec["effective_rank"] <= E
    assert len(spec["singular_values"]) == min(spec["n_examples"], E)


def test_edge_list_matches_support():
    base_B = dimension_base()[0]
    tgt, src = edge_list(base_B)
    assert len(tgt) == int((base_B != 0).sum())
    assert np.all(base_B[tgt, src] != 0.0)
