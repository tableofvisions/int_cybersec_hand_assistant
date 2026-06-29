import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(64))
    mail: Mapped[str | None] = mapped_column(String(256))
    url: Mapped[str | None] = mapped_column(String(1024))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Business hours
    bh_always: Mapped[bool] = mapped_column(Boolean, default=False)
    bh_weekday_start: Mapped[int | None] = mapped_column(Integer)  # 1=Mon, 7=Sun
    bh_weekday_end: Mapped[int | None] = mapped_column(Integer)
    bh_time_start: Mapped[int | None] = mapped_column(Integer)     # minutes since 00:00
    bh_time_end: Mapped[int | None] = mapped_column(Integer)


class IncidentSign(Base):
    __tablename__ = "incident_signs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    examples: Mapped[list["IncidentSignExample"]] = relationship(
        back_populates="sign", cascade="all, delete-orphan", order_by="IncidentSignExample.sort_order"
    )


class IncidentSignExample(Base):
    __tablename__ = "incident_sign_examples"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sign_id: Mapped[str] = mapped_column(String(36), ForeignKey("incident_signs.id"), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    sign: Mapped["IncidentSign"] = relationship(back_populates="examples")


class IncidentLinkCategory(Base):
    __tablename__ = "incident_link_categories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(256), nullable=False)

    links: Mapped[list["IncidentLink"]] = relationship(
        back_populates="category", cascade="all, delete-orphan", order_by="IncidentLink.sort_order"
    )


class IncidentLink(Base):
    __tablename__ = "incident_links"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id: Mapped[str] = mapped_column(String(36), ForeignKey("incident_link_categories.id"), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)

    category: Mapped["IncidentLinkCategory"] = relationship(back_populates="links")
