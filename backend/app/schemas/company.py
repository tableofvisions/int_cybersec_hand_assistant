from pydantic import BaseModel

from app.schemas.location import CityOut


class ProfessionOut(BaseModel):
    id: str
    name: str


class CompanyOut(BaseModel):
    id: str
    name: str
    companyType: str | None = None
    profession: ProfessionOut | None = None
    location: CityOut | None = None
    locationId: str | None = None


class UpdateCompanyBody(BaseModel):
    name: str | None = None
    companyType: str | None = None
    profession: dict | None = None  # {"id": "<profession_id>"}
    locationId: str | None = None
