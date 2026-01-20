from sqlmodel import create_engine, Session
from typing import Generator
try:
    # Try relative import when running as part of the package
    from .src.core.config import settings
    from .src.models.user import User
    from .api.models.conversation_state import ConversationState
    from .api.models.error_context import ErrorContext
except ImportError:
    # Fallback to absolute import when needed
    try:
        # For when this is run from the parent directory where backend is a subdirectory
        from backend.src.core.config import settings
        from backend.src.models.user import User
        from backend.api.models.conversation_state import ConversationState
        from backend.api.models.error_context import ErrorContext
    except ImportError:
        # Last resort - import directly
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from src.core.config import settings
        from src.models.user import User
        from api.models.conversation_state import ConversationState
        from api.models.error_context import ErrorContext


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