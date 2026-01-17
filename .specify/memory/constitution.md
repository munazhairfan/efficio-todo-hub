# Project Constitution

## Core Principles

1. **Single Assistant Architecture**: The system must use exactly one assistant for all AI processing. No fallback agents, secondary agents, or parallel assistants are allowed.

2. **MCP Tool Separation**: MCP tools must remain as simple executable functions, not assistants or agents themselves.

3. **User-Centric Design**: All features should prioritize user experience and value delivery.

4. **Clean Architecture**: Clear separation of concerns between AI processing, tool execution, and data management.

## Architecture Constraints

- No multiple assistants in any code path
- No agent selection or routing logic
- MCP tools must not contain reasoning or AI capabilities
- Single assistant must handle all user interactions
