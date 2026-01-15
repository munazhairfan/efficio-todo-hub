import { NextRequest } from 'next/server';
import { pool } from '@/lib/db';
import { cookies } from 'next/headers';
import jwt from 'jsonwebtoken';

// Helper function to verify token
async function verifyToken(token: string) {
  try {
    const decoded = jwt.verify(token, process.env.BETTER_AUTH_SECRET || 'fallback-secret') as { id: string; email: string };

    // Verify user exists
    const userResult = await pool.query(
      'SELECT id FROM users WHERE id = $1',
      [decoded.id]
    );

    if (userResult.rows.length === 0) {
      return null;
    }

    return decoded;
  } catch (error) {
    return null;
  }
}

export async function GET(request: NextRequest) {
  try {
    // Get token from cookie
    const token = cookies().get('auth-token')?.value;

    if (!token) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const user = await verifyToken(token);

    if (!user) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get todos for the user
    const todosResult = await pool.query(
      'SELECT id, title, description, completed, created_at, updated_at FROM todos WHERE user_id = $1 ORDER BY created_at DESC',
      [user.id]
    );

    return Response.json({
      todos: todosResult.rows.map((todo: any) => ({
        id: todo.id,
        title: todo.title,
        description: todo.description,
        completed: todo.completed,
        userId: user.id,
        createdAt: todo.created_at,
        updatedAt: todo.updated_at
      }))
    });
  } catch (error) {
    console.error('Get todos error:', error);
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    // Get token from cookie
    const token = cookies().get('auth-token')?.value;

    if (!token) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const user = await verifyToken(token);

    if (!user) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { title, description } = await request.json();

    // Validate input
    if (!title) {
      return Response.json({ error: 'Title is required' }, { status: 400 });
    }

    // Create new todo
    const newTodoResult = await pool.query(
      'INSERT INTO todos (title, description, user_id, completed, created_at, updated_at) VALUES ($1, $2, $3, $4, NOW(), NOW()) RETURNING id, title, description, completed, created_at, updated_at',
      [title, description || '', user.id, false]
    );

    const newTodo = newTodoResult.rows[0];

    return Response.json({
      id: newTodo.id,
      title: newTodo.title,
      description: newTodo.description,
      completed: newTodo.completed,
      userId: user.id,
      createdAt: newTodo.created_at,
      updatedAt: newTodo.updated_at
    });
  } catch (error) {
    console.error('Create todo error:', error);
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function PUT(request: NextRequest) {
  try {
    // Get token from cookie
    const token = cookies().get('auth-token')?.value;

    if (!token) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const user = await verifyToken(token);

    if (!user) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get the ID from either URL search params or request body for flexibility
    const { searchParams } = new URL(request.url);
    const urlTodoId = searchParams.get('id');
    const { id, title, description, completed } = await request.json();

    // Use ID from request body if not in URL params
    const todoId = urlTodoId || id;

    if (!todoId) {
      return Response.json({ error: 'Todo ID is required' }, { status: 400 });
    }

    // Update the todo
    const updatedTodoResult = await pool.query(
      'UPDATE todos SET title = $1, description = $2, completed = $3, updated_at = NOW() WHERE id = $4 AND user_id = $5 RETURNING id, title, description, completed, created_at, updated_at',
      [title, description, completed, todoId, user.id]
    );

    if (updatedTodoResult.rows.length === 0) {
      return Response.json({ error: 'Todo not found' }, { status: 404 });
    }

    const updatedTodo = updatedTodoResult.rows[0];

    return Response.json({
      id: updatedTodo.id,
      title: updatedTodo.title,
      description: updatedTodo.description,
      completed: updatedTodo.completed,
      userId: user.id,
      createdAt: updatedTodo.created_at,
      updatedAt: updatedTodo.updated_at
    });
  } catch (error) {
    console.error('Update todo error:', error);
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest) {
  try {
    // Get token from cookie
    const token = cookies().get('auth-token')?.value;

    if (!token) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const user = await verifyToken(token);

    if (!user) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get the ID from URL search params (primary) or request body (fallback)
    const { searchParams } = new URL(request.url);
    const urlTodoId = searchParams.get('id');

    // For DELETE requests, the body might be empty, so handle it gracefully
    let bodyTodoId = null;
    try {
      const requestBody = await request.json();
      bodyTodoId = requestBody?.id;
    } catch (e) {
      // If JSON parsing fails (empty body), that's fine
      bodyTodoId = null;
    }

    // Use ID from URL params first, then from request body
    const todoId = urlTodoId || bodyTodoId;

    if (!todoId) {
      return Response.json({ error: 'Todo ID is required' }, { status: 400 });
    }

    // Delete the todo
    const deleteResult = await pool.query(
      'DELETE FROM todos WHERE id = $1 AND user_id = $2',
      [todoId, user.id]
    );

    if (deleteResult.rowCount === 0) {
      return Response.json({ error: 'Todo not found' }, { status: 404 });
    }

    return Response.json({ success: true });
  } catch (error) {
    console.error('Delete todo error:', error);
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}