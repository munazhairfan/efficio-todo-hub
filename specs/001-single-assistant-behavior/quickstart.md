# Quickstart Guide: Single Assistant Conversational + CRUD Behavior

## Overview
This guide explains how to implement a single assistant that handles both conversational responses and task CRUD operations based on user intent.

## Prerequisites
- Python 3.11+
- FastAPI
- SQLModel
- PostgreSQL database

## Implementation Steps

### 1. Update Conversation Endpoint
Modify the conversation endpoint in `api/routes/conversation.py` to:
- Detect user intent (conversational vs task-related)
- Process requests accordingly
- Ensure every request gets a text response

### 2. Implement Intent Detection
Add intent detection logic to differentiate between:
- Conversational messages (casual chat, questions)
- Task creation requests (add, create)
- Task management requests (list, update, delete)

### 3. MCP Tool Integration
- Call MCP tools only when task-related intent is detected
- Generate confirmation text after MCP tool execution
- Respond conversationally for non-task requests

### 4. Response Consistency
- Ensure every user message produces a text response
- For task operations: return confirmation message
- For conversation: return appropriate response

## API Usage

### Request Format
```json
{
  "input": "User message text",
  "sessionId": "Session identifier (optional)",
  "context": {
    "user_id": "Optional user identifier"
  }
}
```

### Response Format
```json
{
  "responseType": "success|clarification|error",
  "message": "Text response to user",
  "clarifyingQuestions": ["Array of clarifying questions"],
  "suggestedActions": ["Array of suggested actions"],
  "conversationId": "Conversation identifier (if applicable)",
  "analysis": {
    "intent": {"is_ambiguous": false},
    "ambiguity": {"is_ambiguous": false},
    "vagueness": {"is_vague": false}
  }
}
```

## Testing
- Verify conversational messages receive appropriate responses
- Verify task operations execute correctly with confirmations
- Confirm every request produces a text response
- Test with both Vercel and Hugging Face deployments