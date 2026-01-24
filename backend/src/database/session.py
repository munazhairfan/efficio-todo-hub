from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from sqlmodel import SQLModel
from typing import Optional


# Create a Base class for declarative models - this doesn't require an engine
Base = declarative_base()


# Create the database engine lazily (only when needed)
_engine: Optional[object] = None
_SessionLocal: Optional[object] = None


def get_engine():
    """Get database engine, creating it if it doesn't exist"""
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.database_url,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_pool_overflow,
            echo=settings.db_echo
        )
        # Import all models to ensure they're registered with SQLModel metadata
        # This ensures tables are created when the engine is first created
        from src.models import task  # noqa: F401
        from src.models import user  # noqa: F401
        # Create all tables - this will work for both new and existing databases
        SQLModel.metadata.create_all(bind=_engine)
    return _engine


def get_session_local():
    """Get SessionLocal, creating it if it doesn't exist"""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


def get_db():
    """Dependency to get database session"""
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()