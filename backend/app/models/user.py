import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)

    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)

    # ADMIN | EDITOR | VIEWER
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="VIEWER")

    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    verification_token: Mapped[str | None] = mapped_column(String(128))
    reset_token: Mapped[str | None] = mapped_column(String(128))
    reset_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    company: Mapped["Company"] = relationship(back_populates="users")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="actor", cascade="all, delete-orphan")
