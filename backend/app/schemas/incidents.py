from pydantic import BaseModel


class BusinessHoursOut(BaseModel):
    always: bool
    weekDayStart: int | None = None
    weekDayEnd: int | None = None
    timeStart: int | None = None
    timeEnd: int | None = None


class EmergencyContactOut(BaseModel):
    id: str
    name: str
    phone: str | None = None
    mail: str | None = None
    url: str | None = None
    businessHours: BusinessHoursOut

    model_config = {"from_attributes": True}


class IncidentSignOut(BaseModel):
    id: str
    title: str
    description: str
    examples: list[str]

    model_config = {"from_attributes": True}


class IncidentLinkOut(BaseModel):
    title: str
    url: str

    model_config = {"from_attributes": True}


class IncidentLinkCategoryOut(BaseModel):
    id: str
    title: str
    links: list[IncidentLinkOut]

    model_config = {"from_attributes": True}


class IncidentStepOut(BaseModel):
    pos: int
    title: str
    text: str
    sourceLabel: str | None = None
    sourceUrl: str | None = None
