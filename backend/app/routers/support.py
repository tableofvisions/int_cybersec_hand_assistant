import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.auth.deps import get_verified_user
from app.database import get_db
from app.models.support import SupportOffer, SupportOrganization, SupportServiceEntry, SupportTopic
from app.models.user import User
from app.schemas.support import (
    SupportOfferOut,
    SupportOrganizationOut,
    SupportSearchRequest,
    SupportSearchResult,
    SupportServiceEntryOut,
    SupportTopicOut,
)

router = APIRouter(prefix="/api/v1/support", tags=["support"])

Db = Annotated[Session, Depends(get_db)]
Auth = Annotated[User, Depends(get_verified_user)]

_EAGER = [
    joinedload(SupportServiceEntry.offer).joinedload(SupportOffer.topics),
    joinedload(SupportServiceEntry.provider),
]


def _entry_to_out(e: SupportServiceEntry) -> SupportServiceEntryOut:
    offer_out = None
    if e.offer:
        offer_out = SupportOfferOut(
            id=e.offer.id,
            name=e.offer.name,
            description=e.offer.description,
            type=e.offer.type,
            topics=[SupportTopicOut(id=t.id, name=t.name, description=t.description) for t in e.offer.topics],
        )
    provider_out = None
    if e.provider:
        provider_out = SupportOrganizationOut(
            id=e.provider.id,
            name=e.provider.name,
            contactPerson=e.provider.contact_person,
            street=e.provider.street,
            streetNumber=e.provider.street_number,
            addressDetails=e.provider.address_details,
            phone=e.provider.phone,
            mail=e.provider.mail,
            website=e.provider.website,
            description=e.provider.description,
        )
    return SupportServiceEntryOut(
        id=e.id,
        offer=offer_out,
        provider=provider_out,
        website=e.website,
    )


@router.post("/search-full", response_model=SupportSearchResult)
def search_full(body: SupportSearchRequest, db: Db, current_user: Auth):
    q = db.query(SupportServiceEntry).options(*_EAGER)

    c = body.searchCriteria
    if c.offerDescriptionLike and c.offerDescriptionLike.strip():
        pattern = f"%{c.offerDescriptionLike.strip()}%"
        q = q.join(SupportOffer, SupportServiceEntry.offer_id == SupportOffer.id).filter(
            SupportOffer.description.ilike(pattern)
        )
    if c.offerType:
        q = q.join(SupportOffer, SupportServiceEntry.offer_id == SupportOffer.id, isouter=True).filter(
            SupportOffer.type == c.offerType
        )
    if c.topicName:
        q = (
            q.join(SupportOffer, SupportServiceEntry.offer_id == SupportOffer.id, isouter=True)
            .join(SupportOffer.topics)
            .filter(SupportTopic.name.ilike(f"%{c.topicName}%"))
        )
    if c.providerName:
        q = q.join(
            SupportOrganization, SupportServiceEntry.organization_id == SupportOrganization.id, isouter=True
        ).filter(SupportOrganization.name.ilike(f"%{c.providerName}%"))

    page = body.pageable.page
    size = body.pageable.size or 9999

    total = q.count()
    entries = q.offset(page * size).limit(size).all()
    total_pages = math.ceil(total / size) if size else 1
    content = [_entry_to_out(e) for e in entries]

    return SupportSearchResult(
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


@router.get("/{entry_id}", response_model=SupportServiceEntryOut)
def get_entry(entry_id: str, db: Db, current_user: Auth):
    entry = (
        db.query(SupportServiceEntry)
        .options(*_EAGER)
        .filter(SupportServiceEntry.id == entry_id)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Support service entry not found")
    return _entry_to_out(entry)
