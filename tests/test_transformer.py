"""Step 6: the causal temporal transformer (measurement model + forecaster)."""
import numpy as np
import pytest

from upg.simulate import simulate_preset
from upg.transformer import (ForecastConfig, TemporalTransformer,
                             alibi_biases, auc_score, causal_mask,
                             evaluate_model, make_batches)


@pytest.fixture(scope="module")
def tiny():
    ds = simulate_preset("clinical_realistic", n_persons=8, T=40, seed=3)
    cfg = ForecastConfig(epochs=6, patience=6, batch_size=4, seed=0)
    model = TemporalTransformer(cfg)
    batch = make_batches(ds, cfg.horizon)
    return ds, cfg, model, batch


def test_batch_shapes(tiny):
    ds, cfg, _m, b = tiny
    P, T, n = 8, 40, 7
    assert b["y0"].shape == (P, T, n)
    assert b["x_future"].shape == (P, T, cfg.horizon, n)
    assert b["valid"].shape == (P, T, cfg.horizon)
    # validity mask: horizon h valid only while t + h < T
    assert b["valid"][:, T - 1, :].sum() == 0
    assert b["valid"][:, 0, :].sum() == cfg.horizon * P
    assert np.all(np.isfinite(b["y0"]))


def test_alibi_and_mask():
    bias = alibi_biases(4, 10)
    assert bias.shape == (4, 10, 10)
    # penalty grows with distance; head 0 is steepest, head H-1 shallowest
    assert bias[0, 5, 4] > bias[0, 5, 1]
    assert bias[0, 5, 1] < bias[3, 5, 1]
    assert abs(bias[0, 5, 1]) > 10 * abs(bias[3, 5, 1])
    m = causal_mask(6)
    assert np.all(np.triu(m, 1) == 0)
    assert np.all(np.diag(m) == 1)


def test_causality_no_future_observation_leak(tiny):
    """Filter and forecast outputs at time t must be invariant to
    observations after t (planned treatment is known-future by design)."""
    _ds, cfg, _model, b = tiny
    model = TemporalTransformer(cfg)
    rng = np.random.default_rng(7)               # non-degenerate heads
    for k in model.params:
        model.params[k].data += rng.normal(0.0, 0.05,
                                           model.params[k].data.shape)
    t0 = 20
    (rec, _sd), (fmu, _fsd), _dyn = model.forward(b)[0]
    b2 = {k: v.copy() for k, v in b.items()}
    b2["y0"][:, t0:, :] += 5.0            # corrupt future observations
    b2["msk"][:, t0:, :] = 1.0
    (rec2, _), (fmu2, _), _ = model.forward(b2)[0]
    assert np.allclose(rec.data[:, :t0], rec2.data[:, :t0], atol=1e-10)
    assert np.allclose(fmu.data[:, :t0], fmu2.data[:, :t0], atol=1e-10)
    # sanity: later outputs DO change
    assert not np.allclose(rec.data[:, t0:], rec2.data[:, t0:], atol=1e-6)


def test_fit_never_worse_than_init_and_deterministic(tiny):
    ds, cfg, _m, b = tiny
    m1 = TemporalTransformer(cfg)
    init_val = m1._eval_loss(b)
    out1 = m1.fit(b, b, verbose=False)
    assert out1["best_val"] <= init_val + 1e-9
    m2 = TemporalTransformer(cfg)
    m2.fit(b, b, verbose=False)
    for k in m1.params:
        assert np.array_equal(m1.params[k].data, m2.params[k].data)


def test_save_load_roundtrip(tmp_path, tiny):
    _ds, cfg, model, b = tiny
    model.fit(b, b, verbose=False)
    p = str(tmp_path / "tf.npz")
    model.save(p)
    loaded = TemporalTransformer.load(p)
    (rec, _), _, _ = model.forward(b)[0]
    (rec2, _), _, _ = loaded.forward(b)[0]
    assert np.allclose(rec.data, rec2.data, atol=1e-12)


def test_evaluate_model_metrics(tiny):
    _ds, _cfg, model, b = tiny
    ev = evaluate_model(model, b)
    assert np.isfinite(ev["filter_rmse"])
    assert 0.0 <= ev["filter_coverage"] <= 1.0
    for h, d in ev["forecast_by_horizon"].items():
        assert np.isfinite(d["rmse"]) and 0.0 <= d["coverage"] <= 1.0
        assert np.isfinite(ev["persistence_rmse_by_horizon"][h])
    assert 0.0 <= ev["regime_accuracy"] <= 1.0
    assert len(ev["rank_residual_by_layer"]) == model.config.n_layers
    # rank residual must be well away from collapse (note 37)
    assert min(ev["rank_residual_by_layer"]) > 1e-3


def test_uniform_attention_null_differs_after_training(tiny):
    _ds, _cfg, model, b = tiny
    model.fit(b, b, verbose=False)
    ev = evaluate_model(model, b)
    ev0 = evaluate_model(model, b, uniform_attention=True)
    assert ev["forecast_by_horizon"][1]["rmse"] != \
        ev0["forecast_by_horizon"][1]["rmse"]


def test_channel_independent_null_shapes():
    ds = simulate_preset("clinical_realistic", n_persons=4, T=30, seed=5)
    cfg = ForecastConfig(epochs=2, patience=2, batch_size=8, seed=1,
                         channel_independent=True)
    m = TemporalTransformer(cfg)
    b = make_batches(ds, cfg.horizon, channel_independent=True)
    assert b["y0"].shape == (4 * 7, 30, 1)
    out = m.fit(b, b, verbose=False)
    assert np.isfinite(out["best_val"])
    ev = evaluate_model(m, b)
    assert "relapse_auc" not in ev["early_warning"]   # person-level only


def test_auc_score():
    labels = np.array([1, 1, 0, 0, 0])
    assert auc_score(labels, np.array([0.9, 0.8, 0.3, 0.2, 0.1])) == 1.0
    assert auc_score(labels, np.array([0.1, 0.2, 0.8, 0.9, 0.7])) == 0.0
    assert abs(auc_score(labels, np.ones(5)) - 0.5) < 1e-12
    assert np.isnan(auc_score(np.zeros(3), np.array([0.1, 0.2, 0.3])))
