"""Error handling utilities for MCP tools."""


class MCPError(Exception):
    """Base exception for MCP tools"""
    pass


class TaskNotFoundError(MCPError):
    """Raised when a task is not found"""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class AuthenticationError(MCPError):
    """Raised when user authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class ValidationError(MCPError):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message)


class AuthorizationError(MCPError):
    """Raised when user is not authorized to perform an action"""
    def __init__(self, message: str = "Authorization failed"):
        super().__init__(message)


def handle_mcp_error(error: Exception) -> dict:
    """Convert exceptions to standardized error responses for MCP tools"""
    if isinstance(error, TaskNotFoundError):
        return {
            "error": "task_not_found",
            "message": str(error),
            "task_id": error.task_id
        }
    elif isinstance(error, (AuthenticationError, AuthorizationError)):
        return {
            "error": "authorization_error",
            "message": str(error)
        }
    elif isinstance(error, ValidationError):
        return {
            "error": "validation_error",
            "message": str(error)
        }
    else:
        # For any other error, return a generic error
        return {
            "error": "internal_error",
            "message": "An internal error occurred"
        }