# Data Model: Chat API + Conversation Handling

## Entities

### Conversation
Represents a thread of messages between a user and the AI assistant

**Fields**:
- `id` (Integer, Primary Key): Unique identifier for the conversation
- `user_id` (Integer): Reference to the user who owns this conversation
- `created_at` (DateTime): Timestamp when the conversation was created
- `updated_at` (DateTime): Timestamp when the conversation was last updated
- `title` (String, Optional): Auto-generated title for the conversation based on initial message

**Relationships**:
- One-to-many with Message entity (one conversation has many messages)

### Message
Represents a single exchange in a conversation, containing the user's input and the AI's response

**Fields**:
- `id` (Integer, Primary Key): Unique identifier for the message
- `conversation_id` (Integer, Foreign Key): Reference to the conversation this message belongs to
- `user_id` (Integer): Reference to the user who sent this message
- `role` (String): Either "user" or "assistant" indicating who sent the message
- `content` (Text): The actual content of the message
- `timestamp` (DateTime): When the message was created
- `metadata` (JSON, Optional): Additional information about the message (for future tool usage)

**Relationships**:
- Many-to-one with Conversation entity (many messages belong to one conversation)

## Validation Rules

### Conversation Validation
- `user_id` must reference an existing user in the users table
- `created_at` and `updated_at` are automatically managed by the system
- `title` must be 1-100 characters if provided

### Message Validation
- `conversation_id` must reference an existing conversation
- `user_id` must match the user_id of the associated conversation
- `role` must be either "user" or "assistant"
- `content` must be 1-10000 characters
- `timestamp` is automatically set to current time when created

## State Transitions

### Conversation Lifecycle
1. **Created**: When a user initiates a new conversation
2. **Active**: When messages are being exchanged
3. **Archived**: After a period of inactivity (future feature)

### Message Lifecycle
1. **Created**: When a message is first stored
2. **Processed**: After AI response is generated (future feature)
3. **Delivered**: When response is sent to user (future feature)

## Indexes

### Required Indexes
- Index on `conversations.user_id` for efficient user conversation retrieval
- Index on `messages.conversation_id` for efficient conversation message retrieval
- Composite index on `messages.conversation_id` and `messages.timestamp` for chronological message ordering
- Index on `messages.user_id` for efficient user message queries