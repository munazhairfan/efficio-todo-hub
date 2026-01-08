"""
Database configuration per backend/CLAUDE.md guidelines
"""
import os

# Database URL from environment variable per backend/CLAUDE.md
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Connection pool settings per research.md
POOL_SIZE = 20
CONNECTION_TIMEOUT = 30