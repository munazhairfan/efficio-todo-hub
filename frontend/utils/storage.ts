// Utilities for localStorage management of conversation context

const CONVERSATION_STORAGE_KEY = 'chat_conversation_id';

export const ConversationStorage = {
  // Store conversation ID in localStorage
  setConversationId(conversationId: string): void {
    try {
      localStorage.setItem(CONVERSATION_STORAGE_KEY, conversationId);
    } catch (error) {
      console.error('Failed to save conversation ID to localStorage:', error);
    }
  },

  // Retrieve conversation ID from localStorage
  getConversationId(): string | null {
    try {
      return localStorage.getItem(CONVERSATION_STORAGE_KEY);
    } catch (error) {
      console.error('Failed to retrieve conversation ID from localStorage:', error);
      return null;
    }
  },

  // Clear conversation ID from localStorage
  clearConversationId(): void {
    try {
      localStorage.removeItem(CONVERSATION_STORAGE_KEY);
    } catch (error) {
      console.error('Failed to clear conversation ID from localStorage:', error);
    }
  },

  // Store entire conversation context
  setConversationContext(context: any): void {
    try {
      const contextStr = JSON.stringify(context);
      localStorage.setItem(`${CONVERSATION_STORAGE_KEY}_context`, contextStr);
    } catch (error) {
      console.error('Failed to save conversation context to localStorage:', error);
    }
  },

  // Retrieve conversation context
  getConversationContext(): any {
    try {
      const contextStr = localStorage.getItem(`${CONVERSATION_STORAGE_KEY}_context`);
      return contextStr ? JSON.parse(contextStr) : null;
    } catch (error) {
      console.error('Failed to retrieve conversation context from localStorage:', error);
      return null;
    }
  }
};