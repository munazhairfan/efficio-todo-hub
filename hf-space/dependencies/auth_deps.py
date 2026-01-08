from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from core.auth.jwt_handler import verify_access_token
from core.auth.user_extractor import validate_and_extract_user
from models.user import User
from sqlmodel import select


async def get_current_user(token_data: dict = Depends(verify_access_token)) -> User:
    """
    Dependency to provide current authenticated user.
    Based on research.md decision for authenticated user dependency.
    # UI Component: ProtectedRoute -> Dependency: get_current_user
    """
    # token_data is the decoded JWT payload
    user_id = token_data.get("sub")  # Extract user ID from the payload
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return user