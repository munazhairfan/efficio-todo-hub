import time
from typing import Dict, Optional
from datetime import datetime, timedelta
from threading import Lock


class RateLimitRecord:
    """
    Represents a user's current rate limit state
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.request_count = 0
        self.window_start = time.time()
        self.last_request_time = time.time()


class RateLimitConfiguration:
    """
    Defines the rate limiting parameters
    """
    def __init__(self):
        self.max_requests = 10  # Maximum 10 requests per window
        self.time_window_seconds = 60  # 60-second window
        self.is_enabled = True  # Rate limiting is active


class InMemoryRateLimiter:
    """
    In-memory rate limiter for chatbot endpoints
    Uses a thread-safe dictionary to track user request counts
    """
    def __init__(self):
        self.records: Dict[str, RateLimitRecord] = {}
        self.config = RateLimitConfiguration()
        self._lock = Lock()  # Thread safety for concurrent access

    def is_allowed(self, user_id: str) -> tuple[bool, Optional[str]]:
        """
        Check if a request from the user is allowed based on rate limits

        Args:
            user_id: The authenticated user ID

        Returns:
            tuple: (is_allowed: bool, error_message: Optional[str])
        """
        if not self.config.is_enabled:
            return True, None

        with self._lock:
            current_time = time.time()

            # Check if we have a record for this user
            if user_id in self.records:
                record = self.records[user_id]

                # Check if the time window has expired
                if current_time - record.window_start >= self.config.time_window_seconds:
                    # Reset the window - create a new record
                    record.request_count = 1
                    record.window_start = current_time
                    record.last_request_time = current_time
                    self.records[user_id] = record
                    return True, None
                else:
                    # Still in the same window, check if limit exceeded
                    if record.request_count >= self.config.max_requests:
                        # Rate limit exceeded
                        seconds_remaining = int(self.config.time_window_seconds - (current_time - record.window_start))
                        error_msg = f"You're sending messages too fast. Please wait a moment."
                        return False, error_msg
                    else:
                        # Increment request count and update timestamp
                        record.request_count += 1
                        record.last_request_time = current_time
                        self.records[user_id] = record
                        return True, None
            else:
                # First request from this user, create a new record
                new_record = RateLimitRecord(user_id)
                new_record.request_count = 1
                new_record.window_start = current_time
                new_record.last_request_time = current_time
                self.records[user_id] = new_record
                return True, None

    def cleanup_expired_records(self):
        """
        Remove expired rate limit records to prevent memory growth
        """
        with self._lock:
            current_time = time.time()
            expired_users = []

            for user_id, record in self.records.items():
                # If the window has expired and it's been a while since the last request, remove the record
                if current_time - record.window_start >= self.config.time_window_seconds * 2:  # Double the window time
                    expired_users.append(user_id)

            for user_id in expired_users:
                del self.records[user_id]


# Global instance of the rate limiter
rate_limiter = InMemoryRateLimiter()