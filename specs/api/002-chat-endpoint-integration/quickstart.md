# Quickstart: Chat Endpoint Integration

## Overview
This feature integrates the AI agent with the existing chat endpoint to process user messages and return AI-generated responses.

## Prerequisites
- Python 3.11+
- PostgreSQL database configured
- Existing MCP tools and AI agent modules installed

## API Endpoint
```
POST /api/{user_id}/chat
```

## Request Format
```json
{
  "message": "Your message to the AI agent"
}
```

## Response Format
```json
{
  "response": "AI agent's response",
  "action_taken": true/false
}
```

## Testing
Run the following command to test the integration:
```bash
pytest tests/unit/test_chat_api.py
pytest tests/integration/test_chat_integration.py
```

## Key Files
- `backend/src/api/chat.py` - Updated chat endpoint
- `backend/src/agents/task_management_agent.py` - AI agent logic
- `backend/src/mcp_tools.py` - MCP tools integration

## Example Usage
1. Send a POST request to `/api/123/chat` with a message
2. The system will:
   - Load conversation history for user 123
   - Save your message to the database
   - Call the AI agent with the conversation context
   - Save the AI's response to the database
   - Return the response to the frontend