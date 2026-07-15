"""Fail-closed resolution of the public retrospective-data clone.

``UPG_DATA_ROOT`` is intentionally reserved for the external content-addressed
study store.  Public Batch K inputs use ``UPG_PUBLIC_DATA_ROOT`` instead.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping


PUBLIC_REQUIRED = (
    Path("ipip_neo_johnson/data_120_300/IPIP120.dat"),
    Path("kossakowski_esm/ESMdata/ESMdata.csv"),
)


class PublicDataLayoutError(ValueError):
    """A selected public-data root exists or was configured but is invalid."""


def validate_public_data_root(path: Path, *, source: str) -> Path:
    root = path.expanduser().resolve()
    if not root.is_dir():
        raise PublicDataLayoutError(f"{source} is not a directory: {root}")
    missing = [relative.as_posix() for relative in PUBLIC_REQUIRED
               if not (root / relative).is_file()]
    if missing:
        raise PublicDataLayoutError(
            f"{source} has an invalid public-data layout at {root}; missing: "
            + ", ".join(missing)
        )
    return root


def resolve_public_data_root(
    *,
    repo_root: Path,
    explicit: Path | None = None,
    environ: Mapping[str, str] | None = None,
    allow_absent_sibling: bool = False,
) -> Path | None:
    """Resolve explicit CLI > public-data env > sibling clone.

    An explicitly selected or environment-selected invalid layout raises and
    never falls through to another location.  Only an absent auto-discovered
    sibling may return ``None`` for optional preflight operation.
    """
    environment = os.environ if environ is None else environ
    if explicit is not None:
        return validate_public_data_root(explicit, source="--data-root")
    configured = environment.get("UPG_PUBLIC_DATA_ROOT")
    if configured:
        return validate_public_data_root(
            Path(configured), source="UPG_PUBLIC_DATA_ROOT"
        )
    sibling = repo_root.resolve().parent / "upg-data" / "redistributable"
    if sibling.is_dir():
        return validate_public_data_root(sibling, source="sibling upg-data clone")
    if allow_absent_sibling:
        return None
    raise PublicDataLayoutError(
        "public data not found; pass --data-root or set UPG_PUBLIC_DATA_ROOT "
        f"(expected sibling layout at {sibling}). UPG_DATA_ROOT is reserved "
        "for the external content-addressed study store."
    )
