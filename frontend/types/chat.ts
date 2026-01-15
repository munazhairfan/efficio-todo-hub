// Types for chat functionality

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  status: 'sent' | 'delivered' | 'error';
  conversationId?: string;
}

export interface ConversationContext {
  id: string;
  userId: string;
  conversationId?: string;
  createdAt: Date;
  lastActive: Date;
  status: 'active' | 'inactive' | 'ended' | 'archived';
}