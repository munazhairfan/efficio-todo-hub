# Quickstart: Database Layer

## Setup Instructions

### Database Setup
1. Set up PostgreSQL database (Neon recommended)
2. Add database URL to environment variables:
   ```bash
   DATABASE_URL="postgresql://username:password@ep-spring-cloud-ah41ixls-pooler.c-3.us-east-1.aws.neon.tech/dbname?sslmode=require"
   ```

### Backend Setup
1. Install dependencies:
   ```bash
   pip install sqlmodel asyncpg alembic
   ```

2. Create database directory structure:
   ```
   backend/
   ├── models.py
   ├── db.py
   └── database/
       ├── __init__.py
       ├── models/
       │   ├── __init__.py
       │   ├── base.py
       │   ├── user.py
       │   └── todo.py
       ├── config.py
       ├── session.py
       └── migrations/
           └── alembic/
   ```

### Initialize Alembic
1. Run initialization command:
   ```bash
   cd backend
   alembic init database/migrations/alembic
   ```

2. Update alembic.ini to point to the correct database URL
3. Update env.py to import and configure your models for autogenerate

## Key Components

### Database Configuration (db.py)
- AsyncEngine for PostgreSQL connections
- Database URL from environment variables
- Connection pooling settings

### Models (database/models/)
- Base model with UUID primary key support
- User model with identity reference
- Todo model with user association

### Session Management (database/session.py)
- Dependency for FastAPI to provide database sessions
- Async context management for database operations

## Running the Database Layer

### Development
1. Set up environment variables
2. Run database migrations:
   ```bash
   alembic upgrade head
   ```
3. Start the backend to test database connectivity

### Database Operations
- Generate new migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`
- Rollback migrations: `alembic downgrade -1`

## Multi-user Data Isolation
- All user-specific data must include user_id foreign key
- Query patterns must filter by user_id to ensure data isolation
- Use database indexes on user_id fields for performance