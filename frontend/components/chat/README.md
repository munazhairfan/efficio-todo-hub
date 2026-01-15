# Chat Components Documentation

This directory contains the chat interface components for the Efficio Todo Hub application.

## Components

### ChatInterface
The main chat interface component that provides a complete chat experience with:
- Message input field with send button
- Real-time message display
- Loading states and typing indicators
- Error handling and display
- Conversation context management
- Accessibility features
- Character counting and input validation
- Keyboard shortcuts

#### Props
- `userId`: The ID of the current user (required)

#### Features
- Auto-scroll to bottom when new messages arrive
- Conversation persistence across page refreshes
- Rate limiting error handling
- Network error retry functionality
- Responsive design
- Smooth animations for message transitions

### MessageBubble
Displays individual chat messages with:
- Different styling for user vs assistant messages
- Timestamp display
- Message status indicators (sent, delivered, error)
- Smooth entry animations

#### Props
- `message`: The ChatMessage object to display (required)
- `isOwnMessage`: Boolean indicating if the message is from the current user (optional, default: false)

## Services

### chatService
Provides business logic for chat operations:
- Message sending with retry functionality
- Conversation context management
- Message validation
- Error handling

## Types

### ChatMessage Interface
```typescript
interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  status: 'sent' | 'delivered' | 'error';
  conversationId?: string;
}
```

### ConversationContext Interface
```typescript
interface ConversationContext {
  id: string;
  userId: string;
  conversationId?: string;
  createdAt: Date;
  lastActive: Date;
  status: 'active' | 'inactive' | 'ended' | 'archived';
}
```

## Storage Utilities

### ConversationStorage
Manages conversation context in localStorage:
- Set/get/clear conversation ID
- Store/retrieve conversation context

## Integration

The ChatInterface is integrated into the dashboard page (`/frontend/app/dashboard/page.tsx`) and can be used in other parts of the application by importing and passing the user ID.

## Error Handling

The chat system includes comprehensive error handling:
- Network error retry with exponential backoff
- Rate limiting detection and user feedback
- Message validation to prevent empty or oversized submissions
- Clear error messages with dismiss functionality

## Accessibility

The chat interface includes:
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Focus management