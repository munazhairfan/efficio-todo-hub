# Tasks: Backend UI Alignment

**Feature**: Backend UI Alignment
**Branch**: `003-ui-backend-alignment`
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Summary

This document lists all tasks required to restructure the backend of the todo app to align with the existing UI folder organization, while maintaining all existing functionality.

## Dependencies

User stories dependency graph:
- US1 (P1) - Access UI and perform todo operations - Depends on foundational backend restructuring
- US2 (P2) - Backend services remain compatible - Depends on US1
- US3 (P3) - Backend code structure follows UI conventions - Depends on US1 and US2

## Implementation Strategy

**MVP Scope**: Complete foundational backend restructuring (Phase 1-2) and US1 (core todo functionality) to enable basic UI-backend integration.

**Incremental Delivery**: Each user story represents a complete, independently testable increment.

## Phase 1: Setup

**Goal**: Prepare environment for backend restructuring

- [ ] T001 Set up development environment with Python 3.11
- [ ] T002 Verify PostgreSQL database connection
- [ ] T003 Configure environment variables (DATABASE_URL, BETTER_AUTH_SECRET)

## Phase 2: Foundational

**Goal**: Restructure core backend architecture to match UI organization patterns

- [ ] T004 Create new backend directory structure per implementation plan
- [ ] T005 [P] Move models to models/ directory (user.py, todo.py, base.py)
- [ ] T006 [P] Move API routes to api/ directory (auth/, todos/, users/)
- [ ] T007 [P] Create services layer (auth_service.py, todo_service.py)
- [ ] T008 [P] Create core modules (auth/, security/, config/)
- [ ] T009 [P] Move utilities to utils/ directory
- [ ] T010 [P] Move dependencies to dependencies/ directory
- [ ] T011 Update main.py to use new import paths
- [ ] T012 Update all import statements to reflect new structure
- [ ] T013 Add inline comments linking backend endpoints to UI components/pages

## Phase 3: [US1] Access UI and Perform Todo Operations

**Goal**: Enable users to access the UI and perform all todo operations with full authentication support

**Independent Test Criteria**: User can sign up/sign in, create todos, view todos, update todos, and delete todos with all functionality working seamlessly with the backend

**Acceptance**:
1. Given user has access to the UI, when user signs up/signs in and performs todo operations, then all operations complete successfully with data persisted in the backend
2. Given user is authenticated, when user interacts with any UI component that requires backend data, then the data is properly retrieved from and stored to the backend

- [ ] T014 [P] [US1] Implement auth service functions in services/auth_service.py
- [ ] T015 [P] [US1] Implement todo service functions in services/todo_service.py
- [ ] T016 [P] [US1] Update auth endpoints to use service layer (api/auth/handlers.py)
- [ ] T017 [P] [US1] Update todo endpoints to use service layer (api/todos/handlers.py)
- [ ] T018 [US1] Add mapping comments between auth endpoints and UI auth components
- [ ] T019 [US1] Add mapping comments between todo endpoints and UI todo components
- [ ] T020 [US1] Test complete authentication flow (signup, signin, verify)
- [ ] T021 [US1] Test complete todo CRUD operations
- [ ] T022 [US1] Validate API response formats match UI data requirements

## Phase 4: [US2] Backend Services Remain Compatible

**Goal**: Ensure all existing backend services remain fully functional and compatible with the new UI structure

**Independent Test Criteria**: All existing API endpoints continue to function as expected, existing authentication mechanisms work, and data models remain consistent

**Acceptance**:
1. Given existing API endpoints, when requests are made to them, then they return expected responses without errors
2. Given existing authentication flow, when users authenticate, then the process works exactly as before

- [ ] T023 [P] [US2] Verify all auth endpoints maintain backward compatibility
- [ ] T024 [P] [US2] Verify all todo endpoints maintain backward compatibility
- [ ] T025 [US2] Test existing API endpoints with current frontend
- [ ] T026 [US2] Validate JWT token format remains unchanged
- [ ] T027 [US2] Verify database models remain unchanged
- [ ] T028 [US2] Test existing authentication flow with current frontend
- [ ] T029 [US2] Confirm no breaking changes to API response schemas

## Phase 5: [US3] Backend Code Structure Follows UI Conventions

**Goal**: Organize backend folder structure, naming conventions, and modularity to follow the style of the UI folder

**Independent Test Criteria**: Backend code follows similar organizational patterns as the UI code, with clear separation of concerns and consistent naming conventions

**Acceptance**:
1. Given backend code structure, when examining the organization, then it follows patterns similar to the UI folder structure
2. Given backend modules, when reviewing naming conventions, then they align with the style used in the UI components

- [ ] T030 [P] [US3] Organize backend modules by feature similar to UI components
- [ ] T031 [P] [US3] Apply consistent naming conventions across backend modules
- [ ] T032 [US3] Refactor code for better modularity following UI patterns
- [ ] T033 [US3] Ensure service layer follows UI component architecture patterns
- [ ] T034 [US3] Review and update code documentation to match new structure
- [ ] T035 [US3] Verify folder organization matches UI patterns (80% consistency target)

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Finalize implementation and ensure all requirements are met

- [ ] T036 Add comprehensive inline comments mapping backend to UI components
- [ ] T037 Update README with new backend structure documentation
- [ ] T038 Perform final compatibility testing with existing frontend
- [ ] T039 Verify all edge cases from spec are handled properly
- [ ] T040 Conduct final review of code structure alignment with UI patterns
- [ ] T041 Run complete test suite to ensure no regressions
- [ ] T042 Document any breaking changes (should be none)
- [ ] T043 Prepare migration guide for team members

## Parallel Execution Examples

**US1 Parallel Tasks**: T014-T017 can be executed in parallel by different developers
**US2 Parallel Tasks**: T023-T024 can be executed in parallel for different endpoint types
**US3 Parallel Tasks**: T030-T033 can be executed in parallel by refactoring different modules