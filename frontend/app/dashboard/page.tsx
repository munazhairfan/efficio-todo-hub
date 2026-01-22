'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { api, conversationApi, errorApi } from '@/lib/api';
import { Todo } from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Plus, Edit, Trash2, LogOut, MessageSquare, Send } from 'lucide-react';
import ErrorHandler from '@/components/ErrorHandler';
import ConfirmationDialog, { useConfirmationDialog } from '@/components/ConfirmationDialog';
import ChatInterface from '@/components/ChatInterface';

export default function DashboardPage() {
  const { user, loading: authLoading, isAuthenticated, signout } = useAuth();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState(''); // For traditional form
  const [pageLoading, setPageLoading] = useState(true);
  const [error, setError] = useState(''); // General error
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  // Conversation robustness state
  const [sessionId, setSessionId] = useState<string>('');
  const [clarificationQuestions, setClarificationQuestions] = useState<string[]>([]);
  const [showClarificationDialog, setShowClarificationDialog] = useState(false);
  const [currentClarificationContext, setCurrentClarificationContext] = useState<Record<string, any>>({});
  const [isProcessing, setIsProcessing] = useState(false);

  // Error handling state
  const { ConfirmationDialog: ConfirmationDlg, showConfirmation, hideConfirmation, isOpen: isConfirmationOpen } = useConfirmationDialog();

  // Refs for chat functionality
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Check authentication status
    // If auth is still loading, do nothing yet
    // If user is authenticated, load todos
    // If user is not authenticated, redirect to auth
    if (authLoading) {
      // Still loading auth state, do nothing yet
      return;
    }

    if (!isAuthenticated) {
      // User is not authenticated, redirect to auth
      router.push('/auth');
      return;
    }

    // User is authenticated, fetch todos and initialize session
    fetchTodos();
    setSessionId(api.generateSessionId());
  }, [authLoading, isAuthenticated, router]);

  const fetchTodos = async () => {
    try {
      setPageLoading(true);
      const response = await api.getTodos();
      setTodos(response.todos || []);
    } catch (err) {
      setError('Failed to load todos');
      console.error('Error fetching todos:', err);
    } finally {
      setPageLoading(false);
    }
  };

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    // Direct API call to bypass assistant - traditional UI should not go through assistant
    try {
      const response = await api.createTodo({
        title: newTodo,
        description: '',
        completed: false
      });
      setTodos([response, ...todos]);
      setNewTodo('');
    } catch (err) {
      setError('Failed to create todo');
      console.error('Error creating todo:', err);
    }
  };

  const toggleTodo = async (todo: Todo) => {
    // Direct API call to bypass assistant - manual UI actions should not go through assistant
    try {
      const updatedTodo = await api.updateTodo(todo.id, {
        ...todo,
        completed: !todo.completed
      });
      setTodos(todos.map(t => t.id === updatedTodo.id ? updatedTodo : t));
    } catch (err) {
      setError('Failed to update todo');
      console.error('Error updating todo:', err);
    }
  };

  const deleteTodo = async (id: string) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    // Show confirmation dialog before deletion
    showConfirmation({
      title: "Confirm Deletion",
      message: `Are you sure you want to delete the task "${todo.title}"? This action cannot be undone.`,
      variant: 'destructive',
      onConfirm: async () => {
        try {
          await api.deleteTodo(id);
          setTodos(todos.filter(todo => todo.id !== id));
        } catch (err) {
          setError('Failed to delete todo');
          console.error('Error deleting todo:', err);
        }
      }
    });
  };

  const startEditing = (todo: Todo) => {
    setEditingTodo(todo);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
  };

  const handleEditTodo = async () => {
    if (!editingTodo) return;

    try {
      const updatedTodo = await api.updateTodo(editingTodo.id, {
        title: editTitle,
        description: editDescription,
      });
      setTodos(todos.map(t => t.id === updatedTodo.id ? updatedTodo : t));
      setEditingTodo(null);
      setEditTitle('');
      setEditDescription('');
    } catch (err) {
      setError('Failed to update todo');
      console.error('Error updating todo:', err);
    }
  };

  const handleSignOut = () => {
    signout();
    if (typeof window !== 'undefined') {
      window.location.href = '/auth';
    }
  };


  const completedCount = todos.filter(todo => todo.completed).length;
  const totalCount = todos.length;

  return (
    <div className="min-h-screen bg-mint-julep p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center py-6 mb-8">
          <h1 className="text-4xl font-black text-merlot">Efficio Dashboard</h1>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="font-bold text-merlot">Welcome back!</p>
              <p className="text-sm text-mojo">Let's get things done!</p>
            </div>
            <Button
              onClick={handleSignOut}
              variant="outline"
              className="border-2 border-merlot text-merlot hover:bg-merlot hover:text-white"
            >
              <LogOut className="mr-2 h-4 w-4" />
              Sign Out
            </Button>
          </div>
        </header>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-4xl font-black text-merlot">{totalCount}</p>
                <p className="text-lg text-mojo">Total Tasks</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-4xl font-black text-mojo">{completedCount}</p>
                <p className="text-lg text-merlot">Completed</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl">
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-4xl font-black text-confetti">{totalCount - completedCount}</p>
                <p className="text-lg text-merlot">Remaining</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Assistant functionality now available via floating chat button */}
        <div className="mb-8 p-4 text-center bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-yellow-800 font-medium">💬 Need help? Use the floating chat button in the bottom-right corner to talk to your task assistant!</p>
        </div>

        {/* Traditional Add Todo Form */}
        <Card className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl mb-8">
          <CardHeader>
            <CardTitle className="text-2xl font-black text-merlot">Add New Task</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddTodo} className="flex gap-4">
              <Input
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="What needs to be done?"
                className="h-12 border-2 border-merlot text-lg rounded-lg px-4"
              />
              <Button
                type="submit"
                className="h-12 bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl"
              >
                <Plus className="mr-2 h-5 w-5" />
                Add Task
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Todo List */}
        <Card className="border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-xl">
          <CardHeader>
            <CardTitle className="text-2xl font-black text-merlot">Your Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            {pageLoading ? (
              <div className="text-center py-8">
                <p className="text-xl text-merlot">Loading your tasks...</p>
              </div>
            ) : error ? (
              <ErrorHandler
                error={{
                  message: error,
                  type: 'error',
                  suggestions: ['Try refreshing the page', 'Check your internet connection']
                }}
                onDismiss={() => setError('')}
              />
            ) : todos.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-xl text-merlot">No tasks yet! Add your first task above.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {todos.map(todo => (
                  <div
                    key={todo.id}
                    className={`flex items-center justify-between p-4 border-2 rounded-lg ${
                      todo.completed
                        ? 'border-confetti bg-confetti/50'
                        : 'border-merlot bg-white'
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <Checkbox
                        checked={todo.completed}
                        onCheckedChange={() => toggleTodo(todo)}
                        className="h-6 w-6 border-2 border-merlot data-[state=checked]:bg-merlot data-[state=checked]:text-white"
                      />
                      <div>
                        <h3 className={`text-lg font-bold ${todo.completed ? 'line-through text-gray-500' : 'text-merlot'}`}>
                          {todo.title}
                        </h3>
                        {todo.description && (
                          <p className={`text-sm ${todo.completed ? 'line-through text-gray-500' : 'text-mojo'}`}>
                            {todo.description}
                          </p>
                        )}
                        <p className="text-xs text-gray-500">
                          {new Date(todo.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => startEditing(todo)}
                            className="border-2 border-merlot text-merlot hover:bg-merlot hover:text-white"
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                        </DialogTrigger>
                        <DialogContent className="sm:max-w-md bg-mint-julep border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                          <DialogHeader>
                            <DialogTitle className="text-merlot">Edit Task</DialogTitle>
                          </DialogHeader>
                          <div className="space-y-4 py-4">
                            <div className="space-y-2">
                              <Label htmlFor="edit-title" className="text-merlot">Title</Label>
                              <Input
                                id="edit-title"
                                value={editTitle}
                                onChange={(e) => setEditTitle(e.target.value)}
                                className="h-10 border-2 border-merlot text-lg rounded-lg px-4"
                              />
                            </div>
                            <div className="space-y-2">
                              <Label htmlFor="edit-description" className="text-merlot">Description</Label>
                              <Input
                                id="edit-description"
                                value={editDescription}
                                onChange={(e) => setEditDescription(e.target.value)}
                                className="h-10 border-2 border-merlot text-lg rounded-lg px-4"
                              />
                            </div>
                          </div>
                          <Button onClick={handleEditTodo} className="w-full bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl">
                            Update Task
                          </Button>
                        </DialogContent>
                      </Dialog>

                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => deleteTodo(todo.id)}
                        className="border-2 border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>

                      {todo.completed && (
                        <Badge variant="secondary" className="bg-green-100 text-green-800 border-green-200">
                          Completed
                        </Badge>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

      </div>


      {/* Confirmation Dialog */}
      {ConfirmationDlg}
    </div>
  );
}
