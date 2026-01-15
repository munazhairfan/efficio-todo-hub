# Quickstart: Frontend Chat Integration

## Overview
This guide explains how to implement the frontend chat integration feature that connects the chat UI to the backend chat endpoint.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL database (Neon recommended)
- Basic understanding of Next.js and FastAPI
- Existing authentication system in place

## Backend Setup

### 1. Add Chat Endpoint
Create a new chat endpoint in the backend:

```python
# backend/api/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])

@router.post("/chat")
async def chat_endpoint(
    user_id: str,
    message: str,
    conversation_id: Optional[str] = None
):
    """
    Handle chat messages from frontend
    """
    # Validate inputs
    if not message or len(message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Generate new conversation ID if not provided
    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    # Process the message (implement chatbot logic here)
    response_text = f"Echo: {message}"  # Replace with actual chatbot logic

    return {
        "conversation_id": conversation_id,
        "response": response_text,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "success"
    }
```

### 2. Register Chat Route
Add the chat route to your main application:

```python
# backend/main.py
from backend.api.routes.chat import router as chat_router

app.include_router(chat_router)
```

## Frontend Setup

### 1. Update API Client
Add chat functionality to the API client:

```typescript
// frontend/lib/api.ts
class ApiClient {
  // ... existing methods ...

  async sendMessage(userId: string, message: string, conversationId?: string) {
    const response = await fetch(`/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth-token')}`
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      })
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    return response.json();
  }
}
```

### 2. Create Chat Interface Component
Create a chat interface component:

```tsx
// frontend/components/ChatInterface.tsx
'use client';

import { useState, useRef, useEffect } from 'react';
import { api } from '@/lib/api';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  status: 'sent' | 'delivered' | 'error';
}

interface ChatProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await api.sendMessage(userId, inputValue, conversationId);

      // Update conversation ID if new conversation started
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
        // Store in localStorage for persistence
        localStorage.setItem('chat_conversation_id', response.conversation_id);
      }

      // Add assistant response
      const assistantMessage: Message = {
        id: `resp_${Date.now()}`,
        content: response.response,
        sender: 'assistant',
        timestamp: new Date(response.timestamp),
        status: 'delivered'
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      // Add error message
      const errorMessage: Message = {
        id: `error_${Date.now()}`,
        content: 'Sorry, there was an error processing your message.',
        sender: 'assistant',
        timestamp: new Date(),
        status: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg">
              Assistant is typing...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            className="flex-1 border rounded-lg p-2 resize-none"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
```

## Implementation Details

### 1. Conversation Management
- The frontend stores the conversation_id in localStorage
- Conversation ID is included in subsequent requests to maintain context
- New conversations are started when no conversation_id exists

### 2. Error Handling
- Network errors are caught and displayed to the user
- Empty messages are prevented from being sent
- Loading states provide feedback during API calls

### 3. Message Display
- User messages appear on the right with blue styling
- Assistant messages appear on the left with gray styling
- Auto-scrolling to the latest message
- Loading indicators when waiting for responses

## Testing
Run the following commands to test the chat integration:

```bash
# Backend tests
cd backend
pytest tests/test_chat.py

# Frontend tests
cd frontend
npm run test
```

## Deployment
1. Ensure the backend chat endpoint is registered
2. Update frontend API client with the correct endpoint
3. Test the chat interface with various message types
4. Verify conversation context is maintained across sessions