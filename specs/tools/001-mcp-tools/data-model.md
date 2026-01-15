# Data Model: MCP Tools Implementation

## Task Entity

**Fields:**
- `id` (Integer, Primary Key): Unique identifier for the task
- `user_id` (String): Identifier for the user who owns the task
- `title` (String, Required): Title of the task
- `description` (String, Optional): Detailed description of the task
- `status` (String): Either "pending" or "completed"
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated

**Validation Rules:**
- `title` must not be empty (min length: 1 character)
- `user_id` must exist and be valid
- `status` must be either "pending" or "completed"
- `user_id` must match the authenticated user for operations

**State Transitions:**
- New task: `status` defaults to "pending"
- When complete_task is called: `status` changes from "pending" to "completed"

## MCP Tool Response Format

**Common Response Structure:**
- `task_id` (Integer): The ID of the affected task
- `status` (String): Operation status (e.g., "created", "completed", "deleted", "updated")
- `title` (String): Title of the task

**List Tasks Response:**
- Array of task objects with fields: id, title, description, status, created_at

## Relationships

- **User to Tasks**: One-to-Many (one user can have many tasks)
- Each task belongs to exactly one user
- Access control: Only the owning user can modify a task