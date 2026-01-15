from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from ..database.session import get_db
from ..core.config import settings


def get_current_user(db: Session = Depends(get_db)):
    """
    Dependency to get the current user from the token.
    For now, this is a placeholder that returns a mock user.
    """
    # This will be implemented with proper authentication later
    # For now, returning a mock user for demonstration
    return {"id": 1, "username": "mock_user"}


def get_db_session() -> Generator:
    """
    Dependency to get database session
    """
    try:
        db = next(get_db())
        yield db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        db.close()