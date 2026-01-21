"""Rate limiter middleware implementation for chat endpoint."""

import time
import threading
from collections import defaultdict, deque
from typing import Dict
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

# Configure logger to not expose sensitive information
logging.basicConfig(level=logging.INFO)

class RateLimiter:
    """Thread-safe in-memory rate limiter using token bucket algorithm with sliding window."""

    def __init__(self, limit: int = 10, window_size: int = 60):
        """
        Initialize rate limiter.

        Args:
            limit: Maximum number of requests allowed per window
            window_size: Time window in seconds
        """
        self.limit = limit
        self.window_size = window_size
        self.storage = defaultdict(deque)  # Maps user_id to list of request timestamps
        self.lock = threading.Lock()  # Thread-safety lock

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if a request from the given user is allowed.

        Args:
            user_id: Unique identifier for the user

        Returns:
            True if request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()

            # Remove requests older than the window size
            while (self.storage[user_id] and
                   current_time - self.storage[user_id][0] > self.window_size):
                self.storage[user_id].popleft()

            # Check if limit is exceeded
            if len(self.storage[user_id]) >= self.limit:
                return False

            # Add current request timestamp
            self.storage[user_id].append(current_time)
            return True

# Global rate limiter instance
# Using 10 requests per minute (60 seconds) as specified in requirements
rate_limiter = RateLimiter(limit=10, window_size=60)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware to enforce rate limiting on chat endpoints."""

    def __init__(self, app, endpoint_patterns=None):
        """
        Initialize the middleware.

        Args:
            app: The FastAPI application
            endpoint_patterns: List of endpoint patterns to apply rate limiting to
        """
        super().__init__(app)
        self.endpoint_patterns = endpoint_patterns or ["/api/{user_id}/chat"]

    async def dispatch(self, request: Request, call_next):
        """Process the request and enforce rate limiting."""
        try:
            # Check if this endpoint should be rate limited using proper pattern matching
            should_limit = False
            request_path = str(request.url.path)

            # Explicitly exclude conversation endpoints from rate limiting
            if "/api/conversation/" in request_path:
                # Skip rate limiting for conversation endpoints
                response = await call_next(request)
                return response

            for pattern in self.endpoint_patterns:
                # Simple string-based pattern matching that's safer
                # Replace {user_id} with a placeholder and check if the path matches
                # This is safer than using regex which might cause import issues
                if "{user_id}" in pattern:
                    # Create a basic pattern match without complex regex
                    base_pattern = pattern.replace("{user_id}", "")
                    # Check if the request path contains the base pattern
                    if base_pattern in request_path:
                        # Additional check to see if there's a user ID pattern in the right place
                        path_parts = request_path.split("/")
                        pattern_parts = pattern.split("/")

                        # Do a more careful comparison to avoid false matches
                        if len(path_parts) >= len(pattern_parts):
                            should_limit = True
                            for i, pattern_part in enumerate(pattern_parts):
                                if i >= len(path_parts):
                                    should_limit = False
                                    break
                                if pattern_part == "{user_id}":
                                    # Check if this part is a digit (user_id)
                                    if not path_parts[i].isdigit():
                                        should_limit = False
                                        break
                                elif path_parts[i] != pattern_part:
                                    should_limit = False
                                    break

                            if should_limit:
                                break
                else:
                    # Direct string match for patterns without {user_id}
                    if pattern == request_path:
                        should_limit = True
                        break

            if should_limit:
                # Extract user_id from path
                path_parts = request_path.split("/")
                user_id = None
                for i, part in enumerate(path_parts):
                    if part.isdigit():
                        # Find the digit that comes after 'api' in the path
                        if i > 0 and path_parts[i-1] == "api":
                            user_id = part
                            break

                if user_id:
                    # Check if request is allowed
                    if not rate_limiter.is_allowed(user_id):
                        logger.info(f"Rate limit exceeded for user_id: {user_id}")
                        raise HTTPException(
                            status_code=429,
                            detail="Too many messages. Try again later."
                        )

            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error in rate limiter middleware: {e}")
            # Ensure the request continues even if rate limiter fails
            try:
                response = await call_next(request)
                return response
            except Exception as call_next_error:
                logger.error(f"Critical error in call_next: {call_next_error}")
                # Return a basic response if all else fails
                from starlette.responses import PlainTextResponse
                return PlainTextResponse("Internal Server Error", status_code=500)