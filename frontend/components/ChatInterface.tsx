'use client';

import { useState, useRef, useEffect } from 'react';
import { chatService } from '@/services/chatService';
import { ChatMessage } from '@/types/chat';
import { ConversationStorage } from '@/utils/storage';
import MessageBubble from './MessageBubble';

interface ChatProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [visibleMessageCount, setVisibleMessageCount] = useState(50); // Show last 50 messages initially
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const MAX_MESSAGE_LENGTH = 2000; // Define max message length constant
  const MESSAGES_PER_LOAD = 50; // Number of messages to load at a time

  // Add animation styles for message bubbles
  useEffect(() => {
    const styleId = 'chat-animation-styles';
    if (!document.querySelector(`#${styleId}`)) {
      const style = document.createElement('style');
      style.id = styleId;
      style.textContent = `
        @keyframes fadeInSlideUp {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeInSlideUp {
          animation: fadeInSlideUp 0.3s ease-out forwards;
        }
      `;
      document.head.appendChild(style);
    }
  }, []);

  // Load any existing conversation from localStorage
  useEffect(() => {
    const existingConversationId = ConversationStorage.getConversationId();
    if (existingConversationId) {
      // We could load previous messages here if needed
      console.log('Restoring conversation:', existingConversationId);
    }
  }, []);

  // Function to load more messages
  const loadMoreMessages = () => {
    setVisibleMessageCount(prev => prev + MESSAGES_PER_LOAD);
  };

  // Get visible messages (most recent ones)
  const getVisibleMessages = () => {
    if (messages.length <= visibleMessageCount) {
      return messages;
    }
    // Return the most recent messages
    return messages.slice(-visibleMessageCount);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Validate message
    const validation = chatService.validateMessage(inputValue);
    if (!validation.isValid) {
      setError(validation.error || null);
      return;
    }

    // Clear any previous errors
    setError(null);

    // Get current conversation ID
    const conversationId = chatService.getCurrentConversationId();

    // Create and add user message immediately
    const userMessage = chatService.createUserMessage(inputValue, conversationId);
    setMessages(prev => [...prev, userMessage]);

    // Clear input
    setInputValue('');

    // Set loading state
    setIsLoading(true);

    try {
      // Send message via service
      const response = await chatService.sendMessage({
        userId,
        message: inputValue,
        conversationId
      });

      // Create and add assistant message
      const assistantMessage = chatService.createAssistantMessage(
        response.response,
        response.conversation_id
      );

      setMessages(prev => [...prev, assistantMessage]);

      // Update conversation ID if new one was returned
      if (response.conversation_id && !conversationId) {
        chatService.setCurrentConversationId(response.conversation_id);
      }
    } catch (err) {
      console.error('Failed to send message:', err);
      const errorMessage = chatService.createErrorMessage(
        'Sorry, there was an error processing your message. Please try again.',
        conversationId
      );
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      handleSendMessage();
    } else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      // Allow Ctrl+Enter or Cmd+Enter to create a new line
      // This is handled automatically by the textarea
    } else if (e.key === 'Escape') {
      // Clear input with Escape key
      setInputValue('');
    }
  };

  // Calculate character count for the input field
  const charCount = inputValue.length;
  const isOverLimit = charCount > MAX_MESSAGE_LENGTH;

  return (
    <div
      className="flex flex-col h-full bg-white rounded-lg shadow-md"
      role="main"
      aria-label="Chat interface"
    >
      {/* Chat header */}
      <div className="p-4 border-b bg-gray-50 rounded-t-lg">
        <h2 className="text-lg font-semibold" id="chat-header">Chat with Assistant</h2>
      </div>

      {/* Messages container */}
      <div
        className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 flex flex-col"
        aria-live="polite"
        aria-labelledby="chat-header"
        role="log"
      >
        {messages.length === 0 ? (
          <div
            className="flex items-center justify-center h-full text-gray-500"
            aria-label="No messages in conversation"
          >
            <p>Start a conversation by sending a message...</p>
          </div>
        ) : (
          <>
            {/* Load More Button - shown when there are more messages than currently displayed */}
            {messages.length > visibleMessageCount && (
              <div className="flex justify-center mb-4">
                <button
                  onClick={loadMoreMessages}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg text-sm"
                  aria-label="Load more messages"
                >
                  Load More Messages
                </button>
              </div>
            )}

            {/* Render visible messages */}
            {getVisibleMessages().map((message) => (
              <MessageBubble
                key={message.id}
                message={message}
                isOwnMessage={message.sender === 'user'}
              />
            ))}
          </>
        )}

        {isLoading && (
          <div
            className="flex justify-start mb-4"
            aria-label="Assistant is typing"
          >
            <div
              className="mr-auto bg-gray-200 text-gray-800 px-4 py-2 rounded-lg max-w-xs md:max-w-md"
              role="status"
            >
              <div className="flex items-center">
                <div className="animate-pulse mr-2" aria-hidden="true">●</div>
                <span>Assistant is typing...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} aria-live="polite" />
      </div>

      {/* Error message display */}
      {error && (
        <div
          className="p-3 bg-red-100 text-red-700 text-sm border-t"
          role="alert"
          aria-live="assertive"
        >
          {error}
          <button
            onClick={() => setError(null)}
            className="float-right text-red-900 hover:text-red-700"
            aria-label="Close error message"
          >
            ×
          </button>
        </div>
      )}

      {/* Input area */}
      <div className="p-4 border-t bg-white">
        <div className="flex space-x-2">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            className={`flex-1 border rounded-lg p-2 resize-none min-h-[40px] max-h-32 ${isOverLimit ? 'border-red-500' : ''}`}
            rows={1}
            disabled={isLoading}
            aria-label="Type your message"
            aria-describedby="send-instructions"
            maxLength={MAX_MESSAGE_LENGTH}
            autoFocus
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim() || isOverLimit}
            className={`px-4 py-2 rounded-lg disabled:opacity-50 transition-colors ${
              isOverLimit
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
            aria-label="Send message"
          >
            Send
          </button>
        </div>
        <div className="flex justify-between items-center mt-2">
          <div
            id="send-instructions"
            className="text-xs text-gray-500 sr-only"
          >
            Press Enter to send, Ctrl/Cmd+Enter for new line, Esc to clear
          </div>
          <div className={`text-xs ${isOverLimit ? 'text-red-500' : 'text-gray-500'}`}>
            {charCount}/{MAX_MESSAGE_LENGTH}
          </div>
        </div>
      </div>
    </div>
  );
}