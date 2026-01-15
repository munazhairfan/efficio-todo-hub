"""Input validation utilities for chat endpoint."""

from typing import Optional
from fastapi import HTTPException


def validate_message_content(message: str) -> None:
    """
    Validate message content according to security requirements.

    Args:
        message: The message content to validate

    Raises:
        HTTPException: If validation fails
    """
    # Check if message is empty
    if not message or not message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    # Check message length (must be <= 1000 characters)
    if len(message) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Message too long, must be 1000 characters or less"
        )


def validate_user_identity(requested_user_id: str, authenticated_user_id: str) -> None:
    """
    Validate that the requested user_id matches the authenticated user.

    Args:
        requested_user_id: The user_id from the request path
        authenticated_user_id: The user_id from the authentication token

    Raises:
        HTTPException: If user identity validation fails
    """
    if str(requested_user_id) != str(authenticated_user_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's conversations"
        )


def sanitize_input(input_str: str) -> str:
    """
    Sanitize input string by removing potentially harmful content.

    Args:
        input_str: The input string to sanitize

    Returns:
        Sanitized string
    """
    # Strip leading/trailing whitespace
    sanitized = input_str.strip()

    # In a more advanced implementation, we might add more sanitization
    # such as removing potential SQL injection or XSS attempts

    return sanitized