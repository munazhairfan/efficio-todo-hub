# Quickstart Guide: AI Agent Behavior for Todo Chatbot

**Feature**: AI Agent Behavior for Todo Chatbot
**Created**: 2026-01-14
**Status**: Ready

## Overview

Quickstart guide for implementing and testing the AI agent behavior for the todo chatbot. This guide covers how to set up, test, and verify the AI agent's behavior according to the specification.

## Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- PostgreSQL database configured
- MCP tools properly configured
- Running backend API server

## Setup

### 1. Environment Configuration

```bash
# Navigate to backend directory
cd backend

# Install dependencies
poetry install
# OR with pip
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://localhost/chat_db"
export SECRET_KEY="your-secret-key-here"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Database Initialization

```bash
# Initialize database tables
python db_init.py
```

### 3. Start the API Server

```bash
# Start the backend server
uvicorn main:app --reload --port 8000
```

## Usage Examples

### 1. Task Creation

```python
# Example user message: "Add a task to buy groceries"
# Expected behavior: Agent calls add_task MCP tool and confirms
# Response: "I've added the task 'buy groceries' to your list!"
```

### 2. Task Listing

```python
# Example user message: "Show me my tasks"
# Expected behavior: Agent calls list_tasks MCP tool
# Response: Formatted list of user's tasks
```

### 3. Task Completion

```python
# Example user message: "Complete task #1"
# Expected behavior: Agent calls complete_task MCP tool
# Response: Confirmation of completion
```

### 4. Non-Task Conversation

```python
# Example user message: "How are you?"
# Expected behavior: Agent responds conversationally without MCP tools
# Response: Friendly reply without tool calls
```

## Testing the Agent

### 1. Manual Testing

Test the agent behavior by sending requests to the chat endpoint:

```bash
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'
```

### 2. Expected Responses by Intent

| User Message | Expected Intent | Expected Action | Expected Response |
|-------------|----------------|-----------------|-------------------|
| "Add task to buy groceries" | ADD_TASK | add_task tool call | Confirmation message |
| "Show me my tasks" | LIST_TASKS | list_tasks tool call | Formatted task list |
| "Complete task #1" | COMPLETE_TASK | complete_task tool call | Completion confirmation |
| "Delete task #1" | DELETE_TASK | delete_task tool call | Deletion confirmation |
| "Update task #1 to 'updated title'" | UPDATE_TASK | update_task tool call | Update confirmation |
| "How are you?" | UNKNOWN | No tool call | Conversational response |

### 3. Error Condition Testing

Test error handling with invalid inputs:

```bash
# Test with invalid task ID
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "message": "Complete task #999999",
    "conversation_id": null
  }'
```

Expected: Error message without technical details.

## Verification Checklist

### Functional Requirements
- [ ] Agent recognizes ADD_TASK intent and calls add_task MCP tool
- [ ] Agent recognizes LIST_TASKS intent and calls list_tasks MCP tool
- [ ] Agent recognizes COMPLETE_TASK intent and calls complete_task MCP tool
- [ ] Agent recognizes DELETE_TASK intent and calls delete_task MCP tool
- [ ] Agent recognizes UPDATE_TASK intent and calls update_task MCP tool
- [ ] Agent handles UNKNOWN intent without MCP tool calls
- [ ] Agent provides confirmation responses after successful tool calls
- [ ] Agent handles errors gracefully without exposing technical details
- [ ] Agent responds conversationally to non-task messages

### Safety Requirements
- [ ] Agent validates user_id for all MCP tool calls
- [ ] Agent prevents unauthorized access to tasks
- [ ] Agent does not hallucinate task IDs
- [ ] Agent does not bypass MCP tools for direct database access

### Quality Requirements
- [ ] Responses are friendly and human-sounding
- [ ] Confirmation messages are specific and clear
- [ ] Error messages are user-friendly
- [ ] Agent asks for clarification when needed
- [ ] Response time is under 2 seconds

## Troubleshooting

### Common Issues

1. **Intent Not Recognized**
   - Check if message contains expected keywords
   - Verify regex patterns in the agent

2. **MCP Tool Call Fails**
   - Verify user_id is passed correctly
   - Check MCP tool implementation

3. **Authentication Error**
   - Verify Authorization header format
   - Check token validity

4. **Response Time Exceeded**
   - Check database connection
   - Verify MCP tool performance

## Next Steps

1. Integrate with frontend chat interface
2. Add conversation history awareness
3. Enhance intent recognition with more patterns
4. Expand error handling for additional scenarios