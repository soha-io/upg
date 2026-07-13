"""
Canonical registry constants for the Unified Person Graph (UPG).

Single source of truth for:
  * the eight strata (prefix -> file stem, batch letter, mother node id),
  * the interface bindings that stitch strata together at composition,
  * the mother-to-mother couplings that have no interface node,
  * the dimension ordering used by the spectral and dynamic analyses.

These mirror, exactly, the constants that were previously scattered across
``compose_greatgraph.py`` and ``verify_math.py`` in Batch J. Keeping them in
one place is what lets the composition and the verification agree by
construction rather than by coincidence.
"""
from __future__ import annotations

import os

# --------------------------------------------------------------------------
# Where the vendored registries live (packaged with upg, so hermetic).
# --------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# --------------------------------------------------------------------------
# The eight strata.  Insertion order is significant: it fixes node ordering
# in the composed Great Graph and therefore the reproducibility of every
# order-dependent statistic (BFS start node, weighted-degree ties, ...).
#   prefix : (file_stem, batch_letter, mother_node_id_within_stratum)
# THER has no published mother; one is synthesized at composition.
# --------------------------------------------------------------------------
STRATA: dict[str, tuple[str, str, str | None]] = {
    "DIS":  ("udg",     "A", "P"),
    "THER": ("utg",     "B", None),
    "DEV":  ("udevg",   "C", "D"),
    "PER":  ("uperg",   "D", "P"),
    "TEM":  ("utempg",  "E", "T"),
    "NEED": ("uneedg",  "F", "N"),
    "ME":   ("umeg",    "G", "ME"),
    "SYS":  ("usysg",   "H", "SYS"),
}

# Dimension order for the 8-node dimension graph (spectral analysis).
DIMS = ["TEM", "DEV", "PER", "NEED", "ME", "DIS", "THER", "SYS"]
# Endogenous dimensions for the dynamic model (THER enters as control input).
ENDO = ["TEM", "DEV", "PER", "NEED", "ME", "DIS", "SYS"]

# --------------------------------------------------------------------------
# Interface bindings: (stratum, interface_node, partner_stratum, direction)
#   "out":  stratum.interface -> partner mother
#   "in" :  partner mother    -> stratum.interface
#   "both": both edges
# --------------------------------------------------------------------------
BINDINGS: list[tuple[str, str, str, str]] = [
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
MOTHER_PAIRS: set[tuple[str, str]] = {
    ("TEM", "DEV"), ("DEV", "TEM"), ("DEV", "PER"), ("DEV", "NEED"),
    ("DEV", "ME"), ("DEV", "DIS"), ("PER", "DIS"), ("PER", "SYS"),
    ("SYS", "PER"), ("ME", "NEED"), ("DIS", "THER"), ("THER", "DIS"),
    ("THER", "TEM"), ("THER", "PER"), ("THER", "NEED"),
    ("DIS", "NEED"), ("DIS", "SYS"), ("NEED", "DIS"),
}

# Node ids that carry the "interface" role even though they do not end in _IF.
INTERFACE_EXCEPTIONS = {"OUT_ADJ", "PERSON_IF"}

# Published census (Batch J).  Used as regression anchors.
PUBLISHED = {
    "dimension_nodes": 8,
    "dimension_edge_rows": 41,
    "greatgraph_nodes": 253,
    "greatgraph_edges": 522,
    "cross_stratum_edges": 35,
    "self_loops": 20,
    "negative_edges": 33,
    "nodes_per_stratum": {
        "DIS": 18, "THER": 39, "DEV": 21, "PER": 54,
        "TEM": 30, "NEED": 33, "ME": 28, "SYS": 30,
    },
}
