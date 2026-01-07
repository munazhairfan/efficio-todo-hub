from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session


async def get_db_session():
    """
    Dependency to provide database session.
    Based on research.md decision for database session dependency.
    # Used by all API endpoints that require database access
    """
    async for session in get_session():
        yield session