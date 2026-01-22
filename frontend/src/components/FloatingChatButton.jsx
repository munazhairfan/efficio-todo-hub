'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, MessageCircle, X } from 'lucide-react';
import { useAuth } from '@/components/auth/AuthProvider';

export default function FloatingChatButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();
  const [conversationId, setConversationId] = useState(null);

  // Load conversation from localStorage when component mounts
  useEffect(() => {
    const loadConversation = () => {
      if (!user?.id) return;

      try {
        const savedConversations = localStorage.getItem(`chat_conversation_${user.id}`);
        if (savedConversations) {
          const parsed = JSON.parse(savedConversations);
          setMessages(parsed.messages || []);
          setConversationId(parsed.conversationId || null);
        } else {
          // Initialize with welcome message if no saved conversation
          setMessages([
            { id: 1, type: 'assistant', content: 'Hello! I\'m your task management assistant. How can I help you today?' }
          ]);
        }
      } catch (error) {
        console.error('Failed to load conversation:', error);
        // Initialize with welcome message on error
        setMessages([
          { id: 1, type: 'assistant', content: 'Hello! I\'m your task management assistant. How can I help you today?' }
        ]);
      }
    };

    loadConversation();
  }, [user?.id]);

  // Save conversation to localStorage whenever messages change
  useEffect(() => {
    if (!user?.id || messages.length === 0) return;

    try {
      const conversationData = {
        messages,
        conversationId,
        timestamp: Date.now()
      };
      localStorage.setItem(`chat_conversation_${user.id}`, JSON.stringify(conversationData));
    } catch (error) {
      console.error('Failed to save conversation:', error);
    }
  }, [messages, user?.id, conversationId]);

  // Toggle chat window
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Close chat window
  const closeChat = () => {
    setIsOpen(false);
  };

  // Clear conversation history
  const clearConversation = () => {
    if (user?.id) {
      try {
        localStorage.removeItem(`chat_conversation_${user.id}`);
        setMessages([
          { id: 1, type: 'assistant', content: 'Hello! I\'m your task management assistant. How can I help you today?' }
        ]);
        setConversationId(null);
      } catch (error) {
        console.error('Failed to clear conversation:', error);
      }
    }
  };

  // Handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Check if user is authenticated
      const token = localStorage.getItem('authToken');
      const isAuthenticated = token && user?.id;

      // Check if this is a task-related request that requires authentication
      const taskRelatedKeywords = [
        'add task', 'create task', 'new task', 'complete task', 'finish task',
        'delete task', 'remove task', 'update task', 'edit task', 'list task',
        'my tasks', 'show tasks', 'task list', 'todo', 'to-do', 'todos'
      ];

      const isTaskRelated = taskRelatedKeywords.some(keyword =>
        inputValue.toLowerCase().includes(keyword.toLowerCase())
      );

      if (isTaskRelated && !isAuthenticated) {
        // For task-related requests without authentication, provide helpful response
        const assistantMessage = {
          id: Date.now() + 1,
          type: 'assistant',
          content: `I'd be happy to help you manage your tasks! However, you'll need to sign in first to access your personal task list. Please log in to your account, and then I can help you add, complete, delete, or manage your tasks. In the meantime, I can answer questions about how the app works!`
        };

        setMessages(prev => [...prev, assistantMessage]);
        setIsLoading(false);
        return;
      }

      // For non-task related questions, allow unauthenticated users to ask general questions
      if (!isAuthenticated) {
        // Check if it's a general question about the app
        const generalInfoKeywords = [
          'how does this work', 'how to use', 'what can you do', 'features',
          'help', 'instructions', 'guide', 'tutorial', 'explain', 'about',
          'what is this', 'how to', 'can you help', 'what can i do'
        ];

        const isGeneralInfoQuery = generalInfoKeywords.some(keyword =>
          inputValue.toLowerCase().includes(keyword.toLowerCase())
        );

        if (isGeneralInfoQuery) {
          // Provide helpful information about the app for guests
          let infoResponse = '';

          if (inputValue.toLowerCase().includes('work') || inputValue.toLowerCase().includes('use') || inputValue.toLowerCase().includes('how')) {
            infoResponse = `Our todo app helps you manage your tasks efficiently! You can add, complete, update, and delete tasks. I can assist you with managing your personal task list through our chat interface. To get started with task management, simply sign up or log in to your account. Until then, I can answer general questions about the app's features.`;
          } else if (inputValue.toLowerCase().includes('features') || inputValue.toLowerCase().includes('what can you')) {
            infoResponse = `I can help you manage your tasks in several ways:\n• Add new tasks to your list\n• List your current tasks\n• Mark tasks as completed\n• Update or edit existing tasks\n• Delete tasks you no longer need\n\nTo use these features, please sign in to your account. For general questions, I'm happy to help even without logging in!`;
          } else {
            infoResponse = `Welcome! Our app helps you manage your tasks and stay organized. You can interact with me to manage your personal task list. To access your tasks, please sign in to your account. In the meantime, I'm happy to answer any questions you have about how the app works!`;
          }

          const assistantMessage = {
            id: Date.now() + 1,
            type: 'assistant',
            content: infoResponse
          };

          setMessages(prev => [...prev, assistantMessage]);
          setIsLoading(false);
          return;
        }
      }

      // If user is authenticated, proceed with the API call
      if (!token || !user?.id) {
        throw new Error('You must be logged in to use the chatbot for task management');
      }

      // Call the backend API
      const response = await fetch('/api/conversation/clarify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          input: inputValue.trim(),
          context: {
            user_id: user?.id || localStorage.getItem('user_id') || localStorage.getItem('userId') || 'temp_user',
            conversation_id: conversationId || undefined
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `API error: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if provided in response
      if (data.conversationId || data.conversation_id) {
        setConversationId(data.conversationId || data.conversation_id);
      }

      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.message || data.response || 'I received your message.'
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error.message || 'Unable to process your request'}. Please try again.`
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <Button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 z-50 rounded-full w-16 h-16 shadow-lg bg-blue-600 hover:bg-blue-700 flex items-center justify-center"
          aria-label="Open chat"
        >
          <MessageCircle className="h-6 w-6 text-white" />
        </Button>
      )}

      {/* Chat Window - Only show when open */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-96 h-96 flex flex-col border rounded-lg shadow-xl bg-white">
          <Card className="flex-1 flex flex-col h-full border-0 rounded-none">
            <CardHeader className="p-3 pb-2 flex-row items-center justify-between border-b">
              <CardTitle className="text-sm font-medium">Task Assistant</CardTitle>
              <div className="flex space-x-1">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearConversation}
                  className="h-8 w-8 p-0"
                  aria-label="Clear chat history"
                  title="Clear chat history"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                  </svg>
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={closeChat}
                  className="h-8 w-8 p-0"
                  aria-label="Close chat"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>

            <CardContent className="flex-1 p-0 flex flex-col h-[calc(100%-130px)]">
              {/* Messages Area */}
              <ScrollArea className="flex-1 p-4 h-full">
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.type === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                          message.type === 'user'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {message.content}
                      </div>
                    </div>
                  ))}

                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="max-w-xs px-3 py-2 rounded-lg text-sm bg-gray-100 text-gray-800">
                        Thinking...
                      </div>
                    </div>
                  )}
                </div>
              </ScrollArea>

              {/* Input Area */}
              <div className="p-4 border-t">
                <div className="flex space-x-2">
                  <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Type your message..."
                    className="flex-1 text-sm"
                    disabled={isLoading}
                  />
                  <Button
                    onClick={handleSendMessage}
                    disabled={!inputValue.trim() || isLoading}
                    size="sm"
                    className="h-9"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </>
  );
}