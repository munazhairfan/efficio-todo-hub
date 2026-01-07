# Data Model: Todo CRUD API

## Key Entities

### Todo (Existing Database Model)
- **Fields**:
  - id: UUID (primary key, unique, required) - from existing database model
  - title: string (required, max length 255) - from existing database model
  - description: string (optional, text field) - from existing database model
  - completed: boolean (required, default: false) - from existing database model
  - created_at: datetime (timezone-aware, required, auto-generated) - from existing database model
  - updated_at: datetime (timezone-aware, required, auto-generated) - from existing database model
  - user_id: UUID (foreign key to User, required) - from existing database model

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

### TodoCreate (Request Model)
- **Fields**:
  - title: string (required, max length 255)
  - description: string (optional)
  - completed: boolean (optional, default: false)

- **Validation Rules**:
  - Title must be provided and not empty
  - Title must not exceed 255 characters
  - Description length validation if needed

### TodoUpdate (Request Model)
- **Fields**:
  - title: string (optional, max length 255)
  - description: string (optional)
  - completed: boolean (optional)

- **Validation Rules**:
  - If title is provided, it must not be empty
  - If title is provided, it must not exceed 255 characters

### TodoResponse (Response Model)
- **Fields**:
  - id: UUID (required)
  - title: string (required)
  - description: string (optional)
  - completed: boolean (required)
  - created_at: datetime (required)
  - updated_at: datetime (required)
  - user_id: UUID (required, but may be hidden from client depending on requirements)

- **Validation Rules**:
  - All fields must be present and valid
  - Timestamps must be timezone-aware

## Relationships
- Todo belongs to User (many-to-one, via user_id foreign key)
- User → Todo (one-to-many, via user_id foreign key)

## API Response Models

### TodoListResponse
- **Fields**:
  - todos: List[TodoResponse] (required)

### TodoSingleResponse
- **Fields**:
  - todo: TodoResponse (required)

## Error Response Models

### HTTPException Response
- **Fields**:
  - detail: string (required)

## Schema Evolution
- Models will be based on existing SQLModel database models
- API models will be separate Pydantic models for validation
- No database schema changes required as per constraints