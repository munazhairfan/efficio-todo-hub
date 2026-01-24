from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    database_url: str = "sqlite:///./todo_app.db"  # Default to SQLite for local development
    secret_key: str = "dev-secret-key-change-in-production"  # Default for development/testing
    openrouter_api_key: str = ""  # Optional - will be set via OPENROUTER_API_KEY environment variable if needed
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database settings
    db_pool_size: int = 5  # Reduced for Hugging Face environment
    db_pool_overflow: int = 10
    db_echo: bool = False

    # API settings
    api_prefix: str = "/api"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()