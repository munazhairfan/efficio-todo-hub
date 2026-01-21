# Implementation Plan: Single Assistant Conversational + CRUD Behavior

**Branch**: `001-single-assistant-behavior` | **Date**: 2026-01-21 | **Spec**: [link]
**Input**: Feature specification from `/specs/001-single-assistant-behavior/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a single unified assistant that handles both conversational responses and task CRUD operations. The assistant will detect user intent (conversational vs task-related) and respond appropriately, ensuring every user message produces a text response. The solution will replace any current multi-assistant architecture with a single, stateless assistant implementation.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, uvicorn
**Storage**: PostgreSQL (via SQLModel/SQLAlchemy)
**Testing**: pytest
**Target Platform**: Linux server (Vercel/Hugging Face deployment)
**Project Type**: web (backend API)
**Performance Goals**: <3 seconds response time per request
**Constraints**: Stateless operation (no in-memory state between requests), 100% response rate to user messages
**Scale/Scope**: Single assistant serving multiple users simultaneously

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No constitution file found in .specify/memory/constitution.md, skipping constitution check.

## Project Structure

### Documentation (this feature)

```text
specs/001-single-assistant-behavior/
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
├── src/
│   ├── main.py
│   ├── api/
│   │   ├── routes/
│   │   │   └── conversation.py
│   │   └── models/
│   ├── services/
│   │   └── conversation_service.py
│   ├── middleware/
│   │   └── rate_limiter.py
│   ├── utils/
│   │   ├── intent_detector.py
│   │   ├── question_generator.py
│   │   └── ambiguous_pattern_matcher.py
│   ├── models/
│   └── core/
├── api/
│   └── routes/
│       └── conversation.py
├── services/
├── utils/
├── database.py
└── server.py

efficio-todo-hub-backend/
├── main.py
├── api/
│   └── routes/
│       └── conversation.py
├── services/
├── utils/
├── database.py
└── src/
    ├── main.py
    ├── api/
    │   └── routes/
    │       └── conversation.py
    ├── services/
    ├── middleware/
    └── utils/
```

**Structure Decision**: Using existing backend structure with modifications to conversation route to implement single assistant behavior. Two deployments exist: Vercel backend (in /backend directory) and Hugging Face backend (in /efficio-todo-hub-backend directory). Both will be updated with consistent changes.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
