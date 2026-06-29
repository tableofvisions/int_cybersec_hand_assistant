import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class GlossaryCategory(Base):
    __tablename__ = "glossary_categories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    image_src: Mapped[str | None] = mapped_column(String(512))

    terms: Mapped[list["GlossaryTerm"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id: Mapped[str] = mapped_column(String(36), ForeignKey("glossary_categories.id"), nullable=False)

    keyword: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    definition: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    category: Mapped["GlossaryCategory"] = relationship(back_populates="terms")
    synonyms: Mapped[list["GlossarySynonym"]] = relationship(back_populates="term", cascade="all, delete-orphan")
    sources: Mapped[list["GlossarySource"]] = relationship(back_populates="term", cascade="all, delete-orphan")
    references: Mapped[list["GlossaryReference"]] = relationship(
        back_populates="term",
        foreign_keys="GlossaryReference.term_id",
        cascade="all, delete-orphan",
    )


class GlossarySynonym(Base):
    __tablename__ = "glossary_synonyms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    term_id: Mapped[str] = mapped_column(String(36), ForeignKey("glossary_terms.id"), nullable=False)
    value: Mapped[str] = mapped_column(String(256), nullable=False)

    term: Mapped["GlossaryTerm"] = relationship(back_populates="synonyms")


class GlossarySource(Base):
    __tablename__ = "glossary_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    term_id: Mapped[str] = mapped_column(String(36), ForeignKey("glossary_terms.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)

    term: Mapped["GlossaryTerm"] = relationship(back_populates="sources")


class GlossaryReference(Base):
    """Cross-reference: term → referenced_term (both must exist)."""
    __tablename__ = "glossary_references"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    term_id: Mapped[str] = mapped_column(String(36), ForeignKey("glossary_terms.id"), nullable=False)
    referenced_term_id: Mapped[str] = mapped_column(String(36), ForeignKey("glossary_terms.id"), nullable=False)

    term: Mapped["GlossaryTerm"] = relationship(back_populates="references", foreign_keys=[term_id])
    referenced_term: Mapped["GlossaryTerm"] = relationship(foreign_keys=[referenced_term_id])
