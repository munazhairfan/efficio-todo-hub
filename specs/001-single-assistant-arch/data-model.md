# Data Model: Single Assistant Architecture

## Core Entities

### Assistant
- **Name**: Single unified AI assistant
- **Responsibilities**:
  - Process all user messages (chat and task-related)
  - Recognize intent from natural language
  - Invoke MCP tools when required
  - Return natural language responses
- **Attributes**: None (behavioral entity, not persisted)

### MCP Tools (Unchanged)
- **Purpose**: Simple executable functions for task operations
- **Types**:
  - `add_task`: Create new task
  - `list_tasks`: Retrieve user's tasks
  - `complete_task`: Mark task as completed
  - `delete_task`: Remove task
  - `update_task`: Modify task details
- **Attributes**: Functions with defined parameters (no persistence)

### User Session
- **Purpose**: Maintains conversation context within the single assistant
- **Relationships**: Links to user and conversation history
- **Attributes**:
  - `user_id`: Identifier for the user
  - `session_id`: Unique session identifier
  - `conversation_context`: Current state of conversation (temporary)

### Messages (Unchanged)
- **Purpose**: Store chat history for context
- **Attributes**:
  - `id`: Unique identifier
  - `conversation_id`: Link to conversation
  - `user_id`: Creator of message
  - `role`: 'user' or 'assistant'
  - `content`: Message text
  - `timestamp`: Creation time

### Conversations (Unchanged)
- **Purpose**: Group related messages
- **Attributes**:
  - `id`: Unique identifier
  - `user_id`: Owner of conversation
  - `title`: Conversation topic
  - `created_at`: Creation timestamp
  - `updated_at`: Last activity timestamp

## State Transitions

### Message Processing Flow
1. **Input Received** → User message enters system
2. **Intent Recognition** → Assistant analyzes message intent
3. **Tool Decision** → Determine if MCP tool is needed
4. **Tool Execution** → Execute appropriate MCP tool (if needed)
5. **Response Generation** → Generate natural language response
6. **Response Sent** → Return response to user

## Validation Rules

### Assistant Processing
- All messages must flow through single assistant instance
- Intent recognition must precede tool invocation
- Response must always originate from assistant

### MCP Tool Invocation
- Tools must be called only by assistant
- Tools must return structured data to assistant
- Tools must not contain conversational logic

### Session Management
- Conversation context must be preserved within session
- User isolation must be maintained
- Session state must be consistent