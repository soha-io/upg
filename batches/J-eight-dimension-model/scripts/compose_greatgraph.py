#!/usr/bin/env python3
"""Compose and verify the Great Graph from canonical public registries.

The safe default is ``--check``: compose entirely in memory, enforce the
published census/encapsulation invariants, and require byte parity with both
canonical and Batch-J mirrors. ``--write`` is explicit and occurs only after
all invariants pass.
"""
from __future__ import annotations

import argparse
import csv
import io
import os
from pathlib import Path
import tempfile


REPO = Path(__file__).resolve().parents[3]
PACKAGE_DATA = REPO / "src" / "upg" / "data"
REGISTRIES = REPO / "registries"
J_DATA = Path(__file__).resolve().parents[1] / "data"

STRATA = {
    "DIS":  ("udg",    "P", "A"),
    "THER": ("utg",    None, "B"),
    "DEV":  ("udevg",  "D", "C"),
    "PER":  ("uperg",  "P", "D"),
    "TEM":  ("utempg", "T", "E"),
    "NEED": ("uneedg", "N", "F"),
    "ME":   ("umeg",   "ME", "G"),
    "SYS":  ("usysg",  "SYS", "H"),
}

BINDINGS = [
    ("TEM", "PERS_IF", "PER", "out"),
    ("TEM", "OUT_ADJ", "DIS", "out"),
    ("NEED", "MOT_IF", "ME", "out"),
    ("NEED", "PERS_IF", "PER", "in"),
    ("ME", "NEEDS_IF", "NEED", "in"),
    ("ME", "SYS_IF", "SYS", "both"),
    ("ME", "PERS_IF", "PER", "in"),
    ("ME", "TEMP_IF", "TEM", "in"),
    ("ME", "DIS_IF", "DIS", "out"),
    ("ME", "THER_IF", "THER", "in"),
    ("SYS", "PERSON_IF", "PER", "out"),
    ("SYS", "NEEDS_IF", "NEED", "out"),
    ("SYS", "ME_IF", "ME", "out"),
    ("SYS", "DEV_IF", "DEV", "out"),
    ("SYS", "DIS_IF", "DIS", "out"),
    ("SYS", "THER_IF", "THER", "in"),
]
BIND_W = 0.90
MOTHER_PAIRS = {
    ("TEM", "DEV"), ("DEV", "TEM"), ("DEV", "PER"), ("DEV", "NEED"),
    ("DEV", "ME"), ("DEV", "DIS"), ("PER", "DIS"), ("PER", "SYS"),
    ("SYS", "PER"), ("ME", "NEED"), ("DIS", "THER"), ("THER", "DIS"),
    ("THER", "TEM"), ("THER", "PER"), ("THER", "NEED"), ("DIS", "NEED"),
    ("DIS", "SYS"), ("NEED", "DIS"),
}
EXPECTED = {
    "nodes": 253,
    "edges": 522,
    "cross_stratum": 35,
    "self_loops": 20,
    "negative_edges": 33,
    "encapsulation_violations": 0,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def compose() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    nodes: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []
    mother: dict[str, str] = {}
    for prefix, (stem, mother_id, batch) in STRATA.items():
        for row in read_csv(PACKAGE_DATA / f"{stem}_nodes.csv"):
            nodes.append({
                "node_id": f"{prefix}.{row['node_id']}",
                "stratum": prefix,
                "label": row.get("label", ""),
                "level": row.get("level", ""),
                "parent": f"{prefix}.{row['parent']}" if row.get("parent") else "",
                "role": "internal",
            })
        for row in read_csv(PACKAGE_DATA / f"{stem}_edges.csv"):
            edges.append({
                "source": f"{prefix}.{row['source']}",
                "target": f"{prefix}.{row['target']}",
                "weight": row["weight"],
                "sign": row["sign"],
                "type": row["type"],
                "gate": row.get("gate", "none") or "none",
                "origin": f"Batch {batch}",
            })
        if mother_id:
            mother[prefix] = f"{prefix}.{mother_id}"

    mother["THER"] = "THER.THER"
    nodes.append({
        "node_id": "THER.THER",
        "stratum": "THER",
        "label": "Universal therapy workflow (mother node, synthesized at composition)",
        "level": "-1",
        "parent": "",
        "role": "mother",
    })
    for index in range(1, 12):
        edges.append({
            "source": "THER.THER", "target": f"THER.N{index:02d}",
            "weight": "0.85", "sign": "+", "type": "hierarchical",
            "gate": "none", "origin": "Batch J (composition)",
        })

    for node in nodes:
        if node["node_id"] in mother.values():
            node["role"] = "mother"
        else:
            local = node["node_id"].split(".", 1)[1]
            if local.endswith("_IF") or local in ("OUT_ADJ", "PERSON_IF"):
                node["role"] = "interface"

    existing = {(edge["source"], edge["target"]) for edge in edges}
    for node in nodes:
        parent, child = node["parent"], node["node_id"]
        if parent and (parent, child) not in existing and (child, parent) not in existing:
            edges.append({
                "source": parent, "target": child, "weight": "0.80", "sign": "+",
                "type": "hierarchical-implicit", "gate": "none",
                "origin": "Batch J (parent field)",
            })

    for stratum, interface, partner, direction in BINDINGS:
        source, target = f"{stratum}.{interface}", mother[partner]
        if direction in ("out", "both"):
            edges.append({
                "source": source, "target": target, "weight": str(BIND_W),
                "sign": "+", "type": "binding", "gate": "none",
                "origin": "Batch J (composition)",
            })
        if direction in ("in", "both"):
            edges.append({
                "source": target, "target": source, "weight": str(BIND_W),
                "sign": "+", "type": "binding", "gate": "none",
                "origin": "Batch J (composition)",
            })

    for row in read_csv(REGISTRIES / "upg_dimension_edges.csv"):
        pair = (row["source"], row["target"])
        if pair in MOTHER_PAIRS and row["source"] != row["target"]:
            edges.append({
                "source": mother[row["source"]], "target": mother[row["target"]],
                "weight": row["weight"], "sign": row["sign"],
                "type": f"interstratum-{row['type']}", "gate": row["gate"],
                "origin": "Batch J (dimension edge)",
            })
    return nodes, edges


def validate(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> dict[str, int]:
    node_ids = [node["node_id"] for node in nodes]
    if len(node_ids) != len(set(node_ids)):
        raise ValueError("duplicate node IDs in composed graph")
    known = set(node_ids)
    dangling = [(edge["source"], edge["target"]) for edge in edges
                if edge["source"] not in known or edge["target"] not in known]
    if dangling:
        raise ValueError(f"dangling composed edges: {dangling[:5]}")
    roles = {node["node_id"]: node["role"] for node in nodes}
    strata = {node["node_id"]: node["stratum"] for node in nodes}
    cross = [edge for edge in edges if strata[edge["source"]] != strata[edge["target"]]]
    violations = [
        (edge["source"], edge["target"]) for edge in cross
        if roles[edge["source"]] not in ("mother", "interface")
        and roles[edge["target"]] not in ("mother", "interface")
    ]
    actual = {
        "nodes": len(nodes),
        "edges": len(edges),
        "cross_stratum": len(cross),
        "self_loops": sum(edge["source"] == edge["target"] for edge in edges),
        "negative_edges": sum(edge["sign"] == "-" for edge in edges),
        "encapsulation_violations": len(violations),
    }
    if actual != EXPECTED:
        raise ValueError(f"composition invariant mismatch: expected {EXPECTED}, got {actual}")
    return actual


def serialize(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def expected_paths() -> dict[str, tuple[Path, Path]]:
    return {
        "nodes": (
            REGISTRIES / "upg_greatgraph_nodes.csv",
            J_DATA / "upg_greatgraph_nodes.csv",
        ),
        "edges": (
            REGISTRIES / "upg_greatgraph_edges.csv",
            J_DATA / "upg_greatgraph_edges.csv",
        ),
    }


def check_parity(payloads: dict[str, bytes]) -> None:
    mismatches = []
    for kind, paths in expected_paths().items():
        for path in paths:
            if not path.is_file() or path.read_bytes() != payloads[kind]:
                mismatches.append(path.relative_to(REPO).as_posix())
    if mismatches:
        raise ValueError("composed bytes differ from checked-in registry: " + ", ".join(mismatches))


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify invariants and byte parity (default)")
    mode.add_argument("--write", action="store_true", help="explicitly refresh canonical and Batch-J mirrors")
    args = parser.parse_args()
    nodes, edges = compose()
    actual = validate(nodes, edges)  # every failure occurs before any write
    payloads = {"nodes": serialize(nodes), "edges": serialize(edges)}
    if args.write:
        for kind, paths in expected_paths().items():
            for path in paths:
                atomic_write(path, payloads[kind])
        print(f"wrote verified Great Graph: {actual}")
        return 0
    check_parity(payloads)
    print(f"verified Great Graph invariants and byte parity: {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
