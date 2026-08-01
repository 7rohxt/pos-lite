from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration, loaded from .env and validated by type."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str

    # JWT 
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings() # This is where the objects are created 