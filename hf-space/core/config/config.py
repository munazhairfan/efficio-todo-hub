"""
Configuration settings for the application
"""
import os
from typing import Optional


class Settings:
    """Application settings"""

    def __init__(self):
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")
        self.auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key")
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"
        self.app_name: str = "Todo API with Authentication"
        self.api_v1_prefix: str = "/api"
        self.jwt_algorithm: str = "HS256"
        self.access_token_expire_minutes: int = 30


# Create a single instance of settings
settings = Settings()