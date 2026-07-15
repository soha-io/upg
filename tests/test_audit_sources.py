from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "batches/K-real-data-evidence/scripts/audit_sources.py"
)
SPEC = importlib.util.spec_from_file_location("batch_k_audit_sources", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
audit_sources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_sources)


class SourceAuditOcrTests(unittest.TestCase):
    def _source(self, root: Path, name: str) -> Path:
        for directory in ("project", "data", "sources-part-1", "sources-part-2"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        source = root / "project" / name
        source.write_bytes(b"synthetic PDF fixture")
        return source.resolve()

    def test_known_scan_without_explicit_ocr_input_is_not_mislabeled(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "inputs"
            source = self._source(
                root, "07. Chess-Thomas-Temperament-and-its-functional-significance.pdf"
            )
            audit_sources.configure(root, Path(temporary) / "out", None)
            with (
                mock.patch.object(audit_sources, "file_hash", return_value="0" * 64),
                mock.patch.object(audit_sources, "pdf_pages", return_value=2),
                mock.patch.object(audit_sources, "pdf_words", return_value=0),
            ):
                row = audit_sources.inspect_pdf(("project", source))
            self.assertEqual(row["status"], "no_extractable_text")
            self.assertEqual(row["text_method"], "no_extractable_text")

    def test_complete_explicit_ocr_sidecars_are_used(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "inputs"
            source = self._source(
                root, "07. Chess-Thomas-Temperament-and-its-functional-significance.pdf"
            )
            ocr_root = base / "ocr-input"
            pages = ocr_root / "chess_pages"
            pages.mkdir(parents=True)
            (pages / "001.txt").write_text("three recovered words", encoding="utf-8")
            (pages / "002.txt").write_text("and two", encoding="utf-8")
            audit_sources.configure(root, base / "out", ocr_root)
            with (
                mock.patch.object(audit_sources, "file_hash", return_value="0" * 64),
                mock.patch.object(audit_sources, "pdf_pages", return_value=2),
                mock.patch.object(audit_sources, "pdf_words", return_value=0),
            ):
                row = audit_sources.inspect_pdf(("project", source))
            self.assertEqual(row["status"], "ok")
            self.assertEqual(row["words"], 5)
            self.assertEqual(row["text_method"], "page_image_tesseract_ocr")

    def test_incomplete_explicit_ocr_inputs_fail_the_pdf_row(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "inputs"
            source = self._source(
                root, "07. Chess-Thomas-Temperament-and-its-functional-significance.pdf"
            )
            pages = base / "ocr-input/chess_pages"
            pages.mkdir(parents=True)
            (pages / "001.txt").write_text("incomplete", encoding="utf-8")
            audit_sources.configure(root, base / "out", base / "ocr-input")
            with (
                mock.patch.object(audit_sources, "file_hash", return_value="0" * 64),
                mock.patch.object(audit_sources, "pdf_pages", return_value=2),
                mock.patch.object(audit_sources, "pdf_words", return_value=0),
            ):
                row = audit_sources.inspect_pdf(("project", source))
            self.assertEqual(row["status"], "failed")
            self.assertIn("OCR page sidecars are incomplete", row["error"])

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "inputs"
            source = self._source(root, "12 .Measrmnt_of_temp_in_Infancy.pdf")
            ocr_root = base / "ocr-input"
            ocr_root.mkdir()
            (ocr_root / "rothbart_measurement_ocr.pdf").write_bytes(b"short OCR fixture")
            audit_sources.configure(root, base / "out", ocr_root)
            with (
                mock.patch.object(audit_sources, "file_hash", return_value="0" * 64),
                mock.patch.object(audit_sources, "pdf_pages", side_effect=[10, 1]),
                mock.patch.object(audit_sources, "pdf_words", return_value=0),
            ):
                row = audit_sources.inspect_pdf(("project", source))
            self.assertEqual(row["status"], "failed")
            self.assertIn("OCR PDF is incomplete or mismatched", row["error"])

    def test_explicit_ocr_root_is_hashed_as_atomic_run_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "inputs"
            self._source(root, "ordinary.pdf")
            ocr_root = base / "ocr-input"
            ocr_root.mkdir()
            (ocr_root / "sidecar.txt").write_text("lineage", encoding="utf-8")
            output = base / "published-audit"
            with mock.patch.object(
                audit_sources,
                "run_audit",
                return_value={"ocr_requirement_satisfied": True},
            ):
                audit_sources.main(
                    [
                        "--root", str(root),
                        "--ocr-root", str(ocr_root),
                        "--require-ocr",
                        "--out", str(output),
                    ]
                )
            manifest = json.loads(
                (output / "run_completion_manifest.json").read_text(encoding="utf-8")
            )
            inputs = {record["label"]: record for record in manifest["inputs"]}
            self.assertIn("ocr_sidecars", inputs)
            self.assertEqual(inputs["ocr_sidecars"]["files"], 1)


if __name__ == "__main__":
    unittest.main()
