# Quickstart Guide: Database Layer

This guide provides instructions for setting up and using the PostgreSQL database layer with SQLModel ORM.

## Setup

1. **Install Dependencies**: Make sure you have all required dependencies installed:
   ```bash
   pip install sqlmodel asyncpg alembic psycopg2-binary
   ```

2. **Environment Configuration**: Set up your database URL in environment variables:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://username:password@localhost/dbname"
   ```

3. **Database Initialization**: Initialize your database with the required tables:
   ```bash
   # Run migrations to create tables
   cd backend
   alembic upgrade head
   ```

## Database Models

The database layer includes two main models:

### User Model
- `id`: UUID primary key
- `email`: Unique email address (required)
- `created_at`: Timestamp when record was created (timezone-aware)
- `updated_at`: Timestamp when record was last updated (timezone-aware)

### Todo Model
- `id`: UUID primary key
- `title`: Task title (required, max 255 chars)
- `description`: Optional task description
- `completed`: Boolean indicating completion status (default: false)
- `user_id`: UUID foreign key linking to User (required)
- `created_at`: Timestamp when record was created (timezone-aware)
- `updated_at`: Timestamp when record was last updated (timezone-aware)

## Usage

### Database Sessions
Use the provided session dependency in your FastAPI routes:

```python
from backend.database.session import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_user_todos(user_id: UUID, session: AsyncSession = Depends(get_session)):
    todos = await session.exec(select(Todo).where(Todo.user_id == user_id))
    return todos.all()
```

### Multi-user Data Isolation
All queries should filter by `user_id` to ensure data isolation:

```python
# Always filter by user_id to ensure data isolation
todos = await session.exec(
    select(Todo).where(Todo.user_id == current_user.id)
)
```

## Migrations

The database uses Alembic for schema migrations:

- Create new migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`
- Rollback migrations: `alembic downgrade -1`

## Configuration

Database configuration is located in `backend/database/config.py` and connection settings in `backend/db.py`.

The database layer follows all requirements from the specification:
- PostgreSQL with Neon hosting support
- SQLModel ORM with FastAPI compatibility
- UUID primary keys for security
- Timezone-aware timestamps
- User_id-based data isolation
- Proper indexing for performance