from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from typing import AsyncGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable
# Default to SQLite for local development, but allow override for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app_hf.db")

try:
    # Create async engine with connection pooling settings
    # Different settings for PostgreSQL vs SQLite
    if "postgresql" in DATABASE_URL.lower():
        # PostgreSQL settings
        engine = create_async_engine(
            DATABASE_URL,
            echo=True,  # Set to True for debugging, False in production
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=300,
        )
    else:
        # SQLite settings
        engine = create_async_engine(
            DATABASE_URL,
            echo=True,  # Set to True for debugging, False in production
            # SQLite doesn't support connection pooling the same way, so use minimal settings
            pool_size=5,
            max_overflow=0,
            pool_pre_ping=True,
            pool_recycle=300,
            # SQLite-specific settings
            connect_args={"check_same_thread": False}  # Required for SQLite with async
        )
except Exception as e:
    # This is to catch import-time errors and provide better debugging
    print(f"Error creating database engine: {e}")
    raise

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for getting async database sessions per backend/CLAUDE.md"""
    async with AsyncSessionLocal() as session:
        yield session