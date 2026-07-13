"""Composition census + encapsulation: the Great Graph is built exactly."""
from upg import build_person_graph, encapsulation_violations
from upg.registry import PUBLISHED


def test_node_and_edge_counts():
    pg = build_person_graph()
    assert pg.n == PUBLISHED["greatgraph_nodes"] == 253
    assert len(pg.edges) == PUBLISHED["greatgraph_edges"] == 522


def test_cross_stratum_self_and_negative_counts():
    pg = build_person_graph()
    assert len(pg.cross_stratum_edges()) == PUBLISHED["cross_stratum_edges"] == 35
    assert len(pg.self_loops()) == PUBLISHED["self_loops"] == 20
    assert len(pg.negative_edges()) == PUBLISHED["negative_edges"] == 33


def test_nodes_per_stratum():
    pg = build_person_graph()
    assert pg.nodes_per_stratum() == PUBLISHED["nodes_per_stratum"]


def test_encapsulation_zero_violations():
    pg = build_person_graph()
    assert encapsulation_violations(pg) == []


def test_ther_mother_synthesized():
    pg = build_person_graph()
    roles = pg.role_of()
    assert roles["THER.THER"] == "mother"
    # THER mother has exactly 11 hierarchical children (workflow phases N01-N11)
    kids = [e for e in pg.edges
            if e.source == "THER.THER" and e.type == "hierarchical"]
    assert len(kids) == 11


def test_weights_normalized_to_magnitude_and_sign():
    pg = build_person_graph()
    for e in pg.edges:
        assert e.weight >= 0.0, e                       # magnitude only
        if e.sign == "-":
            assert e.signed_weight < 0.0, e             # sign carried correctly
        else:
            assert e.signed_weight >= 0.0, e


def test_mother_nodes_have_role():
    pg = build_person_graph()
    roles = pg.role_of()
    for mid in ("DIS.P", "PER.P", "TEM.T", "NEED.N", "ME.ME", "SYS.SYS",
                "DEV.D", "THER.THER"):
        assert roles[mid] == "mother", mid
