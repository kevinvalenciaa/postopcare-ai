"""POC-010: PDF text extraction pipeline.

PyMuPDF for layout-aware text, pdfplumber for tables.
Filters repeated headers/footers and page numbers across pages.
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_PAGE_NUM = re.compile(r"^\s*(?:page\s*)?\d+\s*(?:of\s*\d+)?\s*$", re.IGNORECASE)


@dataclass
class ExtractedPDF:
    path: str
    text: str
    tables: list[list[list[str]]] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def _detect_repeated_lines(pages: list[str], threshold: float = 0.6) -> set[str]:
    """Lines appearing on >threshold of pages are likely headers/footers."""
    counter: Counter[str] = Counter()
    for page_text in pages:
        seen = set()
        for line in page_text.splitlines():
            stripped = line.strip()
            if 0 < len(stripped) < 120 and stripped not in seen:
                counter[stripped] += 1
                seen.add(stripped)
    if not pages:
        return set()
    return {line for line, count in counter.items() if count / len(pages) >= threshold}


def _clean_page(text: str, repeated: set[str]) -> str:
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped in repeated:
            continue
        if _PAGE_NUM.match(stripped):
            continue
        out.append(line.rstrip())
    return "\n".join(out)


def extract(pdf_path: str | Path) -> ExtractedPDF:
    """Extract clean text + tables from a PDF.

    Uses PyMuPDF blocks for multi-column reading order, pdfplumber for tables.
    """
    pdf_path = str(pdf_path)
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise RuntimeError("PyMuPDF not installed. Run: pip install PyMuPDF") from e

    raw_pages: list[str] = []
    doc = fitz.open(pdf_path)
    try:
        metadata = dict(doc.metadata or {})
        for page in doc:
            blocks = page.get_text("blocks")
            blocks_sorted = sorted(blocks, key=lambda b: (round(b[1] / 10), b[0]))
            page_text = "\n".join(b[4] for b in blocks_sorted if isinstance(b[4], str)).strip()
            raw_pages.append(page_text)
    finally:
        doc.close()

    repeated = _detect_repeated_lines(raw_pages)
    cleaned_pages = [_clean_page(p, repeated) for p in raw_pages]
    full_text = "\n\n".join(p for p in cleaned_pages if p.strip())

    tables: list[list[list[str]]] = []
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pp:
            for page in pp.pages:
                page_tables = page.extract_tables() or []
                for t in page_tables:
                    cleaned = [[(cell or "").strip() for cell in row] for row in t if any(row)]
                    if cleaned:
                        tables.append(cleaned)
    except ImportError:
        logger.info("pdfplumber not installed — skipping table extraction")
    except Exception as e:
        logger.warning("pdfplumber extraction failed: %s", e)

    logger.info("Extracted %d pages, %d tables, %d chars from %s",
                len(raw_pages), len(tables), len(full_text), pdf_path)
    return ExtractedPDF(path=pdf_path, text=full_text, tables=tables, metadata=metadata)


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        print("Usage: python -m ingestion.pdf_extractor <path/to/file.pdf>")
        sys.exit(1)
    result = extract(sys.argv[1])
    print(f"=== {result.path} ===")
    print(result.text[:1000])
    print(f"\n[{len(result.tables)} tables extracted]")
