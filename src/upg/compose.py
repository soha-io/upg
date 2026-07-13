"""
Composition of the eight strata into the Great Graph.

This is a faithful port of Batch J's ``compose_greatgraph.py``: it produces
the same 253 nodes and 522 edges, in the same order, but returns a typed
:class:`~upg.schema.PersonGraph` instead of writing CSVs.  The ordering of
strata (from :data:`upg.registry.STRATA`), of nodes within a stratum (CSV
order), and of the five edge-construction passes is preserved exactly, so
every order-dependent statistic downstream reproduces the published numbers.

Encapsulation rule (project spec J.4): a stratum's internal nodes never
connect directly to another stratum's internal nodes.  Every cross-stratum
edge touches a mother or interface node.  :func:`encapsulation_violations`
audits this and returns the offending edges (empty list == pass).
"""
from __future__ import annotations

from .io import load_dimension_edge_rows, load_stratum_rows
from .registry import (BIND_W, BINDINGS, INTERFACE_EXCEPTIONS, MOTHER_PAIRS,
                       STRATA)
from .schema import Edge, Node, PersonGraph


def _local(node_id: str) -> str:
    """The part after the stratum prefix, e.g. 'DIS.P' -> 'P'."""
    return node_id.split(".", 1)[1]


def build_person_graph() -> PersonGraph:
    """Compose the eight strata into the full-resolution Great Graph."""
    node_rows: list[dict] = []
    edge_rows: list[dict] = []
    mother: dict[str, str] = {}

    # ---- 1. namespace every stratum's nodes and edges -------------------
    for pref, (stem, letter, mother_id) in STRATA.items():
        nrows, erows = load_stratum_rows(pref)
        for r in nrows:
            node_rows.append({
                "node_id": f"{pref}.{r['node_id']}",
                "stratum": pref,
                "label": r.get("label", ""),
                "level": r.get("level", ""),
                "parent": f"{pref}.{r['parent']}" if r.get("parent") else "",
                "role": "internal",
            })
        for r in erows:
            edge_rows.append({
                "source": f"{pref}.{r['source']}",
                "target": f"{pref}.{r['target']}",
                # magnitude only: a couple of source rows double-encode the
                # sign in the weight column (weight="-0.50", sign="-"); abs()
                # normalizes to the project's convention (magnitude + sign).
                "weight": abs(float(r["weight"])),
                "sign": r["sign"],
                "type": r["type"],
                "gate": (r.get("gate", "none") or "none"),
                "origin": f"Batch {letter}",
            })
        if mother_id:
            mother[pref] = f"{pref}.{mother_id}"

    # ---- 2. synthesize the THER mother over workflow phases N01-N11 -----
    mother["THER"] = "THER.THER"
    node_rows.append({
        "node_id": "THER.THER", "stratum": "THER",
        "label": "Universal therapy workflow (mother node, synthesized at composition)",
        "level": "-1", "parent": "", "role": "mother",
    })
    for i in range(1, 12):
        edge_rows.append({
            "source": "THER.THER", "target": f"THER.N{i:02d}",
            "weight": 0.85, "sign": "+", "type": "hierarchical",
            "gate": "none", "origin": "Batch J (composition)",
        })

    # ---- 3. mark mother / interface roles -------------------------------
    mother_ids = set(mother.values())
    for nr in node_rows:
        if nr["node_id"] in mother_ids:
            nr["role"] = "mother"
        elif _local(nr["node_id"]).endswith("_IF") or \
                _local(nr["node_id"]) in INTERFACE_EXCEPTIONS:
            nr["role"] = "interface"

    # ---- 4. implicit hierarchical edges from the parent field -----------
    have = {(e["source"], e["target"]) for e in edge_rows}
    for nr in node_rows:
        p, c = nr["parent"], nr["node_id"]
        if p and (p, c) not in have and (c, p) not in have:
            edge_rows.append({
                "source": p, "target": c, "weight": 0.80, "sign": "+",
                "type": "hierarchical-implicit", "gate": "none",
                "origin": "Batch J (parent field)",
            })

    # ---- 5. interface-binding edges -------------------------------------
    for strat, iface, partner, direction in BINDINGS:
        a, b = f"{strat}.{iface}", mother[partner]
        if direction in ("out", "both"):
            edge_rows.append({"source": a, "target": b, "weight": BIND_W,
                              "sign": "+", "type": "binding", "gate": "none",
                              "origin": "Batch J (composition)"})
        if direction in ("in", "both"):
            edge_rows.append({"source": b, "target": a, "weight": BIND_W,
                              "sign": "+", "type": "binding", "gate": "none",
                              "origin": "Batch J (composition)"})

    # ---- 6. mother-to-mother stitches for interface-less couplings ------
    for r in load_dimension_edge_rows():
        if (r["source"], r["target"]) in MOTHER_PAIRS and r["source"] != r["target"]:
            edge_rows.append({
                "source": mother[r["source"]], "target": mother[r["target"]],
                "weight": abs(float(r["weight"])), "sign": r["sign"],
                "type": f"interstratum-{r['type']}", "gate": r["gate"],
                "origin": "Batch J (dimension edge)",
            })

    nodes = [Node(**nr) for nr in node_rows]
    edges = [Edge(**er) for er in edge_rows]
    return PersonGraph(nodes=nodes, edges=edges)


def encapsulation_violations(pg: PersonGraph) -> list[tuple[str, str]]:
    """Cross-stratum edges that touch neither a mother nor an interface node."""
    role = pg.role_of()
    strat = pg.stratum_of()
    bad: list[tuple[str, str]] = []
    for e in pg.edges:
        if strat[e.source] != strat[e.target]:
            ok = role[e.source] in ("mother", "interface") or \
                 role[e.target] in ("mother", "interface")
            if not ok:
                bad.append((e.source, e.target))
    return bad
