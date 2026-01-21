# Data Model: Single Assistant Conversational + CRUD Behavior

## Entities

### User Message
**Description**: Represents input from the user
- **Fields**:
  - `input` (string, optional): Main content of the user's message
  - `message` (string, optional): Alternative field name for message content
  - `text` (string, optional): Alternative field name for message content
  - `sessionId` (string, optional): Identifier for the conversation session
  - `session_id` (string, optional): Alternative field name for session ID
  - `context` (dict, optional): Additional context information
  - `ctx` (dict, optional): Alternative field name for context

### Assistant Response
**Description**: Represents output from the assistant
- **Fields**:
  - `responseType` (string): Type of response (success, clarification, etc.)
  - `message` (string): Text response to the user
  - `clarifyingQuestions` (list): Questions to clarify user intent
  - `suggestedActions` (list): Suggested follow-up actions
  - `conversationId` (string, optional): ID of the conversation
  - `analysis` (dict): Analysis of the user input including intent, ambiguity, and vagueness data

### Task
**Description**: Represents a task entity with CRUD operations
- **Fields**:
  - `id` (int): Unique identifier for the task
  - `title` (string): Title of the task
  - `description` (string, optional): Detailed description of the task
  - `status` (string): Status of the task (pending, completed, etc.)
  - `created_at` (datetime): Timestamp when task was created
  - `updated_at` (datetime): Timestamp when task was last updated

## Validation Rules

### User Message Validation
- At least one of `input`, `message`, or `text` must be provided
- If provided, `sessionId` or `session_id` must be a valid identifier format
- Context data must be a valid dictionary structure

### Assistant Response Validation
- `responseType` must be one of: "success", "clarification", "error"
- `message` must be a non-empty string
- `clarifyingQuestions` must be an array of strings
- `suggestedActions` must be an array of strings

### Task Validation
- `title` must be a non-empty string with maximum length
- `status` must be one of predefined valid statuses
- Timestamps must be valid ISO 8601 format

## State Transitions

### Task State Transitions
- `pending` → `completed`: When task is marked as done
- `completed` → `pending`: When task is reopened
- `pending` → `pending`: When task details are updated