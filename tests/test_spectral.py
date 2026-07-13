"""Spectral anatomy of the dimension graph (Batch J Section 6)."""
from upg import dimension_spectral_report

EXPECTED_EIGENVALUES = [0.0, 1.568, 1.929, 2.436, 2.510, 2.930, 3.189, 3.562]


def test_algebraic_connectivity():
    sp = dimension_spectral_report()
    assert abs(sp.algebraic_connectivity - 1.568) < 1e-3


def test_full_laplacian_spectrum():
    sp = dimension_spectral_report()
    for got, exp in zip(sp.eigenvalues, EXPECTED_EIGENVALUES):
        assert abs(got - exp) < 1e-3, (got, exp)


def test_personality_is_the_bridge():
    sp = dimension_spectral_report()
    node, mag = sp.bridge_ranking[0]
    assert node == "PER"
    assert abs(mag - 0.015) < 1e-3


def test_two_shores_partition():
    sp = dimension_spectral_report()
    dispositional = {"TEM", "DEV", "PER"}
    transactional = {"NEED", "ME", "DIS", "THER", "SYS"}
    assert set(sp.partition[0]) | set(sp.partition[1]) == dispositional | transactional
    assert {frozenset(sp.partition[0]), frozenset(sp.partition[1])} == \
        {frozenset(dispositional), frozenset(transactional)}


def test_disorder_has_max_centrality():
    sp = dimension_spectral_report()
    top = max(sp.centrality.items(), key=lambda t: t[1])
    assert top[0] == "DIS"
    assert abs(top[1] - 1.0) < 1e-9
