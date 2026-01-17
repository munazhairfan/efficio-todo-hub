# Data Model: Single Assistant Architecture

## Overview
The single assistant architecture maintains the existing data model with no changes. The architecture change is purely in the AI processing layer, not in the underlying data structures.

## Entities

### Task
- **Fields**:
  - id (integer): Unique identifier
  - user_id (integer): Owner of the task
  - title (string): Task title
  - description (string, nullable): Task description
  - completed (boolean): Completion status
  - created_at (datetime): Creation timestamp
  - updated_at (datetime): Last update timestamp

### Conversation
- **Fields**:
  - id (integer): Unique identifier
  - user_id (integer): Owner of the conversation
  - title (string): Conversation title
  - created_at (datetime): Creation timestamp
  - updated_at (datetime): Last update timestamp

### Message
- **Fields**:
  - id (integer): Unique identifier
  - conversation_id (integer): Associated conversation
  - user_id (integer): Author of the message
  - role (string): Role of the sender (user/assistant)
  - content (string): Message content
  - created_at (datetime): Creation timestamp

## Relationships
- User has many Conversations
- Conversation has many Messages
- User has many Tasks

## Validation Rules
- Task title must not be empty
- Task user_id must reference an existing user
- Message role must be either 'user' or 'assistant'
- Conversation user_id must reference the message author

## State Transitions
- Task: pending → completed (when marked complete)
- Message: created → persisted (after database storage)