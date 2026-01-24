from typing import Generator, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from src.database.session import get_db
from src.core.config import settings


from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from src.core.config import settings
from src.models.user import User
from sqlmodel import select

security = HTTPBearer(auto_error=False)  # Don't auto-error so we can handle unauthenticated users gracefully


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to get the current user from the JWT token.
    Returns None for unauthenticated users, allowing endpoints to handle authentication as needed.
    """
    if not credentials or not credentials.credentials:
        # Return None for unauthenticated users, which will be handled by individual endpoints
        return None

    try:
        # Decode the JWT token
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")

        if user_id is None:
            return None  # Return None instead of raising exception to allow fallback

        # Get user from database
        try:
            user = db.exec(select(User).where(User.id == int(user_id))).first()
            if user is None:
                return None  # Return None instead of raising exception to allow fallback
        except ValueError:
            # If user_id is not numeric, it might be invalid
            return None

        return user
    except jwt.ExpiredSignatureError:
        return None  # Return None instead of raising exception to allow fallback
    except jwt.JWTError:
        return None  # Return None instead of raising exception to allow fallback
    except Exception as e:
        # For any other error, return None to indicate unauthenticated state
        return None


def get_db_session() -> Generator:
    """
    Dependency to get database session
    """
    try:
        db = next(get_db())
        yield db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        db.close()