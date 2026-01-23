'use client';

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, MessageCircle } from 'lucide-react';
import { useAuth } from '@/components/auth/AuthProvider';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
}

export default function SimpleChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, type: 'assistant', content: 'Hello! I\'m your task management assistant. How can I help you today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Load any existing conversation from localStorage
  useEffect(() => {
    if (!user?.id) return;

    try {
      const savedConversations = localStorage.getItem(`chat_conversation_${user.id}`);
      if (savedConversations) {
        const parsed = JSON.parse(savedConversations);
        setMessages(parsed.messages || [
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
  }, [user?.id]);

  // Save conversation to localStorage whenever messages change
  useEffect(() => {
    if (!user?.id || messages.length === 0) return;

    try {
      const conversationData = {
        messages,
        timestamp: Date.now()
      };
      localStorage.setItem(`chat_conversation_${user.id}`, JSON.stringify(conversationData));
    } catch (error) {
      console.error('Failed to save conversation:', error);
    }
  }, [messages, user?.id]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use the proper authentication state from the AuthProvider
      // Check if authentication is still loading
      if (authLoading) {
        const assistantMessage: Message = {
          id: Date.now() + 1,
          type: 'assistant',
          content: 'Loading authentication status...'
        };
        setMessages(prev => [...prev, assistantMessage]);
        setIsLoading(false);
        return;
      }

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
        const assistantMessage: Message = {
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
          'what is this', 'how to', 'can you help', 'what can i do', 'what is',
          'how does', 'tell me about', 'what do', 'what does', 'describe', 'what is adding'
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
          } else if (inputValue.toLowerCase().includes('what is adding')) {
            infoResponse = `Adding a task means creating a new item in your to-do list. For example, you can say "Add a task to buy groceries" or "Create a task to call John". When you're logged in, I can add these tasks to your personal list. Until you log in, I can answer questions about how the app works!`;
          } else {
            infoResponse = `Welcome! Our app helps you manage your tasks and stay organized. You can interact with me to manage your personal task list. To access your tasks, please sign in to your account. In the meantime, I'm happy to answer any questions you have about how the app works!`;
          }

          const assistantMessage: Message = {
            id: Date.now() + 1,
            type: 'assistant',
            content: infoResponse
          };

          setMessages(prev => [...prev, assistantMessage]);
          setIsLoading(false);
          return;
        } else {
          // For non-general questions when not authenticated, suggest logging in but still try to help
          const assistantMessage: Message = {
            id: Date.now() + 1,
            type: 'assistant',
            content: `I'd be happy to help! For general questions about the app, I can assist even without logging in. For task management (adding, completing, deleting tasks), please sign in to your account. In the meantime, I'll do my best to answer your question.`
          };

          setMessages(prev => [...prev, assistantMessage]);
        }
      }

      // Make the API call to get a response (either authenticated or unauthenticated)
      const apiCallHeaders: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Only add authorization header if authenticated
      if (isAuthenticated) {
        const token = localStorage.getItem('authToken');
        if (token) {
          apiCallHeaders['Authorization'] = `Bearer ${token}`;
        }
      }

      const response = await fetch('/api/conversation/clarify', {
        method: 'POST',
        headers: apiCallHeaders,
        body: JSON.stringify({
          input: inputValue.trim(),
          context: {
            user_id: user?.id || (isAuthenticated ? 'temp_user' : 'guest_user')
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({})); // Catch potential JSON parsing errors
        throw new Error(errorData.detail || `API error: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant response
      const assistantMessage: Message = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.message || data.response || 'I received your message.'
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      // Add error message to chat
      const errorMessage: Message = {
        id: Date.now() + 1,
        type: 'assistant',
        content: `Sorry, I encountered an error: ${(error as Error).message || 'Unable to process your request'}. Please try again.`
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl bg-white p-4">
      <div className="flex items-center gap-2 mb-4">
        <MessageCircle className="h-5 w-5 text-merlot" />
        <h3 className="text-lg font-black text-merlot">Task Assistant</h3>
      </div>

      <ScrollArea className="h-64 mb-4 p-2 border rounded-lg bg-gray-50">
        <div className="space-y-3" ref={scrollAreaRef}>
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

      <div className="flex gap-2">
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask me anything - add tasks, update, delete, list, or just chat..."
          className="h-12 border-2 border-merlot text-lg rounded-lg px-4 flex-1"
          disabled={isLoading}
        />
        <Button
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isLoading}
          className="h-12 bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl"
        >
          <Send className="h-4 w-4 mr-2" />
          Send
        </Button>
      </div>

      <p className="text-xs text-gray-600 mt-2 text-center">
        Examples: "Add a task to buy groceries", "Show my tasks", "Mark task #1 as complete"
      </p>
    </div>
  );
}