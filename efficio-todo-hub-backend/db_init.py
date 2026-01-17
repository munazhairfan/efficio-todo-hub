"""Database initialization script.

This script provides utilities for initializing the database
and running migrations.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path so we can import our modules
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.database.session import Base


def init_db():
    """Initialize the database with tables."""
    from src.database.session import get_engine

    engine = get_engine()

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def run_migrations():
    """Run alembic migrations."""
    # Set the database URL in the environment
    os.environ['DATABASE_URL'] = settings.database_url

    # Create alembic config
    alembic_cfg = Config("alembic.ini")

    # Run migrations
    command.upgrade(alembic_cfg, "head")
    print("Database migrations applied successfully!")


def create_migration(message):
    """Create a new migration."""
    # Set the database URL in the environment
    os.environ['DATABASE_URL'] = settings.database_url

    # Create alembic config
    alembic_cfg = Config("alembic.ini")

    # Generate migration
    command.revision(alembic_cfg, autogenerate=True, message=message)
    print(f"Migration created: {message}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db_init.py [init|upgrade|create-migration]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init_db()
    elif command == "upgrade":
        run_migrations()
    elif command == "create-migration":
        if len(sys.argv) < 3:
            print("Usage: python db_init.py create-migration \"migration message\"")
            sys.exit(1)
        create_migration(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print("Usage: python db_init.py [init|upgrade|create-migration]")
        sys.exit(1)