"""
Utility helper functions for the application
"""


def format_response(data, message="Success", status_code=200):
    """
    Format a standard API response
    """
    return {
        "data": data,
        "message": message,
        "status_code": status_code
    }


def validate_email(email: str) -> bool:
    """
    Basic email validation
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_input(input_str: str) -> str:
    """
    Basic input sanitization
    """
    if not input_str:
        return ""
    return input_str.strip()


def generate_uuid():
    """
    Generate a new UUID
    """
    import uuid
    return uuid.uuid4()