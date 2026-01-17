from sqlmodel import create_engine, Session
from typing import Generator
from .core.config import settings


# Create database engine lazily (only when needed)
_engine = None


def get_engine():
    """Get database engine, creating it if it doesn't exist"""
    global _engine
    if _engine is None:
        _engine = create_engine(settings.database_url, echo=True)
    return _engine


def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session