# Quickstart: Single Assistant Architecture

## Overview
The single assistant architecture consolidates all AI processing into one assistant that handles both normal chat and MCP tool invocation as needed.

## Setup

### Prerequisites
- Python 3.11+
- OpenRouter API key

### Configuration
1. Set environment variable:
   ```bash
   export OPENROUTER_API_KEY="your-api-key-here"
   ```

## Usage

### Sending Messages
Messages are processed by the single assistant which:
1. Analyzes the user's intent
2. Decides whether to respond directly or call MCP tools
3. Returns a natural language response

### Task Operations
The assistant automatically calls MCP tools when needed:
- "Add a task to buy groceries" → `add_task` tool
- "Show my tasks" → `list_tasks` tool
- "Complete task 1" → `complete_task` tool
- "Delete task 1" → `delete_task` tool
- "Update task 1 to call mom" → `update_task` tool

## API Integration
The API endpoint remains unchanged:
```
POST /api/{user_id}/chat
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "message": "Your message here",
  "conversation_id": null  // or existing conversation ID
}
```

## Key Benefits
- Simplified architecture with one assistant
- AI-driven tool selection
- Maintained functionality
- Better maintainability