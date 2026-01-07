# Todo App - Full Stack Application with Authentication

A full-stack todo application with authentication, featuring a Next.js frontend and FastAPI backend. This application provides all basic CRUD operations for managing tasks with secure authentication and authorization.

## Features

- **Authentication System**: Secure user signup, signin, and profile management
- **Task Management**: Create, read, update, and delete tasks
- **Protected Routes**: Authentication required for task operations
- **Responsive UI**: Modern interface built with Next.js and Tailwind CSS
- **Secure API**: FastAPI backend with JWT authentication
- **Database Integration**: PostgreSQL database with SQLModel ORM

## Requirements

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL database
- Vercel account (for frontend deployment)

## Frontend Setup

1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Create `.env.local` file with:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Run development server: `npm run dev`

## Backend Setup

1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
   FRONTEND_URL=http://localhost:3000
   ```
4. Run the server: `uvicorn main:app --reload`

## Production Deployment

### Frontend Deployment to Vercel

1. Connect your Vercel account to your GitHub repository
2. Set environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your production backend URL
3. Vercel will automatically detect the Next.js configuration and deploy

### Backend Deployment

The backend can be deployed to various platforms:

#### Option 1: Deploy to Railway/Render/Hetzner
1. Set environment variables:
   - `SECRET_KEY`: Your JWT secret key
   - `DATABASE_URL`: PostgreSQL database URL
   - `FRONTEND_URL`: Your production frontend URL
2. Deploy using platform-specific commands

#### Option 2: Deploy backend as Vercel Functions (Advanced)
1. Create `api/index.py` with FastAPI mounted as ASGI app
2. Use Vercel's Python runtime

## Authentication Flow

1. **Signup**: User registers with email/password, receives JWT token
2. **Signin**: User authenticates with credentials, receives JWT token
3. **Protected Routes**: JWT token required in Authorization header
4. **Profile Access**: Token validated to retrieve user profile
5. **Task Operations**: Token validated to ensure user owns the task

## Environment Configuration

### Frontend Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL (required)

### Backend Environment Variables
- `SECRET_KEY`: JWT secret key for token signing
- `DATABASE_URL`: PostgreSQL database connection string
- `FRONTEND_URL`: Allowed origin for CORS (defaults to http://localhost:3000)

## Security Considerations

- Use strong, randomly generated `SECRET_KEY` in production
- Use HTTPS in production for all API communications
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement rate limiting for authentication endpoints
