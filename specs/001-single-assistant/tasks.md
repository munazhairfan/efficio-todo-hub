# Tasks: Single Assistant Architecture

## Feature Overview
Implement a single assistant architecture that consolidates the current dual-assistant system (OpenRouter AI and Local Task Management Agent) into one unified assistant. This unified assistant will handle all conversational chat, natural language intent understanding, MCP tool invocation, and natural language responses while maintaining all current functionality.

## Dependencies
- US1 must be completed before US2, US3, US4
- US2, US3, US4 can be developed in parallel after US1

## Parallel Execution Examples
- US2 and US3 can run in parallel: One developer works on main backend, another on duplicate backend
- US2 and US4 can run in parallel: Testing can happen simultaneously with backend updates

## Implementation Strategy
MVP scope: US1 (Identify and mark single assistant as source of truth)
Incremental delivery: Each user story delivers a complete, testable increment

---

## Phase 1: Setup

- [ ] T001 Set up development environment and verify current system functionality
- [ ] T002 [P] Audit all AI-related files to identify assistant implementations
- [ ] T003 [P] Document current architecture with multiple assistants

---

## Phase 2: Foundational

- [ ] T004 Create backup of current codebase before major changes
- [ ] T005 [P] Identify all files with AI behavior, agents, assistants, AI clients, fallback logic, pattern matching
- [ ] T006 [P] Map file dependencies and call flows between assistant components

---

## Phase 3: [US1] Identify and Mark Single Assistant Source of Truth

**Goal**: Locate all assistant implementations and mark exactly one as the source of truth.

**Independent Test Criteria**:
- All AI processing flows through single designated file
- No other assistant implementations remain active
- System responds to test messages via single assistant

**Tasks**:

- [ ] T007 [US1] Identify main assistant file: backend/src/services/openrouter_client.py as Single Assistant Source of Truth
- [ ] T008 [US1] Identify secondary assistant files: backend/src/agents/task_management_agent.py as to-be-removed
- [ ] T009 [US1] Identify fallback logic in backend/src/api/chat.py to local agent
- [ ] T010 [US1] Document all import references to task_management_agent in the codebase
- [ ] T011 [US1] Document all call sites where secondary assistant is invoked

---

## Phase 4: [US2] Remove Extra Assistants from Main Backend

**Goal**: Delete or fully disable all secondary assistants in main backend directory.

**Independent Test Criteria**:
- No references to secondary assistants in main backend
- Build passes without secondary assistant files
- All functionality works through single assistant

**Tasks**:

- [ ] T012 [US2] Remove import of process_user_message_with_context from backend/src/api/chat.py
- [ ] T013 [US2] Remove fallback logic to local agent in backend/src/api/chat.py
- [ ] T014 [US2] Replace empty MCP tools schemas with complete schemas in backend/src/api/chat.py
- [ ] T015 [US2] Update OpenRouter client to handle tool calls and execution in backend/src/services/openrouter_client.py
- [ ] T016 [US2] Test main backend functionality without secondary assistant

---

## Phase 5: [US3] Remove Extra Assistants from Duplicate Backend

**Goal**: Delete or fully disable all secondary assistants in duplicate backend directory.

**Independent Test Criteria**:
- No references to secondary assistants in duplicate backend
- Build passes without secondary assistant files in duplicate backend
- All functionality works through single assistant in duplicate backend

**Tasks**:

- [ ] T017 [US3] Remove import of process_user_message_with_context from efficio-todo-hub-backend/src/api/chat.py
- [ ] T018 [US3] Remove fallback logic to local agent in efficio-todo-hub-backend/src/api/chat.py
- [ ] T019 [US3] Replace empty MCP tools schemas with complete schemas in efficio-todo-hub-backend/src/api/chat.py
- [ ] T020 [US3] Update OpenRouter client to handle tool calls and execution in efficio-todo-hub-backend/src/services/openrouter_client.py
- [ ] T021 [US3] Test duplicate backend functionality without secondary assistant

---

## Phase 6: [US4] Verify Chat Flow and MCP Tool Boundaries

**Goal**: Ensure single assistant handles all chat requests and MCP tools are used correctly.

**Independent Test Criteria**:
- All chat responses originate from the same assistant
- No branching or fallback to other assistants
- MCP tools called only by single assistant
- All user scenarios work as specified

**Tasks**:

- [ ] T022 [US4] Trace chat request flow: Frontend → chat API → single assistant → response in both backends
- [ ] T023 [US4] Verify MCP tools contain no conversational logic in backend/src/mcp_tools.py
- [ ] T024 [US4] Verify MCP tools contain no AI reasoning in backend/src/mcp_tools.py
- [ ] T025 [US4] Confirm MCP tools only execute actions (CRUD, utilities) in backend/src/mcp_tools.py
- [ ] T026 [US4] Test Scenario 1: "Add a task to buy groceries" processes through single assistant
- [ ] T027 [US4] Test Scenario 2: "Show my tasks" processes through single assistant
- [ ] T028 [US4] Test Scenario 3: "How are you today?" processes through single assistant
- [ ] T029 [US4] Test Scenario 4: "Complete task 1" processes through single assistant
- [ ] T030 [US4] Verify no code path invokes a second assistant in either backend

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T031 Clean up unused imports and dead code paths
- [ ] T032 Run syntax checks to ensure code compiles without errors
- [ ] T033 Update documentation to reflect single assistant architecture
- [ ] T034 Perform final integration test across both backend directories
- [ ] T035 Verify success criteria are met: 100% single assistant processing, all MCP tools accessible, etc.