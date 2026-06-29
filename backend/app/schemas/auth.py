from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str
    company_domain: str | None = None
    location_id: int | None = None
    profession_id: int | None = None
    size_class: str | None = None

    @field_validator("email", mode="before")
    @classmethod
    def normalise_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Passwort muss mindestens 8 Zeichen haben")
        return v


class LoginRequest(BaseModel):
    username: str   # OAuth2 spec uses "username" for the email field
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class VerifyRequest(BaseModel):
    token: str


class ResetRequestBody(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def normalise_email(cls, v: str) -> str:
        return v.strip().lower()


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Passwort muss mindestens 8 Zeichen haben")
        return v


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_verified: bool
    company_id: str

    model_config = {"from_attributes": True}
