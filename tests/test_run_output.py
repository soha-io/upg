import hashlib
import json
from pathlib import Path

import pytest

from upg.run_output import (COMPLETION_MANIFEST, atomic_output_run,
                            prepare_output_directory,
                            validate_output_destination)


def test_frozen_namespace_cannot_be_bypassed_by_override(tmp_path):
    frozen = tmp_path / "results" / "real_data"
    frozen.mkdir(parents=True)
    for candidate in (frozen, frozen / "child"):
        with pytest.raises(PermissionError, match="immutable frozen"):
            prepare_output_directory(
                candidate, allow_nonempty=True, protected_dirs=[frozen]
            )


def test_output_guard_refuses_nonempty_directory(tmp_path):
    run = tmp_path / "real_data_corrected_v1"
    run.mkdir()
    (run / "lineage.json").write_text("frozen", encoding="utf-8")
    with pytest.raises(FileExistsError, match="non-empty"):
        prepare_output_directory(run)
    assert (run / "lineage.json").read_text(encoding="utf-8") == "frozen"


def test_generic_override_does_not_override_protected_check(tmp_path):
    run = tmp_path / "ordinary"
    run.mkdir()
    (run / "existing.txt").write_text("x", encoding="utf-8")
    assert prepare_output_directory(run, allow_nonempty=True) == run.resolve()
    with pytest.raises(PermissionError):
        validate_output_destination(
            run, protected_dirs=[run], allow_nonempty=True
        )


def test_atomic_run_publishes_manifest_and_input_hash(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text("a,b\n1,2\n", encoding="utf-8")
    final = tmp_path / "run-v1"
    with atomic_output_run(
        final, inputs={"fixture": source}, metadata={"analysis_id": "test"}
    ) as work:
        assert not final.exists()
        (work / "result.json").write_text('{"ok": true}\n', encoding="utf-8")
    manifest = json.loads((final / COMPLETION_MANIFEST).read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    assert manifest["metadata"]["analysis_id"] == "test"
    assert manifest["inputs"][0]["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert manifest["outputs"][0]["path"] == "result.json"
    assert not list(tmp_path.glob(".run-v1.tmp-*"))


def test_atomic_run_failure_leaves_no_partial_output(tmp_path):
    final = tmp_path / "run-v2"
    with pytest.raises(RuntimeError, match="boom"):
        with atomic_output_run(final) as work:
            (work / "partial.txt").write_text("partial", encoding="utf-8")
            raise RuntimeError("boom")
    assert not final.exists()
    assert not list(tmp_path.glob(".run-v2.tmp-*"))


def test_atomic_run_refuses_existing_even_when_empty(tmp_path):
    final = tmp_path / "run-v3"
    final.mkdir()
    with pytest.raises(FileExistsError, match="already exists"):
        with atomic_output_run(final):
            pass
