from datetime import datetime, timedelta, timezone

import jwt
from jwt import PyJWTError

from app.config import settings

_ALGORITHM = settings.algorithm


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expire}, settings.secret_key, algorithm=_ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """Returns the subject (user id) or None if invalid/expired."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[_ALGORITHM])
        return payload.get("sub")
    except PyJWTError:
        return None
