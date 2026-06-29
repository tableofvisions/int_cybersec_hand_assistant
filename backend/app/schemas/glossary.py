from typing import Any

from pydantic import BaseModel


class GlossaryCategoryOut(BaseModel):
    id: str
    name: str
    description: str
    imageSrc: str | None = None

    model_config = {"from_attributes": True}


class GlossaryEntryLightOut(BaseModel):
    id: str
    keyword: str
    definition: str | None = None

    model_config = {"from_attributes": True}


class GlossarySourceOut(BaseModel):
    id: str
    name: str
    url: str

    model_config = {"from_attributes": True}


class GlossaryTermOut(BaseModel):
    id: str
    keyword: str
    definition: str | None = None
    description: str | None = None
    category: GlossaryCategoryOut | None = None
    synonyms: list[str] = []
    sources: list[GlossarySourceOut] = []
    createdAt: str
    updatedAt: str

    model_config = {"from_attributes": True}


class GlossaryEntryOut(BaseModel):
    term: GlossaryTermOut
    category: GlossaryCategoryOut
    references: dict[str, GlossaryEntryLightOut]


class GlossarySearchResult(BaseModel):
    totalPages: int
    totalElements: int
    pageable: Any
    numberOfElements: int
    size: int
    content: list[GlossaryEntryLightOut]
    number: int
    sort: Any = None
    first: bool
    last: bool
    empty: bool


class PageableSort(BaseModel):
    direction: str = "ASC"
    property: str = "keyword"
    ignoreCase: bool = True
    nullHandling: str = "NATIVE"
    ascending: bool = True


class Pageable(BaseModel):
    page: int = 0
    size: int = 20
    sort: list[PageableSort] = []


class SearchCriteria(BaseModel):
    all: str = ""


class GlossarySearchRequest(BaseModel):
    pageable: Pageable = Pageable()
    searchCriteria: SearchCriteria = SearchCriteria()


class GlossaryCategorySearchRequest(BaseModel):
    category: str
    pageable: Pageable = Pageable()
