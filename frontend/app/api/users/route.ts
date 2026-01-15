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

    // Get user profile
    const userResult = await pool.query(
      'SELECT id, email, name, created_at, updated_at FROM users WHERE id = $1',
      [user.id]
    );

    if (userResult.rows.length === 0) {
      return Response.json({ error: 'User not found' }, { status: 404 });
    }

    const userData = userResult.rows[0];

    return Response.json({
      user: {
        id: userData.id,
        email: userData.email,
        name: userData.name,
        createdAt: userData.created_at,
        updatedAt: userData.updated_at
      }
    });
  } catch (error) {
    console.error('Get user error:', error);
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

    const currentUser = await verifyToken(token);

    if (!currentUser) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { name, email } = await request.json();

    // Update the user
    const updatedUserResult = await pool.query(
      'UPDATE users SET name = $1, email = $2, updated_at = NOW() WHERE id = $3 RETURNING id, email, name, created_at, updated_at',
      [name, email || currentUser.email, currentUser.id]
    );

    if (updatedUserResult.rows.length === 0) {
      return Response.json({ error: 'User not found' }, { status: 404 });
    }

    const updatedUser = updatedUserResult.rows[0];

    return Response.json({
      user: {
        id: updatedUser.id,
        email: updatedUser.email,
        name: updatedUser.name,
        createdAt: updatedUser.created_at,
        updatedAt: updatedUser.updated_at
      }
    });
  } catch (error) {
    console.error('Update user error:', error);
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

    const currentUser = await verifyToken(token);

    if (!currentUser) {
      return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Delete user and associated todos
    await pool.query('BEGIN'); // Start transaction

    try {
      // Delete user's todos first (due to foreign key constraint)
      await pool.query('DELETE FROM todos WHERE user_id = $1', [currentUser.id]);

      // Delete the user
      const deleteResult = await pool.query(
        'DELETE FROM users WHERE id = $1',
        [currentUser.id]
      );

      if (deleteResult.rowCount === 0) {
        await pool.query('ROLLBACK');
        return Response.json({ error: 'User not found' }, { status: 404 });
      }

      await pool.query('COMMIT');

      // Clear the auth cookie
      cookies().delete('auth-token');

      return Response.json({ success: true });
    } catch (error) {
      await pool.query('ROLLBACK');
      throw error;
    }
  } catch (error) {
    console.error('Delete user error:', error);
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}