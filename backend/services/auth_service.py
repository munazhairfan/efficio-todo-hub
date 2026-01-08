"""
Authentication Service Layer
Handles all authentication-related business logic
"""
from typing import Optional, Dict, Any
from datetime import timedelta
from fastapi import HTTPException, status
import uuid
from models.user import User
from core.auth.jwt_handler import create_access_token
from core.security.password import hash_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def create_user_service(email: str, password: str, name: str, db: AsyncSession) -> Dict[str, Any]:
    """
    Service function to create a new user
    # UI Component: SignupForm -> Service: create_user_service
    """
    # Normalize email: trim whitespace and convert to lowercase for comparison
    normalized_email = email.strip().lower()

    # Check if user already exists
    result = await db.execute(select(User).where(func.lower(func.trim(User.email)) == normalized_email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password before storing
    hashed_password = hash_password(password)

    # Create new user
    new_user = User(
        email=email,
        password=hashed_password,
        name=name
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Create JWT token with user information
    user_data = {
        "sub": str(new_user.id),  # user ID as subject
        "email": new_user.email,
        "is_active": True
    }

    # Set token expiration (24 hours by default)
    expire = timedelta(hours=24)
    access_token = create_access_token(
        data=user_data,
        expires_delta=expire
    )

    return {
        "token": access_token,  # Changed from access_token to token for frontend compatibility
        "token_type": "bearer",
        "user": {
            "id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name,
            "createdAt": new_user.created_at.isoformat(),
            "updatedAt": new_user.updated_at.isoformat()
        }
    }


async def authenticate_user_service(email: str, password: str, db: AsyncSession) -> Dict[str, Any]:
    """
    Service function to authenticate user
    # UI Component: SigninForm -> Service: authenticate_user_service
    """
    # Normalize email: trim whitespace and convert to lowercase for comparison
    normalized_email = email.strip().lower()

    # Find user by email
    result = await db.execute(select(User).where(func.lower(func.trim(User.email)) == normalized_email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify the password
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token with user information
    user_data = {
        "sub": str(user.id),  # user ID as subject
        "email": user.email,
        "is_active": True
    }

    # Set token expiration (24 hours by default)
    expire = timedelta(hours=24)
    access_token = create_access_token(
        data=user_data,
        expires_delta=expire
    )

    return {
        "token": access_token,  # Changed from access_token to token for frontend compatibility
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "createdAt": user.created_at.isoformat(),
            "updatedAt": user.updated_at.isoformat()
        }
    }