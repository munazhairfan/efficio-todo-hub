# Task List: Todo In-Memory Python Console App

## Feature Overview
Implement a console-based Todo application in Python that supports all basic CRUD operations and marking tasks complete. The project emphasizes clean code principles and proper Python project structure with in-memory task storage.

---

## Phase 1: Project Setup

- [ ] T001 Create project directory structure (src/, tests/, docs/)
- [ ] T002 Initialize Python project with requirements.txt
- [ ] T003 Create initial .gitignore file for Python project

---

## Phase 2: Foundational Components

- [ ] T004 [P] Create Task dataclass in src/models.py with id, title, description, completed fields
- [ ] T005 [P] Create TaskList class in src/models.py for in-memory storage
- [ ] T006 [P] Implement utility functions for ID generation in src/utils.py
- [ ] T007 [P] Create formatting functions for console display in src/utils.py

---

## Phase 3: User Story 1 - Add New Task (Priority: P1)

**Story Goal**: Enable users to create new tasks with title and description, storing them in memory with unique ID and default incomplete status.

**Independent Test**: Can be fully tested by running the add task function and verifying a new task appears in the system with a unique ID and "Incomplete" status.

### Implementation Tasks:

- [ ] T008 [P] [US1] Implement add_task function in src/todo.py with title/description validation
- [ ] T009 [P] [US1] Add unique ID assignment to new tasks in src/todo.py
- [ ] T010 [P] [US1] Set default "Incomplete" status for new tasks in src/todo.py
- [ ] T011 [US1] Create CLI function for adding tasks in src/cli.py
- [ ] T012 [US1] Add user prompts for title and description in CLI
- [ ] T013 [US1] Display confirmation message after successful task creation
- [ ] T014 [US1] Handle validation errors for empty titles in CLI

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Story Goal**: Allow users to see all tasks with their details (ID, title, description) and completion status in a clear format.

**Independent Test**: Can be fully tested by adding tasks and then viewing the list. Delivers value by allowing users to see their tasks.

### Implementation Tasks:

- [ ] T015 [P] [US2] Implement get_all_tasks function in src/todo.py
- [ ] T016 [P] [US2] Implement list_tasks function in src/todo.py with proper formatting
- [ ] T017 [P] [US2] Create task display formatting in src/utils.py for console output
- [ ] T018 [US2] Create CLI function for viewing tasks in src/cli.py
- [ ] T019 [US2] Display appropriate message when no tasks exist
- [ ] T020 [US2] Format task output with clear status indicators in console
- [ ] T021 [US2] Handle edge case of empty task list

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Story Goal**: Allow users to update the status of tasks by toggling between complete/incomplete states with confirmation.

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete and verifying the status changes.

### Implementation Tasks:

- [ ] T022 [P] [US3] Implement toggle_complete function in src/todo.py
- [ ] T023 [P] [US3] Add mark_complete and mark_incomplete functions in src/todo.py
- [ ] T024 [P] [US3] Validate task ID exists before toggling status in src/todo.py
- [ ] T025 [US3] Create CLI function for toggling task status in src/cli.py
- [ ] T026 [US3] Add user prompts for task ID input in CLI
- [ ] T027 [US3] Display confirmation message after status change
- [ ] T028 [US3] Handle validation errors for invalid task IDs

---

## Phase 6: User Story 4 - Update Task Details (Priority: P2)

**Story Goal**: Allow users to modify the title or description of existing tasks by ID with confirmation.

**Independent Test**: Can be fully tested by updating task details and verifying changes persist.

### Implementation Tasks:

- [ ] T029 [P] [US4] Implement update_task function in src/todo.py
- [ ] T030 [P] [US4] Add validation for task ID existence in src/todo.py
- [ ] T031 [P] [US4] Allow updating title and/or description fields in src/todo.py
- [ ] T032 [US4] Create CLI function for updating tasks in src/cli.py
- [ ] T033 [US4] Add user prompts for task ID and new details in CLI
- [ ] T034 [US4] Display confirmation message after successful update
- [ ] T035 [US4] Handle validation errors for invalid task IDs

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Story Goal**: Allow users to remove tasks from the system by ID with confirmation.

**Independent Test**: Can be fully tested by deleting tasks and verifying they no longer appear in the list.

### Implementation Tasks:

- [ ] T036 [P] [US5] Implement delete_task function in src/todo.py
- [ ] T037 [P] [US5] Add validation for task ID existence in src/todo.py
- [ ] T038 [P] [US5] Remove task from in-memory storage in src/todo.py
- [ ] T039 [US5] Create CLI function for deleting tasks in src/cli.py
- [ ] T040 [US5] Add user prompts for task ID input in CLI
- [ ] T041 [US5] Display confirmation message after successful deletion
- [ ] T042 [US5] Handle validation errors for invalid task IDs

---

## Phase 8: CLI Integration and Main Application

- [ ] T043 Create main menu loop in src/main.py with all options
- [ ] T044 Connect all CLI functions to main menu options
- [ ] T045 Implement proper exit functionality
- [ ] T046 Add error handling for user input in CLI
- [ ] T047 Create clear menu display with numbered options

---

## Phase 9: Unit Testing

- [ ] T048 [P] Create test suite for Task model in tests/test_models.py
- [ ] T049 [P] Create test suite for task management functions in tests/test_todo.py
- [ ] T050 [P] Create test suite for CLI functions in tests/test_cli.py
- [ ] T051 Add tests for all edge cases and validation scenarios
- [ ] T052 Test all user stories with acceptance scenarios

---

## Phase 10: Polish & Cross-Cutting Concerns

- [X] T053 Refactor code for clean code principles and single responsibility
- [X] T054 Add proper error handling throughout the application
- [X] T055 Review and optimize console output formatting
- [X] T056 Create usage documentation in docs/usage.md
- [X] T057 Perform final integration testing of all features
- [X] T058 Verify all success criteria from specification are met

---

## Dependencies

- User Story 2 (View Tasks) depends on User Story 1 (Add Task) being partially complete to have tasks to view
- User Stories 3-5 (Mark/Update/Delete) depend on User Story 1 (Add Task) to have tasks to operate on

## Parallel Execution Examples

- **US1 Tasks**: T008-T010 can be developed in parallel with US2 tasks T015-T017
- **US3-US5 Tasks**: All operation functions (toggle, update, delete) can be developed in parallel after foundational components are complete
- **Testing**: All test files can be developed in parallel with their corresponding implementation files

## Implementation Strategy

1. **MVP Scope**: Complete User Story 1 (Add Task) and User Story 2 (View Tasks) for minimum viable product
2. **Incremental Delivery**: Add one user story at a time, testing each increment
3. **Final Integration**: Complete CLI integration and end-to-end testing in Phase 8