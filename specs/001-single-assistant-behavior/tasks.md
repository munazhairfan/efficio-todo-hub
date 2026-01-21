# Implementation Tasks: Single Assistant Conversational + CRUD Behavior

**Feature**: Single Assistant that handles both conversation and task management
**Branch**: `001-single-assistant-behavior`
**Timeline**: Iterative delivery with MVP on US1

## Implementation Strategy

Build iteratively with User Story 1 (P1) as the MVP. Each story is independently testable with increasing functionality.

### MVP Scope (Iteration 1)
- Implement basic conversation functionality (US1)
- Ensure every message gets a response
- Basic intent detection for conversation vs tasks

### Iteration 2
- Implement task creation functionality (US2)
- Connect to MCP tools for task operations

### Iteration 3
- Implement full CRUD operations for tasks (US3)
- Handle update, delete, list operations

### Iteration 4
- Implement mixed conversation-task flows (US4)
- Advanced error handling and edge cases

## Phase 1: Setup Tasks

### Project Initialization
- [X] T001 Set up project structure per implementation plan in backend/
- [X] T002 Configure Python 3.11 environment with FastAPI, SQLModel dependencies
- [X] T003 Initialize database connection with PostgreSQL via SQLModel/SQLAlchemy
- [X] T004 [P] Set up Hugging Face backend structure in efficio-todo-hub-backend/

## Phase 2: Foundation Tasks

### Core Infrastructure
- [X] T010 Create unified assistant module that handles both conversation and tasks
- [X] T011 Implement intent detection utilities for task vs conversation classification
- [X] T012 [P] Set up database session dependency for conversation route
- [X] T013 Create conversation service to handle state management
- [X] T014 Implement basic response structure matching API contract

## Phase 3: [US1] Normal Chat Interaction

### Story Goal: User can send casual messages like "Hi, how are you?" and get friendly responses
### Independent Test: Send conversational messages and receive appropriate responses without task operations

- [X] T020 [US1] Implement basic conversational response logic in conversation route
- [X] T021 [US1] Add default response handling for non-task messages
- [X] T022 [US1] Ensure every message produces a text response regardless of content
- [X] T023 [US1] Add flexible input field handling (input/message/text fields)
- [X] T024 [US1] Test basic conversation flow with sample messages
- [X] T025 [US1] Verify 100% response rate for conversational messages

## Phase 4: [US2] Task Creation Request

### Story Goal: User can request to add tasks like "Add a task to buy groceries" and get confirmation
### Independent Test: Request task creation and receive confirmation with MCP tool call

- [X] T030 [US2] Implement task creation intent detection in conversation route
- [X] T031 [US2] Integrate with add_task MCP tool for task creation requests
- [X] T032 [US2] Generate confirmation response after successful task creation
- [X] T033 [US2] Validate required fields for task creation (title/input)
- [X] T034 [US2] Test task creation flow with sample requests
- [X] T035 [US2] Verify proper error handling for invalid task requests

## Phase 5: [US3] Task Management Actions

### Story Goal: User can request delete, update, list tasks and get proper responses
### Independent Test: Request delete/update/list operations and receive appropriate responses

- [X] T040 [US3] Implement task listing intent detection in conversation route
- [X] T041 [US3] Integrate with list_tasks MCP tool for task listing requests
- [X] T042 [US3] Implement task update intent detection in conversation route
- [X] T043 [US3] Integrate with update_task MCP tool for task update requests
- [X] T044 [US3] Implement task deletion intent detection in conversation route
- [X] T045 [US3] Integrate with delete_task MCP tool for task deletion requests
- [X] T046 [US3] Generate appropriate responses after all task operations
- [X] T047 [US3] Test all CRUD operations with sample requests
- [X] T048 [US3] Verify error handling for invalid task IDs or operations

## Phase 6: [US4] Mixed Conversational and Task Requests

### Story Goal: User can alternate between casual chat and task requests seamlessly
### Independent Test: Have conversation that includes both chat and task requests with appropriate responses

- [X] T050 [US4] Implement intent detection that works within conversation flows
- [X] T051 [US4] Ensure conversation context is maintained between messages
- [X] T052 [US4] Test alternating chat and task requests in single session
- [X] T053 [US4] Handle edge case where single message contains multiple intents
- [X] T054 [US4] Validate conversation continuity with session IDs
- [X] T055 [US4] Test realistic conversation flows with mixed requests

## Phase 7: Polish & Validation

### Quality Assurance
- [X] T060 Validate all API responses match OpenAPI contract specification
- [X] T061 [P] Ensure single assistant implementation with no fallback agents
- [X] T062 Implement stateless operation with database-loaded conversation history
- [X] T063 Add proper error logging and monitoring
- [X] T064 Validate 100% response rate for all message types
- [X] T065 Test performance targets (responses under 3 seconds)
- [X] T066 Verify rate limiter doesn't interfere with conversation endpoints
- [X] T067 Deploy to both Vercel and Hugging Face with consistent functionality

## Dependency Graph

US1 (P1) → US2 (P1) → US3 (P1) → US4 (P2)

User Story 1 must be completed before User Story 2, etc. Each story builds on the previous implementation.

## Parallel Execution Examples

**US1 Parallel Tasks**: T020-T022 can be worked in parallel since they all work on the conversation response logic

**US3 Parallel Tasks**: T040/T042/T044 can be worked in parallel (different intent detections), while T041/T043/T045 can be worked in parallel (different MCP tool integrations)

**Cross-Story Parallelism**: Tasks in different phases cannot be done in parallel, but infrastructure tasks (Phase 2) can be done while conversation flow is being developed (Phase 3).