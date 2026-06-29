import secrets

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.auth.password import hash_password
from app.database import get_db
from app.models.progress import Progress
from app.models.user import User
from app.services.email import send_invite_email

router = APIRouter(prefix="/api/v1/users", tags=["users"])


class InviteUserRequest(BaseModel):
    mail: EmailStr
    firstName: str
    lastName: str

    @field_validator("mail", mode="before")
    @classmethod
    def normalise_email(cls, v: str) -> str:
        return v.strip().lower()


class ReinviteRequest(BaseModel):
    userID: str


class UpdateUserRequest(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    mail: EmailStr | None = None

    @field_validator("mail", mode="before")
    @classmethod
    def normalise_email(cls, v: str | None) -> str | None:
        return v.strip().lower() if v else v


class UserOut(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_verified: bool
    company_id: str

    model_config = {"from_attributes": True}


@router.get("", response_model=list[UserOut])
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(User).filter(User.company_id == current_user.company_id).order_by(User.first_name).all()


@router.post("/invite", response_model=UserOut)
def invite_user(
    body: InviteUserRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if db.query(User).filter_by(email=body.mail).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-Mail bereits registriert")

    verification_token = secrets.token_urlsafe(32)
    user = User(
        company_id=current_user.company_id,
        email=body.mail,
        hashed_password=hash_password(secrets.token_urlsafe(16)),
        first_name=body.firstName,
        last_name=body.lastName,
        role="VIEWER",
        is_verified=False,
        verification_token=verification_token,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    inviter_name = f"{current_user.first_name} {current_user.last_name}".strip()
    background_tasks.add_task(send_invite_email, user.email, user.first_name, verification_token, inviter_name)
    return user


@router.post("/reinvite")
def reinvite_user(
    body: ReinviteRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.id == body.userID,
        User.company_id == current_user.company_id,
    ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.verification_token = secrets.token_urlsafe(32)
    user.is_verified = False
    db.commit()

    inviter_name = f"{current_user.first_name} {current_user.last_name}".strip()
    background_tasks.add_task(send_invite_email, user.email, user.first_name, user.verification_token, inviter_name)
    return {"message": "Einladung erneut versendet"}


@router.post("/password-change")
async def change_password(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    body = await request.body()
    new_password = body.decode("utf-8").strip()
    if len(new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwort zu kurz")

    current_user.hashed_password = hash_password(new_password)
    db.commit()
    return {"message": "Passwort geändert"}


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: str,
    body: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Keine Berechtigung")

    if body.firstName is not None:
        user.first_name = body.firstName
    if body.lastName is not None:
        user.last_name = body.lastName
    if body.mail is not None:
        if db.query(User).filter(User.email == body.mail, User.id != user_id).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-Mail bereits verwendet")
        user.email = body.mail

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Keine Berechtigung")

    db.query(Progress).filter(Progress.completed_by == user_id).update({"completed_by": None})
    db.delete(user)
    db.commit()
    return {"message": "Benutzer gelöscht"}
