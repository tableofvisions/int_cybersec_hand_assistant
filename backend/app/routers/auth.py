import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi import BackgroundTasks

from app.auth.deps import get_current_user
from app.config import settings
from app.auth.jwt import create_access_token
from app.auth.password import hash_password, verify_password
from app.database import get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    ResetPasswordRequest,
    ResetRequestBody,
    TokenResponse,
    UserResponse,
    VerifyRequest,
)
from app.services.email import send_password_reset_email, send_verification_email

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

_RESET_TOKEN_TTL_HOURS = 2


# ── Register ──────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=body.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-Mail bereits registriert")

    # Company anlegen (oder per Domain joinen)
    company = None
    if body.company_domain:
        company = db.query(Company).filter_by(domain=body.company_domain).first()

    if not company:
        company = Company(
            name=body.company_name,
            domain=body.company_domain,
            location_id=body.location_id,
            profession_id=body.profession_id,
            size_class=body.size_class,
        )
        db.add(company)
        db.flush()

    auto_verify = settings.dev_auto_verify
    verification_token = None if auto_verify else secrets.token_urlsafe(32)

    user = User(
        company_id=company.id,
        email=body.email,
        hashed_password=hash_password(body.password),
        first_name=body.first_name,
        last_name=body.last_name,
        role="ADMIN",
        is_verified=auto_verify,
        verification_token=verification_token,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if not auto_verify:
        background_tasks.add_task(send_verification_email, user.email, user.first_name, verification_token)

    return user


# ── Login ─────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form.username.strip().lower()).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ungültige Zugangsdaten")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="E-Mail noch nicht verifiziert")

    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    return TokenResponse(access_token=create_access_token(user.id))


# ── Verify ────────────────────────────────────────────────────────────────────

@router.post("/verify")
def verify_email(body: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(verification_token=body.token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ungültiger Verifizierungstoken")

    user.is_verified = True
    user.verification_token = None
    db.commit()

    return {"message": "E-Mail erfolgreich verifiziert"}


# ── Password Reset Request ────────────────────────────────────────────────────

@router.post("/reset-request")
def reset_request(body: ResetRequestBody, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=body.email).first()

    # Immer 200 zurückgeben — kein User-Enumeration-Angriff möglich
    if user:
        user.reset_token = secrets.token_urlsafe(32)
        user.reset_token_expires_at = datetime.now(timezone.utc) + timedelta(hours=_RESET_TOKEN_TTL_HOURS)
        db.commit()
        background_tasks.add_task(send_password_reset_email, user.email, user.first_name, user.reset_token)

    return {"message": "Falls die E-Mail registriert ist, wurde ein Reset-Link gesendet"}


# ── Password Reset ────────────────────────────────────────────────────────────

@router.post("/reset")
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(reset_token=body.token).first()

    if not user or not user.reset_token_expires_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ungültiger oder abgelaufener Token")

    expires = user.reset_token_expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token abgelaufen")

    user.hashed_password = hash_password(body.new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    db.commit()

    return {"message": "Passwort erfolgreich zurückgesetzt"}


# ── Me ────────────────────────────────────────────────────────────────────────

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user
