import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(128), unique=True)
    size_class: Mapped[str | None] = mapped_column(String(16))
    profession_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("professions.id"), nullable=True)
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("loc_cities.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    users: Mapped[list["User"]] = relationship(back_populates="company")
    progress_entries: Mapped[list["Progress"]] = relationship(back_populates="company")
    profession_rel: Mapped["Profession | None"] = relationship(foreign_keys=[profession_id])
    location_rel: Mapped["City | None"] = relationship(foreign_keys=[location_id])
