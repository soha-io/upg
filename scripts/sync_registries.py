#!/usr/bin/env python3
"""
Refresh the vendored registries from the authoring batch folders.

The package vendors a canonical snapshot of the eight strata + dimension
registries under ``src/upg/data`` so it is self-contained.  When you edit a
registry in its batch folder, run this to re-sync:

    python scripts/sync_registries.py

It copies from ``<model root>/Batch X - .../data/`` into the package data dir
and reports which files changed.  The model root is assumed to be the parent
of this repository (i.e. the folder that holds both ``upg/`` and the batch
folders).
"""
from __future__ import annotations

import filecmp
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MODEL_ROOT = os.path.dirname(REPO)
DATA = os.path.join(REPO, "src", "upg", "data")

# file stem -> batch folder name
SOURCES = {
    "udg":     "Batch A - Psychopathology",
    "utg":     "Batch B - Psychotherapy",
    "udevg":   "Batch C - Developmental",
    "uperg":   "Batch D - Personality",
    "utempg":  "Batch E - Temperament",
    "uneedg":  "Batch F - Needs",
    "umeg":    "Batch G - Motivation & Emotion",
    "usysg":   "Batch H - Systems",
}
DIMENSION = ("Batch J - Eight-Dimension Model",
             ["upg_dimension_nodes.csv", "upg_dimension_edges.csv"])


def _sync(src: str, dst: str) -> bool:
    if not os.path.exists(src):
        print(f"  MISSING source: {src}")
        return False
    changed = not (os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False))
    shutil.copyfile(src, dst)
    print(f"  {'UPDATED' if changed else 'unchanged'}: {os.path.basename(dst)}")
    return changed


def main() -> None:
    n_changed = 0
    for stem, folder in SOURCES.items():
        for kind in ("nodes", "edges"):
            src = os.path.join(MODEL_ROOT, folder, "data", f"{stem}_{kind}.csv")
            dst = os.path.join(DATA, f"{stem}_{kind}.csv")
            n_changed += _sync(src, dst)
    folder, files = DIMENSION
    for name in files:
        src = os.path.join(MODEL_ROOT, folder, "data", name)
        dst = os.path.join(DATA, name)
        n_changed += _sync(src, dst)
    print(f"\n{n_changed} file(s) updated. Re-run the test suite to confirm "
          f"the published numbers still hold.")


if __name__ == "__main__":
    main()
