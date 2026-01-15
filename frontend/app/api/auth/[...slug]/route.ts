import { NextRequest } from 'next/server';
import { pool } from '@/lib/db';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { cookies } from 'next/headers';

export async function POST(request: NextRequest) {
  try {
    const { email, password, name } = await request.json();
    const path = request.nextUrl.pathname;

    if (path.includes('/signup')) {
      // Check if user already exists
      const existingUserResult = await pool.query(
        'SELECT id FROM users WHERE email = $1',
        [email.toLowerCase()]
      );

      if (existingUserResult.rows.length > 0) {
        return Response.json({ error: 'User already exists' }, { status: 400 });
      }

      // Hash the password
      const saltRounds = 10;
      const hashedPassword = await bcrypt.hash(password, saltRounds);

      // Create new user
      const newUserResult = await pool.query(
        'INSERT INTO users (email, password, name, created_at, updated_at) VALUES ($1, $2, $3, NOW(), NOW()) RETURNING id, email, name',
        [email.toLowerCase(), hashedPassword, name]
      );

      const user = newUserResult.rows[0];

      // Generate JWT token
      const token = jwt.sign(
        { id: user.id, email: user.email },
        process.env.BETTER_AUTH_SECRET || 'fallback-secret',
        { expiresIn: '24h' }
      );

      // Set cookie
      cookies().set('auth-token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        maxAge: 60 * 60 * 24, // 24 hours
        path: '/',
      });

      return Response.json({
        token,
        token_type: 'bearer',
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
        }
      });
    } else if (path.includes('/signin')) {
      // Find user by email
      const userResult = await pool.query(
        'SELECT id, email, password, name FROM users WHERE email = $1',
        [email.toLowerCase()]
      );

      if (userResult.rows.length === 0) {
        return Response.json({ error: 'Invalid credentials' }, { status: 401 });
      }

      const user = userResult.rows[0];

      // Verify password
      const isValid = await bcrypt.compare(password, user.password);
      if (!isValid) {
        return Response.json({ error: 'Invalid credentials' }, { status: 401 });
      }

      // Generate JWT token
      const token = jwt.sign(
        { id: user.id, email: user.email },
        process.env.BETTER_AUTH_SECRET || 'fallback-secret',
        { expiresIn: '24h' }
      );

      // Set cookie
      cookies().set('auth-token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        maxAge: 60 * 60 * 24, // 24 hours
        path: '/',
      });

      return Response.json({
        token,
        token_type: 'bearer',
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
        }
      });
    } else if (path.includes('/verify')) {
      // Verify token endpoint
      const { token } = await request.json();

      try {
        const decoded = jwt.verify(token, process.env.BETTER_AUTH_SECRET || 'fallback-secret') as { id: string; email: string };

        // Get user info
        const userResult = await pool.query(
          'SELECT id, email, name FROM users WHERE id = $1',
          [decoded.id]
        );

        if (userResult.rows.length === 0) {
          return Response.json({
            user: {},
            is_valid: false
          });
        }

        const user = userResult.rows[0];

        return Response.json({
          user: {
            id: user.id,
            email: user.email,
            name: user.name,
          },
          is_valid: true
        });
      } catch (error) {
        return Response.json({
          user: {},
          is_valid: false
        });
      }
    }

    return Response.json({ error: 'Invalid endpoint' }, { status: 400 });
  } catch (error) {
    console.error('Auth error:', error);
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}