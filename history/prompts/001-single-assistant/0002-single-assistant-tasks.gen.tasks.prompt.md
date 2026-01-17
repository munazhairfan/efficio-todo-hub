---
id: phr_0002_single_assistant_tasks
stage: tasks
feature: single-assistant
date: 2026-01-18
title: Single Assistant Architecture Tasks
---

# Single Assistant Architecture Tasks

## Prompt Text

```
TASK GROUP 1 — IDENTIFY ASSISTANT IMPLEMENTATIONS

1. Locate all files responsible for AI behavior, including but not limited to:
   - Agents
   - Assistants
   - AI clients
   - Fallback logic
   - Pattern matching or intent handlers

2. Explicitly list:
   - Which file currently acts as the main assistant
   - Which files act as secondary, fallback, or local assistants

3. Mark exactly ONE file as the "Single Assistant Source of Truth".
   - This file will remain.
   - All others must be removed or merged.


TASK GROUP 2 — REMOVE EXTRA ASSISTANTS (NO CREATION)

4. Delete or fully disable all secondary assistants.
   - Remove local / pattern-based agents.
   - Remove fallback routing logic.
   - Remove any conditional logic choosing between assistants.

5. Ensure no imports, references, or calls remain to removed assistants.
   - Clean unused imports.
   - Clean dead code paths.
   - Ensure build passes without them.

IMPORTANT:
- Do NOT replace deleted assistants with new ones.
- Do NOT introduce abstraction layers.


TASK GROUP 3 — MERGE REQUIRED LOGIC INTO SINGLE ASSISTANT

6. If deleted assistants contained required logic (e.g. intent detection):
   - Move that logic into the remaining assistant.
   - Integrate it directly, not via delegation.

7. Ensure the single assistant can:
   - Respond conversationally to normal chat
   - Detect when a task-related action is requested
   - Decide to call MCP tools when needed

NOTE:
- All reasoning must happen inside this one assistant.


TASK GROUP 4 — MCP TOOL BOUNDARIES

8. Verify MCP tools:
   - Contain NO conversational logic
   - Contain NO AI reasoning
   - Only execute actions (CRUD, utilities, etc.)

9. Ensure MCP tools are invoked ONLY by the single assistant.
   - No other file may call MCP tools for chat purposes.


TASK GROUP 5 — CHAT FLOW VERIFICATION

10. Trace the chat request flow:
    - Frontend → chat API → single assistant → response

11. Confirm:
    - All chat responses originate from the same assistant
    - No branching or fallb
```

## Response Text

Generated comprehensive task list for single assistant architecture implementation:

### Task Groups Implemented:

**TASK GROUP 1 — IDENTIFY ASSISTANT IMPLEMENTATIONS**
- Identified main assistant: backend/src/services/openrouter_client.py
- Identified secondary assistants: backend/src/agents/task_management_agent.py
- Marked openrouter_client.py as "Single Assistant Source of Truth"

**TASK GROUP 2 — REMOVE EXTRA ASSISTANTS**
- Created tasks to remove fallback logic in chat endpoints
- Created tasks to remove imports of local agent
- Created tasks to clean up unused references

**TASK GROUP 3 — MERGE REQUIRED LOGIC**
- Created tasks to enhance OpenRouter client with tool calling capabilities
- Created tasks to maintain intent detection in single assistant
- Ensured all reasoning happens inside one assistant

**TASK GROUP 4 — MCP TOOL BOUNDARIES**
- Created tasks to verify MCP tools contain no conversational logic
- Created tasks to ensure MCP tools only execute actions
- Created tasks to confirm MCP tools invoked only by single assistant

**TASK GROUP 5 — CHAT FLOW VERIFICATION**
- Created tasks to trace complete chat request flow
- Created tasks to verify all responses come from same assistant
- Created tasks to confirm no branching to other assistants

### Key Features of Tasks:
- 35 individual tasks organized in 7 phases
- Clear dependency structure with US1 as prerequisite
- Parallel execution opportunities identified
- Independent test criteria for each user story
- Complete coverage of all requirements
- MVP scope defined as US1 (identification phase)
- Tasks follow proper format with checkboxes, IDs, and file paths