"""POC-007: End-to-end RAG pipeline.

generate_handout_section(procedure, section) ->
  query vector store -> retrieve top-k chunks -> format prompt with context
  -> call LLM -> return text + citations + retrieval metadata
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from core.llm_client import generate_text
from core.prompt_manager import PromptManager
from core.vector_store import SearchResult, search

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are a medical writer producing patient-friendly post-operative handouts. "
    "Write at a 6th-8th grade reading level. Be specific and actionable. "
    "Cite supporting evidence inline using [^N] markers where N matches the numbered "
    "source list provided. Never invent citations."
)


@dataclass
class SectionResult:
    procedure: str
    section: str
    text: str
    citations: list[dict] = field(default_factory=list)  # source_id + snippet per citation
    retrieved_chunks: list[dict] = field(default_factory=list)
    model: str = "gpt-4o-mini"

    def to_dict(self) -> dict:
        return {
            "procedure": self.procedure,
            "section": self.section,
            "text": self.text,
            "citations": self.citations,
            "retrieved_chunks": self.retrieved_chunks,
            "model": self.model,
        }


def _format_context(results: list[SearchResult]) -> tuple[str, list[dict]]:
    """Number sources [1], [2], ... and return both context block and citation metadata."""
    blocks = []
    citations = []
    for i, r in enumerate(results, start=1):
        blocks.append(f"[Source {i}] (id={r.metadata.get('source_id')})\n{r.text}")
        citations.append({
            "inline_number": i,
            "source_id": r.metadata.get("source_id"),
            "snippet": r.text[:300],
            "score": r.score,
        })
    return "\n\n".join(blocks), citations


def generate_handout_section(
    procedure: str,
    section: str,
    top_k: int = 5,
    system_prompt: Optional[str] = None,
    extra_vars: Optional[dict] = None,
) -> SectionResult:
    """Generate one handout section by retrieving evidence and prompting the LLM.

    Args:
        procedure: Procedure slug (e.g. 'total-knee-replacement') used as Pinecone filter.
        section: Prompt template name (must exist in src/backend/prompts/).
        top_k: Number of chunks to retrieve.
        system_prompt: Override default medical-writer instructions.
        extra_vars: Additional template variables beyond procedure_name and context.

    Returns:
        SectionResult with text, citations, and retrieval trace.
    """
    pm = PromptManager()
    if not pm.template_exists(section):
        raise ValueError(
            f"Prompt template '{section}' not found. Available: {pm.list_templates()}"
        )

    query = f"{procedure.replace('-', ' ')} {section.replace('_', ' ')}"
    logger.info("rag.search procedure=%s section=%s top_k=%d", procedure, section, top_k)
    results = search(query, top_k=top_k, procedure=procedure)
    logger.info("rag.retrieved %d chunks", len(results))

    context, citations = _format_context(results)

    template_vars = {
        "procedure_name": procedure.replace("-", " ").title(),
        "context": context or "(no retrieved context — generate from general medical knowledge)",
        "recovery_timeline": "varies by patient",
        "pain_level": "moderate",
        "recovery_days": "2-6 weeks",
        "incision_description": "see surgeon notes",
        "healing_days": "10-14",
        "first_followup": "1-2 weeks post-op",
    }
    if extra_vars:
        template_vars.update(extra_vars)

    try:
        prompt = pm.get_prompt(section, **template_vars)
    except KeyError as e:
        raise ValueError(
            f"Template '{section}' missing variable {e}. Provide via extra_vars."
        ) from e

    logger.info("rag.generate prompt_chars=%d", len(prompt))
    text = generate_text(prompt=prompt, system=system_prompt or DEFAULT_SYSTEM_PROMPT)

    return SectionResult(
        procedure=procedure,
        section=section,
        text=text,
        citations=citations,
        retrieved_chunks=[{"id": r.id, "score": r.score, "source_id": r.metadata.get("source_id")} for r in results],
    )


if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--procedure", default="total-knee-replacement")
    parser.add_argument("--section", default="pain_management")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    result = generate_handout_section(args.procedure, args.section, top_k=args.top_k)
    print("=" * 60)
    print(result.text)
    print("=" * 60)
    print(f"Citations: {len(result.citations)}, Retrieved: {len(result.retrieved_chunks)}")
