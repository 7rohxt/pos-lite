from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """All ORM models inherit from this."""
    pass


# echo=True prints SQL while learning; turn off in production later.
engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency: open a session per request, always close it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()