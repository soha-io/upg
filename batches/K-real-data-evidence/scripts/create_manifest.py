#!/usr/bin/env python3
"""Generate or verify the current-layout Batch K artifact manifest.

The uploaded release manifest at ``evidence/manifest.json`` is historical and
is never rewritten by this command.  Writing the current snapshot requires an
explicit ``--write``; verification is the safe default.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


REPO = Path(__file__).resolve().parents[3]
BATCH_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = BATCH_ROOT / "artifact_manifest.json"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def inventory() -> list[dict]:
    proc = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=REPO,
        capture_output=True,
        check=True,
    )
    rows = []
    relatives = sorted(
        Path(raw.decode("utf-8")) for raw in proc.stdout.split(b"\0") if raw
    )
    manifest_relative = MANIFEST.relative_to(REPO)
    for relative in relatives:
        if relative == manifest_relative:
            continue
        path = REPO / relative
        if not path.is_file():
            continue
        rows.append({
            "path": relative.as_posix(),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        })
    return rows


def build_manifest() -> dict:
    return {
        "schema": "upg.batch-k-artifact-manifest.v1",
        "scope": "complete repository files from git tracked/untracked-nonignored inventory",
        "path_root": "repository root",
        "hash_algorithm": "sha256",
        "legacy_manifest": {
            "path": "batches/K-real-data-evidence/evidence/manifest.json",
            "policy": "frozen historical upload manifest; never rewritten here",
        },
        "excluded": [
            "batches/K-real-data-evidence/artifact_manifest.json",
            "git-ignored files and directories",
        ],
        "files": inventory(),
    }


def serialized(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true",
                      help="explicitly replace artifact_manifest.json")
    mode.add_argument("--check", action="store_true",
                      help="verify the checked-in manifest (default)")
    args = parser.parse_args()
    current = serialized(build_manifest())
    if args.write:
        MANIFEST.write_text(current, encoding="utf-8")
        print(f"wrote {MANIFEST} with {len(inventory())} repository files")
        return 0
    if not MANIFEST.is_file():
        print(f"missing {MANIFEST}; run with --write")
        return 1
    recorded = MANIFEST.read_text(encoding="utf-8")
    if recorded != current:
        print(f"stale {MANIFEST}; inspect changes, then run with --write")
        return 1
    print(f"verified {MANIFEST} ({len(inventory())} repository files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
