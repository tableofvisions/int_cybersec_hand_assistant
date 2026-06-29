from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite:////app/data/csa.db"

    cors_origins: str = "http://localhost:3000"

    # Email (Resend)
    resend_api_key: str = ""
    resend_from_email: str = "noreply@example.com"
    frontend_url: str = "http://localhost:3000"

    # Dev-only: skip email verification on register
    dev_auto_verify: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


settings = Settings()