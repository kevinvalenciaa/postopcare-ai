"""POC-012: Hybrid search (BM25 + semantic) with Reciprocal Rank Fusion.

Combines exact-keyword matching (BM25) with semantic similarity
(vector_store) so medical terminology and conceptual queries both
return useful results.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from core.vector_store import SearchResult, search as semantic_search

logger = logging.getLogger(__name__)

_TOKEN = re.compile(r"\b[a-zA-Z][a-zA-Z0-9-]+\b")
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "for", "with",
    "to", "from", "by", "is", "are", "was", "were", "be", "been", "this", "that",
    "i", "you", "we", "they", "it", "have", "has", "had", "do", "does", "did",
}


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN.findall(text) if t.lower() not in _STOPWORDS]


@dataclass
class HybridResult:
    id: str
    score: float
    text: str
    metadata: dict
    sources: list[str]  # ['bm25', 'semantic'] indicating which methods ranked it


def _bm25_search(query: str, corpus: list[SearchResult], top_k: int) -> list[tuple[SearchResult, float]]:
    try:
        from rank_bm25 import BM25Okapi
    except ImportError as e:
        raise RuntimeError("rank_bm25 not installed. Run: pip install rank_bm25") from e
    tokenized = [tokenize(c.text) for c in corpus]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(zip(corpus, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


def _rrf_fuse(rankings: list[list[str]], k: int = 60) -> dict[str, float]:
    """Reciprocal Rank Fusion: each item gets 1/(k + rank) summed across rankings."""
    fused: dict[str, float] = {}
    for ranking in rankings:
        for rank, item_id in enumerate(ranking, start=1):
            fused[item_id] = fused.get(item_id, 0.0) + 1.0 / (k + rank)
    return fused


def hybrid_search(
    query: str,
    procedure: str | None = None,
    top_k: int = 5,
    candidate_pool: int = 20,
    semantic_weight: float = 0.6,
) -> list[HybridResult]:
    """Run semantic + BM25 over the same retrieval pool, fuse with RRF.

    Args:
        query: Natural-language or keyword query.
        procedure: Optional metadata filter forwarded to the vector store.
        top_k: Final number of results to return.
        candidate_pool: How many semantic results to bring in for BM25 to re-rank over.
        semantic_weight: 0..1; higher favors semantic ranks during RRF.

    Returns:
        Top-k HybridResult objects.
    """
    semantic_pool = semantic_search(query, top_k=candidate_pool, procedure=procedure)
    if not semantic_pool:
        return []

    semantic_ranking = [r.id for r in semantic_pool]
    bm25_ranked = _bm25_search(query, semantic_pool, top_k=candidate_pool)
    bm25_ranking = [r.id for r, _ in bm25_ranked]

    fused = _rrf_fuse([semantic_ranking, bm25_ranking])
    semantic_set = set(semantic_ranking[:top_k])
    bm25_set = set(bm25_ranking[:top_k])

    by_id = {r.id: r for r in semantic_pool}
    sorted_ids = sorted(fused, key=lambda i: fused[i], reverse=True)[:top_k]

    out: list[HybridResult] = []
    for rid in sorted_ids:
        base = by_id[rid]
        sources = []
        if rid in semantic_set:
            sources.append("semantic")
        if rid in bm25_set:
            sources.append("bm25")
        out.append(HybridResult(
            id=base.id,
            score=fused[rid] * (1.0 + semantic_weight if "semantic" in sources else 1.0),
            text=base.text,
            metadata=base.metadata,
            sources=sources or ["semantic"],
        ))
    logger.info("hybrid_search query=%r returned %d results", query, len(out))
    return out


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    out = hybrid_search("acetaminophen dosage after surgery", top_k=3)
    for r in out:
        print(f"  [{','.join(r.sources)}] score={r.score:.3f}  {r.text[:80]}")
