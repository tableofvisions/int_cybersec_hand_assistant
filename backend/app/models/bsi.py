import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class BsiVersion(Base):
    __tablename__ = "bsi_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    version_tag: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    release_date: Mapped[str] = mapped_column(String(32), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(512))
    # draft → published; only published versions are shown to users
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    measures: Mapped[list["Measure"]] = relationship(back_populates="bsi_version")


class Measure(Base):
    """One BSI control or sub-control from the Grundschutz++ catalog."""
    __tablename__ = "measures"
    __table_args__ = (
        UniqueConstraint("control_id", "bsi_version_id", name="uq_control_version"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bsi_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("bsi_versions.id"), nullable=False)

    # BSI hierarchy
    control_id: Mapped[str] = mapped_column(String(32), nullable=False)   # e.g. "PERF.1.1.1"
    # Plain string — no FK because control_id is only unique within a version (composite constraint)
    parent_control_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    group_id: Mapped[str] = mapped_column(String(16), nullable=False)      # e.g. "PERF"
    group_title: Mapped[str] = mapped_column(String(128), nullable=False)  # e.g. "Monitoring-Evaluation"
    subgroup_id: Mapped[str] = mapped_column(String(16), nullable=False)   # e.g. "PERF.1"
    subgroup_title: Mapped[str] = mapped_column(String(128), nullable=False)

    title: Mapped[str] = mapped_column(String(256), nullable=False)
    requirement_text: Mapped[str] = mapped_column(Text, nullable=False)
    guidance_text: Mapped[str | None] = mapped_column(Text)

    # "normal-SdT" | "erhöht"
    sec_level: Mapped[str] = mapped_column(String(32), nullable=False, default="normal-SdT")
    # 0 = not assessed, 1–5 scale from OSCAL
    effort_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # BSI's own UUID — used to detect same control across versions
    bsi_uuid: Mapped[str | None] = mapped_column(String(64))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    bsi_version: Mapped["BsiVersion"] = relationship(back_populates="measures")
    mapping: Mapped["Mapping | None"] = relationship(back_populates="measure", uselist=False)
    # viewonly relationship — no FK, joined by string equality within the same version
    sub_controls: Mapped[list["Measure"]] = relationship(
        "Measure",
        primaryjoin="and_(Measure.parent_control_id == Measure.control_id, "
                    "foreign(Measure.parent_control_id) == Measure.control_id)",
        foreign_keys="[Measure.parent_control_id]",
        viewonly=True,
    )


class Area(Base):
    """One of the 4 business areas that BSI controls are mapped to."""
    __tablename__ = "areas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    emoji: Mapped[str | None] = mapped_column(String(8))
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    mappings: Mapped[list["Mapping"]] = relationship(back_populates="area")


class Mapping(Base):
    """LLM output: links a BSI measure to one of the 4 business areas."""
    __tablename__ = "mappings"
    __table_args__ = (
        UniqueConstraint("measure_id", name="uq_mapping_measure"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    measure_id: Mapped[str] = mapped_column(String(36), ForeignKey("measures.id"), nullable=False)
    area_id: Mapped[str] = mapped_column(String(36), ForeignKey("areas.id"), nullable=False)

    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text)
    # LLM-generated user-friendly reformulation of the requirement
    short_description: Mapped[str | None] = mapped_column(Text)
    model_version: Mapped[str | None] = mapped_column(String(64))

    is_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    measure: Mapped["Measure"] = relationship(back_populates="mapping")
    area: Mapped["Area"] = relationship(back_populates="mappings")
    checklist_item: Mapped["ChecklistItem | None"] = relationship(back_populates="mapping", uselist=False)


class ChecklistItem(Base):
    """Published checklist entry — only approved mappings become checklist items."""
    __tablename__ = "checklist_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mapping_id: Mapped[str] = mapped_column(String(36), ForeignKey("mappings.id"), nullable=False, unique=True)
    # denormalized for efficient filtering without joining through mappings
    bsi_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("bsi_versions.id"), nullable=False)
    # 1 = highest priority; NULL = unranked
    priority: Mapped[int | None] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    mapping: Mapped["Mapping"] = relationship(back_populates="checklist_item")
    progress_entries: Mapped[list["Progress"]] = relationship(back_populates="checklist_item")
