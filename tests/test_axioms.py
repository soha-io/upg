"""The five axioms are computable properties of the composed object (Batch J 4.4)."""
from upg import axiom_audit, build_person_graph


def _report():
    return axiom_audit(build_person_graph())


def test_axiom1_weakly_connected():
    r = _report()
    assert r.weakly_connected is True
    assert r.component_size == r.n_nodes == 253


def test_axiom2_no_isolated_nodes():
    assert _report().isolated_nodes == 0


def test_axiom3_full_reachability():
    assert abs(_report().reachability_fill - 1.0) < 1e-9


def test_axiom4_self_loops():
    assert _report().self_loops == 20


def test_axiom5_signed_superposition():
    assert _report().negative_edges == 33
