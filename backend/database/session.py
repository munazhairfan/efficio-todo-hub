from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions per backend/CLAUDE.md
    Provides async context management for database operations per research.md
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()