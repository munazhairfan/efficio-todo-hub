from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    database_url: str  # Required - will be set via DATABASE_URL environment variable
    secret_key: str  # Required - will be set via SECRET_KEY environment variable
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


settings = Settings()