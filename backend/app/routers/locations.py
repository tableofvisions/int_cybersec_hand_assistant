import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.location import City, County, Country, State
from app.schemas.location import (
    CityLightOut,
    CityOut,
    CountryOut,
    CountyOut,
    LocationSearchRequest,
    LocationSearchResult,
    StateOut,
)

router = APIRouter(prefix="/api/v1/locations", tags=["locations"])

Db = Annotated[Session, Depends(get_db)]


def _city_to_full(city: City) -> CityOut:
    county = city.county
    state = county.state
    country = state.country
    return CityOut(
        id=str(city.id),
        name=city.name,
        postalCode=city.postal_code,
        county=CountyOut(
            id=str(county.id),
            name=county.name,
            code=county.code,
            state=StateOut(
                id=str(state.id),
                name=state.name,
                code=state.code,
                country=CountryOut(id=str(country.id), name=country.name, code=country.code),
            ),
        ),
    )


@router.post("/search", response_model=LocationSearchResult)
def search_locations(body: LocationSearchRequest, db: Db):
    q_str = body.searchCriteria.all.strip()
    page = body.pageable.page
    size = body.pageable.size or 10

    q = db.query(City).options(
        joinedload(City.county).joinedload(County.state).joinedload(State.country)
    )
    if q_str:
        pattern = f"%{q_str}%"
        q = q.filter(or_(City.name.ilike(pattern), City.postal_code.ilike(pattern)))
    q = q.order_by(City.name)

    total = q.count()
    cities = q.offset(page * size).limit(size).all()
    total_pages = math.ceil(total / size) if size else 1
    content = [CityLightOut(id=c.id, name=c.name, postalCode=c.postal_code) for c in cities]

    return LocationSearchResult(
        totalPages=total_pages,
        totalElements=total,
        pageable={"pageNumber": page, "pageSize": size},
        numberOfElements=len(content),
        size=size,
        content=content,
        number=page,
        first=(page == 0),
        last=(page >= total_pages - 1),
        empty=(len(content) == 0),
    )


@router.get("/{city_id}", response_model=CityOut)
def get_location(city_id: int, db: Db):
    city = db.query(City).options(
        joinedload(City.county).joinedload(County.state).joinedload(State.country)
    ).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="Location not found")
    return _city_to_full(city)
