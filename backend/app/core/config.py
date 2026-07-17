from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "BEYOND CIBIL"
    environment: str = "development"
    debug: bool = Field(default=False, validation_alias="BEYOND_CIBIL_DEBUG")
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/beyond_cibil"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800
    supabase_url: str | None = None
    supabase_anon_key: SecretStr | None = Field(default=None, repr=False)
    supabase_publishable_key: SecretStr | None = Field(default=None, repr=False)
    supabase_secret_key: SecretStr | None = Field(default=None, repr=False)
    supabase_service_role_key: SecretStr | None = Field(default=None, repr=False)
    log_level: str = "INFO"
    jwt_secret_key: str = Field(default="change-me-before-production", repr=False)
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7


@lru_cache
def get_settings() -> Settings:
    return Settings()
