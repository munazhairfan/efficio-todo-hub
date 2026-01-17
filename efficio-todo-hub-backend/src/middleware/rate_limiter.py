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
        # Check if this endpoint should be rate limited
        should_limit = any(pattern.replace("{user_id}", "[0-9]+") in str(request.url.path)
                         for pattern in self.endpoint_patterns)

        if should_limit:
            # Extract user_id from path
            path_parts = request.url.path.split("/")
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