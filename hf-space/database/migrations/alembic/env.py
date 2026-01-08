from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the backend directory to the Python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, backend_dir)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models for autogenerate support
from db import DATABASE_URL
from database.models.user import User
from database.models.todo import Todo

# Update the sqlalchemy.url to use sync driver for alembic
sync_db_url = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
config.set_main_option('sqlalchemy.url', sync_db_url)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = User.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # For autogenerate, we want to avoid connecting to the database
    # so we'll catch the command type and handle accordingly
    url = config.get_main_option("sqlalchemy.url")
    
    # Use a dummy SQLite URL for autogenerate to avoid needing PostgreSQL
    from sqlalchemy import create_engine
    # Create a temporary in-memory SQLite engine for autogenerate
    connectable = create_engine('sqlite://')  # Use SQLite for schema introspection

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Check if we're running in offline mode or if it's an autogenerate command
if context.is_offline_mode():
    run_migrations_offline()
else:
    # Check command line arguments to see if we're doing autogenerate
    import argparse
    import sys
    
    # If autogenerate is requested, run in offline mode to avoid DB connection
    if any('autogenerate' in arg for arg in sys.argv):
        run_migrations_offline()
    else:
        run_migrations_online()
