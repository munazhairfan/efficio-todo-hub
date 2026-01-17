# Research: Single Assistant Architecture

## Decision: Use OpenRouter AI as Single Assistant
**Rationale**: OpenRouter provides advanced AI capabilities and supports tool calling natively, making it ideal for the single assistant role
**Alternatives considered**:
- Keeping local agent as primary (rejected - less capable)
- Creating hybrid system (rejected - violates single assistant constraint)

## Decision: Enhance OpenRouter Client with Tool Execution Capability
**Rationale**: Allows AI to intelligently decide when to call tools based on user intent
**Alternatives considered**:
- Pre-processing user input for intent (rejected - moves intelligence away from AI)

## Technical Approach
The implementation will:
1. Remove all references to the local task management agent
2. Enhance the OpenRouter client to handle tool calls from AI responses
3. Enable the AI to execute MCP tools when appropriate
4. Maintain all existing functionality while consolidating to one assistant

## Tool Calling Flow
1. AI analyzes user message and decides to call a tool
2. AI sends tool call request to the system
3. System executes the appropriate MCP tool
4. Tool results are sent back to AI
5. AI generates final response for user

This approach maintains the AI's ability to make intelligent decisions about when to use tools while ensuring only one assistant is involved in the process.