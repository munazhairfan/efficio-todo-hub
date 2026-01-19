from sqlmodel import create_engine, Session
from typing import Generator
try:
    # Try relative import when running as part of the package
    from .core.config import settings
except ImportError:
    # Fallback to absolute import when needed
    try:
        from backend.core.config import settings
    except ImportError:
        # Last resort - import directly
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from core.config import settings


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