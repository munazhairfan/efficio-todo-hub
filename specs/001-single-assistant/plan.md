# Implementation Plan: Single Assistant Architecture

## Technical Context

**Project Overview**: A chatbot-based todo management system that currently has multiple assistants (OpenRouter AI and Local Task Management Agent) that need to be consolidated into a single assistant.

**Current Architecture**:
- OpenRouter AI Assistant: Primary AI that connects to external OpenRouter API for advanced AI capabilities
- Local Task Management Agent: Pattern-matching based agent for fallback and task operations
- Both assistants can call the same MCP tools for actual task operations

**Target Architecture**:
- Single assistant that handles all AI processing
- Assistant will use OpenRouter API for AI capabilities
- Assistant will have full MCP tool schemas to enable AI-driven tool calling
- No fallback or secondary agents

**Files to Modify**:
- `backend/src/api/chat.py` - Main chat endpoint
- `backend/src/services/openrouter_client.py` - OpenRouter API client
- `efficio-todo-hub-backend/src/api/chat.py` - Duplicate backend chat endpoint
- `efficio-todo-hub-backend/src/services/openrouter_client.py` - Duplicate backend OpenRouter client

**Technologies Used**:
- Python FastAPI backend
- OpenRouter API for AI capabilities
- MCP tools for task operations
- SQLModel/SQLAlchemy for database operations

## Constitution Check

- ✅ **One Assistant Only**: The plan ensures exactly one assistant handles all requests
- ✅ **No Fallback Agents**: Removes all fallback or secondary agents
- ✅ **MCP Tools Remain Simple**: MCP tools stay as executable functions, not assistants
- ✅ **Single Pipeline**: All user messages go through one assistant pipeline

## Gates

- ✅ **Architecture Alignment**: Plan aligns with single-assistant requirement
- ✅ **No Violations**: No multiple assistants, fallbacks, or parallel processing
- ✅ **Functionality Preservation**: All existing functionality maintained

## Phase 0: Research

### Research Findings

**Decision**: Use OpenRouter AI as the single assistant with enhanced tool calling capabilities
**Rationale**: OpenRouter provides advanced AI capabilities and supports tool calling natively, making it ideal for the single assistant role
**Alternatives considered**:
- Keeping local agent as primary (rejected - less capable)
- Creating hybrid system (rejected - violates single assistant constraint)

**Decision**: Enhance OpenRouter client with tool execution capability
**Rationale**: Allows AI to intelligently decide when to call tools based on user intent
**Alternatives considered**:
- Pre-processing user input for intent (rejected - moves intelligence away from AI)

## Phase 1: Design

### Data Model
*(No significant changes needed - using existing task data model)*

### API Contracts
*(No changes needed - keeping existing chat endpoint contract)*

### Implementation Steps

1. **Remove Local Agent Dependency**
   - Update imports in chat endpoints
   - Remove fallback logic to local agent

2. **Enhance MCP Tool Schemas**
   - Add complete tool schemas to OpenRouter client
   - Enable AI to call tools when appropriate

3. **Implement Tool Execution**
   - Add tool execution logic to OpenRouter client
   - Handle multi-turn conversations for tool results

4. **Update Both Backend Directories**
   - Apply changes to main backend
   - Apply changes to duplicate backend

5. **Testing and Validation**
   - Verify single assistant handles all cases
   - Confirm all MCP tools work correctly

## Phase 2: Implementation Strategy

### Step 1: Update Chat Endpoints
- Remove import of local agent
- Remove fallback logic
- Add MCP tool schemas to OpenRouter call

### Step 2: Enhance OpenRouter Client
- Add tool calling detection
- Add tool execution capability
- Add multi-turn conversation handling

### Step 3: Synchronize Both Backends
- Apply same changes to both backend directories
- Ensure consistency

### Step 4: Validation
- Test all task operations work
- Confirm single assistant handles all requests