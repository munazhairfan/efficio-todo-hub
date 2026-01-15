# Implementation Plan: Authentication Guard for Chat Endpoint

**Branch**: `001-chat-auth-guard` | **Date**: 2026-01-13 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/001-chat-auth-guard/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement authentication guard for the chat endpoint by validating Authorization headers with Bearer tokens. The system will extract and validate tokens using existing authentication utilities, compare the token user_id with the URL user_id, and return appropriate HTTP errors (401/403) for invalid requests. This ensures only authenticated users can access their own conversations while preserving existing chat functionality.

## Technical Context

**Language/Version**: TypeScript (Frontend), Python 3.11 (Backend)
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, Better Auth, Next.js 14
**Storage**: PostgreSQL for backend data, browser storage for frontend state
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (Next.js frontend with FastAPI backend)
**Project Type**: Web application (monorepo with frontend/backend)
**Performance Goals**: Sub-millisecond authentication validation overhead
**Constraints**: Must reuse existing auth validation logic, must not modify existing chat behavior
**Scale/Scope**: Individual user conversations with authentication guard

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Clean Code and Pythonic Design**: ✓ Will follow clean code principles in both TypeScript and Python implementations
- **Console-Based Interface**: ❌ NOT APPLICABLE - This is a web application, not console-based (ADAPTED)
- **In-Memory Data Persistence**: ❌ NOT APPLICABLE - Using PostgreSQL database, not in-memory storage
- **Complete CRUD Functionality**: ✓ Will maintain existing functionality while adding auth guard
- **Modularity and Separation of Concerns**: ✓ Will maintain separation between auth logic and chat functionality
- **Error Handling and Validation**: ✓ Core requirement for authentication validation
- **External Dependencies**: ⚠ Using FastAPI, SQLModel, and other dependencies as per existing architecture

*Note: The original constitution was written for a console-based in-memory application, while this project is a web application with database persistence. Some principles need adaptation for the current architecture.*

## Project Structure

### Documentation (this feature)
```text
specs/001-chat-auth-guard/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── main.py                 # FastAPI application entry point
├── api/
│   ├── routes/
│   │   ├── chat.py        # Chat endpoint with auth guard (MODIFIED)
│   │   ├── todos.py       # Todo-related endpoints
│   │   └── auth.py        # Authentication endpoints
│   └── models/
│       ├── todo.py        # Todo model definitions
│       ├── user.py        # User model definitions
│       └── conversation.py # Conversation model definitions
├── services/
│   ├── todo_service.py    # Todo business logic
│   ├── auth_service.py    # Authentication business logic
│   └── conversation_service.py # Conversation business logic
└── tests/
    ├── test_chat.py       # Chat functionality tests (UPDATED)
    ├── test_auth.py       # Authentication tests
    └── test_todos.py      # Todo functionality tests

frontend/
├── app/
│   ├── page.tsx           # Main page component
│   ├── layout.tsx         # Layout component
│   ├── dashboard/
│   │   └── page.tsx       # Dashboard page with chat integration
│   └── auth/
│       └── page.tsx       # Authentication page
├── components/
│   ├── TodoList.tsx       # Todo list component
│   ├── TodoItem.tsx       # Individual todo component
│   ├── AuthForm.tsx       # Authentication form component
│   └── ChatInterface.tsx  # Chat interface component
├── lib/
│   └── api.ts             # API client functions (with auth methods)
└── tests/
    ├── components/
    ├── pages/
    └── services/
```

**Structure Decision**: Web application structure selected as this is a monorepo with Next.js frontend and FastAPI backend. The authentication guard will be implemented in the backend chat endpoint while preserving all existing functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Web Application vs Console | Project evolved from console to web app | Business requirements changed to support web interface |
| Database Persistence vs In-Memory | Production requirements need data persistence | In-memory storage insufficient for real-world usage |