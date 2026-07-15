#!/usr/bin/env python3
"""Check or refresh packaged registry snapshots from the current layout.

The public repository includes the dimension authoring registries under
``registries/``.  Stratum authoring CSVs may be supplied in each current
``batches/<letter>-<slug>/data`` directory; when absent, their already
versioned package snapshots remain authoritative for this public release.
Use ``--write`` for mutation.  The safe default is a parity check.
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PACKAGE_DATA = REPO / "src" / "upg" / "data"
STRATA = {
    "udg": "A-psychopathology",
    "utg": "B-psychotherapy",
    "udevg": "C-developmental",
    "uperg": "D-personality",
    "utempg": "E-temperament",
    "uneedg": "F-needs",
    "umeg": "G-motivation-emotion",
    "usysg": "H-systems",
}


def source_pairs(root: Path) -> list[tuple[Path, Path]]:
    pairs = []
    for stem, folder in STRATA.items():
        for kind in ("nodes", "edges"):
            name = f"{stem}_{kind}.csv"
            pairs.append((root / "batches" / folder / "data" / name,
                          PACKAGE_DATA / name))
    for name in ("upg_dimension_nodes.csv", "upg_dimension_edges.csv"):
        pairs.append((root / "registries" / name, PACKAGE_DATA / name))
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=REPO,
                        help="UPG authoring root (default: this repository)")
    parser.add_argument("--write", action="store_true",
                        help="copy available changed sources into package data")
    parser.add_argument("--require-all", action="store_true",
                        help="fail when private/unpublished stratum sources are absent")
    args = parser.parse_args()

    changed = missing = 0
    for source, destination in source_pairs(args.source_root.resolve()):
        if not source.is_file():
            missing += 1
            print(f"SKIP unavailable authoring source: {source}")
            continue
        same = destination.is_file() and filecmp.cmp(source, destination, shallow=False)
        if same:
            print(f"PASS {source.relative_to(args.source_root.resolve())}")
            continue
        changed += 1
        if args.write:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            print(f"UPDATED {destination.relative_to(REPO)}")
        else:
            print(f"STALE {destination.relative_to(REPO)}")

    if changed and not args.write:
        print(f"registry check failed: {changed} available snapshot(s) stale")
        return 1
    if missing and args.require_all:
        print(f"registry check failed: {missing} required source(s) missing")
        return 1
    print(f"registry check complete: {changed} changed, {missing} unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
