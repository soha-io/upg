"""Gradcheck for every autodiff op (requirement 21: every hand-derived
gradient verified against central finite differences)."""
import numpy as np

from upg.autodiff import (Adam, Tensor, concat, gradcheck, rms_norm,
                          softmax_masked)

RNG = np.random.default_rng(0)


def _t(*shape):
    return Tensor(RNG.normal(0.0, 0.7, size=shape), requires_grad=True)


def test_add_mul_sub_div_pow():
    a, b = _t(3, 4), _t(3, 4)
    gradcheck(lambda a, b: ((a * b + a - b) / (b * b + 3.0)).sum(), [a, b])
    c = _t(2, 3)
    gradcheck(lambda c: (c.pow(3.0) + c.pow(-2.0)).sum(), [c])


def test_broadcasting_grads():
    a, b = _t(4, 5), _t(5)
    b2 = Tensor(b.data.reshape(1, 5), requires_grad=True)
    gradcheck(lambda a, b2: (a * b2 + b2).sum(), [a, b2])
    row = _t(4, 1)
    gradcheck(lambda a, row: (a + row).sum(), [a, row])


def test_matmul_plain_and_batched():
    a, b = _t(3, 4), _t(4, 2)
    gradcheck(lambda a, b: (a @ b).sum(), [a, b])
    # batched left operand, shared right operand (the model's main pattern)
    ab, w = _t(2, 3, 4), _t(4, 2)
    gradcheck(lambda ab, w: (ab @ w).tanh().sum(), [ab, w])
    # fully batched
    x, y = _t(2, 3, 4), _t(2, 4, 3)
    gradcheck(lambda x, y: (x @ y).sum(), [x, y])


def test_nonlinearities():
    x = _t(3, 3)
    for fn in ("exp", "tanh", "sigmoid", "silu", "softplus"):
        gradcheck(lambda x, fn=fn: getattr(x, fn)().sum(), [x])
    gradcheck(lambda x: x.leaky_relu(0.2).sum(), [x])
    y = Tensor(np.abs(RNG.normal(1.0, 0.2, (3, 3))), requires_grad=True)
    gradcheck(lambda y: y.log().sum(), [y])


def test_reductions_reshape_indexing():
    x = _t(3, 4, 2)
    gradcheck(lambda x: x.sum(axis=1).tanh().sum(), [x])
    gradcheck(lambda x: x.mean(axis=(0)).sum(), [x])
    gradcheck(lambda x: x.reshape(3, 8).tanh().sum(), [x])
    gradcheck(lambda x: x.transpose((1, 0, 2)).tanh().sum(), [x])
    idx = np.array([0, 2, 2])          # repeated index: grads must accumulate
    gradcheck(lambda x: x[:, idx, :].tanh().sum(), [x])


def test_concat_and_softmax_and_rmsnorm():
    a, b = _t(2, 3), _t(2, 5)
    gradcheck(lambda a, b: concat([a, b], axis=-1).tanh().sum(), [a, b])

    logits = _t(2, 4)
    mask = np.array([[1, 1, 0, 1], [1, 0, 1, 1]], dtype=float)
    gradcheck(lambda l: (softmax_masked(l, mask) * 3.0).pow(2.0).sum(),
              [logits])
    # masked positions get (near) zero weight
    w = softmax_masked(logits, mask).data
    assert np.all(w[mask == 0] < 1e-9)
    assert np.allclose(w.sum(axis=-1), 1.0, atol=1e-9)

    x, gamma = _t(2, 6), _t(6)
    g2 = Tensor(gamma.data.reshape(1, 6), requires_grad=True)
    gradcheck(lambda x, g2: rms_norm(x, g2).tanh().sum(), [x, g2])


def test_composite_mini_model():
    """A two-layer masked-attention block end to end."""
    x = _t(2, 5, 4)                       # (batch, tokens, d)
    Wq, Wk, Wv = _t(4, 4), _t(4, 4), _t(4, 3)
    mask = (RNG.random((5, 5)) > 0.3).astype(float)
    np.fill_diagonal(mask, 1.0)

    def model(x, Wq, Wk, Wv):
        q, k, v = x @ Wq, x @ Wk, x @ Wv
        logits = (q @ k.transpose((0, 2, 1))) * (1.0 / 2.0)
        att = softmax_masked(logits, mask)
        return (att @ v).tanh().sum()

    gradcheck(model, [x, Wq, Wk, Wv], tol=5e-4)


def test_adam_decreases_quadratic():
    p = Tensor(np.array([[5.0, -3.0]]), requires_grad=True)
    opt = Adam([p], lr=0.2)
    for _ in range(200):
        opt.zero_grad()
        loss = (p * p).sum()
        loss.backward()
        opt.step()
    assert np.all(np.abs(p.data) < 1e-2)


def test_determinism():
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)
    a1 = Tensor(rng1.normal(size=(3, 3)), requires_grad=True)
    a2 = Tensor(rng2.normal(size=(3, 3)), requires_grad=True)
    (a1.tanh().sum()).backward()
    (a2.tanh().sum()).backward()
    assert np.array_equal(a1.grad, a2.grad)
