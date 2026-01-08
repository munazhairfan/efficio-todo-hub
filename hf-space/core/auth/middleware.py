"""
Authentication Middleware for FastAPI
"""
from fastapi import HTTPException, status, Depends
from .jwt_handler import verify_access_token, verify_token
from typing import Dict, Any


def get_current_user(token_data: Dict[str, Any] = Depends(verify_access_token)) -> Dict[str, Any]:
    """
    Get the current user from the token
    """
    # Extract user information from the token
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Return user information
    return {
        "user_id": user_id,
        "email": token_data.get("email", ""),
        "is_authenticated": True
    }


def verify_current_user_optional(token: str = None) -> Dict[str, Any]:
    """
    Verify current user optionally (for routes that allow both authenticated and unauthenticated access)
    """
    if not token:
        return {"user_id": None, "is_authenticated": False}

    try:
        token_data = verify_token(token)
        return {
            "user_id": token_data.get("sub"),
            "email": token_data.get("email", ""),
            "is_authenticated": True
        }
    except HTTPException:
        return {"user_id": None, "is_authenticated": False}


# Example usage in a route:
# @app.get("/protected")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#     return {"message": "This is a protected route", "user_id": current_user["user_id"]}