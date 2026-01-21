# Research: Single Assistant Conversational + CRUD Behavior

## Decision: Unified Assistant Implementation
**Rationale**: Consolidate multiple assistant implementations into a single, unified assistant that handles both conversational responses and task CRUD operations based on intent detection.

## Current Architecture Analysis
- Two separate backend deployments (Vercel and Hugging Face)
- Existing conversation endpoint at `/api/conversation/clarify`
- Current assistant only handles task creation, ignores other CRUD operations
- Current assistant doesn't respond to conversational messages
- Need to implement intent detection to differentiate between conversation and task requests

## Intent Detection Strategy
**Decision**: Use a combination of keyword detection and pattern matching to identify user intent
**Rationale**: Simple and effective approach that doesn't require complex ML models
**Alternatives considered**:
- Full NLP classification model: Overkill for this use case
- Rule-based system: Chosen approach provides good balance of simplicity and effectiveness

## State Management Approach
**Decision**: Stateless design where conversation history is loaded from database for each request
**Rationale**: Follows the "Stateless Rule" from specifications and ensures scalability
**Alternatives considered**:
- In-memory state: Violates specifications and creates scaling issues
- Session-based state: More complex without clear benefits over DB approach

## MCP Tool Integration
**Decision**: Call MCP tools only when intent detection identifies task-related requests
**Rationale**: Follows "Tool Usage Rule" from specifications and prevents silent tool usage
**Implementation**: After MCP tool execution, generate confirmation text response as required

## Response Handling
**Decision**: Ensure every user message receives a text response
**Rationale**: Follows "Every user message MUST produce a text reply" requirement from specifications
**Implementation**: For task operations, return confirmation text; for conversation, return appropriate response