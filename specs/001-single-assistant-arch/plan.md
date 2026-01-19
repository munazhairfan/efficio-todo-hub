# Implementation Plan: Single Assistant Architecture

**Branch**: `001-single-assistant-arch` | **Date**: 2026-01-18 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/001-single-assistant-arch/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement single assistant architecture constraint by consolidating all AI processing through the Task Management Agent. Remove duplicate assistant systems and ensure all user interactions (both general chat and task-specific commands) flow through exactly one assistant endpoint. MCP tools remain as simple executable functions while manual UI task operations continue to function independently.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript (Node.js)
**Primary Dependencies**: FastAPI, SQLModel, PostgreSQL, OpenRouter API, Next.js, Tailwind CSS
**Storage**: PostgreSQL (Neon) database with real persistence
**Testing**: pytest, Jest
**Target Platform**: Web application (Linux server)
**Project Type**: Full-stack web application (backend/frontend monorepo)
**Performance Goals**: Real-time chat responses under 2 seconds, task operations under 1 second
**Constraints**: Must maintain single assistant architecture, MCP tools remain as simple functions, manual UI operations work independently

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

✓ **Single Assistant Architecture**: Plan ensures exactly one assistant handles all AI processing by consolidating the Task Management Agent as the central AI processor for both task-specific and general chat operations.

✓ **MCP Tool Separation**: MCP tools remain as simple executable functions, not assistants or agents themselves. The single assistant may call them but they maintain their simplicity.

✓ **No Multiple Assistants**: The implementation will eliminate duplicate assistant systems by routing all user interactions through the Task Management Agent.

✓ **No Agent Selection/Routing**: All requests will follow a single code path through the unified assistant, eliminating any agent selection or routing logic.

✓ **Clean Architecture**: Clear separation maintained between AI processing (single assistant), MCP tool execution (simple functions), and data management.

## Project Structure

### Documentation (this feature)

```text
specs/001-single-assistant-arch/
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
│   ├── agents/
│   │   └── task_management_agent.py      # Single assistant (to be enhanced)
│   ├── api/
│   │   ├── chat.py                       # Chat endpoint (to be updated)
│   │   └── routes/
│   │       └── conversation.py           # Conversation API (to be redirected)
│   ├── models/
│   ├── services/
│   ├── mcp_tools.py                      # MCP tools (remain as simple functions)
│   └── main.py
└── tests/

frontend/
├── app/
│   └── dashboard/
│       └── page.tsx                      # Dashboard with dual assistants (to be simplified)
├── components/
│   └── ChatInterface.tsx                 # Chat interface (to be unified)
├── services/
│   └── chatService.ts                    # Chat service (to be updated)
└── lib/
    └── api.ts                            # API client (to be updated)
```

**Structure Decision**: Web application with backend/frontend monorepo. The single assistant will be implemented by enhancing the existing Task Management Agent and updating the chat API to route all requests through it.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
