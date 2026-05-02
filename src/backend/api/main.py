"""FastAPI composition root for PostOpCare RAG backend.

Endpoints:
  GET  /api/health                        — readiness probe
  GET  /api/procedures                    — list procedures
  POST /api/generate-section              — single section (RAG)
  POST /api/generate-handout              — full multi-section handout (persists, returns slug)
  GET  /api/handouts/{slug}               — public handout fetch by slug
  GET  /api/handouts/{slug}/qr.png        — QR code encoding the public URL
"""

from __future__ import annotations

import io
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

import qrcode
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from nanoid import generate as generate_nanoid
from pydantic import BaseModel, Field

from core.rag_pipeline import generate_handout_section
from core.readability import score as readability_score
from db.models import (
    Citation,
    Document,
    Handout,
    HandoutSection,
    Procedure,
    get_session,
    init_db,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:3000")
SLUG_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SLUG_SIZE = 12

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
    slug: Optional[str] = None
    publicUrl: Optional[str] = None
    qrUrl: Optional[str] = None


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


def _new_slug() -> str:
    return generate_nanoid(SLUG_ALPHABET, SLUG_SIZE)


def _ensure_document(session, source_id: str, snippet: str) -> Document:
    """Find or create a Document row for a citation source. Stub-creates rows for
    chunk source_ids that haven't been ingested into the documents table yet."""
    if not source_id:
        source_id = "unknown"
    doc = session.query(Document).filter_by(source_id=source_id).first()
    if doc:
        return doc
    doc = Document(
        source_type="rag-snippet",
        source_id=source_id,
        title=snippet[:200] if snippet else None,
        raw_text=snippet,
    )
    session.add(doc)
    session.flush()
    return doc


def _persist_handout(
    session,
    procedure: Procedure,
    sections: list[SectionOut],
    citations: list[CitationOut],
    citation_source_by_id: dict[int, tuple[str, str]],
    metrics: QualityMetricsOut,
) -> Handout:
    """Insert handout + sections + citations. Returns the saved Handout."""
    for _ in range(5):
        slug = _new_slug()
        if not session.query(Handout).filter_by(slug=slug).first():
            break
    else:
        raise RuntimeError("Could not allocate a unique slug after 5 attempts")

    handout = Handout(
        procedure_id=procedure.id,
        slug=slug,
        model_version="gpt-4o-mini",
        status="published",
        published=True,
    )
    session.add(handout)
    session.flush()

    for section in sections:
        section_row = HandoutSection(
            handout_id=handout.id,
            section_name=section.type,
            body_md=section.content,
            body_html=None,
            readability_grade=metrics.readabilityGrade,
            readability_ease=None,
        )
        session.add(section_row)
        session.flush()
        for cid in section.citationIds:
            source_id, snippet = citation_source_by_id.get(cid, ("unknown", ""))
            doc = _ensure_document(session, source_id, snippet)
            session.add(Citation(
                section_id=section_row.id,
                document_id=doc.id,
                inline_number=cid,
                snippet=snippet,
            ))
    session.commit()
    session.refresh(handout)
    return handout


def _handout_to_dto(session, handout: Handout) -> HandoutOut:
    procedure = session.query(Procedure).filter_by(id=handout.procedure_id).first()
    proc_name = procedure.name if procedure else handout.procedure_id
    sections_out: list[SectionOut] = []
    full_text: list[str] = []
    citation_map: dict[int, CitationOut] = {}

    for section_row in handout.sections:
        section_citation_ids: list[int] = []
        for cit in section_row.citations:
            section_citation_ids.append(cit.inline_number)
            if cit.inline_number not in citation_map:
                doc = cit.document
                citation_map[cit.inline_number] = CitationOut(
                    id=cit.inline_number,
                    authors=", ".join(doc.authors) if doc and doc.authors else "",
                    title=(doc.title if doc and doc.title else cit.snippet or "")[:200],
                    journal=doc.journal if doc and doc.journal else "",
                    year=int(doc.pub_date.split("-")[0]) if doc and doc.pub_date and doc.pub_date.split("-")[0].isdigit() else 0,
                    pmid=doc.source_id.replace("PMID:", "") if doc and doc.source_id and doc.source_id.startswith("PMID:") else None,
                )
        sections_out.append(SectionOut(
            id=str(uuid.uuid4()),
            type=section_row.section_name.replace("_", "-"),
            title=next((title for slug, title in SECTION_ORDER if slug == section_row.section_name), section_row.section_name),
            content=section_row.body_md,
            citationIds=sorted(set(section_citation_ids)),
        ))
        full_text.append(section_row.body_md)

    metrics = _build_quality_metrics(
        sections_text="\n\n".join(full_text),
        citation_count=len(citation_map),
        sections_count=len(sections_out),
    )
    public_url = f"{PUBLIC_BASE_URL.rstrip('/')}/h/{handout.slug}"
    return HandoutOut(
        id=str(handout.id),
        procedure=procedure.slug if procedure else handout.procedure_id,
        generatedAt=handout.generated_at.replace(tzinfo=timezone.utc).isoformat(),
        title=f"After Your {proc_name}: Recovery Guide",
        sections=sections_out,
        citations=sorted(citation_map.values(), key=lambda c: c.id),
        qualityMetrics=metrics,
        slug=handout.slug,
        publicUrl=public_url,
        qrUrl=f"/api/handouts/{handout.slug}/qr.png",
    )


@app.post("/api/generate-handout", response_model=HandoutOut)
def generate_handout(req: GenerateSectionRequest):
    """Generate all sections, persist to DB, return DTO with slug + public URL + QR path."""
    session = get_session()
    try:
        proc = session.query(Procedure).filter_by(slug=req.procedure_id).first()
        if not proc:
            raise HTTPException(status_code=404, detail=f"Unknown procedure {req.procedure_id}")

        sections_out: list[SectionOut] = []
        citation_meta: dict[str, dict] = {}
        citation_source_by_id: dict[int, tuple[str, str]] = {}
        full_text_parts: list[str] = []

        for section_type, _section_title in SECTION_ORDER:
            try:
                r = generate_handout_section(req.procedure_id, section_type, top_k=req.top_k)
            except ValueError as e:
                logger.warning("Skipping section %s: %s", section_type, e)
                continue
            section_citation_ids: list[int] = []
            for c in r.citations:
                sid = c.get("source_id") or "unknown"
                snippet = c.get("snippet", "")
                if sid not in citation_meta:
                    cid = len(citation_meta) + 1
                    citation_meta[sid] = {"id": cid}
                    citation_source_by_id[cid] = (sid, snippet)
                section_citation_ids.append(citation_meta[sid]["id"])
            sections_out.append(SectionOut(
                id=str(uuid.uuid4()),
                type=section_type.replace("_", "-"),
                title=next((t for s, t in SECTION_ORDER if s == section_type), section_type),
                content=r.text,
                citationIds=sorted(set(section_citation_ids)),
            ))
            full_text_parts.append(r.text)

        citations_out = [
            CitationOut(id=meta["id"], title=citation_source_by_id.get(meta["id"], ("", ""))[1][:120])
            for meta in sorted(citation_meta.values(), key=lambda m: m["id"])
        ]
        metrics = _build_quality_metrics(
            sections_text="\n\n".join(full_text_parts),
            citation_count=len(citations_out),
            sections_count=len(sections_out),
        )

        handout = _persist_handout(session, proc, sections_out, citations_out, citation_source_by_id, metrics)
        public_url = f"{PUBLIC_BASE_URL.rstrip('/')}/h/{handout.slug}"

        return HandoutOut(
            id=str(handout.id),
            procedure=req.procedure_id,
            generatedAt=handout.generated_at.replace(tzinfo=timezone.utc).isoformat(),
            title=f"After Your {proc.name}: Recovery Guide",
            sections=sections_out,
            citations=citations_out,
            qualityMetrics=metrics,
            slug=handout.slug,
            publicUrl=public_url,
            qrUrl=f"/api/handouts/{handout.slug}/qr.png",
        )
    finally:
        session.close()


@app.get("/api/handouts/{slug}", response_model=HandoutOut)
def get_handout(slug: str):
    session = get_session()
    try:
        handout = session.query(Handout).filter_by(slug=slug, published=True).first()
        if not handout:
            raise HTTPException(status_code=404, detail="Handout not found")
        return _handout_to_dto(session, handout)
    finally:
        session.close()


@app.get("/api/handouts/{slug}/qr.png")
def get_handout_qr(slug: str):
    session = get_session()
    try:
        exists = session.query(Handout).filter_by(slug=slug, published=True).first()
        if not exists:
            raise HTTPException(status_code=404, detail="Handout not found")
    finally:
        session.close()
    public_url = f"{PUBLIC_BASE_URL.rstrip('/')}/h/{slug}"
    img = qrcode.make(public_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return Response(
        content=buf.getvalue(),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=86400, immutable"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
