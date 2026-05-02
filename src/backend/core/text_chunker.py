"""POC-004: Sentence-aware text chunker.

Splits long medical documents into overlapping chunks for embedding.
Never breaks mid-sentence. Output is structured for direct ingestion
by vector_store.add_documents.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Optional

_SENT_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


@dataclass
class Chunk:
    text: str
    source_id: str
    chunk_index: int
    start_pos: int
    end_pos: int

    def to_dict(self) -> dict:
        return asdict(self)


def _split_sentences(text: str) -> list[tuple[str, int, int]]:
    sentences = []
    cursor = 0
    for match in _SENT_END.finditer(text):
        end = match.start()
        sentences.append((text[cursor:end].strip(), cursor, end))
        cursor = match.end()
    if cursor < len(text):
        sentences.append((text[cursor:].strip(), cursor, len(text)))
    return [s for s in sentences if s[0]]


def chunk_text(
    text: str,
    source_id: str,
    max_chars: int = 1000,
    overlap_chars: int = 100,
) -> list[Chunk]:
    """Split text into chunks with sentence-boundary awareness.

    Args:
        text: Source text (typically a PubMed abstract or PDF page).
        source_id: Identifier (PMID, URL, file path) — propagated to each chunk.
        max_chars: Hard upper bound per chunk.
        overlap_chars: Chars of trailing context to repeat at the start of the next chunk.

    Returns:
        List of Chunk dataclasses.
    """
    if not text or not text.strip():
        return []

    sentences = _split_sentences(text)
    if not sentences:
        return []

    chunks: list[Chunk] = []
    current_text = ""
    current_start: Optional[int] = None
    current_end = 0

    def emit():
        nonlocal current_text, current_start, current_end
        if not current_text:
            return
        chunks.append(
            Chunk(
                text=current_text,
                source_id=source_id,
                chunk_index=len(chunks),
                start_pos=current_start or 0,
                end_pos=current_end,
            )
        )

    for sentence, s_start, s_end in sentences:
        prospective = (current_text + " " + sentence).strip() if current_text else sentence
        if len(prospective) <= max_chars:
            current_text = prospective
            current_start = s_start if current_start is None else current_start
            current_end = s_end
            continue
        if current_text:
            emit()
            tail = current_text[-overlap_chars:] if overlap_chars else ""
            current_text = (tail + " " + sentence).strip() if tail else sentence
            current_start = max(0, current_end - overlap_chars) if overlap_chars else s_start
            current_end = s_end
        else:
            # Single sentence exceeds max_chars — emit it whole rather than mid-break.
            current_text = sentence
            current_start = s_start
            current_end = s_end
            emit()
            current_text = ""
            current_start = None

    emit()
    return chunks


if __name__ == "__main__":
    sample = (
        "Total knee arthroplasty (TKA) is a common surgical procedure. "
        "Post-operative pain management typically involves a multimodal approach. "
        "Patients are encouraged to begin physical therapy within 24 hours. "
        "Weight bearing as tolerated is generally safe by post-op day one. "
        "Complications include deep vein thrombosis and infection. "
        "Patients should be educated on warning signs requiring immediate attention. "
    ) * 5
    out = chunk_text(sample, source_id="PMID:12345", max_chars=400, overlap_chars=80)
    for c in out:
        print(f"[{c.chunk_index}] ({c.start_pos}-{c.end_pos}, {len(c.text)} chars) {c.text[:60]}...")
