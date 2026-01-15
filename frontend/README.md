# Efficio Todo App - Frontend

## Overview
This is the frontend implementation of the Efficio Todo application, built with Next.js 14, TypeScript, and Tailwind CSS. The UI visually matches the reference design while connecting to an existing backend API.

## Features
- User authentication (sign up, sign in, sign out)
- Todo management (create, read, update, delete)
- Responsive design with visually appealing UI
- JWT-based authentication with token management
- User profile management

## Tech Stack
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Server Components
- Shadcn/ui components

## Project Structure
```
frontend/
├── app/                 # Next.js App Router pages
│   ├── (auth)/          # Authentication pages (sign up, sign in)
│   ├── dashboard/       # Main dashboard with todos
│   ├── profile/         # User profile page
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Landing page
│   └── not-found.tsx    # 404 error page
├── components/          # Reusable UI components
│   ├── ui/              # Base UI components (buttons, inputs, etc.)
│   ├── auth/            # Authentication components
│   ├── todo/            # Todo-specific components
│   └── navigation/      # Navigation components
├── lib/                 # Utility functions and API client
│   ├── api.ts           # API client for backend communication
│   └── auth.ts          # Authentication utilities
├── styles/              # Global styles and Tailwind config
│   └── globals.css      # Global CSS and Tailwind imports
├── types/               # TypeScript type definitions
│   └── index.ts         # Shared type definitions
└── public/              # Static assets
```

## API Integration
The frontend connects to Vercel API routes directly. All backend functionality (authentication, user management, todo operations) is handled by serverless functions deployed on Vercel.

## Environment Variables
Create a `.env.local` file in the frontend directory:
```
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=your_jwt_secret_key
```

**Note**: Make sure your Neon PostgreSQL database has the required tables created. Run the schema.sql file to initialize the database:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Todos table
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for efficient querying by user_id
CREATE INDEX IF NOT EXISTS idx_todos_user_id ON todos(user_id);
```

## Getting Started
1. Install dependencies: `npm install` or `yarn install`
2. Set up environment variables
3. Run the development server: `npm run dev` or `yarn dev`
4. Visit `http://localhost:3000`

## Authentication Flow
1. Users can sign up or sign in via the `/auth` page
2. JWT tokens are stored in HTTP-only cookies for security
3. Tokens are automatically managed by the browser for API requests
4. Protected routes (`/dashboard`, `/profile`) require authentication

## Todo Management
- Users can create, read, update, and delete todos
- Todos are isolated by user (each user sees only their todos)
- Todos have title, description, and completion status
- Loading states and error handling are implemented

## Styling
The application uses Tailwind CSS with custom styling that matches the reference UI design. Color palette, typography, and spacing follow the design specification.

## Error Handling
- Network errors are caught and displayed to users
- Form validation prevents invalid submissions
- Authentication errors redirect to sign-in page
- Loading states provide feedback during API calls