from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.auth.deps import get_current_user
from app.database import get_db
from app.models.company import Company
from app.models.location import City, County, State, Country
from app.models.profession import Profession
from app.models.user import User
from app.routers.locations import _city_to_full
from app.schemas.company import CompanyOut, ProfessionOut, UpdateCompanyBody

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

Db = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _company_to_out(company: Company) -> CompanyOut:
    profession_out = None
    if company.profession_rel:
        profession_out = ProfessionOut(
            id=str(company.profession_rel.id),
            name=company.profession_rel.name,
        )

    location_out = None
    if company.location_rel:
        location_out = _city_to_full(company.location_rel)

    return CompanyOut(
        id=company.id,
        name=company.name,
        companyType=company.size_class,
        profession=profession_out,
        location=location_out,
        locationId=str(company.location_id) if company.location_id else None,
    )


def _load_company(company_id: str, db: Session) -> Company:
    company = (
        db.query(Company)
        .options(
            joinedload(Company.profession_rel),
            joinedload(Company.location_rel)
            .joinedload(City.county)
            .joinedload(County.state)
            .joinedload(State.country),
        )
        .filter(Company.id == company_id)
        .first()
    )
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


@router.get("/my", response_model=CompanyOut)
def get_my_company(user: CurrentUser, db: Db):
    return _company_to_out(_load_company(user.company_id, db))


@router.put("", response_model=CompanyOut)
def update_company(body: UpdateCompanyBody, user: CurrentUser, db: Db):
    company = _load_company(user.company_id, db)

    if body.name is not None:
        company.name = body.name

    if "companyType" in body.model_fields_set:
        company.size_class = body.companyType

    if "profession" in body.model_fields_set:
        if body.profession is None:
            company.profession_id = None
        else:
            prof_id_raw = body.profession.get("id")
            if prof_id_raw is not None:
                try:
                    prof_id = int(prof_id_raw)
                except (ValueError, TypeError):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid profession id")
                profession = db.query(Profession).filter(Profession.id == prof_id).first()
                if not profession:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profession not found")
                company.profession_id = prof_id

    if "locationId" in body.model_fields_set:
        if body.locationId is None:
            company.location_id = None
        else:
            try:
                loc_id = int(body.locationId)
            except (ValueError, TypeError):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid location id")
            city = db.query(City).filter(City.id == loc_id).first()
            if not city:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
            company.location_id = loc_id

    db.commit()
    db.refresh(company)
    return _company_to_out(_load_company(user.company_id, db))
