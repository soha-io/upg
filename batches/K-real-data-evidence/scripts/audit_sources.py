#!/usr/bin/env python3
"""Inventory and text-access audit for the four Batch K input archives."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path("/workspace/batch-k-run/work")
OUT = ROOT / "audit"
OUT.mkdir(parents=True, exist_ok=True)
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
        if row["words"] == 0 and "chess-thomas" in lower:
            page_texts = sorted((OUT / "ocr" / "chess_pages").glob("*.txt"))
            row["words"] = sum(len(p.read_text(errors="ignore").split()) for p in page_texts)
            row["text_method"] = "page_image_tesseract_ocr"
        elif row["words"] == 0 and "measrmnt_of_temp" in lower:
            ocr_pdf = OUT / "ocr" / "rothbart_measurement_ocr.pdf"
            row["words"] = pdf_words(ocr_pdf)
            row["text_method"] = "ocrmypdf_tesseract"
        if row["words"] == 0:
            row["status"] = "no_extractable_text"
    except Exception as exc:  # audit must retain failures
        row["status"] = "failed"
        row["error"] = f"{type(exc).__name__}: {exc}"
    return row


def main() -> None:
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
            for r in rows if "ocr" in r["text_method"]
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
    with (OUT / "source_audit_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
