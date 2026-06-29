from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Country(Base):
    __tablename__ = "loc_countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(8), nullable=False)

    states: Mapped[list["State"]] = relationship(back_populates="country")


class State(Base):
    __tablename__ = "loc_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("loc_countries.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(8), nullable=False)

    country: Mapped["Country"] = relationship(back_populates="states")
    counties: Mapped[list["County"]] = relationship(back_populates="state")


class County(Base):
    __tablename__ = "loc_counties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("loc_states.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(16), nullable=False)

    state: Mapped["State"] = relationship(back_populates="counties")
    cities: Mapped[list["City"]] = relationship(back_populates="county")


class City(Base):
    __tablename__ = "loc_cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    county_id: Mapped[int] = mapped_column(Integer, ForeignKey("loc_counties.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    postal_code: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    county: Mapped["County"] = relationship(back_populates="cities")
