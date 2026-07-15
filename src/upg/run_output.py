"""Immutable, atomic, hash-lined experiment output handling."""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Iterator, Mapping, Sequence


COMPLETION_MANIFEST = "run_completion_manifest.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_output_destination(
    path: Path,
    *,
    protected_dirs: Sequence[Path] = (),
    allow_nonempty: bool = False,
) -> Path:
    """Fail before writes for protected, file, or occupied destinations."""
    destination = path.expanduser().resolve()
    for protected in protected_dirs:
        frozen = protected.expanduser().resolve()
        if _is_within(destination, frozen):
            raise PermissionError(
                f"immutable frozen output namespace: {destination} is within {frozen}"
            )
    if destination.is_file():
        raise FileExistsError(f"output path is a file: {destination}")
    if destination.is_dir() and any(destination.iterdir()) and not allow_nonempty:
        raise FileExistsError(
            f"output directory is non-empty: {destination}; choose a new versioned directory"
        )
    return destination


def prepare_output_directory(
    path: Path,
    allow_nonempty: bool = False,
    *,
    protected_dirs: Sequence[Path] = (),
) -> Path:
    """Compatibility helper; atomic study runs should use ``atomic_output_run``."""
    destination = validate_output_destination(
        path, protected_dirs=protected_dirs, allow_nonempty=allow_nonempty
    )
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def _file_inventory(root: Path) -> list[dict]:
    rows = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_file() and path.name != COMPLETION_MANIFEST:
            rows.append({
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            })
    return rows


def _input_record(label: str, path: Path) -> dict:
    source = path.expanduser().resolve()
    if source.is_file():
        return {
            "label": label,
            "kind": "file",
            "path": str(source),
            "bytes": source.stat().st_size,
            "sha256": _sha256(source),
        }
    if not source.is_dir():
        raise FileNotFoundError(f"lineage input does not exist: {source}")
    digest = hashlib.sha256()
    count = total = 0
    for item in sorted(source.rglob("*"), key=lambda value: value.as_posix()):
        if not item.is_file():
            continue
        relative = item.relative_to(source).as_posix()
        item_hash = _sha256(item)
        size = item.stat().st_size
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(str(size).encode("ascii") + b"\0")
        digest.update(item_hash.encode("ascii") + b"\n")
        count += 1
        total += size
    return {
        "label": label,
        "kind": "directory-tree",
        "path": str(source),
        "files": count,
        "bytes": total,
        "sha256": digest.hexdigest(),
    }


@contextmanager
def atomic_output_run(
    final_dir: Path,
    *,
    protected_dirs: Sequence[Path] = (),
    inputs: Mapping[str, Path] | None = None,
    metadata: Mapping[str, object] | None = None,
) -> Iterator[Path]:
    """Yield a hidden temporary run and publish it atomically on success.

    Inputs are hashed before execution and rehashed before publication; a
    mutation aborts the run.  The completion manifest is written last inside
    the temporary directory, then the complete directory is renamed into
    place. Existing and protected destinations are never replaced.
    """
    destination = validate_output_destination(
        final_dir, protected_dirs=protected_dirs, allow_nonempty=False
    )
    if destination.exists():
        raise FileExistsError(
            f"output destination already exists: {destination}; choose a new version"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    lineage_inputs = inputs or {}
    before = [_input_record(label, path) for label, path in lineage_inputs.items()]
    temporary = Path(tempfile.mkdtemp(
        prefix=f".{destination.name}.tmp-", dir=destination.parent
    ))
    try:
        yield temporary
        after = [_input_record(label, path) for label, path in lineage_inputs.items()]
        if before != after:
            raise RuntimeError("lineage input changed while the run was executing")
        manifest = {
            "schema": "upg.atomic-run-completion.v1",
            "status": "complete",
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "output_name": destination.name,
            "metadata": dict(metadata or {}),
            "inputs": before,
            "outputs": _file_inventory(temporary),
        }
        (temporary / COMPLETION_MANIFEST).write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if destination.exists():
            raise FileExistsError(f"output appeared during run: {destination}")
        os.rename(temporary, destination)
    except BaseException:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
