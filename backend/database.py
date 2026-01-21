from sqlmodel import create_engine, Session
from typing import Generator
import sys
import os

# Add the backend directory to the Python path to allow absolute imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    # Try absolute import from the backend directory
    from src.core.config import settings
    from src.models.user import User
    from api.models.conversation_state import ConversationState, ConversationStateCreate, ConversationStateUpdate, ConversationStateResponse
    from api.models.error_context import ErrorContext
except ImportError:
    # Fallback to relative import when running as part of the package
    try:
        from .src.core.config import settings
        from .src.models.user import User
        from .api.models.conversation_state import ConversationState, ConversationStateCreate, ConversationStateUpdate, ConversationStateResponse
        from .api.models.error_context import ErrorContext
    except ImportError:
        # Last resort - try various import patterns
        try:
            # For when running from parent directory
            from backend.src.core.config import settings
            from backend.src.models.user import User
            from backend.api.models.conversation_state import ConversationState, ConversationStateCreate, ConversationStateUpdate, ConversationStateResponse
            from backend.api.models.error_context import ErrorContext
        except ImportError:
            print("Error: Could not import configuration modules")
            raise


# Create database engine lazily (only when needed)
_engine = None


def get_engine():
    """Get database engine, creating it if it doesn't exist"""
    global _engine
    if _engine is None:
        # Handle different database URL schemes to avoid asyncpg dependency issues
        database_url = settings.database_url

        # If using PostgreSQL and asyncpg isn't available, fall back to psycopg2
        if database_url.startswith("postgresql://") or database_url.startswith("postgresql+"):
            try:
                # Try to use psycopg2 sync driver instead of asyncpg
                if "postgresql+asyncpg://" in database_url:
                    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
                elif "postgresql+psycopg://" in database_url:
                    database_url = database_url.replace("postgresql+psycopg://", "postgresql://")
            except:
                pass  # If there's an issue, continue with original URL

        _engine = create_engine(database_url, echo=True)
    return _engine


def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session