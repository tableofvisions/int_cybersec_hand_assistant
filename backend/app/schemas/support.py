from typing import Any

from pydantic import BaseModel


class SupportTopicOut(BaseModel):
    id: str
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}


class SupportOfferOut(BaseModel):
    id: str
    name: str
    description: str | None = None
    type: str
    topics: list[SupportTopicOut] = []

    model_config = {"from_attributes": True}


class SupportOrganizationOut(BaseModel):
    id: str
    name: str
    contactPerson: str | None = None
    street: str | None = None
    streetNumber: str | None = None
    addressDetails: str | None = None
    phone: str | None = None
    mail: str | None = None
    website: str | None = None
    description: str | None = None

    model_config = {"from_attributes": True}


class SupportServiceEntryOut(BaseModel):
    id: str
    offer: SupportOfferOut | None = None
    provider: SupportOrganizationOut | None = None
    website: str | None = None

    model_config = {"from_attributes": True}


class SupportSearchResult(BaseModel):
    totalPages: int
    totalElements: int
    pageable: Any
    numberOfElements: int
    size: int
    content: list[SupportServiceEntryOut]
    number: int
    sort: Any = None
    first: bool
    last: bool
    empty: bool


class PageableSort(BaseModel):
    direction: str = "ASC"
    property: str = "id"
    ignoreCase: bool = True
    nullHandling: str = "NATIVE"
    ascending: bool = True


class Pageable(BaseModel):
    page: int = 0
    size: int = 9999
    sort: list[PageableSort] = []


class SupportSearchCriteria(BaseModel):
    offerDescriptionLike: str = ""
    offerType: str | None = None
    topicName: str | None = None
    providerName: str | None = None


class SupportSearchRequest(BaseModel):
    pageable: Pageable = Pageable()
    searchCriteria: SupportSearchCriteria = SupportSearchCriteria()
