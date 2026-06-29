from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.profession import Profession

router = APIRouter(prefix="/api/v1/professions", tags=["professions"])


class ProfessionOut(BaseModel):
    id: str
    name: str


@router.get("/all", response_model=list[ProfessionOut])
def get_all_professions(db: Session = Depends(get_db)):
    professions = db.query(Profession).filter(Profession.is_active == True).order_by(Profession.name).all()  # noqa: E712
    return [ProfessionOut(id=str(p.id), name=p.name) for p in professions]
