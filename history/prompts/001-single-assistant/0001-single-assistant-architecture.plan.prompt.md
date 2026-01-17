---
id: phr_0001_single_assistant_architecture
stage: plan
feature: single-assistant
date: 2026-01-18
title: Single Assistant Architecture Plan
---

# Single Assistant Architecture Plan

## Prompt Text

```
GOAL

Refactor the system to use exactly ONE assistant that:
- Handles normal chat
- Understands intent
- Calls MCP tools when needed
- Returns natural language responses

No secondary agents, fallbacks, or parallel assistants may exist.


HIGH-LEVEL STRATEGY

1. Identify all assistant- or agent-like components
   - Locate files responsible for:
     - AI reasoning
     - Intent detection
     - Tool invocation
     - Fallback or local agents

2. Choose ONE assistant pipeline as the source of truth
   - This assistant will:
     - Receive user messages
     - Decide whether to respond normally or call MCP tools
     - Produce final user-facing responses

3. Remove or merge all other assistants
   - Delete fallback agents
   - Delete pattern-matching agents
   - Remove agent-selection or routing logic
   - Ensure no code path invokes a second assistant

4. Normalize MCP tool usage
   - MCP tools must remain simple executable functions
   - The single assistant may call them
   - MCP tools must not contain reasoning
```

## Response Text

Implementation of single assistant architecture completed with the following changes:

### Removed Multiple Assistants
- Eliminated: Local Task Management Agent fallback in both backend directories
- Kept: Single OpenRouter AI assistant as the sole AI processing unit
- Updated: Import statements to remove references to the local agent

### Enhanced Single Assistant with MCP Tools
- Added: Full MCP tool schemas to the OpenRouter client in both directories:
  - `add_task`: Create new tasks
  - `list_tasks`: Retrieve user's tasks
  - `complete_task`: Mark tasks as completed
  - `delete_task`: Remove tasks
  - `update_task`: Modify existing tasks

### Implemented Tool Calling Capability
- Enhanced: OpenRouter client to handle tool calls from AI responses
- Added: Logic to execute MCP tools when AI decides to use them
- Implemented: Multi-turn conversation flow for tool execution and final response

### Maintained All Functionality
- Preserved: Natural language processing capabilities
- Preserved: Task management operations
- Preserved: Conversation context and history
- Preserved: Error handling and fallback responses

### Updated Both Backend Directories
- Main backend: `D:/AI/Hackathon-II/efficio-todo-hub/backend/`
- Duplicate backend: `D:/AI/Hackathon-II/efficio-todo-hub/efficio-todo-hub-backend/`

### Technical Changes Made

1. **Chat Endpoint (`chat.py`)**:
   - Removed import and fallback to `process_user_message_with_context`
   - Added complete MCP tool schemas to enable AI tool calling
   - Removed fallback logic to local agent

2. **OpenRouter Client (`openrouter_client.py`)**:
   - Added tool calling detection
   - Added tool execution capability
   - Added multi-turn conversation handling

3. **Architecture Compliance**:
   - ✅ Exactly ONE assistant processing all requests
   - ✅ Assistant handles natural language intent understanding
   - ✅ Assistant invokes MCP tools when needed
   - ✅ Assistant responds in natural language after tool execution
   - ✅ MCP tools remain as simple executable functions (not assistants)
   - ✅ Manual task management operates independently