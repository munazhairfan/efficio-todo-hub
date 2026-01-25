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
        print(f"DEBUG: Attempting to decode JWT token")
        print(f"DEBUG: Secret key (first 10 chars): {settings.secret_key[:10] if settings.secret_key else 'NOT SET'}")
        print(f"DEBUG: Algorithm: {settings.algorithm}")
        print(f"DEBUG: Raw token (first 20 chars): {credentials.credentials[:20] if credentials.credentials else 'NO TOKEN'}...")
        print(f"DEBUG: Full token length: {len(credentials.credentials) if credentials.credentials else 0}")

        # Let's also try to decode without verification to see the token contents
        try:
            # Decode header and payload without verification to inspect token
            import base64
            if credentials.credentials:
                token_parts = credentials.credentials.split('.')
                if len(token_parts) == 3:
                    # Decode header
                    header_part = token_parts[0]
                    # Add padding if needed
                    header_part += '=' * (4 - len(header_part) % 4)
                    header_bytes = base64.b64decode(header_part)
                    header_json = header_bytes.decode('utf-8')
                    print(f"DEBUG: JWT Header: {header_json}")

                    # Decode payload
                    payload_part = token_parts[1]
                    # Add padding if needed
                    payload_part += '=' * (4 - len(payload_part) % 4)
                    payload_bytes = base64.b64decode(payload_part)
                    payload_json = payload_bytes.decode('utf-8')
                    print(f"DEBUG: JWT Payload: {payload_json}")

                    # Extract algorithm from header to see if it matches settings
                    import json
                    header_data = json.loads(header_json)  # Use header_json from above
                    token_algorithm = header_data.get('alg', 'unknown')
                    print(f"DEBUG: Token algorithm from header: {token_algorithm}")
                    print(f"DEBUG: Expected algorithm from settings: {settings.algorithm}")

                    if token_algorithm != settings.algorithm:
                        print(f"DEBUG: WARNING: Token algorithm '{token_algorithm}' doesn't match expected '{settings.algorithm}'")

        except Exception as e:
            print(f"DEBUG: Could not decode token header/payload for inspection: {e}")
            print(f"DEBUG: Token structure might be invalid or improperly formatted")

        # Decode JWT with verification
        try:
            payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        except jwt.JWTError as e:
            print(f"DEBUG: JWT verification failed - Token: {credentials.credentials[:50]}..., Error: {str(e)}")
            raise
        user_id: str = payload.get("sub")

        print(f"DEBUG: JWT decode successful, user_id: {user_id}")

        if user_id is None:
            print("DEBUG: JWT payload has no 'sub' field, returning None")
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
        print(f"DEBUG: JWT token expired: {str(jwt.ExpiredSignatureError)}")
        return None  # Return None instead of raising exception to allow fallback
    except jwt.JWTError as je:
        print(f"DEBUG: JWT error during decoding: {str(je)}")
        print(f"DEBUG: JWT error type: {type(je)}")
        return None  # Return None instead of raising exception to allow fallback
    except Exception as e:
        # For any other error, return None to indicate unauthenticated state
        print(f"DEBUG: General error in get_current_user: {str(e)}")
        print(f"DEBUG: General error type: {type(e)}")
        import traceback
        print(f"DEBUG: Full traceback: {traceback.format_exc()}")
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