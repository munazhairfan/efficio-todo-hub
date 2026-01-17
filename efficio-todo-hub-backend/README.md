---
title: Efficio Todo Hub - Backend API
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# Efficio Todo Hub Backend API

Backend API for the Efficio Todo Hub application, providing chat and conversation handling capabilities.

## Features
- RESTful API for chat conversations
- Conversation persistence in PostgreSQL
- Message history tracking
- Mock AI responses with tool call simulation
- User authentication framework
- MCP (Model Context Protocol) tools for AI agent task management

## Prerequisites
- Python 3.11+
- PostgreSQL database

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database URL and other settings
```

3. Initialize the database:
```bash
# Using the provided script
python db_init.py init
# Or using Alembic directly
alembic upgrade head
```

## Running the Application

```bash
# Using uvicorn (local development)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Hugging Face Spaces Deployment

```bash
# Using the server.py entry point (for Hugging Face Spaces)
python server.py
```

The application is configured to:
- Bind to host `0.0.0.0` (required by Hugging Face)
- Use port from the `PORT` environment variable (provided by Hugging Face)
- Serve the FastAPI application via uvicorn

## API Endpoints

### Chat API
- `POST /api/{user_id}/chat` - Send a message and get AI response

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

## Testing

Run the tests:
```bash
pytest tests/
```

## Configuration

The application uses Pydantic Settings for configuration management. Create a `.env` file in the backend root directory with the following variables:

```
DATABASE_URL=postgresql://username:password@localhost/chat_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DB_POOL_SIZE=20
DB_POOL_OVERFLOW=0
DB_ECHO=False
API_PREFIX=/api
DEBUG=False
```

## Database Migrations

Generate a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

## Architecture

- **Models**: Located in `src/models/` - SQLAlchemy models
- **Services**: Located in `src/services/` - Business logic layer
- **API Routes**: Located in `src/api/` - FastAPI route handlers
- **Core**: Located in `src/core/` - Configuration and dependencies
- **Database**: Located in `src/database/` - Database session and models
- **MCP Tools**: Located in `src/mcp_tools.py` - Model Context Protocol tools for AI agents
- **AI Agent**: Located in `src/agents/task_management_agent.py` - AI decision-making logic for task management

## MCP Tools

The backend includes MCP (Model Context Protocol) tools that allow AI agents to manage user tasks:

- `add_task`: Create new tasks for users
- `list_tasks`: Retrieve tasks with optional filtering
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks from user's list
- `update_task`: Modify task title or description

For detailed documentation on MCP tools, see [MCP_TOOLS.md](MCP_TOOLS.md).

## AI Agent

The backend includes an AI agent that processes natural language requests and calls the appropriate MCP tools:

- **Location**: `src/agents/task_management_agent.py`
- **Functionality**: Reads user messages, detects intent, calls MCP tools, returns friendly responses
- **Supported Actions**: Add, list, complete, delete, update tasks via natural language
- **Integration**: Seamlessly connects user requests to MCP tool execution

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=src
```

## Environment Setup for Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up database:
```bash
python db_init.py init
```

4. Run the application:
```bash
uvicorn src.main:app --reload
```