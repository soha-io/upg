#!/usr/bin/env python3
"""Inventory and text-access audit for the four Batch K input archives."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from upg.run_output import atomic_output_run


BATCH_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
ROOT = Path(os.environ.get("UPG_SOURCE_AUDIT_ROOT",
                           BATCH_ROOT / "source-audit-input")).expanduser().resolve()
OUT = BATCH_ROOT / "results" / "source_audit_current" / "v1"
OCR_ROOT: Path | None = None
COLLECTIONS: dict[str, Path] = {}

OCR_SOURCE_MARKERS = {
    "chess-thomas": "page_image_tesseract_ocr",
    "measrmnt_of_temp": "ocrmypdf_tesseract",
}


def configure(root: Path, out: Path, ocr_root: Path | None = None) -> None:
    global ROOT, OUT, OCR_ROOT, COLLECTIONS
    ROOT = root.expanduser().resolve()
    OUT = out.expanduser().resolve()
    OCR_ROOT = ocr_root.expanduser().resolve() if ocr_root is not None else None
    COLLECTIONS = {
        "project": ROOT / "project",
        "data": ROOT / "data",
        "sources_part_1": ROOT / "sources-part-1",
        "sources_part_2": ROOT / "sources-part-2",
    }


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_pages(path: Path) -> int:
    proc = subprocess.run(
        ["pdfinfo", str(path)], capture_output=True, text=True, check=True
    )
    match = re.search(r"^Pages:\s+(\d+)", proc.stdout, re.MULTILINE)
    if not match:
        raise ValueError("pdfinfo returned no page count")
    return int(match.group(1))


def pdf_words(path: Path) -> int:
    proc = subprocess.run(
        ["pdftotext", str(path), "-"], capture_output=True, check=True
    )
    return len(re.findall(rb"\S+", proc.stdout))


def inspect_pdf(item: tuple[str, Path]) -> dict:
    collection, path = item
    row = {
        "collection": collection,
        "relative_path": str(path.relative_to(COLLECTIONS[collection])),
        "bytes": path.stat().st_size,
        "sha256": "",
        "pages": 0,
        "words": 0,
        "text_method": "embedded_text",
        "status": "ok",
        "error": "",
    }
    try:
        row["sha256"] = file_hash(path)
        row["pages"] = pdf_pages(path)
        row["words"] = pdf_words(path)
        lower = path.name.lower()
        if row["words"] == 0 and OCR_ROOT is not None and "chess-thomas" in lower:
            page_texts = sorted((OCR_ROOT / "chess_pages").glob("*.txt"))
            if page_texts:
                if len(page_texts) != row["pages"]:
                    raise ValueError(
                        f"OCR page sidecars are incomplete: expected {row['pages']}, "
                        f"found {len(page_texts)}"
                    )
                page_word_counts = [
                    len(page.read_text(errors="ignore").split()) for page in page_texts
                ]
                if any(count == 0 for count in page_word_counts):
                    raise ValueError("OCR page sidecars include an empty page-text file")
                row["words"] = sum(page_word_counts)
                row["text_method"] = OCR_SOURCE_MARKERS["chess-thomas"]
        elif row["words"] == 0 and OCR_ROOT is not None and "measrmnt_of_temp" in lower:
            ocr_pdf = OCR_ROOT / "rothbart_measurement_ocr.pdf"
            if ocr_pdf.is_file():
                ocr_pages = pdf_pages(ocr_pdf)
                if ocr_pages != row["pages"]:
                    raise ValueError(
                        f"OCR PDF is incomplete or mismatched: expected {row['pages']} pages, "
                        f"found {ocr_pages}"
                    )
                row["words"] = pdf_words(ocr_pdf)
                row["text_method"] = OCR_SOURCE_MARKERS["measrmnt_of_temp"]
        if row["words"] == 0:
            row["status"] = "no_extractable_text"
            row["text_method"] = "no_extractable_text"
    except Exception as exc:  # audit must retain failures
        row["status"] = "failed"
        row["error"] = f"{type(exc).__name__}: {exc}"
    return row


def run_audit() -> dict:
    counts = {}
    pdf_items: list[tuple[str, Path]] = []
    metadata_stubs: list[str] = []
    for name, root in COLLECTIONS.items():
        files = [p for p in root.rglob("*") if p.is_file()]
        if name == "project":
            # Test execution creates these reproducibility-environment files;
            # they were not members of the uploaded ZIP.
            files = [
                p for p in files
                if not any(part in {".venv", ".pytest_cache", "__pycache__"}
                           or part.endswith(".egg-info") for part in p.parts)
                and p != root / "upg" / "uv.lock"
            ]
        counts[name] = len(files)
        metadata_stubs.extend(
            str(p.relative_to(root)) for p in files
            if "__MACOSX" in p.parts or p.name.startswith("._")
        )
        pdf_items.extend(
            (name, p) for p in files
            if p.suffix.lower() == ".pdf"
            and "__MACOSX" not in p.parts and not p.name.startswith("._")
        )

    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(inspect_pdf, item) for item in pdf_items]
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda r: (r["collection"], r["relative_path"]))

    fields = [
        "collection", "relative_path", "bytes", "sha256", "pages", "words",
        "text_method", "status", "error",
    ]
    with (OUT / "pdf_text_audit.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    by_hash: dict[str, list[str]] = {}
    for row in rows:
        if row["sha256"]:
            by_hash.setdefault(row["sha256"], []).append(
                f"{row['collection']}/{row['relative_path']}"
            )
    duplicates = [paths for paths in by_hash.values() if len(paths) > 1]
    summary = {
        "collection_file_counts": counts,
        "all_input_files": sum(counts.values()),
        "research_source_registry_entries": 223,
        "research_source_pdfs": sum(
            r["collection"] in {"sources_part_1", "sources_part_2"} for r in rows
        ),
        "research_source_html_files": 1,
        "substantive_pdf_files_including_data_documentation": len(rows),
        "pdf_pages": sum(int(r["pages"]) for r in rows),
        "pdf_words_after_ocr_fallback": sum(int(r["words"]) for r in rows),
        "pdf_status_counts": {
            status: sum(r["status"] == status for r in rows)
            for status in sorted({r["status"] for r in rows})
        },
        "ocr_fallbacks": [
            {
                "path": f"{r['collection']}/{r['relative_path']}",
                "pages": r["pages"],
                "words": r["words"],
                "method": r["text_method"],
            }
            for r in rows if r["text_method"] in set(OCR_SOURCE_MARKERS.values())
        ],
        "exact_pdf_duplicate_groups": duplicates,
        "metadata_stub_count": len(metadata_stubs),
        "metadata_stubs": metadata_stubs,
        "scope_note": (
            "Word counts are token-like whitespace counts used only to verify text access; "
            "they are not bibliometric measures. Exact duplicates remain registered but "
            "must not be counted as independent evidence."
        ),
    }
    expected_ocr_rows = [
        row for row in rows
        if any(marker in Path(row["relative_path"]).name.lower()
               for marker in OCR_SOURCE_MARKERS)
    ]
    summary["expected_ocr_source_status"] = [
        {
            "path": f"{row['collection']}/{row['relative_path']}",
            "status": row["status"],
            "method": row["text_method"],
        }
        for row in expected_ocr_rows
    ]
    summary["ocr_requirement_satisfied"] = (
        len(expected_ocr_rows) == len(OCR_SOURCE_MARKERS)
        and all(
            row["status"] == "ok"
            and row["text_method"] in set(OCR_SOURCE_MARKERS.values())
            for row in expected_ocr_rows
        )
    )
    with (OUT / "source_audit_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=ROOT,
        help="extracted input root containing project/, data/, sources-part-1/, and sources-part-2/",
    )
    parser.add_argument("--out", type=Path, default=OUT,
                        help="new, nonexistent versioned audit output directory")
    parser.add_argument(
        "--ocr-root",
        type=Path,
        default=None,
        help=(
            "optional immutable input directory containing chess_pages/*.txt and "
            "rothbart_measurement_ocr.pdf; it is hashed into run lineage"
        ),
    )
    parser.add_argument(
        "--require-ocr",
        action="store_true",
        help="abort publication unless both known image-only sources use complete OCR sidecars",
    )
    args = parser.parse_args(argv)
    if args.require_ocr and args.ocr_root is None:
        parser.error("--require-ocr requires an explicit --ocr-root")
    ocr_root = args.ocr_root.expanduser().resolve() if args.ocr_root is not None else None
    if ocr_root is not None and not ocr_root.is_dir():
        parser.error(f"OCR input root is not a directory: {ocr_root}")
    configure(args.root, args.out, ocr_root)
    missing = [str(path) for path in COLLECTIONS.values() if not path.is_dir()]
    if missing:
        parser.error("missing extracted collection directory/directories: " + ", ".join(missing))
    final_out = args.out.expanduser().resolve()
    protected = (
        BATCH_ROOT / "evidence" / "audit",
        BATCH_ROOT / "results" / "real_data",
    )
    inputs = {name: path for name, path in COLLECTIONS.items()}
    inputs["audit_script"] = Path(__file__)
    inputs["output_helper"] = REPO_ROOT / "src" / "upg" / "run_output.py"
    inputs["project_metadata"] = REPO_ROOT / "pyproject.toml"
    inputs["environment_lock"] = REPO_ROOT / "uv.lock"
    if ocr_root is not None:
        inputs["ocr_sidecars"] = ocr_root
    try:
        with atomic_output_run(
            final_out,
            protected_dirs=protected,
            inputs=inputs,
            metadata={"analysis_id": "batch-k-source-audit-v1"},
        ) as temporary:
            configure(args.root, temporary, ocr_root)
            summary = run_audit()
            if args.require_ocr and not summary["ocr_requirement_satisfied"]:
                raise RuntimeError(
                    "required OCR sidecars did not produce successful text access for both "
                    "known image-only sources"
                )
    except (FileExistsError, PermissionError, RuntimeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
