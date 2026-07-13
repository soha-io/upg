"""Registry integrity: the vendored source registries load and are well-formed."""
from upg.io import load_dimension_edge_rows, load_dimension_node_rows, load_stratum_rows
from upg.registry import STRATA

RAW_NODE_COUNTS = {
    "DIS": 18, "THER": 38, "DEV": 21, "PER": 54,
    "TEM": 30, "NEED": 33, "ME": 28, "SYS": 30,
}
RAW_EDGE_COUNTS = {
    "DIS": 32, "THER": 30, "DEV": 31, "PER": 64,
    "TEM": 47, "NEED": 57, "ME": 60, "SYS": 60,
}


def test_all_strata_present():
    assert set(STRATA) == set(RAW_NODE_COUNTS)


def test_raw_node_and_edge_counts():
    for pref in STRATA:
        nodes, edges = load_stratum_rows(pref)
        assert len(nodes) == RAW_NODE_COUNTS[pref], pref
        assert len(edges) == RAW_EDGE_COUNTS[pref], pref


def test_no_duplicate_node_ids_within_stratum():
    for pref in STRATA:
        nodes, _ = load_stratum_rows(pref)
        ids = [r["node_id"] for r in nodes]
        assert len(ids) == len(set(ids)), pref


def test_edges_have_valid_sign_and_weight():
    for pref in STRATA:
        _, edges = load_stratum_rows(pref)
        for e in edges:
            assert e["sign"] in ("+", "-"), (pref, e)
            # magnitude must lie in [0, 1]; a couple of Batch B rows encode
            # the sign in the weight column too (weight="-0.50", sign="-"),
            # which is why we check the absolute value here.
            assert 0.0 <= abs(float(e["weight"])) <= 1.0, (pref, e)


def test_weight_column_sign_is_self_consistent():
    """Where the weight column carries a negative magnitude, the sign column
    must agree (no weight<0 paired with sign '+')."""
    for pref in STRATA:
        _, edges = load_stratum_rows(pref)
        for e in edges:
            if float(e["weight"]) < 0:
                assert e["sign"] == "-", (pref, e)


def test_dimension_registry_shape():
    nodes = load_dimension_node_rows()
    edges = load_dimension_edge_rows()
    assert len(nodes) == 8
    self_loops = [r for r in edges if r["source"] == r["target"]]
    negative = [r for r in edges if r["sign"] == "-"]
    assert len(edges) == 41                 # 34 inter-dimension + 7 self-loops
    assert len(self_loops) == 7
    assert len(negative) == 5
