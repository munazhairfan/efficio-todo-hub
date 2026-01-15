# API Contract: AI Agent Response Format

**Contract**: AI Agent Response Format
**Created**: 2026-01-14
**Status**: Active
**Related Feature**: AI Agent Behavior for Todo Chatbot

## Overview

This contract defines the expected response format and behavior of the AI agent when processing user messages and calling MCP tools. This ensures consistent behavior across different implementations and consumers.

## Response Schema

### Agent Response Object

```json
{
  "response": "string",
  "action_taken": "boolean",
  "error": "string | null",
  "tasks": "array | null"
}
```

### Field Definitions

- `response` (required): Natural language response to the user
  - Type: String
  - Constraints: Non-empty, human-readable text

- `action_taken` (required): Whether an MCP tool was called
  - Type: Boolean
  - Values: true if tool was called, false otherwise

- `error` (optional): Error message if operation failed
  - Type: String | null
  - Constraints: Null if no error, otherwise human-readable error message

- `tasks` (optional): Array of tasks if list_tasks was called
  - Type: Array | null
  - Constraints: Null if not listing tasks, otherwise array of task objects

## Behavioral Contracts

### 1. Task Creation Contract
**When**: User intent is ADD_TASK
**Then**:
- `response` contains confirmation message with task title
- `action_taken` is true
- `error` is null on success
- `tasks` is null

**Example**:
```json
{
  "response": "I've added the task 'buy groceries' to your list!",
  "action_taken": true,
  "error": null,
  "tasks": null
}
```

### 2. Task Listing Contract
**When**: User intent is LIST_TASKS
**Then**:
- `response` contains formatted list of tasks
- `action_taken` is true
- `error` is null on success
- `tasks` contains array of task objects

**Example**:
```json
{
  "response": "Here are your pending tasks:\n- 1: buy groceries\n- 2: walk the dog",
  "action_taken": true,
  "error": null,
  "tasks": [
    {"id": 1, "title": "buy groceries", "status": "pending"},
    {"id": 2, "title": "walk the dog", "status": "pending"}
  ]
}
```

### 3. Task Completion Contract
**When**: User intent is COMPLETE_TASK
**Then**:
- `response` contains completion confirmation with task title
- `action_taken` is true
- `error` is null on success
- `tasks` is null

**Example**:
```json
{
  "response": "I've marked task 'buy groceries' as completed!",
  "action_taken": true,
  "error": null,
  "tasks": null
}
```

### 4. Non-Task Conversation Contract
**When**: User intent is UNKNOWN (non-task related)
**Then**:
- `response` contains conversational reply
- `action_taken` is false
- `error` is null
- `tasks` is null

**Example**:
```json
{
  "response": "I'm doing well, thank you for asking! How can I help you with your tasks today?",
  "action_taken": false,
  "error": null,
  "tasks": null
}
```

### 5. Error Handling Contract
**When**: Tool call fails or invalid input
**Then**:
- `response` contains user-friendly error message
- `action_taken` is false
- `error` contains error details (optional)
- `tasks` is null

**Example**:
```json
{
  "response": "I couldn't find that task. Please check the task number and try again.",
  "action_taken": false,
  "error": "Task not found",
  "tasks": null
}
```

## Validation Rules

### Response Format
- All responses must be in natural language
- Confirmation messages must reference specific action taken
- Error messages must be user-friendly without technical details
- Response time must be under 2 seconds

### Intent Recognition
- Agent must classify intent based on keyword matching
- Unknown intents should result in conversational responses
- Ambiguous intents should prompt for clarification

### Tool Calling
- All MCP tool calls must include valid user_id
- Tool parameters must be validated before calling
- Authorization must be verified for each operation

## Backward Compatibility

- Existing response format must be maintained
- New fields may be added but not removed
- Error handling behavior must remain consistent
- User experience should not degrade

## Success Metrics

- 90% of clear task management requests result in successful MCP tool calls
- 95% of MCP tool calls initiated by the AI agent complete successfully
- Less than 5% of user requests result in error responses due to agent misinterpretation
- 100% of non-task-related messages are handled without inappropriate MCP tool calls