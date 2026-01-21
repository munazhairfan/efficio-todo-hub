# Feature Specification: Single Assistant Conversational + CRUD Behavior

**Feature Branch**: `001-single-assistant-behavior`
**Created**: 2026-01-21
**Status**: Draft
**Input**: User description: "# Sub-Part: Single Assistant Conversational + CRUD Behavior

## Goal
Fix the chatbot so there is ONLY ONE assistant that:
1. Replies to every user message like a normal chat assistant
2. Performs CRUD actions (add, list, update, delete tasks) when instructed
3. Confirms CRUD actions with a text response
4. Does NOT create multiple assistants or fallback agents

## Non-Goals (STRICT)
- Do NOT create a second assistant
- Do NOT add fallback/local agents
- Do NOT modify user authentication logic
- Do NOT modify existing todo CRUD REST endpoints
- Do NOT modify frontend UI logic for buttons/forms

## Current Problem
- Assistant only adds tasks
- Assistant ignores delete/update commands
- Assistant does not reply to normal conversation
- Assistant behaves like a command-only bot, not a chat assistant


## Desired Assistant Behavior
- Every user message MUST produce a text reply
- If the message contains a task intent:
  - Call the correct MCP tool
  - Then reply with confirmation text
- If the message is conversational:
  - Reply conversationally without calling tools

## Single Assistant Rule
There MUST be exactly ONE assistant implementation.
All logic (conversation + task actions) must live inside it.

## Tool Usage Rule
- MCP tools are used ONLY when intent requires them
- Tools are NEVER used silently
- After a tool call, assistant MUST respond in text

## Stateless Rule
- No in-memory state
- Conversation history is loaded from database each request"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Normal Chat Interaction (Priority: P1)

User sends a casual message like "Hi, how are you?" and expects a friendly response. The assistant should reply conversationally without triggering any task management tools.

**Why this priority**: This is the core chat functionality that users expect from any chatbot. Without this, the assistant fails as a conversational agent.

**Independent Test**: User can send conversational messages and receive appropriate responses without any task management functionality being triggered.

**Acceptance Scenarios**:

1. **Given** user sends a casual message like "Hello", **When** assistant receives the message, **Then** assistant responds with a friendly conversational reply
2. **Given** user asks a question like "How are you?", **When** assistant processes the request, **Then** assistant responds appropriately without performing any task actions

---

### User Story 2 - Task Creation Request (Priority: P1)

User sends a message requesting to add a task like "Add a task to buy groceries" and expects the assistant to create the task and confirm the action with a text response.

**Why this priority**: This is one of the core task management functions that the assistant currently supports partially, and it's a primary use case.

**Independent Test**: User can request task creation and the assistant both calls the appropriate tool and responds with confirmation text.

**Acceptance Scenarios**:

1. **Given** user sends "Add a task to buy groceries", **When** assistant processes the request, **Then** assistant calls the add_task tool and replies with confirmation
2. **Given** user sends "Create a task to finish report", **When** assistant processes the request, **Then** assistant creates the task and acknowledges completion

---

### User Story 3 - Task Management Actions (Priority: P1)

User sends requests for other task management actions like deleting, updating, or listing tasks, and expects the assistant to perform the action and confirm with text response.

**Why this priority**: This addresses the main issue - the assistant currently ignores delete/update commands and doesn't handle full CRUD operations.

**Independent Test**: User can request delete, update, or list operations and the assistant performs them correctly with appropriate responses.

**Acceptance Scenarios**:

1. **Given** user sends "Delete task #1", **When** assistant processes the request, **Then** assistant calls the delete_task tool and confirms deletion
2. **Given** user sends "Update task #2 to 'Buy milk'", **When** assistant processes the request, **Then** assistant calls the update_task tool and confirms the update
3. **Given** user sends "List my tasks", **When** assistant processes the request, **Then** assistant calls the list_tasks tool and returns the task list

---

### User Story 4 - Mixed Conversational and Task Requests (Priority: P2)

User alternates between casual conversation and task management requests, and expects the assistant to handle both appropriately without confusion.

**Why this priority**: This ensures the assistant can seamlessly switch between conversation and task modes as needed in real usage.

**Independent Test**: User can have a conversation that includes both casual chat and task requests, with the assistant responding appropriately to each.

**Acceptance Scenarios**:

1. **Given** user starts with "Hi there" then says "Add a task to call mom", **When** assistant processes both messages, **Then** first gets conversational response, second gets task confirmation
2. **Given** user asks "What can you do?" then "List my tasks", **When** assistant processes both requests, **Then** first gets capability explanation, second gets task list

---

### Edge Cases

- What happens when user sends a malformed request that's neither clear conversation nor clear task intent?
- How does the system handle requests when database connectivity is unavailable?
- What if the MCP tools are temporarily unavailable - does the assistant still provide a response?
- How does the assistant handle requests with multiple intents in a single message?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST respond to every user message with a text reply
- **FR-002**: System MUST detect task-related intents and call appropriate MCP tools
- **FR-003**: System MUST respond conversationally to non-task-related messages
- **FR-004**: System MUST confirm MCP tool execution with text responses
- **FR-005**: System MUST handle task CRUD operations (add, list, update, delete)
- **FR-006**: System MUST load conversation history from database for each request
- **FR-007**: System MUST NOT create multiple assistant instances
- **FR-008**: System MUST process requests without maintaining in-memory state between requests

### Key Entities *(include if feature involves data)*

- **User Message**: Represents input from the user, containing text and optional metadata
- **Assistant Response**: Represents output from the assistant, containing text response and optional tool call information
- **Task**: Represents a task entity with properties like title, description, status, and ID

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of user messages produce a text response from the assistant
- **SC-002**: Task management commands (add, list, update, delete) are correctly detected and executed 95% of the time
- **SC-003**: Casual conversation messages receive appropriate conversational responses 95% of the time
- **SC-004**: Assistant performs both conversation and task actions within 3 seconds per request
- **SC-005**: Only one assistant instance is active at any given time (no duplicate assistants created)