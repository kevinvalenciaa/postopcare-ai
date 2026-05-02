"""POC-014: LLM-based citation verifier.

For each (claim, source_text) pair, asks an LLM whether the source
supports the claim. Produces a verdict, confidence, and rationale.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass, field
from typing import Optional

from core.llm_client import generate_text

logger = logging.getLogger(__name__)

VERIFY_SYSTEM = (
    "You are a meticulous medical fact-checker. Given a CLAIM and a SOURCE TEXT, "
    "decide whether the source supports the claim. Reply ONLY with valid JSON in the form: "
    '{"verdict": "support|partial|contradict|unrelated", "confidence": 0.0-1.0, "rationale": "..."}. '
    "Do not include any other text."
)

CONFIDENCE_THRESHOLD = 0.8


@dataclass
class VerificationResult:
    claim: str
    source_id: str
    verdict: str
    confidence: float
    rationale: str
    flagged: bool = False

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "source_id": self.source_id,
            "verdict": self.verdict,
            "confidence": round(self.confidence, 3),
            "rationale": self.rationale,
            "flagged": self.flagged,
        }


def _build_prompt(claim: str, source_text: str) -> str:
    return f"CLAIM:\n{claim}\n\nSOURCE TEXT:\n{source_text}\n\nReply with JSON only."


def _parse_response(raw: str) -> dict:
    raw = raw.strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        raw = match.group(0)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"verdict": "unrelated", "confidence": 0.0, "rationale": "Failed to parse model output."}


def verify_claim(claim: str, source_text: str, source_id: str) -> VerificationResult:
    """Verify a single claim against a single source."""
    response = generate_text(
        prompt=_build_prompt(claim, source_text),
        system=VERIFY_SYSTEM,
        temperature=0.0,
        max_tokens=400,
    )
    parsed = _parse_response(response)
    confidence = float(parsed.get("confidence", 0.0) or 0.0)
    return VerificationResult(
        claim=claim,
        source_id=source_id,
        verdict=parsed.get("verdict", "unrelated"),
        confidence=confidence,
        rationale=parsed.get("rationale", ""),
        flagged=confidence < CONFIDENCE_THRESHOLD or parsed.get("verdict") in {"contradict", "unrelated"},
    )


async def _verify_async(claim: str, source_text: str, source_id: str) -> VerificationResult:
    return await asyncio.to_thread(verify_claim, claim, source_text, source_id)


def verify_all(pairs: list[tuple[str, str, str]]) -> list[VerificationResult]:
    """Verify many (claim, source_text, source_id) tuples concurrently."""
    async def _gather():
        tasks = [_verify_async(c, s, sid) for c, s, sid in pairs]
        return await asyncio.gather(*tasks)
    return asyncio.run(_gather())


def report(results: list[VerificationResult]) -> str:
    """Render results as a Markdown table."""
    lines = [
        "## Citation Verification Report",
        "",
        f"Total claims: {len(results)}  |  Flagged: {sum(1 for r in results if r.flagged)}",
        "",
        "| # | Verdict | Confidence | Source | Claim |",
        "|---|---------|------------|--------|-------|",
    ]
    for i, r in enumerate(results, start=1):
        flag = " ⚠️" if r.flagged else ""
        claim_preview = r.claim[:60].replace("|", "\\|")
        lines.append(
            f"| {i}{flag} | {r.verdict} | {r.confidence:.2f} | {r.source_id} | {claim_preview} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = verify_all([
        ("Patients can return to driving after 2 weeks following total knee replacement.",
         "Most patients are cleared to drive 4-6 weeks after total knee replacement, depending on which knee was replaced.",
         "PMID:1"),
        ("Acetaminophen is a common first-line analgesic post-op.",
         "Acetaminophen is commonly used as a first-line analgesic in multimodal post-operative pain management.",
         "PMID:2"),
    ])
    print(report(results))
