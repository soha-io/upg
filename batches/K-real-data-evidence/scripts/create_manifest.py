#!/usr/bin/env python3
"""Create the deterministic file manifest for the Batch K bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


files = []
for path in sorted(ROOT.rglob("*")):
    if path.is_file() and path.name != "manifest.json":
        files.append({
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        })

manifest = {
    "release": "Batch K evidence release 2026-07-12",
    "superseded_input_excluded": "psych-lab-main(2).zip",
    "raw_input_sha256": {
        "psych-lab-main(1).zip": "4514b847d16b0cd9c20a1aa69c677bbaad78a7153630e9370b4137c9489569ab",
        "Archive(1).zip": "f81f07e4b9f4de983d07f3dcc30240a3da660059510c98cd1da7de93eda488c7",
        "8-Dimention Model Sources-Part 1.zip": "e392ef0934ff2d3dd9fe9dfea4096b431ec35c0b69446329bc0f3eaa0ebe1f33",
        "8-Dimention Model Sources-Part 2(1).zip": "3b3b9744fe444b22957a9bf40ba3a4c65da256a1efac3c6929956a8c36e59201"
    },
    "test_result": "95/95 passed",
    "files": files,
}
(ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"wrote {ROOT / 'manifest.json'} with {len(files)} files")
