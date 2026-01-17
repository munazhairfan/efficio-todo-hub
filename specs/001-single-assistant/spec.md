# Feature Specification: Single Assistant Architecture

## Overview

Implement a single assistant architecture that consolidates the current dual-assistant system (OpenRouter AI and Local Task Management Agent) into one unified assistant. This unified assistant will handle all conversational chat, natural language intent understanding, MCP tool invocation, and natural language responses while maintaining all current functionality.

## User Scenarios & Testing

**Scenario 1: Task Management via Natural Language**
- User sends message: "Add a task to buy groceries"
- System processes with single assistant
- Assistant recognizes intent, invokes add_task MCP tool
- Assistant responds with confirmation

**Scenario 2: Task Listing**
- User sends message: "Show my tasks"
- System processes with single assistant
- Assistant recognizes intent, invokes list_tasks MCP tool
- Assistant responds with formatted task list

**Scenario 3: Normal Chat**
- User sends message: "How are you today?"
- System processes with single assistant
- Assistant responds with appropriate chat response (no MCP tools invoked)

**Scenario 4: Task Completion**
- User sends message: "Complete task 1"
- System processes with single assistant
- Assistant recognizes intent, invokes complete_task MCP tool
- Assistant responds with confirmation

## Functional Requirements

1. **Single Assistant Processing**: All user messages must be processed by exactly one assistant without delegation to other agents.

2. **Intent Recognition**: The single assistant must recognize natural language intents for add, list, complete, delete, and update tasks.

3. **MCP Tool Invocation**: The assistant must invoke appropriate MCP tools based on recognized intent.

4. **Chat Response**: The assistant must provide natural language responses after tool execution or for normal chat.

5. **Error Handling**: The assistant must handle tool execution errors gracefully and provide informative responses.

6. **Conversation Context**: The assistant must maintain conversation context for multi-turn interactions.

7. **API Endpoint Consistency**: The chat endpoint must consistently return responses from the same assistant.

## Non-functional Requirements

1. **Performance**: Assistant response time should be under 5 seconds for typical requests.
2. **Reliability**: System should maintain 99% uptime for assistant functionality.
3. **Maintainability**: Single codebase for assistant logic without duplicated intelligence.

## Success Criteria

1. 100% of user messages are processed by a single assistant without delegation.
2. All MCP tools (add, list, complete, delete, update tasks) are accessible through the single assistant.
3. Natural language understanding accuracy maintains current levels (>=90% for task-related commands).
4. System performance remains consistent with current dual-assistant implementation.
5. No fallback agents or secondary assistants exist in the codebase.

## Key Entities

- User messages and intent
- Task objects (ID, title, status, etc.)
- Conversation context
- MCP tool schemas and responses

## Assumptions

- OpenRouter API will continue to be available for advanced AI capabilities
- Current MCP tools implementation will remain compatible
- Existing frontend contracts will remain unchanged
- Natural language processing requirements can be met by OpenRouter alone

## Dependencies

- MCP tools implementation for task operations
- OpenRouter API for AI capabilities
- Database services for task persistence
- Authentication system for user identification