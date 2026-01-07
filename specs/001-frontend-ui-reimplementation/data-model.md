# Data Model: Frontend UI Reimplementation

## Entities

### User
- **Fields**:
  - id: string (unique identifier from backend)
  - email: string (user's email address)
  - name: string (user's display name)
  - createdAt: Date (when user account was created)
  - updatedAt: Date (when user account was last updated)

- **Relationships**:
  - Has many: Todo items (one user can have multiple todos)

### Todo
- **Fields**:
  - id: string (unique identifier from backend)
  - title: string (the todo item text)
  - description: string (optional detailed description)
  - completed: boolean (whether the todo is completed)
  - createdAt: Date (when todo was created)
  - updatedAt: Date (when todo was last updated)
  - userId: string (foreign key to user who owns this todo)

- **Relationships**:
  - Belongs to: User (one user owns this todo)

### Authentication Token
- **Fields**:
  - token: string (JWT token string)
  - expiration: Date (when token expires)
  - userId: string (user this token belongs to)

- **Relationships**:
  - Belongs to: User (token is associated with a specific user)

## Validation Rules

### User
- Email must be a valid email format
- Name must be between 1 and 100 characters
- Email must be unique across all users

### Todo
- Title must be between 1 and 255 characters
- Completed must be a boolean value
- userId must reference an existing user
- User can only access their own todos

## State Transitions

### Todo State Transitions
- Active → Completed: When user marks todo as complete
- Completed → Active: When user unmarks todo as complete

### Authentication State Transitions
- Unauthenticated → Authenticated: When user successfully signs in
- Authenticated → Unauthenticated: When user signs out or token expires