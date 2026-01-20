from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from typing import Optional
import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext

from database import get_session
from src.core.config import settings
from src.models.user import User, UserCreate, UserUpdate, UserResponse

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/api/users", tags=["users"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_jwt_token(authorization: str = Header(None)):
    """
    Verify JWT token from Authorization header and extract user information.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is required")

    # Check if authorization header starts with "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format. Expected 'Bearer <token>'")

    # Extract the token part after "Bearer "
    token = authorization[7:]  # Remove "Bearer " prefix

    try:
        # Decode the JWT token using the secret key and algorithm from settings
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(UserLogin):
    name: str


@router.get("/", response_model=UserResponse)
def get_current_user(
    authorization: str = Header(None),
    session: Session = Depends(get_session)
):
    """
    Get current authenticated user's information.
    Extracts user ID from JWT token and returns user details.
    """
    token_payload = verify_jwt_token(authorization)

    user_id = token_payload.get("sub") or token_payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user ID not found")

    # Query the user from the database
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return user data as response
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserRegister,
    session: Session = Depends(get_session)
):
    """
    Register a new user.
    Creates a new user in the database with hashed password.
    """
    # Check if user with this email already exists
    existing_user = session.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user
    user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Return user data as response
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.post("/login")
def login_user(
    user_data: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Login user and return JWT token.
    Verifies credentials and returns a JWT token.
    """
    # Find user by email
    user = session.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Create access token
    access_token = create_access_token(data={"sub": user.id, "email": user.email})

    # Return token and user info
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    }


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    authorization: str = Header(None),
    session: Session = Depends(get_session)
):
    """
    Update user information.
    """
    # Verify the token and get current user
    token_payload = verify_jwt_token(authorization)
    current_user_id = token_payload.get("sub") or token_payload.get("id")

    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    # Find the user to update
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields if provided
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email

    session.add(user)
    session.commit()
    session.refresh(user)

    # Return updated user data
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    authorization: str = Header(None),
    session: Session = Depends(get_session)
):
    """
    Delete a user.
    """
    # Verify the token and get current user
    token_payload = verify_jwt_token(authorization)
    current_user_id = token_payload.get("sub") or token_payload.get("id")

    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    # Find the user to delete
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}