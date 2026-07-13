"""
Loaders for the vendored registries.

All registries are read from :data:`upg.registry.DATA_DIR`, so the package is
hermetic (no dependency on the surrounding batch folders at run time).  Use
``scripts/sync_registries.py`` to refresh the vendored copies from the
authoring batch folders.
"""
from __future__ import annotations

import csv
import os

import numpy as np

from .registry import DATA_DIR, DIMS, STRATA


def read_csv(name: str) -> list[dict]:
    """Read a CSV from the packaged data directory as a list of dict rows."""
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_stratum_rows(prefix: str) -> tuple[list[dict], list[dict]]:
    """Return (node_rows, edge_rows) for one stratum, un-namespaced."""
    stem, _letter, _mother = STRATA[prefix]
    return read_csv(f"{stem}_nodes.csv"), read_csv(f"{stem}_edges.csv")


def load_dimension_node_rows() -> list[dict]:
    return read_csv("upg_dimension_nodes.csv")


def load_dimension_edge_rows() -> list[dict]:
    return read_csv("upg_dimension_edges.csv")


def dimension_magnitude_matrix() -> np.ndarray:
    """8x8 dimension coupling matrix of edge *magnitudes*.

    Parallel channels (e.g. the two SYS support/thwart edges) are combined by
    mean magnitude, exactly as Batch J's ``dimension_W`` did.  Entry
    ``W[target, source]`` holds the mean magnitude of edges source -> target.
    Signs are intentionally dropped here: the spectral analysis operates on
    magnitudes (it symmetrises immediately afterwards).
    """
    idx = {d: i for i, d in enumerate(DIMS)}
    mags: dict[tuple[int, int], list[float]] = {}
    for r in load_dimension_edge_rows():
        key = (idx[r["source"]], idx[r["target"]])   # (source, target)
        mags.setdefault(key, []).append(abs(float(r["weight"])))
    W = np.zeros((len(DIMS), len(DIMS)))
    for (j, i), vals in mags.items():                # source j -> target i
        W[i, j] = float(np.mean(vals))
    return W
