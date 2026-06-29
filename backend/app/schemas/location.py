from typing import Any

from pydantic import BaseModel


class CountryOut(BaseModel):
    id: str
    name: str
    code: str


class StateOut(BaseModel):
    id: str
    name: str
    code: str
    country: CountryOut


class CountyOut(BaseModel):
    id: str
    name: str
    code: str
    state: StateOut


class CityOut(BaseModel):
    id: str
    name: str
    postalCode: str
    county: CountyOut


class CityLightOut(BaseModel):
    id: int
    name: str
    postalCode: str


class LocationSearchResult(BaseModel):
    totalPages: int
    totalElements: int
    pageable: Any
    numberOfElements: int
    size: int
    content: list[CityLightOut]
    number: int
    first: bool
    last: bool
    empty: bool


class Pageable(BaseModel):
    page: int = 0
    size: int = 10
    sort: list[Any] = []


class SearchCriteria(BaseModel):
    all: str = ""


class LocationSearchRequest(BaseModel):
    pageable: Pageable = Pageable()
    searchCriteria: SearchCriteria = SearchCriteria()
