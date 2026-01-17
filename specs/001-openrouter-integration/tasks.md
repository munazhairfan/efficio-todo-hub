# Implementation Tasks: OpenRouter AI Integration

**Feature**: 001-openrouter-integration | **Date**: 2026-01-16 | **Spec**: specs/001-openrouter-integration/spec.md

## Dependencies

User stories can be implemented in parallel since they are focused on different aspects of the same integration:
- US1 (Send Message to AI Chatbot) and US2 (Secure API Key Handling) can be developed together
- US3 (Graceful Failure Handling) can be implemented after the core functionality

## Parallel Execution Examples

**Example 1**: While implementing the OpenRouter client function, another developer can work on updating the chat endpoint integration.
**Example 2**: While implementing error handling, another developer can work on testing the integration.

## Implementation Strategy

**MVP First**: Start with basic OpenRouter integration (T001-T007) to get the core functionality working, then add error handling and security enhancements.

**Incremental Delivery**:
- Phase 1: Basic OpenRouter client and integration
- Phase 2: Security and error handling
- Phase 3: Testing and verification

---

## Phase 1: Setup

- [X] T001 Create directory for OpenRouter service at backend/src/services/openrouter_client.py
- [X] T002 Install httpx dependency for HTTP requests to OpenRouter API

## Phase 2: Foundational Components

- [X] T003 [P] Update backend/src/core/config.py to include OPENROUTER_API_KEY environment variable access
- [X] T004 [P] Create basic OpenRouter client function skeleton in backend/src/services/openrouter_client.py

## Phase 3: User Story 1 - Send Message to AI Chatbot (Priority: P1)

**Goal**: User sends a message to the chatbot and receives an intelligent response from the OpenRouter AI service.

**Independent Test Criteria**: Can be fully tested by sending a message to the chat endpoint and verifying that a response from OpenRouter is returned, delivering the core AI interaction capability.

- [X] T005 [P] [US1] Implement call_openrouter function in backend/src/services/openrouter_client.py with proper headers and endpoint
- [X] T006 [P] [US1] Configure OpenRouter payload structure with model selection and message formatting in backend/src/services/openrouter_client.py
- [X] T007 [P] [US1] Implement response parsing to extract assistant text safely in backend/src/services/openrouter_client.py
- [X] T008 [P] [US1] Integrate OpenRouter client with chat endpoint in backend/src/api/chat.py to replace mock responses
- [X] T009 [US1] Update chat endpoint to format conversation history for OpenRouter in backend/src/api/chat.py

## Phase 4: User Story 2 - Secure API Key Handling (Priority: P1)

**Goal**: The system securely accesses the OpenRouter API key from environment variables without exposing it in code or logs.

**Independent Test Criteria**: Can be tested by verifying that the API key is read from environment variables and not hardcoded in the code, ensuring secure configuration management.

- [X] T010 [P] [US2] Ensure OPENROUTER_API_KEY is read using os.getenv without defaults in backend/src/services/openrouter_client.py
- [X] T011 [P] [US2] Add security checks to prevent logging of API key values in backend/src/services/openrouter_client.py
- [X] T012 [US2] Validate that no API key values are exposed in error messages in backend/src/services/openrouter_client.py

## Phase 5: User Story 3 - Graceful Failure Handling (Priority: P2)

**Goal**: When the OpenRouter service is unavailable, the system handles the failure gracefully without crashing.

**Independent Test Criteria**: Can be tested by simulating OpenRouter unavailability and verifying that the application handles the error without crashing.

- [X] T013 [P] [US3] Implement error handling for request exceptions in backend/src/services/openrouter_client.py
- [X] T014 [P] [US3] Return controlled fallback message when OpenRouter is unavailable in backend/src/services/openrouter_client.py
- [X] T015 [P] [US3] Add timeout handling to prevent hanging requests in backend/src/services/openrouter_client.py
- [X] T016 [US3] Ensure unhandled exceptions are caught and converted to safe responses in backend/src/services/openrouter_client.py

## Phase 6: Integration and Verification

- [X] T017 Update the task management agent to optionally use OpenRouter instead of or alongside MCP tools in backend/src/agents/task_management_agent.py
- [X] T018 Configure model selection and temperature parameters appropriately in backend/src/services/openrouter_client.py
- [X] T019 Test that intent detection and MCP tools remain untouched in backend/src/agents/task_management_agent.py

## Phase 7: Verification and Polish

- [X] T020 Start server locally and send test chat request to verify AI response is real
- [X] T021 Verify that the application handles OpenRouter timeouts without crashing the server
- [X] T022 Test that 95% of chat interactions successfully return AI responses when OpenRouter is available
- [X] T023 Confirm zero API keys are exposed in application logs or error messages
- [X] T024 Verify users receive AI-generated responses within 10 seconds of sending a message