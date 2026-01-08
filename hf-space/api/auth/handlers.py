from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from core.auth.jwt_handler import verify_token as verify_jwt_token
from services.auth_service import create_user_service, authenticate_user_service
from dependencies.db_deps import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

# Initialize the router
router = APIRouter()

# Pydantic models for request/response
class UserSignup(BaseModel):
    email: str
    password: str
    name: str

class UserSignin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    token: str  # Changed from access_token to token for frontend compatibility
    token_type: str
    user: dict

class VerifyTokenRequest(BaseModel):
    token: str

class VerifyTokenResponse(BaseModel):
    user: dict
    is_valid: bool


@router.post("/auth/signup", response_model=TokenResponse)
async def signup(user: UserSignup, db: AsyncSession = Depends(get_db_session)):
    """
    Create a new user account and return JWT token
    # UI Component: Navbar Login Button -> Auth Form -> Backend Endpoint: POST /api/auth/signup
    # Expected by UI pattern: Form with email/password fields, returns token for auth state
    """
    result = await create_user_service(user.email, user.password, user.name, db)
    return result


@router.post("/auth/signin", response_model=TokenResponse)
async def signin(user: UserSignin, db: AsyncSession = Depends(get_db_session)):
    """
    Authenticate user and return JWT token
    # UI Component: Navbar Login Button -> Auth Form -> Backend Endpoint: POST /api/auth/signin
    # Expected by UI pattern: Form with email/password fields, returns token for auth state
    """
    result = await authenticate_user_service(user.email, user.password, db)
    return result


@router.post("/auth/verify", response_model=VerifyTokenResponse)
async def verify_token_endpoint(request: VerifyTokenRequest):
    """
    Verify if a token is valid
    # UI Component: AuthProvider -> Backend Endpoint: POST /api/auth/verify
    """
    try:
        payload = verify_jwt_token(request.token)
        return {
            "user": {
                "id": payload.get("sub"),
                "email": payload.get("email", "")
            },
            "is_valid": True
        }
    except HTTPException:
        return {
            "user": {},
            "is_valid": False
        }