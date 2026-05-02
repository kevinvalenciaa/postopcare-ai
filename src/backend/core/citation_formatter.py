"""POC-008: AMA citation formatter.

Converts PubMed (or generic) article metadata into AMA-style references.
Handles missing fields gracefully — a record with just a title still produces output.
"""

from __future__ import annotations

from typing import Optional


def _format_authors(authors: list[str], max_authors: int = 6) -> str:
    """AMA: list up to 6 authors, then 'et al.'. Format: 'Last FM, Last FM, ...'."""
    if not authors:
        return ""
    formatted = []
    for full in authors[:max_authors]:
        parts = full.strip().split()
        if len(parts) >= 2:
            last = parts[-1]
            initials = "".join(p[0] for p in parts[:-1] if p)
            formatted.append(f"{last} {initials}")
        else:
            formatted.append(full.strip())
    suffix = ", et al" if len(authors) > max_authors else ""
    return ", ".join(formatted) + suffix


def _format_year(date: str) -> str:
    if not date:
        return ""
    return date.split("-")[0].strip() if "-" in date else date.split()[0].strip()


def format_reference(meta: dict) -> str:
    """Build a single AMA reference list entry from article metadata.

    Expected (any may be missing):
      title, authors (list), journal, pub_date, volume, issue, pages, pmid, doi

    Example output:
      Smith JA, Doe RB. Pain management after total knee arthroplasty.
      J Bone Joint Surg. 2022;104(5):420-428. doi:10.1234/abcd. PMID: 12345678.
    """
    parts = []
    authors = _format_authors(meta.get("authors") or [])
    if authors:
        parts.append(f"{authors}.")
    title = (meta.get("title") or "").strip()
    if title:
        parts.append(title.rstrip(".") + ".")
    journal = (meta.get("journal") or "").strip()
    year = _format_year(meta.get("pub_date") or "")
    journal_segment = ""
    if journal:
        journal_segment = journal
        if year:
            journal_segment += f". {year}"
        vol = meta.get("volume")
        issue = meta.get("issue")
        pages = meta.get("pages")
        locator = ""
        if vol:
            locator = f";{vol}"
            if issue:
                locator += f"({issue})"
        if pages:
            locator += f":{pages}"
        if locator:
            journal_segment += locator
        parts.append(journal_segment + ".")
    elif year:
        parts.append(f"{year}.")
    doi = (meta.get("doi") or "").strip()
    if doi:
        parts.append(f"doi:{doi}.")
    pmid = (meta.get("pmid") or "").strip()
    if pmid:
        parts.append(f"PMID: {pmid}.")
    return " ".join(parts).strip()


def format_inline(index: int) -> str:
    """Inline citation marker. AMA uses superscript numbers; we emit ^N for caller to render."""
    return f"^{index}"


def build_reference_list(metas: list[dict]) -> list[str]:
    """Numbered reference list: '1. Smith JA. ... 2. Jones BC. ...'"""
    return [f"{i + 1}. {format_reference(m)}" for i, m in enumerate(metas)]


def to_markdown_section(metas: list[dict], heading: str = "References") -> str:
    """Render the reference list as a Markdown section."""
    lines = [f"## {heading}", ""]
    lines.extend(build_reference_list(metas))
    return "\n".join(lines)


if __name__ == "__main__":
    samples = [
        {
            "title": "Pain management after total knee arthroplasty: a systematic review",
            "authors": ["John A Smith", "Robert B Doe", "Carol C White"],
            "journal": "J Bone Joint Surg",
            "pub_date": "2022-05-15",
            "volume": "104",
            "issue": "5",
            "pages": "420-428",
            "pmid": "12345678",
            "doi": "10.1234/jbjs.abcd",
        },
        {"title": "Minimal record with only a title", "pmid": "99999999"},
    ]
    for line in build_reference_list(samples):
        print(line)
