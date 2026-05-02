"""POC-005: Pinecone-backed vector store.

Wraps Pinecone for add/search/delete with OpenAI embeddings.
Falls back to an in-memory cosine-similarity store when Pinecone
is unavailable (no API key) so dev/tests can run without cloud access.
"""

from __future__ import annotations

import logging
import os
import uuid
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

from core.llm_client import embed_batch, embed_text
from core.text_chunker import Chunk

load_dotenv()
logger = logging.getLogger(__name__)

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "postopcare-rag")
EMBEDDING_DIM = 1536


@dataclass
class SearchResult:
    id: str
    score: float
    text: str
    metadata: dict


class _InMemoryStore:
    """Fallback used when PINECONE_API_KEY is missing."""

    def __init__(self):
        self.vectors: dict[str, tuple[list[float], dict]] = {}

    def upsert(self, vectors):
        for v in vectors:
            self.vectors[v["id"]] = (v["values"], v["metadata"])

    def query(self, vector, top_k, filter=None):
        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            na = sum(x * x for x in a) ** 0.5
            nb = sum(x * x for x in b) ** 0.5
            return dot / (na * nb) if na and nb else 0.0

        scored = []
        for vid, (vec, meta) in self.vectors.items():
            if filter and any(meta.get(k) != v for k, v in filter.items()):
                continue
            scored.append((vid, cosine(vector, vec), meta))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def delete(self, ids):
        for i in ids:
            self.vectors.pop(i, None)


def _get_index():
    """Return a Pinecone index handle, or fall back to in-memory store."""
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        logger.warning("PINECONE_API_KEY not set — using in-memory fallback (data is ephemeral).")
        if not hasattr(_get_index, "_fallback"):
            _get_index._fallback = _InMemoryStore()
        return _get_index._fallback
    try:
        from pinecone import Pinecone, ServerlessSpec
    except ImportError as e:
        raise RuntimeError("pinecone-client not installed. Run: pip install pinecone-client") from e
    pc = Pinecone(api_key=api_key)
    existing = {idx["name"] for idx in pc.list_indexes()}
    if INDEX_NAME not in existing:
        logger.info("Creating Pinecone index %s (dim=%d, cosine)", INDEX_NAME, EMBEDDING_DIM)
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return pc.Index(INDEX_NAME)


def add_documents(chunks: list[Chunk], procedure: str, batch_size: int = 100) -> list[str]:
    """Embed and upsert chunks. Returns the list of vector IDs created."""
    if not chunks:
        return []
    index = _get_index()
    ids = [f"{procedure}__{c.source_id}__{c.chunk_index}__{uuid.uuid4().hex[:8]}" for c in chunks]
    embeddings = embed_batch([c.text for c in chunks])
    payload = []
    for cid, chunk, vec in zip(ids, chunks, embeddings):
        payload.append({
            "id": cid,
            "values": vec,
            "metadata": {
                "text": chunk.text,
                "source_id": chunk.source_id,
                "chunk_index": chunk.chunk_index,
                "procedure": procedure,
            },
        })
    for start in range(0, len(payload), batch_size):
        batch = payload[start:start + batch_size]
        if isinstance(index, _InMemoryStore):
            index.upsert(batch)
        else:
            index.upsert(vectors=batch)
    logger.info("Upserted %d chunks for procedure=%s", len(payload), procedure)
    return ids


def search(query: str, top_k: int = 5, procedure: Optional[str] = None) -> list[SearchResult]:
    """Embed the query and return the top-k most similar chunks."""
    index = _get_index()
    qvec = embed_text(query)
    filter_dict = {"procedure": procedure} if procedure else None

    if isinstance(index, _InMemoryStore):
        raw = index.query(qvec, top_k=top_k, filter=filter_dict)
        return [SearchResult(id=vid, score=score, text=meta.get("text", ""), metadata=meta)
                for vid, score, meta in raw]

    response = index.query(vector=qvec, top_k=top_k, filter=filter_dict, include_metadata=True)
    matches = response.get("matches", []) if isinstance(response, dict) else response.matches
    out = []
    for m in matches:
        meta = m["metadata"] if isinstance(m, dict) else m.metadata
        out.append(SearchResult(
            id=m["id"] if isinstance(m, dict) else m.id,
            score=m["score"] if isinstance(m, dict) else m.score,
            text=(meta or {}).get("text", ""),
            metadata=meta or {},
        ))
    return out


def delete(ids: list[str]) -> None:
    index = _get_index()
    if isinstance(index, _InMemoryStore):
        index.delete(ids)
    else:
        index.delete(ids=ids)
    logger.info("Deleted %d vectors", len(ids))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample = [
        Chunk(text="Pain management after total knee replacement involves multimodal analgesia.",
              source_id="PMID:1", chunk_index=0, start_pos=0, end_pos=80),
        Chunk(text="Physical therapy should begin within 24 hours of surgery.",
              source_id="PMID:1", chunk_index=1, start_pos=80, end_pos=140),
        Chunk(text="Wound care: keep the incision clean and dry. Watch for redness or drainage.",
              source_id="PMID:2", chunk_index=0, start_pos=0, end_pos=80),
    ]
    add_documents(sample, procedure="total-knee-replacement")
    results = search("how do I manage pain after surgery?", top_k=2, procedure="total-knee-replacement")
    for r in results:
        print(f"  {r.score:.3f}  {r.text}")
