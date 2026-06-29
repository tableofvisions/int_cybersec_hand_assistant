import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Progress(Base):
    """Tracks one company's status on one checklist item."""
    __tablename__ = "progress"
    __table_args__ = (
        UniqueConstraint("company_id", "checklist_item_id", name="uq_progress_company_item"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    checklist_item_id: Mapped[str] = mapped_column(String(36), ForeignKey("checklist_items.id"), nullable=False)

    # OPEN | IN_PROGRESS | DONE | NOT_APPLICABLE
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="OPEN")
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_by: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    company: Mapped["Company"] = relationship(back_populates="progress_entries")
    checklist_item: Mapped["ChecklistItem"] = relationship(back_populates="progress_entries")
    comments: Mapped[list["Comment"]] = relationship(back_populates="progress", cascade="all, delete-orphan")


class Comment(Base):
    """Free-text comment on a progress entry (multiple per entry, ordered by time)."""
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    progress_id: Mapped[str] = mapped_column(String(36), ForeignKey("progress.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    progress: Mapped["Progress"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")
