from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    database_url: str = "postgresql://localhost/chat_db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database settings
    db_pool_size: int = 20
    db_pool_overflow: int = 0
    db_echo: bool = False

    # API settings
    api_prefix: str = "/api"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()