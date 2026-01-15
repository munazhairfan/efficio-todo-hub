# Tasks: Chatbot Security & Rate Limiting

**Input**: Design documents from `/specs/001-chat-security/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create rate limiting and validation utility files structure in backend
- [X] T002 [P] Install any required dependencies for rate limiting (if needed beyond standard library)

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Create rate limiter middleware in backend/src/middleware/rate_limiter.py
- [X] T004 Create input validators in backend/src/utils/validators.py
- [X] T005 Setup thread-safe in-memory storage with locks for rate limiting
- [X] T006 Configure logging for security events without message content
- [X] T007 Define standardized error response format for security violations

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Send Valid Messages Within Rate Limits (Priority: P1) 🎯 MVP

**Goal**: Enable users to send messages to the chatbot within the rate limits, with the system processing their requests normally

**Independent Test**: Can be fully tested by sending messages within the 10-per-minute limit and verifying that responses are returned normally

### Implementation for User Story 1

- [X] T008 [US1] Integrate rate limiter middleware with chat endpoint in backend/src/api/routes/chat.py
- [X] T009 [US1] Implement token bucket algorithm with sliding window counter for rate limiting
- [X] T010 [US1] Set rate limit to 10 messages per minute per user_id
- [X] T011 [US1] Ensure rate limits reset automatically after 60 seconds
- [X] T012 [US1] Process valid messages (1-1000 characters) normally through the chat endpoint
- [X] T013 [US1] Add logging for successful message processing

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Handle Rate Limit Exceeded (Priority: P2)

**Goal**: Return a 429 error with a readable message when users exceed the rate limit of 10 messages per minute

**Independent Test**: Can be tested by sending more than 10 messages in one minute and verifying that HTTP 429 is returned with a readable error message

### Implementation for User Story 2

- [X] T014 [US2] Implement HTTP 429 status code return when rate limit is exceeded
- [X] T015 [US2] Create readable error message for rate limit exceeded scenario
- [X] T016 [US2] Ensure no internal system details are exposed in rate limit error responses
- [X] T017 [US2] Add logging for rate limit exceeded events (without message content)
- [X] T018 [US2] Verify rate limits reset after 60 seconds allowing new messages

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Validate Message Content (Priority: P3)

**Goal**: Reject invalid messages (empty or too long) with appropriate error messages

**Independent Test**: Can be tested by sending empty messages and messages over 1000 characters and verifying appropriate error responses

### Implementation for User Story 3

- [X] T019 [US3] Implement validation to reject empty messages
- [X] T020 [US3] Implement validation to reject messages longer than 1000 characters
- [X] T021 [US3] Return readable error messages for all validation failures
- [X] T022 [US3] Ensure no stack traces are exposed in validation error responses
- [X] T023 [US3] Add logging for validation failures (without message content)

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Validate User Identity (Priority: P4)

**Goal**: Validate that the user_id in the URL matches the authenticated user

**Independent Test**: Can be tested by making requests with mismatched user_ids and verifying they are rejected

### Implementation for User Story 4

- [X] T024 [US4] Implement validation that compares URL user_id with authenticated user
- [X] T025 [US4] Return appropriate error when user_id doesn't match authenticated user
- [X] T026 [US4] Allow requests when user_id matches authenticated user
- [X] T027 [US4] Add logging for user identity validation failures
- [X] T028 [US4] Ensure no internal system details are exposed in identity validation errors

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T029 [P] Add comprehensive error handling for edge cases in rate limiter
- [ ] T030 Handle concurrent requests from the same user safely with thread locks
- [ ] T031 Add configuration for rate limits via environment variables
- [ ] T032 [P] Add unit tests for rate limiting functionality in backend/tests/unit/test_rate_limiter.py
- [ ] T033 Add integration tests for chat security in backend/tests/integration/test_chat_security.py
- [ ] T034 Performance test to ensure <50ms rate limit check overhead
- [ ] T035 Update API client in frontend/lib/api.ts to handle security error responses appropriately
- [ ] T036 Add error feedback in frontend chat components to handle security errors gracefully

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 rate limiting foundation
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 validation foundation
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Builds on US1 identity validation foundation

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all foundational tasks together:
Task: "Create rate limiter middleware in backend/src/middleware/rate_limiter.py"
Task: "Create input validators in backend/src/utils/validators.py"
Task: "Setup thread-safe in-memory storage with locks for rate limiting"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence