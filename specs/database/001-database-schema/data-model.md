# Data Model: Database Schema

## Key Entities

### User
- **Fields**:
  - id: UUID (primary key, unique, required)
  - email: string (unique, required, valid email format)
  - created_at: datetime (timezone-aware, required, auto-generated)
  - updated_at: datetime (timezone-aware, required, auto-generated)

- **Validation Rules**:
  - Email must be unique and follow valid email format
  - ID must be a valid UUID
  - Created_at and updated_at must be timezone-aware timestamps

- **Constraints**:
  - Primary key: id (UUID)
  - Unique constraint: email
  - Non-null constraints: all fields

### Todo
- **Fields**:
  - id: UUID (primary key, unique, required)
  - title: string (required, max length 255)
  - description: string (optional, text field)
  - completed: boolean (required, default: false)
  - created_at: datetime (timezone-aware, required, auto-generated)
  - updated_at: datetime (timezone-aware, required, auto-generated)
  - user_id: UUID (foreign key to User, required)

- **Validation Rules**:
  - ID must be a valid UUID
  - Title must not be empty
  - User_id must reference a valid User
  - Created_at and updated_at must be timezone-aware timestamps

- **Constraints**:
  - Primary key: id (UUID)
  - Foreign key: user_id → User.id
  - Index: user_id (for efficient filtering)
  - Non-null constraints: id, title, completed, created_at, updated_at, user_id

## Relationships
- User → Todo (one-to-many, via user_id foreign key)
- Todo belongs to User (many-to-one, via user_id foreign key)

## Database Configuration

### Connection Settings
- Database: PostgreSQL (hosted on Neon)
- Driver: asyncpg (for async operations)
- Pool size: 20 connections (adjustable based on load)
- Connection timeout: 30 seconds

### Indexes
- User.email: Unique index for fast lookups
- Todo.user_id: Index for efficient user-specific queries
- Todo.created_at: Index for time-based queries (if needed)

### Data Types
- UUID: PostgreSQL UUID type with Python UUID objects
- Datetime: Timezone-aware timestamps using PostgreSQL timestamptz
- Boolean: Native PostgreSQL boolean type
- String: Varchar with appropriate length limits
- Text: PostgreSQL text type for longer content

## Schema Evolution
- Migrations: Managed with Alembic
- Version control: Each schema change tracked as migration revision
- Rollback capability: All migrations support rollback
- Auto-generation: Use Alembic autogenerate for new migrations