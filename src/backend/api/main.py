"""FastAPI composition root for PostOpCare RAG backend.

Endpoints:
  GET  /api/health                        — readiness probe
  GET  /api/procedures                    — list procedures
  POST /api/generate-section              — single section (RAG)
  POST /api/generate-handout              — full multi-section handout
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.citation_formatter import build_reference_list
from core.rag_pipeline import generate_handout_section
from core.readability import score as readability_score
from db.models import Procedure, get_session, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PostOpCare RAG API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    init_db()


SECTION_ORDER = [
    ("overview", "Overview"),
    ("pain_management", "Pain Management"),
    ("activity_restrictions", "Activity Restrictions"),
    ("wound_care", "Wound Care"),
    ("warning_signs", "Warning Signs"),
    ("follow_up", "Follow-Up Care"),
]


class ProcedureOut(BaseModel):
    id: str
    name: str
    specialty: str
    description: Optional[str] = None


class GenerateSectionRequest(BaseModel):
    procedure_id: str = Field(..., description="Procedure slug, e.g. 'total-knee-replacement'")
    section: str = Field(..., description="Prompt template name, e.g. 'pain_management'")
    top_k: int = 5


class CitationOut(BaseModel):
    id: int
    authors: str = ""
    title: str = ""
    journal: str = ""
    year: int = 0
    pmid: Optional[str] = None


class SectionOut(BaseModel):
    id: str
    type: str
    title: str
    content: str
    citationIds: list[int]


class QualityMetricsOut(BaseModel):
    overallScore: int
    readabilityGrade: float
    citationCoverage: int
    completeness: int
    safetyCheck: str


class HandoutOut(BaseModel):
    id: str
    procedure: str
    generatedAt: str
    title: str
    sections: list[SectionOut]
    citations: list[CitationOut]
    qualityMetrics: QualityMetricsOut


@app.get("/api/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.get("/api/procedures", response_model=list[ProcedureOut])
def list_procedures():
    session = get_session()
    try:
        rows = session.query(Procedure).order_by(Procedure.specialty, Procedure.name).all()
        return [
            ProcedureOut(id=p.slug, name=p.name, specialty=p.specialty, description=p.description)
            for p in rows
        ]
    finally:
        session.close()


@app.post("/api/generate-section")
def generate_section(req: GenerateSectionRequest):
    try:
        result = generate_handout_section(req.procedure_id, req.section, top_k=req.top_k)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result.to_dict()


def _section_type_to_template(section_type: str) -> str:
    return section_type.replace("-", "_")


def _build_quality_metrics(sections_text: str, citation_count: int, sections_count: int) -> QualityMetricsOut:
    rb = readability_score(sections_text)
    coverage = min(100, int((citation_count / max(1, sections_count)) * 25))
    completeness = min(100, int((sections_count / len(SECTION_ORDER)) * 100))
    overall = int((coverage + completeness + max(0, 100 - rb.grade_level * 8)) / 3)
    return QualityMetricsOut(
        overallScore=overall,
        readabilityGrade=round(rb.grade_level, 1),
        citationCoverage=coverage,
        completeness=completeness,
        safetyCheck="passed" if rb.grade_level <= 9 else "flagged",
    )


@app.post("/api/generate-handout", response_model=HandoutOut)
def generate_handout(req: GenerateSectionRequest):
    """Generates all standard sections for a procedure. Reuses the section
    request shape for simplicity — `section` is ignored."""
    session = get_session()
    try:
        proc = session.query(Procedure).filter_by(slug=req.procedure_id).first()
        if not proc:
            raise HTTPException(status_code=404, detail=f"Unknown procedure {req.procedure_id}")
        title = f"After Your {proc.name}: Recovery Guide"
    finally:
        session.close()

    sections_out: list[SectionOut] = []
    citation_meta: dict[str, dict] = {}
    full_text_parts: list[str] = []

    for section_type, section_title in SECTION_ORDER:
        try:
            r = generate_handout_section(req.procedure_id, section_type, top_k=req.top_k)
        except ValueError as e:
            logger.warning("Skipping section %s: %s", section_type, e)
            continue
        section_citation_ids = []
        for c in r.citations:
            sid = c.get("source_id") or "unknown"
            if sid not in citation_meta:
                citation_meta[sid] = {
                    "id": len(citation_meta) + 1,
                    "pmid": sid.replace("PMID:", "") if isinstance(sid, str) and sid.startswith("PMID:") else None,
                    "title": c.get("snippet", "")[:120],
                    "authors": "",
                    "journal": "",
                    "year": 0,
                }
            section_citation_ids.append(citation_meta[sid]["id"])
        sections_out.append(SectionOut(
            id=str(uuid.uuid4()),
            type=section_type.replace("_", "-"),
            title=section_title,
            content=r.text,
            citationIds=sorted(set(section_citation_ids)),
        ))
        full_text_parts.append(r.text)

    citations_out = [CitationOut(**meta) for meta in sorted(citation_meta.values(), key=lambda m: m["id"])]
    metrics = _build_quality_metrics(
        sections_text="\n\n".join(full_text_parts),
        citation_count=len(citations_out),
        sections_count=len(sections_out),
    )

    return HandoutOut(
        id=str(uuid.uuid4()),
        procedure=req.procedure_id,
        generatedAt=datetime.now(timezone.utc).isoformat(),
        title=title,
        sections=sections_out,
        citations=citations_out,
        qualityMetrics=metrics,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
