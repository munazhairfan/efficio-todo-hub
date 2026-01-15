# Data Model: Frontend Chat Integration

## Entities

### ChatMessage
Represents a single message in the conversation, containing content, sender (user/assistant), and timestamp

- **id**: Unique identifier for the message
- **content**: Text content of the message
- **sender**: Type of sender (user or assistant)
- **timestamp**: When the message was sent/received
- **status**: Current status (sent, delivered, error)
- **conversationId**: ID of the conversation this message belongs to

### ConversationContext
Contains the conversation_id and any metadata needed to maintain conversation state

- **id**: Unique identifier for the conversation
- **userId**: ID of the user who owns this conversation
- **conversationId**: Backend-generated conversation identifier
- **createdAt**: When the conversation was initiated
- **lastActive**: When the last message was sent/received
- **status**: Current status of the conversation (active, ended, archived)

## Validation Rules

### ChatMessage Validation
- content must be non-empty string (1-2000 characters)
- sender must be one of 'user' or 'assistant'
- timestamp must be a valid date/time
- status must be one of 'sent', 'delivered', 'error'
- conversationId must be valid and associated with user

### ConversationContext Validation
- userId must be valid and exist in user database
- conversationId must be non-empty string
- createdAt must be in the past
- lastActive must be greater than or equal to createdAt

## State Transitions

### ChatMessage State Transitions
- `CREATED` → `SENDING`: When message is being sent to backend
- `SENDING` → `SENT`: When backend acknowledges receipt
- `SENDING` → `ERROR`: When sending fails
- `SENT` → `DELIVERED`: When confirmed by recipient (if applicable)

### ConversationContext State Transitions
- `INITIALIZED` → `ACTIVE`: When first message is sent/received
- `ACTIVE` → `INACTIVE`: When conversation has been idle for extended period
- `ACTIVE` → `ENDED`: When conversation is explicitly ended by user
- `ENDED` → `ARCHIVED`: When conversation is moved to archive

## API Request/Response Structures

### Chat Message Request
```typescript
interface ChatMessageRequest {
  message: string;
  conversationId?: string;  // Optional for new conversations
  userId: string;
}
```

### Chat Message Response
```typescript
interface ChatMessageResponse {
  conversationId: string;
  response: string;
  timestamp: string;
  error?: string;
}
```

### Frontend Message Object
```typescript
interface FrontendMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  status: 'sent' | 'delivered' | 'error';
}
```