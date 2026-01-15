# Data Model: Conversation Robustness

## Entities

### ConversationState
Represents the current context of the user interaction, including pending clarifications and user intent

- **id**: Unique identifier for the conversation state
- **sessionId**: Session identifier linking to user session
- **currentIntent**: Current user intent or pending clarification request
- **pendingClarifications**: List of clarifying questions awaiting user response
- **contextData**: Additional contextual information for the conversation
- **createdAt**: Timestamp when conversation state was created
- **updatedAt**: Timestamp when conversation state was last updated
- **expiresAt**: Expiration timestamp for cleanup

### ErrorContext
Information about failures that occurred, including type and suggested remediation paths

- **id**: Unique identifier for the error context
- **errorType**: Category of error (user_input, system_failure, network_issue, etc.)
- **originalRequest**: The original request that caused the error
- **errorMessage**: User-friendly error message
- **suggestedActions**: List of suggested alternative actions for the user
- **timestamp**: When the error occurred
- **handled**: Boolean indicating if error was properly handled

## Validation Rules

### ConversationState Validation
- sessionId must be valid and active
- currentIntent must be non-empty when not in clarification state
- pendingClarifications length must be reasonable (< 10 items)
- expiresAt must be in the future

### ErrorContext Validation
- errorType must be one of predefined error categories
- errorMessage must be user-friendly (no technical details)
- suggestedActions must contain actionable alternatives

## State Transitions

### ConversationState Transitions
- `ACTIVE` → `AWAITING_CLARIFICATION`: When ambiguous input detected
- `AWAITING_CLARIFICATION` → `ACTIVE`: When user provides clarification
- `ACTIVE` → `COMPLETED`: When task is completed
- Any state → `EXPIRED`: When expiration time reached

### ErrorContext Transitions
- `DETECTED` → `HANDLED`: When error is properly processed and user notified
- `DETECTED` → `ESCALATED`: When error requires special handling