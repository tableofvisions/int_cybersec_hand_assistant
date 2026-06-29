import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class AuditLog(Base):
    """Immutable record of every state change in the system."""
    __tablename__ = "audit_log"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # e.g. "progress", "user", "company", "checklist_item"
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    # CREATE | UPDATE | DELETE
    action: Mapped[str] = mapped_column(String(16), nullable=False)
    # NULL for system-triggered actions (e.g. BSI ingestion)
    actor_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    # Full JSON payload of the change for auditability
    payload_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    actor: Mapped["User | None"] = relationship(back_populates="audit_logs")
