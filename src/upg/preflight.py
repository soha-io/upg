"""Clean-clone verification for the public UPG research artifact.

The verifier intentionally does not download data or retrain models.  Missing
public-data clones are reported as skips unless ``--require-data`` is used;
restricted datasets are never required for preflight.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

from .data_paths import PublicDataLayoutError, resolve_public_data_root


REPO = Path(__file__).resolve().parents[2]
BATCH_K = REPO / "batches" / "K-real-data-evidence"


class Checks:
    def __init__(self) -> None:
        self.failed = 0
        self.skipped = 0

    def ok(self, name: str, detail: str = "") -> None:
        print(f"PASS  {name}" + (f": {detail}" if detail else ""))

    def fail(self, name: str, detail: str) -> None:
        self.failed += 1
        print(f"FAIL  {name}: {detail}")

    def skip(self, name: str, detail: str) -> None:
        self.skipped += 1
        print(f"SKIP  {name}: {detail}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _run(checks: Checks, name: str, command: list[str]) -> None:
    proc = subprocess.run(command, cwd=REPO, text=True, capture_output=True)
    if proc.returncode:
        tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-20:])
        checks.fail(name, tail or f"exit status {proc.returncode}")
    else:
        detail = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "ok"
        checks.ok(name, detail)


def _report_hardware(checks: Checks) -> None:
    memory = "unknown"
    try:
        total = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        memory = f"{total / (1024 ** 3):.1f} GiB RAM"
    except (AttributeError, KeyError, OSError, ValueError):
        pass
    checks.ok(
        "runtime environment",
        f"Python {platform.python_version()}; {platform.system()} "
        f"{platform.machine()}; {os.cpu_count() or 'unknown'} logical CPUs; {memory}",
    )
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        proc = subprocess.run(
            [nvidia_smi, "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader"],
            text=True,
            capture_output=True,
        )
        gpu = proc.stdout.strip() if proc.returncode == 0 else "nvidia-smi query failed"
    else:
        gpu = "no NVIDIA device reported by nvidia-smi"
    print(f"INFO  accelerator inventory: {gpu}")
    backend_detail = (
        "NumPy CPU; detected NVIDIA hardware is not used by current code"
        if nvidia_smi and proc.returncode == 0
        else "NumPy CPU; current code has no CUDA/GPU backend"
    )
    checks.ok(
        "implemented compute backend",
        backend_detail,
    )


def _check_study_dependencies(checks: Checks) -> None:
    modules = ("matplotlib", "networkx", "pandas", "scipy", "sklearn")
    missing = []
    versions = []
    for name in modules:
        try:
            module = __import__(name)
        except ImportError:
            missing.append(name)
        else:
            versions.append(f"{name}={getattr(module, '__version__', 'unknown')}")
    if missing:
        checks.fail(
            "study dependencies",
            f"missing {', '.join(missing)}; run with --extra study",
        )
    else:
        checks.ok("study dependencies", ", ".join(versions))
    poppler = [tool for tool in ("pdfinfo", "pdftotext") if shutil.which(tool)]
    if len(poppler) == 2:
        checks.ok("optional source-audit tools", "pdfinfo and pdftotext")
    else:
        checks.skip(
            "optional source-audit tools",
            "install Poppler only when rerunning the PDF corpus audit",
        )


def _check_graph(checks: Checks) -> None:
    from . import axiom_audit, build_person_graph, encapsulation_violations

    graph = build_person_graph()
    actual = (
        graph.n,
        len(graph.edges),
        len(graph.cross_stratum_edges()),
        len(graph.self_loops()),
        len(graph.negative_edges()),
        len(encapsulation_violations(graph)),
    )
    expected = (253, 522, 35, 20, 33, 0)
    audit = axiom_audit(graph)
    raw = graph.directed_boolean()
    closure = raw.copy()
    for k in range(graph.n):
        closure |= np.outer(closure[:, k], closure[k, :])
    np.fill_diagonal(closure, False)
    raw_fill = float(closure.sum() / (graph.n * (graph.n - 1)))
    raw_sinks = int((raw.sum(axis=1) == 0).sum())
    graph_ok = (
        actual == expected
        and audit.weakly_connected
        and audit.isolated_nodes == 0
        and abs(audit.reachability_fill - 1.0) < 1e-12
        and abs(raw_fill - 0.3385250015684798) < 1e-12
        and raw_sinks == 109
    )
    if graph_ok:
        checks.ok(
            "formal graph census",
            f"{actual}; semantic reachability=1.000000, "
            f"raw directed={raw_fill:.6f}, raw sinks={raw_sinks}",
        )
    else:
        checks.fail(
            "formal graph census",
            f"census expected {expected}, got {actual}; semantic reachability="
            f"{audit.reachability_fill:.12f}, raw directed={raw_fill:.12f}, "
            f"raw sinks={raw_sinks}",
        )


def _check_registry_snapshot(checks: Checks) -> None:
    pairs = (
        (REPO / "registries" / "upg_dimension_nodes.csv",
         REPO / "src" / "upg" / "data" / "upg_dimension_nodes.csv"),
        (REPO / "registries" / "upg_dimension_edges.csv",
         REPO / "src" / "upg" / "data" / "upg_dimension_edges.csv"),
    )
    mismatches = [source.name for source, packaged in pairs
                  if source.read_bytes() != packaged.read_bytes()]
    if mismatches:
        checks.fail("public/package registry parity", ", ".join(mismatches))
    else:
        checks.ok("public/package registry parity", "2 dimension registries")


def _check_portable_paths(checks: Checks) -> None:
    active = []
    for root in (REPO / "src", REPO / "scripts", REPO / "batches"):
        active.extend(path for path in root.rglob("*.py")
                      if "__pycache__" not in path.parts)
    active += [
        REPO / "README.md",
        BATCH_K / "manuscript_src" / "methods_appendix.md",
    ]
    offenders = []
    legacy_prefix = "/" + "workspace/"
    for path in active:
        text = path.read_text(encoding="utf-8", errors="replace")
        if legacy_prefix in text:
            offenders.append(path.relative_to(REPO).as_posix())
    if offenders:
        checks.fail("portable active paths", ", ".join(offenders))
    else:
        checks.ok("portable active paths", f"{len(active)} scripts/docs")


def _check_batch_k(checks: Checks) -> None:
    results = BATCH_K / "results"
    checkpoints = sorted(results.glob("gat/*.npz")) + sorted(results.glob("forecast/*.npz"))
    try:
        for checkpoint in checkpoints:
            with np.load(checkpoint, allow_pickle=False) as archive:
                if not archive.files:
                    raise ValueError(f"empty checkpoint {checkpoint}")
    except Exception as exc:  # noqa: BLE001 - all corrupt archive failures matter
        checks.fail("Batch K checkpoint readability", str(exc))
    else:
        checks.ok("Batch K checkpoint readability", f"{len(checkpoints)} NPZ files")

    from .gat import MaskedGraphAttentionEstimator
    legacy_gat = sorted(results.glob("gat/gat_*.npz"))
    try:
        loaded = [MaskedGraphAttentionEstimator.load(str(path)) for path in legacy_gat]
        if any(model.B0.shape != (7, 7) for model in loaded):
            raise ValueError("unexpected legacy GAT skeleton shape")
    except Exception as exc:  # noqa: BLE001 - loader compatibility is a release gate
        checks.fail("legacy GAT checkpoint loader", str(exc))
    else:
        checks.ok("legacy GAT checkpoint loader", f"{len(loaded)}/3 loaded")

    provenance_path = results / "forecast" / "training_provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    names = {
        "balanced_regimes": "tf_balanced_regimes.npz",
        "clinical_realistic": "tf_clinical_realistic.npz",
        "transition_rich": "tf_transition_rich.npz",
        "channel_independent_transition_null": "null_ci_transition_rich.npz",
    }
    bad = []
    for key, filename in names.items():
        actual = _sha256(results / "forecast" / filename)
        expected = provenance[key]["checkpoint_sha256"]
        if actual != expected:
            bad.append(filename)
    if bad:
        checks.fail("forecast checkpoint provenance", ", ".join(bad))
    else:
        checks.ok("forecast checkpoint provenance", "4/4 hashes")

    gat = json.loads((results / "gat" / "gat_results.json").read_text(encoding="utf-8"))
    axes = ("median_edge_rmse", "median_edge_dev_corr", "median_rho_abs_err",
            "regime_accuracy", "median_attractor_abs_err")
    wins = {axis: 0 for axis in axes}
    cells = 0
    for preset in gat.values():
        for cell in preset["cells"]:
            cells += 1
            for axis in axes:
                wins[axis] += int(cell["verdict"][axis]["gat_wins"])
    expected_wins = {
        "median_edge_rmse": 12,
        "median_edge_dev_corr": 12,
        "median_rho_abs_err": 12,
        "regime_accuracy": 8,
        "median_attractor_abs_err": 5,
    }
    if cells == 12 and wins == expected_wins:
        checks.ok("frozen GAT result ledger", f"12 cells; wins={wins}")
    else:
        checks.fail("frozen GAT result ledger", f"cells={cells}; wins={wins}")

    quarantine = json.loads(
        (BATCH_K / "chronology_quarantine.json").read_text(encoding="utf-8")
    )
    altered = []
    for row in quarantine["frozen_files"]:
        path = BATCH_K / row["path"]
        if not path.is_file() or _sha256(path) != row["sha256"]:
            altered.append(row["path"])
    if altered:
        checks.fail("chronology quarantine integrity", ", ".join(altered))
    else:
        checks.ok("chronology quarantine integrity",
                  f"{len(quarantine['frozen_files'])} frozen files")


def _check_data(checks: Checks, explicit: Path | None, require: bool) -> None:
    try:
        root = resolve_public_data_root(
            repo_root=REPO,
            explicit=explicit,
            allow_absent_sibling=not require,
        )
    except PublicDataLayoutError as exc:
        checks.fail("public data availability", str(exc))
        return
    if root is None:
        checks.skip(
            "public data availability",
            "pass --data-root or set UPG_PUBLIC_DATA_ROOT; UPG_DATA_ROOT is CAS-only",
        )
        return
    checksum_file = REPO / "data" / "checksums.sha256"
    present = missing = bad = 0
    for line in checksum_file.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        expected, relative = line.split(maxsplit=1)
        path = root / relative.removeprefix("./")
        if not path.is_file():
            missing += 1
        elif _sha256(path) != expected:
            bad += 1
        else:
            present += 1
    if bad or (require and missing):
        checks.fail("public data checksums", f"{present} good, {missing} missing, {bad} bad")
    else:
        suffix = f", {missing} optional files absent" if missing else ""
        checks.ok("public data checksums", f"{present} verified{suffix}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-tests", action="store_true",
                        help="run artifact checks without invoking pytest")
    parser.add_argument("--data-root", type=Path,
                        help="public input clone (overrides UPG_PUBLIC_DATA_ROOT and sibling upg-data)")
    parser.add_argument("--require-data", action="store_true",
                        help="fail if any public checksum target is unavailable")
    args = parser.parse_args(argv)

    checks = Checks()
    _report_hardware(checks)
    _check_study_dependencies(checks)
    _check_graph(checks)
    _check_registry_snapshot(checks)
    _check_portable_paths(checks)
    _run(checks, "registry synchronization check",
         [sys.executable, "scripts/sync_registries.py"])
    _run(checks, "Great Graph composition parity", [
        sys.executable,
        "batches/J-eight-dimension-model/scripts/compose_greatgraph.py",
        "--check",
    ])
    _run(checks, "tracked Python syntax", [
        sys.executable, "-m", "compileall", "-q", "src", "scripts", "batches",
    ])
    _check_batch_k(checks)
    _run(checks, "deterministic reproduction", [sys.executable, "scripts/reproduce.py"])
    _run(checks, "current Batch K manifest", [
        sys.executable,
        str(BATCH_K / "scripts" / "create_manifest.py"),
        "--check",
    ])
    _check_data(checks, args.data_root, args.require_data)
    if not args.skip_tests:
        _run(checks, "pytest", [sys.executable, "-m", "pytest", "-q"])

    print(f"\nPreflight: {checks.failed} failed, {checks.skipped} skipped")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
