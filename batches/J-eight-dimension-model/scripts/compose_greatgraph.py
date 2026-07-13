"""
Batch J — Great Graph composition.

Reads the eight strata's node/edge CSVs (Batches A–H), namespaces every node
with its stratum prefix, adds (i) the synthetic THER mother node over the
UTG workflow, (ii) interface-binding edges that stitch each stratum's
interface nodes to the partner stratum's mother node, and (iii)
mother-to-mother edges for couplings that have no interface node,
taken from data/upg_dimension_edges.csv.

Encapsulation rule (project spec J.4): a stratum's internal nodes never
connect directly to another stratum's internal nodes. Every cross-stratum
edge in the output touches a mother node or an interface node bound to a
mother node. The script enforces and audits this.

Outputs: data/upg_greatgraph_nodes.csv, data/upg_greatgraph_edges.csv
Run: python3 compose_greatgraph.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(HERE, "..", "data")

STRATA = {
    "DIS":  ("Batch A - Psychopathology",            "udg",    "P"),
    "THER": ("Batch B - Psychotherapy",               "utg",    None),  # mother synthesized
    "DEV":  ("Batch C - Developmental",               "udevg",  "D"),
    "PER":  ("Batch D - Personality",                 "uperg",  "P"),
    "TEM":  ("Batch E - Temperament",                 "utempg", "T"),
    "NEED": ("Batch F - Needs",                       "uneedg", "N"),
    "ME":   ("Batch G - Motivation & Emotion",        "umeg",   "ME"),
    "SYS":  ("Batch H - Systems",                     "usysg",  "SYS"),
}

# Interface bindings: (stratum, interface_node, partner_stratum, direction)
# direction "out": stratum.interface -> partner mother
# direction "in" : partner mother -> stratum.interface
# direction "both": both edges
BINDINGS = [
    ("TEM",  "PERS_IF",   "PER",  "out"),
    ("TEM",  "OUT_ADJ",   "DIS",  "out"),
    ("NEED", "MOT_IF",    "ME",   "out"),
    ("NEED", "PERS_IF",   "PER",  "in"),
    ("ME",   "NEEDS_IF",  "NEED", "in"),
    ("ME",   "SYS_IF",    "SYS",  "both"),
    ("ME",   "PERS_IF",   "PER",  "in"),
    ("ME",   "TEMP_IF",   "TEM",  "in"),
    ("ME",   "DIS_IF",    "DIS",  "out"),
    ("ME",   "THER_IF",   "THER", "in"),
    ("SYS",  "PERSON_IF", "PER",  "out"),
    ("SYS",  "NEEDS_IF",  "NEED", "out"),
    ("SYS",  "ME_IF",     "ME",   "out"),
    ("SYS",  "DEV_IF",    "DEV",  "out"),
    ("SYS",  "DIS_IF",    "DIS",  "out"),
    ("SYS",  "THER_IF",   "THER", "in"),
]
BIND_W = 0.90  # binding edges are near-identity conduits

# Dimension-level pairs whose coupling has NO interface node on either side;
# stitched mother-to-mother using the dimension edge table.
MOTHER_PAIRS = {("TEM", "DEV"), ("DEV", "TEM"), ("DEV", "PER"), ("DEV", "NEED"),
                ("DEV", "ME"), ("DEV", "DIS"), ("PER", "DIS"), ("PER", "SYS"),
                ("SYS", "PER"), ("ME", "NEED"), ("DIS", "THER"), ("THER", "DIS"),
                ("THER", "TEM"), ("THER", "PER"), ("THER", "NEED"),
                ("DIS", "NEED"), ("DIS", "SYS"), ("NEED", "DIS")}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    nodes, edges = [], []
    mother = {}

    for pref, (folder, stem, mother_id) in STRATA.items():
        ndir = os.path.join(ROOT, folder, "data", f"{stem}_nodes.csv")
        edir = os.path.join(ROOT, folder, "data", f"{stem}_edges.csv")
        for r in read_csv(ndir):
            nodes.append({
                "node_id": f"{pref}.{r['node_id']}",
                "stratum": pref,
                "label": r.get("label", ""),
                "level": r.get("level", ""),
                "parent": f"{pref}.{r['parent']}" if r.get("parent") else "",
                "role": "internal",
            })
        for r in read_csv(edir):
            edges.append({
                "source": f"{pref}.{r['source']}",
                "target": f"{pref}.{r['target']}",
                "weight": r["weight"],
                "sign": r["sign"],
                "type": r["type"],
                "gate": r.get("gate", "none") or "none",
                "origin": f"Batch {folder.split(' - ')[0][-1]}",
            })
        if mother_id:
            mother[pref] = f"{pref}.{mother_id}"

    # Synthesize the THER mother over the UTG workflow phases N01–N11
    mother["THER"] = "THER.THER"
    nodes.append({"node_id": "THER.THER", "stratum": "THER",
                  "label": "Universal therapy workflow (mother node, synthesized at composition)",
                  "level": "-1", "parent": "", "role": "mother"})
    for i in range(1, 12):
        edges.append({"source": "THER.THER", "target": f"THER.N{i:02d}",
                      "weight": "0.85", "sign": "+", "type": "hierarchical",
                      "gate": "none", "origin": "Batch J (composition)"})

    # Mark mother and interface roles
    for n in nodes:
        if n["node_id"] in mother.values():
            n["role"] = "mother"
        elif n["node_id"].split(".", 1)[1].endswith("_IF") or \
                n["node_id"].split(".", 1)[1] in ("OUT_ADJ", "PERSON_IF"):
            n["role"] = "interface"

    # Implicit hierarchical edges: several strata encode part of their
    # decomposition only in the nodes' parent column (UTG subnodes, UDevG
    # mechanisms, UPerG adaptation/narrative subnodes). Materialize
    # parent -> child edges where no explicit edge exists in either direction.
    have = {(e["source"], e["target"]) for e in edges}
    for nrow in nodes:
        p, c = nrow["parent"], nrow["node_id"]
        if p and (p, c) not in have and (c, p) not in have:
            edges.append({"source": p, "target": c, "weight": "0.80",
                          "sign": "+", "type": "hierarchical-implicit",
                          "gate": "none", "origin": "Batch J (parent field)"})

    # Interface-binding edges
    for strat, iface, partner, direction in BINDINGS:
        a, b = f"{strat}.{iface}", mother[partner]
        if direction in ("out", "both"):
            edges.append({"source": a, "target": b, "weight": str(BIND_W),
                          "sign": "+", "type": "binding", "gate": "none",
                          "origin": "Batch J (composition)"})
        if direction in ("in", "both"):
            edges.append({"source": b, "target": a, "weight": str(BIND_W),
                          "sign": "+", "type": "binding", "gate": "none",
                          "origin": "Batch J (composition)"})

    # Mother-to-mother stitches for interface-less couplings
    for r in read_csv(os.path.join(DATA, "upg_dimension_edges.csv")):
        if (r["source"], r["target"]) in MOTHER_PAIRS and r["source"] != r["target"]:
            edges.append({"source": mother[r["source"]], "target": mother[r["target"]],
                          "weight": r["weight"], "sign": r["sign"],
                          "type": f"interstratum-{r['type']}", "gate": r["gate"],
                          "origin": "Batch J (dimension edge)"})

    # ---- Encapsulation audit -------------------------------------------
    roles = {n["node_id"]: n["role"] for n in nodes}
    strat_of = {n["node_id"]: n["stratum"] for n in nodes}
    violations = []
    for e in edges:
        s, t = e["source"], e["target"]
        if strat_of[s] != strat_of[t]:
            ok = roles[s] in ("mother", "interface") or roles[t] in ("mother", "interface")
            if not ok:
                violations.append((s, t))
    print(f"nodes: {len(nodes)}  edges: {len(edges)}")
    print(f"cross-stratum edges: {sum(1 for e in edges if strat_of[e['source']] != strat_of[e['target']])}")
    print(f"encapsulation violations: {len(violations)}", violations[:5])

    with open(os.path.join(DATA, "upg_greatgraph_nodes.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(nodes[0].keys()))
        w.writeheader(); w.writerows(nodes)
    with open(os.path.join(DATA, "upg_greatgraph_edges.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(edges[0].keys()))
        w.writeheader(); w.writerows(edges)
    print("written: upg_greatgraph_nodes.csv, upg_greatgraph_edges.csv")


if __name__ == "__main__":
    main()
