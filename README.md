# Todo App - Full Stack Application with Authentication

A full-stack todo application with authentication, featuring a Next.js frontend and FastAPI backend. This application provides all basic CRUD operations for managing tasks with secure authentication and authorization.

## Features

- **Authentication System**: Secure user signup, signin, and profile management
- **Task Management**: Create, read, update, and delete tasks
- **AI-Powered Chat Interface**: Conversational AI agent for task management
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

#### Option 2: Deploy to Hugging Face Spaces (Recommended)
1. Fork this repository to your Hugging Face account
2. Create a new Space with Docker or Python runtime
3. The application will automatically use the PORT environment variable and bind to 0.0.0.0
4. Health check endpoint available at `/health`

#### Option 3: Deploy backend as Vercel Functions (Advanced)
1. Create `api/index.py` with FastAPI mounted as ASGI app
2. Use Vercel's Python runtime

## Authentication Flow

1. **Signup**: User registers with email/password, receives JWT token
2. **Signin**: User authenticates with credentials, receives JWT token
3. **Protected Routes**: JWT token required in Authorization header
4. **Profile Access**: Token validated to retrieve user profile
5. **Task Operations**: Token validated to ensure user owns the task

## Chat API Integration

The application includes an AI-powered chat interface that allows users to interact with their tasks through natural language.

### Chat Endpoint
- **POST** `/api/{user_id}/chat` - Send a message to the AI agent
  - Request Body: `{"message": "string", "conversation_id": number | null}`
  - Response: `{"conversation_id": number, "response": "string", "message_id": number, "has_tool_calls": boolean, "tool_calls": array}`

### AI Agent Capabilities
The AI agent can understand and process various task management commands:
- **Add tasks**: "Add a task to buy groceries" or "Create a new task to call mom"
- **List tasks**: "Show me my tasks" or "What do I have to do?"
- **Complete tasks**: "Complete task #1" or "Mark task as done"
- **Delete tasks**: "Delete task #2" or "Remove this task"
- **Update tasks**: "Change task #1 to 'updated title'"

### Conversation Management
- Conversations are maintained with context using `conversation_id`
- Message history is stored and accessible to the AI agent
- Each user's conversations are isolated and secure

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
