# Quickstart: Single Assistant Architecture

## Overview
This guide explains how to implement the single assistant architecture by consolidating all AI processing through one unified assistant.

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database
- Understanding of the existing task management system

## Implementation Steps

### 1. Update Backend Components

#### Step 1.1: Enhance the Task Management Agent
The existing agent at `backend/src/agents/task_management_agent.py` needs to be enhanced to handle general chat conversations in addition to task-specific commands.

#### Step 1.2: Modify Chat API
Update `backend/src/api/chat.py` to route all messages through the Task Management Agent instead of OpenRouter directly.

#### Step 1.3: Redirect Conversation API
Update or deprecate the conversation API in `backend/api/routes/conversation.py` to redirect to the single assistant.

### 2. Update Frontend Components

#### Step 2.1: Consolidate Assistant Interfaces
Modify `frontend/app/dashboard/page.tsx` to remove the duplicate assistant interfaces and consolidate to a single unified experience.

#### Step 2.2: Update Chat Service
Update `frontend/services/chatService.ts` to work with the unified assistant API.

### 3. Testing and Validation

#### Step 3.1: Verify Single Assistant Path
Confirm that all user interactions flow through exactly one assistant endpoint.

#### Step 3.2: Test Task Operations
Verify that task-specific commands (add, list, complete, delete, update) continue to work.

#### Step 3.3: Test General Chat
Verify that general chat conversations work appropriately.

#### Step 3.4: Test Manual UI Operations
Confirm that manual task management through UI elements works independently of the assistant.

## Key Files to Modify
- `backend/src/agents/task_management_agent.py` (enhance with general chat capabilities)
- `backend/src/api/chat.py` (update to use single assistant)
- `backend/api/routes/conversation.py` (redirect or deprecate)
- `frontend/app/dashboard/page.tsx` (consolidate assistant interfaces)
- `frontend/services/chatService.ts` (update API calls)

## Expected Outcomes
- Exactly one assistant handles all AI processing
- No fallback or secondary agent systems remain
- Both chat and task operations function correctly
- Manual UI controls continue to work independently
- No assistant ambiguity in code or behavior