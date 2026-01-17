# Quickstart Guide: Production Database Migrations

## Overview
This guide explains how to set up and run database migrations for the production PostgreSQL database (Neon) to ensure all required chatbot tables exist.

## Prerequisites
- Python 3.11+
- PostgreSQL (Neon) database access
- Alembic installed (included in requirements)

## Setup

### 1. Environment Variables
Ensure the Neon database URL is available in your environment:
```bash
export DATABASE_URL="postgresql://user:password@hostname:port/database_name"
```

### 2. Initialize Alembic
The project already has Alembic initialized in the `alembic/` directory. If starting fresh:
```bash
cd backend
alembic init alembic
```

### 3. Configure Alembic
Update `alembic.ini` and `alembic/env.py` to use the correct database URL from environment variables and reference the SQLModel metadata.

## Implementation Steps

### 1. Update Alembic Configuration
Modify `alembic/env.py` to use SQLModel's metadata:
- Import the metadata from the models
- Set target_metadata to reference the SQLModel metadata
- Configure database URL to read from environment variables

### 2. Generate Initial Migration
Create the initial migration file for the existing models:
```bash
alembic revision --autogenerate -m "Initial migration for conversation and message tables"
```

### 3. Apply Migration Locally
Test the migration locally first:
```bash
alembic upgrade head
```

### 4. Configure Production Deployment
Ensure migrations can run in the production environment:
- Set up environment-specific configuration
- Add migration execution to deployment process
- Handle potential downtime scenarios during migration

## Usage
Once implemented, migrations can be run with:
- `alembic upgrade head` - Apply all pending migrations
- `alembic downgrade -1` - Rollback the last migration
- `alembic current` - Show current migration state
- `alembic history` - Show migration history

## Testing
Test the migration process by:
1. Creating a fresh database
2. Running `alembic upgrade head` to create all tables
3. Verifying the tables exist with correct schema
4. Running the application to ensure chat functionality works