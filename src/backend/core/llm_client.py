"""POC-002: OpenAI client wrapper.

Single import surface for text generation and embeddings used by every
downstream module (vector_store, rag_pipeline, handout_generator,
citation_verifier).
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Copy src/backend/.env.example to .env and fill it in."
        )
    return OpenAI(api_key=api_key)


def generate_text(
    prompt: str,
    system: Optional[str] = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
    max_tokens: int = 1500,
) -> str:
    """Generate a chat completion.

    Args:
        prompt: User message.
        system: Optional system message setting the model's role.
        model: OpenAI chat model. Default gpt-4o-mini for cost.
        temperature: 0.0 deterministic, 1.0 creative. Medical content stays low.
        max_tokens: Cap response length.

    Returns:
        The model's text response.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = _client().chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    text = response.choices[0].message.content or ""
    logger.info(
        "generate_text model=%s tokens_in=%d tokens_out=%d",
        model,
        response.usage.prompt_tokens if response.usage else -1,
        response.usage.completion_tokens if response.usage else -1,
    )
    return text


def embed_text(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Embed a single string. 1536-dim by default (matches Pinecone index).

    Args:
        text: Input string. Must be non-empty.
        model: Embedding model. Default matches POC-005's Pinecone index.

    Returns:
        Float vector.
    """
    if not text or not text.strip():
        raise ValueError("embed_text requires a non-empty string")
    response = _client().embeddings.create(model=model, input=text)
    return response.data[0].embedding


def embed_batch(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    """Embed many strings in one call (cheaper than embed_text per item)."""
    cleaned = [t for t in texts if t and t.strip()]
    if not cleaned:
        return []
    response = _client().embeddings.create(model=model, input=cleaned)
    return [d.embedding for d in response.data]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(generate_text("Say 'hello' in one word.", system="You are terse."))
    vec = embed_text("knee replacement post-operative pain")
    print(f"embedding dim={len(vec)} first5={vec[:5]}")
