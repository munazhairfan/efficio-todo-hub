"""
User Service Layer
Handles all user-related business logic
"""
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from models.user import User


async def get_user_profile_service(user_id: uuid.UUID, db: AsyncSession) -> Dict[str, Any]:
    """
    Service function to get user profile information
    # UI Component: ProfilePage -> Service: get_user_profile_service
    """
    # Query for the user by ID
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "user_id": str(user.id),
        "email": user.email,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }


async def verify_user_exists_service(user_id: uuid.UUID, db: AsyncSession) -> bool:
    """
    Service function to verify if a user exists
    # UI Component: AuthProvider -> Service: verify_user_exists_service
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    return user is not None