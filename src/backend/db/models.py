"""POC-011: SQLAlchemy ORM schema.

Tables: procedures, documents, chunks, handouts, handout_sections, citations.
Default DB is local SQLite (dev); switch to Postgres by changing DATABASE_URL.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./postopcare.db")
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


class Procedure(Base):
    __tablename__ = "procedures"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    specialty: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    common_aliases: Mapped[Optional[list]] = mapped_column(JSON)
    handouts: Mapped[list["Handout"]] = relationship(back_populates="procedure")


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_type: Mapped[str] = mapped_column(String(20), index=True)  # pubmed | guideline | pdf
    source_id: Mapped[str] = mapped_column(String(255), index=True)  # pmid, url, file path
    title: Mapped[Optional[str]] = mapped_column(Text)
    authors: Mapped[Optional[list]] = mapped_column(JSON)
    journal: Mapped[Optional[str]] = mapped_column(String(255))
    pub_date: Mapped[Optional[str]] = mapped_column(String(40))
    raw_text: Mapped[Optional[str]] = mapped_column(Text)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    char_start: Mapped[int] = mapped_column(Integer)
    char_end: Mapped[int] = mapped_column(Integer)
    embedding_id: Mapped[Optional[str]] = mapped_column(String(120))  # pinecone vector id
    document: Mapped["Document"] = relationship(back_populates="chunks")


class Handout(Base):
    __tablename__ = "handouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    procedure_id: Mapped[int] = mapped_column(ForeignKey("procedures.id"), index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    model_version: Mapped[Optional[str]] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft | reviewed | published
    procedure: Mapped["Procedure"] = relationship(back_populates="handouts")
    sections: Mapped[list["HandoutSection"]] = relationship(
        back_populates="handout", cascade="all, delete-orphan"
    )


class HandoutSection(Base):
    __tablename__ = "handout_sections"
    id: Mapped[int] = mapped_column(primary_key=True)
    handout_id: Mapped[int] = mapped_column(ForeignKey("handouts.id"), index=True)
    section_name: Mapped[str] = mapped_column(String(80))
    body_md: Mapped[str] = mapped_column(Text)
    body_html: Mapped[Optional[str]] = mapped_column(Text)
    readability_grade: Mapped[Optional[float]] = mapped_column(Float)
    readability_ease: Mapped[Optional[float]] = mapped_column(Float)
    handout: Mapped["Handout"] = relationship(back_populates="sections")
    citations: Mapped[list["Citation"]] = relationship(
        back_populates="section", cascade="all, delete-orphan"
    )


class Citation(Base):
    __tablename__ = "citations"
    id: Mapped[int] = mapped_column(primary_key=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("handout_sections.id"), index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), index=True)
    inline_number: Mapped[int] = mapped_column(Integer)
    snippet: Mapped[Optional[str]] = mapped_column(Text)
    verification_score: Mapped[Optional[float]] = mapped_column(Float)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    section: Mapped["HandoutSection"] = relationship(back_populates="citations")
    document: Mapped["Document"] = relationship()


Index("idx_chunk_document_index", Chunk.document_id, Chunk.chunk_index)


def init_db() -> None:
    """Create all tables. Idempotent."""
    Base.metadata.create_all(engine)


def get_session() -> Session:
    """Caller is responsible for closing or using as a context manager."""
    return SessionLocal()


if __name__ == "__main__":
    init_db()
    print(f"DB initialized at {DATABASE_URL}")
    print("Tables:", list(Base.metadata.tables.keys()))
