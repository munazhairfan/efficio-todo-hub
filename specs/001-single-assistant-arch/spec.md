# Feature Specification: Single Assistant Architecture

**Feature Branch**: `001-single-assistant-arch`
**Created**: 2026-01-18
**Status**: Draft
**Input**: User description: "SYSTEM ARCHITECTURE CONSTRAINT — NON NEGOTIABLE

This project MUST use exactly ONE assistant.

❌ Do NOT create:
- Multiple assistants
- Fallback agents
- Secondary/local agents
- Pattern-matching agents
- Backup AI processors

✅ REQUIRED BEHAVIOR:

1. There is ONE assistant responsible for:
   - Conversational chat with the user
   - Understanding intent from natural language
   - Invoking MCP tools (add, update, delete, list tasks)
   - Responding in natural language after tool execution

2. The assistant:
   - May call MCP tools when required
   - May respond with normal chat when no tool is needed
   - Must not delegate to another agent

3. MCP tools are:
   - NOT assistants
   - NOT agents
   - Simple executable functions only

4. Manual task management:
   - Users MUST be able to add, update, delete tasks
     using traditional UI elements (buttons, inputs, forms)
   - This operates independently of the assistant
   - The assistant must NOT interfere with manual actions

5. Architecture cleanup:
   - If multiple assistants or agents exist in the codebase,
     REMOVE them.
   - Merge logic into ONE assistant pipeline.
   - Do NOT introduce new assistants while refactoring.

6. Frontend/Backend contract:
   - Frontend sends messages to ONE chat endpoint
   - Backend processes with ONE assistant
   - Responses come from the same assistant every time

Violation of this spec is considered an error.
Do not propose alternative architectures."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Unified Assistant Interaction (Priority: P1)

As a user, I want to interact with a single assistant that can handle both general chat and task-specific operations so that I have a consistent experience and don't need to switch between different interfaces.

**Why this priority**: This is the core requirement of the architecture constraint and eliminates confusion between multiple assistants.

**Independent Test**: Users can engage in natural language conversations and issue task commands (add, update, delete, list tasks) through a single interface and receive appropriate responses.

**Acceptance Scenarios**:

1. **Given** a user opens the chat interface, **When** they type "Add a task to buy groceries", **Then** the assistant processes the command and adds the task to their list.
2. **Given** a user has multiple tasks, **When** they type "Show me my tasks", **Then** the assistant responds with their current task list.

---

### User Story 2 - Traditional Task Management Coexistence (Priority: P1)

As a user, I want to use traditional UI elements (buttons, forms) for task management that operate independently of the assistant so that I can choose my preferred method of interaction.

**Why this priority**: Ensures backward compatibility and gives users flexibility in how they manage tasks.

**Independent Test**: Users can add, update, delete, and view tasks using buttons and forms without any interference from the assistant system.

**Acceptance Scenarios**:

1. **Given** a user is on the dashboard, **When** they use the traditional "Add Task" form, **Then** the task is added without involving the assistant.

---

### User Story 3 - MCP Tool Integration (Priority: P2)

As a user, I want the assistant to seamlessly integrate with MCP tools for advanced task operations so that complex tasks can be handled efficiently.

**Why this priority**: Enables the assistant to perform advanced operations while maintaining the single-assistant architecture.

**Independent Test**: The assistant can invoke appropriate MCP tools when natural language indicates a specific task operation is needed.

**Acceptance Scenarios**:

1. **Given** a user types "Create a recurring task for weekly reports", **When** the assistant recognizes this requires MCP tools, **Then** it invokes the appropriate tool to create the recurring task.

---

### Edge Cases

- What happens when the assistant encounters a malformed natural language command?
- How does the system handle concurrent operations from both the assistant and manual UI elements?
- What occurs when the assistant is temporarily unavailable but manual operations should still function?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST have exactly ONE assistant endpoint for all conversational interactions
- **FR-002**: System MUST remove all existing multiple assistant implementations from the codebase
- **FR-003**: The single assistant MUST handle both general chat and task-specific commands
- **FR-004**: The assistant MUST be able to invoke MCP tools when required for task operations
- **FR-005**: The assistant MUST respond appropriately when no MCP tools are needed (normal chat)
- **FR-006**: The assistant MUST NOT delegate tasks to other agents or assistants
- **FR-007**: Traditional UI task management MUST continue to function independently
- **FR-008**: Traditional UI operations MUST NOT interfere with assistant-managed tasks
- **FR-009**: Frontend MUST send all messages to a single chat endpoint
- **FR-010**: Backend MUST process all messages through the single assistant instance
- **FR-011**: MCP tools MUST function as simple executable functions, not as separate agents
- **FR-012**: System MUST maintain conversation context within the single assistant

### Key Entities *(include if feature involves data)*

- **Assistant**: The unified AI entity responsible for processing all natural language input and coordinating with MCP tools
- **MCP Tools**: Simple executable functions that perform specific task operations when invoked by the assistant
- **User Session**: Maintains conversation context and user state within the single assistant

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All user interactions flow through exactly one assistant endpoint (verified by code analysis showing single assistant implementation)
- **SC-002**: Zero multiple assistant implementations exist in the codebase after refactoring (verified by code review showing removed duplicate components)
- **SC-003**: Users can successfully complete both general chat and task-specific operations through the unified interface (measured by user testing success rate of >95%)
- **SC-004**: Traditional UI elements continue to function without interference (measured by maintaining existing functionality and user satisfaction scores)
