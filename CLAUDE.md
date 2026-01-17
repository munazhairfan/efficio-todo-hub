# Todo App - Hackathon II
 
## Project Overview
This is a monorepo using GitHub Spec-Kit for spec-driven development.
 
## Spec-Kit Structure
Specifications are organized in /specs:
- /specs/overview.md - Project overview
- /specs/features/ - Feature specs (what to build)
- /specs/api/ - API endpoint and MCP tool specs
- /specs/database/ - Schema and model specs
- /specs/ui/ - Component and page specs
 
## How to Use Specs
1. Always read relevant spec before implementing
2. Reference specs with: @specs/features/task-crud.md
3. Update specs if requirements change
 
## Project Structure
- /frontend - Next.js 14 app
- /backend - Python FastAPI server
 
## Development Workflow
1. Read spec: @specs/features/[feature].md
2. Implement backend: @backend/CLAUDE.md
3. Implement frontend: @frontend/CLAUDE.md
4. Test and iterate
 
## Commands
- Frontend: cd frontend && npm run dev
- Backend: cd backend && uvicorn main:app --reload
- Both: docker-compose up

## Active Technologies
- TypeScript (Frontend), Python 3.11 (Backend) + Better Auth (Frontend), FastAPI, SQLModel, PyJWT (Backend) (002-user-auth)
- Neon PostgreSQL database for user data (002-user-auth)
- Python 3.11 + FastAPI, uvicorn, pydantic, python-multipart, psycopg2-binary, sqlmodel, sqlalchemy (001-hf-deployment-hardening)
- PostgreSQL (Neon) via environment variables (001-hf-deployment-hardening)
- Python 3.11 + FastAPI, SQLModel, Alembic, httpx, pydantic, OpenRouter API (001-openrouter-integration)
- Python 3.11, TypeScript/JavaScript (Node.js) + FastAPI, SQLModel, PostgreSQL, OpenRouter API, Next.js, Jest, pytest (001-testing-validation)
- PostgreSQL (Neon) database with real persistence (001-testing-validation)

## Recent Changes
- 002-user-auth: Added TypeScript (Frontend), Python 3.11 (Backend) + Better Auth (Frontend), FastAPI, SQLModel, PyJWT (Backend)
