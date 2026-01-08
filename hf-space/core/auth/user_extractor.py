"""
User extraction utilities for authentication
"""
from typing import Dict, Any, Optional
from .jwt_handler import verify_token
from fastapi import HTTPException, status


def extract_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Extract user information from JWT token
    """
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id:
            return None

        return {
            "user_id": user_id,
            "email": email,
            "is_active": payload.get("is_active", True),
            "token_scopes": payload.get("scopes", []),
            "exp": payload.get("exp"),
        }
    except HTTPException:
        return None
    except Exception:
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract only the user ID from JWT token
    """
    user_info = extract_user_from_token(token)
    return user_info.get("user_id") if user_info else None


def validate_and_extract_user(token: str) -> Dict[str, Any]:
    """
    Validate token and extract user information, raising exception if invalid
    """
    user_info = extract_user_from_token(token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user_info