from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration, loaded from .env and validated by type."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    # JWT settings will be added here later:
    # SECRET_KEY: str
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings() # This is where the objects are created 


# Why separate config file?
# Without a dedicated config file:

# database.py
# DATABASE_URL = os.getenv(...)
# auth.py
# SECRET_KEY = os.getenv(...)
# email.py
# SMTP_USER = os.getenv(...)

# Now configuration is spread everywhere.