# Chat API Documentation

## Overview
The Chat API provides endpoints for managing conversations and exchanging messages between users and an AI assistant. All data is persisted in a PostgreSQL database.

## Endpoints

### POST `/api/{user_id}/chat`
Initiates a new conversation or continues an existing one.

#### Parameters
- `user_id` (path): The ID of the user making the request (positive integer)

#### Request Body
```json
{
  "message": "string (required)",
  "conversation_id": "integer (optional, null for new conversation)"
}
```

#### Request Validation
- `message`: Cannot be empty, must be 1-5000 characters
- `conversation_id`: Must be a positive integer if provided
- `user_id`: Must be a positive integer

#### Response
```json
{
  "conversation_id": "integer",
  "response": "string",
  "message_id": "integer",
  "conversation_title": "string or null",
  "has_tool_calls": "boolean",
  "tool_calls": [
    {
      "tool_name": "string",
      "parameters": "object",
      "execution_status": "string or null"
    }
  ]
}
```

#### Usage Examples

**Start a new conversation:**
```bash
curl -X POST "http://localhost:8000/api/1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how can you help me?",
    "conversation_id": null
  }'
```

**Continue an existing conversation:**
```bash
curl -X POST "http://localhost:8000/api/1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me more about that",
    "conversation_id": 123
  }'
```

## Models

### Conversation
Represents a thread of messages between a user and the AI assistant.
- `id`: Unique identifier
- `user_id`: ID of the user who owns the conversation
- `title`: Auto-generated title based on initial message
- `created_at`: Timestamp when conversation was created
- `updated_at`: Timestamp when conversation was last updated

### Message
Represents a single exchange in a conversation.
- `id`: Unique identifier
- `conversation_id`: ID of the associated conversation
- `user_id`: ID of the user who sent the message
- `role`: Either "user" or "assistant"
- `content`: The actual message content
- `timestamp`: When the message was sent
- `metadata_json`: Additional information about the message (for future tool usage)

## Services

### ConversationService
Handles conversation-related operations:
- `create_conversation()` - Creates a new conversation
- `get_conversation_by_id()` - Retrieves a conversation by its ID
- `get_conversation_messages()` - Gets all messages for a conversation
- `update_conversation_title()` - Updates the conversation title

### MessageService
Handles message-related operations:
- `create_message()` - Creates a new message
- `get_message_by_id()` - Retrieves a message by its ID
- `get_messages_by_conversation()` - Gets all messages for a conversation
- `get_recent_messages()` - Gets recent messages for a conversation

## Authentication
The API uses a placeholder authentication system (`get_current_user`) that will be replaced with proper authentication in production.

## Error Handling
- Invalid requests return 422 Unprocessable Entity
- Unauthorized access returns 403 Forbidden
- Missing resources return 404 Not Found
- Server errors return 500 Internal Server Error

## Database
The API uses PostgreSQL with SQLAlchemy ORM and Alembic for migrations.

## Environment Variables
- `DATABASE_URL` - Connection string for PostgreSQL database
- `SECRET_KEY` - Secret key for JWT tokens
- `ALGORITHM` - Algorithm for JWT encoding
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time