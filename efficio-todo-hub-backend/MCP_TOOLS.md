# MCP (Model Context Protocol) Tools Implementation

This document describes the implementation of MCP tools for AI agents to manage user tasks in the Todo Hub application.

## Overview

The MCP tools provide a standardized interface for AI agents to interact with user tasks. These tools follow the Model Context Protocol specifications and provide full CRUD (Create, Read, Update, Delete) operations for tasks.

## Available Tools

### 1. `add_task`

Creates a new task for a user.

**Parameters:**
- `user_id` (string, required): The ID of the user requesting the operation
- `title` (string, required): The title of the task to create
- `description` (string, optional): Detailed description of the task

**Returns:**
```json
{
  "task_id": 123,
  "status": "created",
  "title": "Task title"
}
```

### 2. `list_tasks`

Retrieves tasks for a user with optional filtering.

**Parameters:**
- `user_id` (string, required): The ID of the user requesting the operation
- `status` (string, optional): Filter by status ("all", "pending", "completed") - defaults to "all"

**Returns:**
```json
[
  {
    "id": 123,
    "title": "Task title",
    "description": "Task description",
    "status": "pending",
    "created_at": "2023-01-01T00:00:00"
  }
]
```

### 3. `complete_task`

Marks a task as completed.

**Parameters:**
- `user_id` (string, required): The ID of the user requesting the operation
- `task_id` (integer, required): The ID of the task to complete

**Returns:**
```json
{
  "task_id": 123,
  "status": "completed",
  "title": "Task title"
}
```

### 4. `delete_task`

Removes a task.

**Parameters:**
- `user_id` (string, required): The ID of the user requesting the operation
- `task_id` (integer, required): The ID of the task to delete

**Returns:**
```json
{
  "task_id": 123,
  "status": "deleted",
  "title": "Task title"
}
```

### 5. `update_task`

Updates task title or description.

**Parameters:**
- `user_id` (string, required): The ID of the user requesting the operation
- `task_id` (integer, required): The ID of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task

**Returns:**
```json
{
  "task_id": 123,
  "status": "updated",
  "title": "New task title"
}
```

## Error Handling

The MCP tools implement comprehensive error handling with the following custom exceptions:

- `ValidationError`: Thrown when input validation fails
- `TaskNotFoundError`: Thrown when a requested task doesn't exist
- `AuthorizationError`: Thrown when a user attempts to access a task they don't own

## Architecture

### Models
- `Task`: Database model with id, user_id, title, description, completed status, and timestamps
- `TaskCreate`, `TaskUpdate`, `TaskResponse`: Pydantic models for API validation

### Services
- `TaskService`: Business logic layer with full CRUD operations
- Proper database session management with transaction handling

### Utilities
- `Error handling utilities`: Standardized error responses following MCP specifications
- Input validation and user authentication

## Security

- User authentication ensures task ownership verification
- Users can only access, modify, or delete their own tasks
- Proper input validation to prevent injection attacks

## Testing

Comprehensive tests are included:
- Unit tests for all MCP tools
- Database connectivity tests
- Integration tests
- Error handling validation