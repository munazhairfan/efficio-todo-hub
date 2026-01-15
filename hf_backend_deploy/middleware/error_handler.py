from typing import Callable, Awaitable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
import logging
from datetime import datetime
from typing import Dict, Any


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: logging.Logger = None):
        super().__init__(app)
        self.logger = logger or logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        try:
            response = await call_next(request)

            # Log successful requests
            if response.status_code >= 400:
                self.logger.warning(f"Request to {request.url} resulted in status {response.status_code}")

            return response
        except HTTPException as http_exc:
            # Handle FastAPI HTTP exceptions
            return self._handle_http_exception(request, http_exc)
        except StarletteHTTPException as starlette_exc:
            # Handle Starlette HTTP exceptions
            return self._handle_starlette_exception(request, starlette_exc)
        except Exception as exc:
            # Handle all other exceptions
            return self._handle_general_exception(request, exc)

    def _handle_http_exception(self, request: Request, exc: HTTPException):
        """Handle FastAPI HTTP exceptions"""
        error_detail = {
            "error": {
                "type": "client_error" if exc.status_code < 500 else "server_error",
                "message": exc.detail if isinstance(exc.detail, str) else "An error occurred",
                "code": exc.status_code
            }
        }

        # Log the error
        self.logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")

        return JSONResponse(
            status_code=exc.status_code,
            content=error_detail
        )

    def _handle_starlette_exception(self, request: Request, exc: StarletteHTTPException):
        """Handle Starlette HTTP exceptions"""
        error_detail = {
            "error": {
                "type": "client_error" if exc.status_code < 500 else "server_error",
                "message": exc.detail if isinstance(exc.detail, str) else "An error occurred",
                "code": exc.status_code
            }
        }

        # Log the error
        self.logger.error(f"Starlette Exception: {exc.status_code} - {exc.detail}")

        return JSONResponse(
            status_code=exc.status_code,
            content=error_detail
        )

    def _handle_general_exception(self, request: Request, exc: Exception):
        """Handle general exceptions and convert to user-friendly messages"""
        # Log the full exception with traceback
        self.logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)

        # Create a user-friendly error response
        error_detail = {
            "error": {
                "type": "server_error",
                "message": "An unexpected error occurred. Our team has been notified.",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        }

        # Don't expose internal error details to the user
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_detail
        )


def setup_error_handling(app):
    """Helper function to add error handling middleware to FastAPI app"""
    app.add_middleware(ErrorHandlerMiddleware)


# Custom exception classes for specific error types
class ValidationError(Exception):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)


class ResourceNotFoundError(Exception):
    """Raised when a requested resource is not found"""
    def __init__(self, resource_type: str, identifier: str = None):
        self.resource_type = resource_type
        self.identifier = identifier
        message = f"{resource_type} not found"
        if identifier:
            message += f" with identifier '{identifier}'"
        super().__init__(message)


class BusinessLogicError(Exception):
    """Raised when business logic validation fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def handle_validation_error(exc: ValidationError) -> JSONResponse:
    """Convert ValidationError to user-friendly response"""
    error_detail = {
        "error": {
            "type": "validation_error",
            "message": exc.message,
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    }

    if exc.field:
        error_detail["error"]["field"] = exc.field

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_detail
    )


def handle_resource_not_found_error(exc: ResourceNotFoundError) -> JSONResponse:
    """Convert ResourceNotFoundError to user-friendly response"""
    error_detail = {
        "error": {
            "type": "resource_not_found",
            "message": str(exc),
            "code": status.HTTP_404_NOT_FOUND
        }
    }

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_detail
    )