from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from typing import AsyncGenerator
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable as per backend/CLAUDE.md
# Use absolute path to ensure consistent database location
db_path = Path(__file__).parent / "todo_app.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")

# Create async engine with connection pooling settings
# Different settings for PostgreSQL vs SQLite
if "postgresql" in DATABASE_URL.lower():
    # Extract the original URL and handle PostgreSQL-specific parameters that asyncpg doesn't support
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(DATABASE_URL)
    query_params = parse_qs(parsed.query)

    # Remove unsupported parameters for asyncpg
    unsupported_params = ['sslmode', 'channel_binding']
    for param in unsupported_params:
        if param in query_params:
            del query_params[param]

    # Reconstruct the query string
    new_query_parts = []
    for key, values in query_params.items():
        for value in values:
            new_query_parts.append(f"{key}={value}")
    new_query = "&".join(new_query_parts)

    # Reconstruct the URL without unsupported parameters
    clean_database_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if new_query:
        clean_database_url += f"?{new_query}"
    if parsed.fragment:
        clean_database_url += f"#{parsed.fragment}"

    # PostgreSQL settings
    engine = create_async_engine(
        clean_database_url,
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