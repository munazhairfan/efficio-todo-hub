# Quickstart Guide: Chat API + Conversation Handling

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon recommended)
- FastAPI dependencies
- Environment variables configured

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart python-jose[cryptography] passlib[bcrypt]
```

### 4. Configure Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Initialize Database
```bash
# Run database migrations to create tables
python -m src.database.init
```

## Running the Service

### Development
```bash
# Start the development server
uvicorn src.api.main:app --reload --port 8000
```

### Production
```bash
# Start the production server
uvicorn src.api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

## API Usage

### Start New Conversation
```bash
curl -X POST "http://localhost:8000/api/123/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how can you help me?"}'
```

### Continue Existing Conversation
```bash
curl -X POST "http://localhost:8000/api/123/chat" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 456, "message": "Tell me more about this topic"}'
```

## API Response Format
```json
{
  "conversation_id": 456,
  "response": "This is the AI response to your message",
  "tool_calls": []
}
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Test Coverage
```bash
pytest --cov=src/ tests/
```

## Environment Configuration

### Development Environment
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://localhost:5432/chat_dev
LOG_LEVEL=debug
```

### Production Environment
```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://prod-server:5432/chat_prod
LOG_LEVEL=warning
MAX_WORKERS=4
TIMEOUT=30
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify DATABASE_URL is correctly configured
- Ensure PostgreSQL server is running
- Check firewall settings if connecting remotely

#### API Endpoint Not Found
- Verify the server is running on the correct port
- Check that the API route is correctly mounted
- Ensure user_id exists in the users table

#### Slow Response Times
- Monitor database query performance
- Check if AI service is responding appropriately
- Review indexing on conversation and message tables