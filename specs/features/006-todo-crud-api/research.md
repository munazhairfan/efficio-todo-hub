# Research: Todo CRUD API Implementation

## API Router Structure Decision

### Decision: Use FastAPI APIRouter for /api/todos endpoints
- **Rationale**: FastAPI's APIRouter provides clean separation of concerns and follows REST conventions
- **Implementation**: Create a dedicated router in routes/todos.py with all todo endpoints
- **Benefits**: Modular design, easy testing, clear endpoint grouping

### Decision: Standard REST endpoint patterns
- **Rationale**: Follow established REST conventions for CRUD operations
- **Endpoints**:
  - POST /api/todos - Create new todo
  - GET /api/todos - List user's todos
  - GET /api/todos/{id} - Get specific todo
  - PUT /api/todos/{id} - Update specific todo
  - DELETE /api/todos/{id} - Delete specific todo
- **Benefits**: Familiar patterns, predictable interface

## Dependency Injection Strategy

### Decision: Database session dependency
- **Rationale**: Use FastAPI's dependency injection for database session management
- **Implementation**: Create get_db_session dependency that provides SQLModel async sessions
- **Benefits**: Automatic session cleanup, consistent error handling, testability

### Decision: Authenticated user dependency
- **Rationale**: Extract user_id from JWT and validate against database
- **Implementation**: Create get_current_user dependency that decodes JWT and returns user object
- **Benefits**: Consistent authentication across endpoints, automatic validation

## Error Handling Strategy

### Decision: HTTP status code mapping
- **Rationale**: Follow HTTP standards and REST conventions
- **Implementation**:
  - 200 OK: Successful GET/PUT operations
  - 201 Created: Successful POST operations
  - 204 No Content: Successful DELETE operations
  - 400 Bad Request: Invalid request format
  - 401 Unauthorized: Missing or invalid authentication
  - 404 Not Found: Resource doesn't exist or doesn't belong to user
  - 422 Unprocessable Entity: Validation errors
  - 500 Internal Server Error: Unexpected server errors
- **Benefits**: Standard responses, clear error semantics

### Decision: Error response format
- **Rationale**: Consistent error response structure for client consumption
- **Implementation**: Standard error response format with detail field
- **Benefits**: Predictable error handling on client side

## Response Model Structure

### Decision: Separate request and response models
- **Rationale**: Different fields needed for creation vs retrieval
- **Implementation**:
  - TodoCreate: title, description, completed (optional)
  - TodoUpdate: title (optional), description (optional), completed (optional)
  - TodoResponse: id, title, description, completed, created_at, updated_at, user_id
- **Benefits**: Type safety, clear contracts, proper validation

## Validation Approach

### Decision: Pydantic model validation
- **Rationale**: Leverage FastAPI's built-in Pydantic integration
- **Implementation**: Define Pydantic models for all request/response bodies
- **Benefits**: Automatic validation, clear documentation, type safety

## Security Considerations

### Decision: User isolation enforcement
- **Rationale**: Ensure users can only access their own data
- **Implementation**: Filter all queries by current user's ID, verify ownership before operations
- **Benefits**: Data security, compliance with requirements

### Decision: JWT validation approach
- **Rationale**: Secure authentication using existing JWT infrastructure
- **Implementation**: Validate JWT signature, check expiration, extract user_id
- **Benefits**: Stateless authentication, secure token handling