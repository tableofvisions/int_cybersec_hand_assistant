import uuid

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# Many-to-many: offers ↔ topics
_offer_topics = Table(
    "support_offer_topics",
    Base.metadata,
    Column("offer_id", String(36), ForeignKey("support_offers.id"), primary_key=True),
    Column("topic_id", String(36), ForeignKey("support_topics.id"), primary_key=True),
)


class SupportTopic(Base):
    __tablename__ = "support_topics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    offers: Mapped[list["SupportOffer"]] = relationship(secondary=_offer_topics, back_populates="topics")


class SupportOrganization(Base):
    __tablename__ = "support_organizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    contact_person: Mapped[str | None] = mapped_column(String(256))
    street: Mapped[str | None] = mapped_column(String(256))
    street_number: Mapped[str | None] = mapped_column(String(32))
    address_details: Mapped[str | None] = mapped_column(String(256))
    phone: Mapped[str | None] = mapped_column(String(64))
    mail: Mapped[str | None] = mapped_column(String(256))
    website: Mapped[str | None] = mapped_column(String(1024))
    description: Mapped[str | None] = mapped_column(Text)

    entries: Mapped[list["SupportServiceEntry"]] = relationship(back_populates="provider")


class SupportOffer(Base):
    __tablename__ = "support_offers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    # INFO | TRAINING | CONSULTATION | OTHER
    type: Mapped[str] = mapped_column(String(32), nullable=False, default="OTHER")

    topics: Mapped[list["SupportTopic"]] = relationship(secondary=_offer_topics, back_populates="offers")
    entries: Mapped[list["SupportServiceEntry"]] = relationship(back_populates="offer")


class SupportServiceEntry(Base):
    __tablename__ = "support_service_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    offer_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("support_offers.id"))
    organization_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("support_organizations.id"))
    website: Mapped[str | None] = mapped_column(String(1024))

    offer: Mapped["SupportOffer | None"] = relationship(back_populates="entries")
    provider: Mapped["SupportOrganization | None"] = relationship(back_populates="entries")
