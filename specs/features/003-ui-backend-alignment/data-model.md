# Data Model: Backend UI Alignment

## Overview
This document describes the data models used in the application, focusing on the entities and their relationships that need to be preserved during the backend restructuring.

## Entities

### User
Represents a registered user in the system

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String - User's email address (unique)
- `created_at`: DateTime - Timestamp when user was created
- `updated_at`: DateTime - Timestamp when user was last updated

**Relationships**:
- One-to-Many with Todo (one user can have many todos)

### Todo
Represents a task item created by a user

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the todo
- `title`: String - Title of the todo item (required, max 255 chars)
- `description`: String (Optional) - Detailed description of the todo (max 1000 chars)
- `completed`: Boolean - Whether the todo is completed (default: false)
- `user_id`: UUID (Foreign Key) - Reference to the owning user
- `created_at`: DateTime - Timestamp when todo was created
- `updated_at`: DateTime - Timestamp when todo was last updated

**Relationships**:
- Many-to-One with User (many todos belong to one user)

### Authentication Token
Represents JWT tokens used for user session management

**Fields**:
- `token`: String - The JWT token string
- `user_id`: UUID - Reference to the user the token belongs to
- `expires_at`: DateTime - Expiration timestamp
- `created_at`: DateTime - Timestamp when token was created

## Validation Rules

### User
- Email must be valid email format
- Email must be unique across all users
- Required fields: email

### Todo
- Title must be 1-255 characters
- Title cannot be empty or just whitespace
- Description can be up to 1000 characters
- Completed defaults to false if not specified
- Required fields: title, user_id

## State Transitions

### Todo
- `incomplete` → `completed` (when user marks as done)
- `completed` → `incomplete` (when user unmarks as done)

## Constraints
- Todo items must belong to an existing user
- Users must have unique email addresses
- All timestamps are stored in UTC timezone