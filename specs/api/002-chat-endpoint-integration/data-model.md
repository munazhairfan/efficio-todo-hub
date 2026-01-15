# Data Model: Chat Endpoint Integration

## Conversation Entity

**Name**: Conversation
**Fields**:
- id: Integer (primary key, auto-increment)
- user_id: String (foreign key reference to user)
- created_at: DateTime (timestamp when conversation was created)
- updated_at: DateTime (timestamp when conversation was last updated)

**Relationships**:
- One Conversation to Many Messages (conversation.messages)

**Validation**:
- user_id must exist and be valid
- created_at and updated_at are automatically managed

## Message Entity

**Name**: Message
**Fields**:
- id: Integer (primary key, auto-increment)
- conversation_id: Integer (foreign key reference to conversation)
- user_id: String (reference to user who sent the message)
- role: String (either "user" or "assistant")
- content: Text (the actual message content)
- created_at: DateTime (timestamp when message was created)

**Relationships**:
- Many Messages to One Conversation (message.conversation)

**Validation**:
- conversation_id must reference an existing conversation
- role must be either "user" or "assistant"
- content must not be empty

## State Transitions

**Conversation**:
- Created when first message is sent by user
- Updated when new messages are added
- Remains active (no explicit end state)

**Message**:
- Created when user sends message or AI generates response
- Immutable after creation (no updates/deletion through this feature)