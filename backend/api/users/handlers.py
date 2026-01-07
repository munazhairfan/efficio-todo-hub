from fastapi import APIRouter, Depends
from dependencies.auth_deps import get_current_user
from pydantic import BaseModel
from typing import Dict, Any
from models.user import User

# Initialize the router
router = APIRouter()

class ProtectedResponse(BaseModel):
    message: str
    user_id: str

@router.get("/protected", response_model=ProtectedResponse)
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    """
    Example of a protected endpoint that requires a valid JWT token
    # UI Component: ProtectedRoute -> Backend Endpoint: GET /api/protected
    """
    return {
        "message": "This is a protected endpoint",
        "user_id": str(current_user.id)
    }

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get user profile information
    # UI Component: Navbar User Profile -> Backend Endpoint: GET /api/profile
    # Expected by UI pattern: Returns user information for display in UI components
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "createdAt": current_user.created_at,
        "updatedAt": current_user.updated_at
    }