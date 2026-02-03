from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import get_settings


settings = get_settings()


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


engine = create_engine(settings.postgres_dsn, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that yields a DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

