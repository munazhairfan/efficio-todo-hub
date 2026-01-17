# Data Model: Production Database Migrations

## Entities

### Conversation
- **id**: Integer - Primary key with auto-increment
- **user_id**: Integer - Foreign key reference to user, indexed for performance
- **title**: String(100) - Auto-generated or user-provided conversation title
- **created_at**: DateTime - Timestamp when conversation was created
- **updated_at**: DateTime - Timestamp when conversation was last updated

### Message
- **id**: Integer - Primary key with auto-increment
- **conversation_id**: Integer - Foreign key reference to conversation, indexed for performance
- **user_id**: Integer - Foreign key reference to user, indexed for performance
- **role**: String(20) - Message role (either "user" or "assistant")
- **content**: Text - The actual content of the message
- **timestamp**: DateTime - Timestamp when message was created, indexed for performance
- **metadata_json**: String - Additional information about the message (for future tool usage)
- **created_at**: DateTime - Timestamp when message was created
- **updated_at**: DateTime - Timestamp when message was last updated

### Relationship
- **Conversation** has a one-to-many relationship with **Message**
- One conversation can have multiple messages
- Messages are linked to conversations via conversation_id foreign key
- Cascade delete is configured so deleting a conversation removes all associated messages