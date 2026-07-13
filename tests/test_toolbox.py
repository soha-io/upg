"""Batch I worked examples: every printed number reproduced (Batch I Section 5)."""
import numpy as np

from upg.dynamics import iterate, spectral_radius
from upg.learning import beta_update, td_update
from upg.spectral import laplacian_spectrum, normalized_laplacian


def test_ex1_signed_superposition():
    W = np.array([[0.0, 0.6, -0.4],
                  [0.5, 0.0, -0.3],
                  [-0.2, -0.1, 0.0]])
    x = np.array([0.8, 0.6, 0.3])
    drive = W @ x
    assert np.allclose(drive, [0.24, 0.31, -0.22], atol=1e-9)
    assert abs(W[0, 1] * x[1] - 0.36) < 1e-9      # insomnia -> rumination
    assert abs(W[0, 2] * x[2] + 0.12) < 1e-9      # protective social contact


def _six_node_graph():
    A = np.zeros((6, 6))
    edges = {(0, 1): 0.9, (0, 2): 0.8, (1, 2): 0.7,
             (3, 4): 0.9, (4, 5): 0.8, (3, 5): 0.7,
             (2, 3): 0.2}
    for (i, j), w in edges.items():
        A[i, j] = w
        A[j, i] = w
    return A


def test_ex2_fiedler_partition_and_bridges():
    A = _six_node_graph()
    lam, V = laplacian_spectrum(A)
    assert abs(lam[0]) < 1e-9
    assert abs(lam[1] - 0.119) < 1e-3
    expected = [0.0, 0.119, 2.227, 2.372, 2.573, 2.709]
    for got, exp in zip(lam, expected):
        assert abs(got - exp) < 1e-3, (got, exp)
    v2 = V[:, 1]
    if v2[0] > 0:
        v2 = -v2
    signs = np.sign(v2).astype(int)
    assert list(signs) == [-1, -1, -1, 1, 1, 1]
    # the two smallest |v2| entries are the bridge nodes 2 and 3
    two_smallest = set(np.argsort(np.abs(v2))[:2].tolist())
    assert two_smallest == {2, 3}


def test_ex2_normalized_laplacian_runs():
    A = _six_node_graph()
    ev = np.linalg.eigvalsh(normalized_laplacian(A))
    assert abs(ev[0]) < 1e-9 and ev[1] > 0


def test_ex3b_unstable_loop_bounded_by_tanh():
    B2 = np.array([[0.7, 0.6], [0.7, 0.5]])
    assert spectral_radius(B2) > 1.0                # runs away when linear
    x = iterate(B2, np.zeros(2), np.zeros(2), u=0.0,
                x0=np.array([0.05, 0.05]), kappa=1.0)
    assert np.all(np.abs(x) <= 1.0) and np.any(np.abs(x) > 0.1)  # bounded, nonzero


def test_ex4_bayesian_behavioural_experiment():
    bu = beta_update(8, 2, successes=0, failures=20)
    assert (bu.a1, bu.b1) == (8, 22)
    assert abs(bu.prior_mean - 0.80) < 1e-9
    assert abs(bu.posterior_mean - 0.267) < 1e-3
    assert abs(bu.shift - 0.533) < 1e-3


def test_ex5_td_extinction_trajectory():
    vals = td_update(-0.8, 0.0, alpha=0.3, gamma=0.9, trials=6)
    assert abs(vals[0] - (-0.56)) < 1e-3
    assert abs(vals[-1] - (-0.0941)) < 1e-3
    # avoidance (never sampled) would leave the value pinned at -0.8
    assert all(v > -0.8 for v in vals)
