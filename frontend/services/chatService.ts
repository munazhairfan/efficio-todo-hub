// Service for handling chat message operations

import { api } from '@/lib/api';
import { ChatMessage, ConversationContext } from '@/types/chat';
import { ConversationStorage } from '@/utils/storage';

export interface SendMessageRequest {
  userId: string;
  message: string;
  conversationId?: string;
}

export interface SendMessageResponse {
  conversation_id: string;
  response: string;
  timestamp: string;
  status?: string;
  error?: string;
}

export interface ChatHistory {
  messages: ChatMessage[];
  conversationId?: string;
}

class ChatService {
  // Send a message to the chat endpoint with retry functionality
  async sendMessage(request: SendMessageRequest): Promise<SendMessageResponse> {
    const maxRetries = 3;
    let lastError;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        // Use the conversation ID from the request or from storage
        const conversationId = request.conversationId || ConversationStorage.getConversationId() || undefined;

        const response = await api.sendMessage(
          request.userId,
          request.message,
          conversationId
        );

        // If a new conversation ID was returned, store it
        if (response.conversation_id && !request.conversationId) {
          ConversationStorage.setConversationId(response.conversation_id);
        }

        return response;
      } catch (error) {
        lastError = error;

        // Check if it's a rate limiting error (HTTP 429)
        if (this.isRateLimitError(error)) {
          throw new Error('Rate limit exceeded. Please slow down your requests.');
        }

        console.error(`Attempt ${attempt} failed to send message:`, error);

        // If this was the last attempt, throw the error
        if (attempt === maxRetries) {
          break;
        }

        // Wait before retrying (exponential backoff)
        await this.delay(1000 * attempt); // 1s, 2s, 3s
      }
    }

    // If all retries failed, throw the last error
    console.error('Failed to send message after all retries:', lastError);
    throw lastError;
  }

  // Check if the error is a rate limit error
  private isRateLimitError(error: any): boolean {
    // Check if error contains status code 429 (rate limit)
    if (error?.status === 429 || error?.response?.status === 429) {
      return true;
    }

    // Check if error message contains rate limit indicators
    const errorMessage = error?.message?.toLowerCase() || '';
    return errorMessage.includes('rate') && errorMessage.includes('limit');
  }

  // Helper method for delay
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Create a user message object
  createUserMessage(content: string, conversationId?: string): ChatMessage {
    return {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent',
      conversationId
    };
  }

  // Create an assistant message object
  createAssistantMessage(content: string, conversationId?: string): ChatMessage {
    return {
      id: `assistant-${Date.now()}`,
      content,
      sender: 'assistant',
      timestamp: new Date(),
      status: 'delivered',
      conversationId
    };
  }

  // Create an error message object
  createErrorMessage(content: string, conversationId?: string): ChatMessage {
    return {
      id: `error-${Date.now()}`,
      content,
      sender: 'assistant',
      timestamp: new Date(),
      status: 'error',
      conversationId
    };
  }

  // Get current conversation ID
  getCurrentConversationId(): string | undefined {
    return ConversationStorage.getConversationId() || undefined;
  }

  // Set conversation ID
  setCurrentConversationId(conversationId: string): void {
    ConversationStorage.setConversationId(conversationId);
  }

  // Clear current conversation
  clearCurrentConversation(): void {
    ConversationStorage.clearConversationId();
  }

  // Initialize a new conversation context
  initializeNewConversation(): void {
    // Clear any existing conversation ID to start fresh
    ConversationStorage.clearConversationId();
  }

  // Validate message before sending
  validateMessage(message: string): { isValid: boolean; error?: string } {
    if (!message || message.trim().length === 0) {
      return {
        isValid: false,
        error: 'Message cannot be empty'
      };
    }

    if (message.length > 2000) {
      return {
        isValid: false,
        error: 'Message is too long (max 2000 characters)'
      };
    }

    return {
      isValid: true
    };
  }
}

export const chatService = new ChatService();