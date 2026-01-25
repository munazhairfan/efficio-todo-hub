"""
Task Intelligence Service for OpenRouter Assistant

This service provides intent detection and task processing logic
that was previously in the local Task Management Agent.
The OpenRouter assistant will use this service to decide when
to call MCP tools versus when to respond normally.
"""

import re
from typing import Dict, Any, Optional, Tuple
from enum import Enum

from src.mcp_tools import add_task, list_tasks, complete_task, delete_task, update_task
from src.utils.errors import TaskNotFoundError, ValidationError, AuthorizationError


class IntentType(Enum):
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"
    UNKNOWN = "unknown"


class TaskIntelligenceService:
    def __init__(self):
        self.patterns = {
            IntentType.ADD_TASK: [
                r'add.*task',
                r'create.*task',
                r'make.*task',
                r'new.*task',
                r'add.*to.*list',
                r'put.*on.*list',
                r'need.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read)',
            ],
            IntentType.LIST_TASKS: [
                r'show.*task',
                r'list.*task',
                r'view.*task',
                r'see.*task',
                r'my.*task',
                r'what.*do.*i.*have',
            ],
            IntentType.COMPLETE_TASK: [
                r'complete.*task',
                r'mark.*as.*done',
                r'finished.*task',
            ],
            IntentType.DELETE_TASK: [
                r'delete.*task',
                r'remove.*task',
            ],
            IntentType.UPDATE_TASK: [
                r'update.*task',
                r'edit.*task',
                r'change.*task',
            ]
        }

        self.compiled_patterns = {
            intent: [re.compile(p, re.IGNORECASE) for p in patterns]
            for intent, patterns in self.patterns.items()
        }

    def _extract_task_id(self, message: str) -> Optional[int]:
        patterns = [
            r'task\s*#(\d+)',
            r'#(\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def _extract_task_details(self, message: str) -> Tuple[Optional[str], Optional[str]]:
        clean_message = re.sub(
            r'^(add|create|make|new)\s+(a\s+)?task\s*(to\s*)?',
            '',
            message,
            flags=re.IGNORECASE
        )
        parts = re.split(r'[.!?]', clean_message, maxsplit=1)
        title = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else None
        return title, description

    def _recognize_intent(self, message: str) -> IntentType:
        for intent, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(message):
                    return intent
        return IntentType.UNKNOWN

    def process_task_request(self, user_id: str, message: str) -> Optional[Dict[str, Any]]:
        intent = self._recognize_intent(message)

        try:
            if intent == IntentType.ADD_TASK:
                title, description = self._extract_task_details(message)
                result = add_task(user_id=user_id, title=title, description=description)
                return {
                    "response": f"Task added: {result['title']}",
                    "handled_locally": True
                }

            elif intent == IntentType.LIST_TASKS:
                status = "all"
                if "pending" in message.lower():
                    status = "pending"
                elif "completed" in message.lower():
                    status = "completed"

                tasks = list_tasks(user_id=user_id, status=status)

                if not tasks:
                    return {
                        "response": "You have no tasks.",
                        "handled_locally": True
                    }

                if status == "all":
                    pending_tasks = [t for t in tasks if t["status"] == "pending"]
                    completed_tasks = [t for t in tasks if t["status"] == "completed"]

                    response = "Here are your tasks:\n"

                    if pending_tasks:
                        response += f"\nPending ({len(pending_tasks)}):\n"
                        response += "\n".join(
                            f"  - #{i + 1}: {task['title']}"
                            for i, task in enumerate(pending_tasks)
                        )

                    if completed_tasks:
                        response += f"\n\nCompleted ({len(completed_tasks)}):\n"
                        response += "\n".join(
                            f"  - #{i + 1}: {task['title']}"
                            for i, task in enumerate(completed_tasks)
                        )
                else:
                    response = f"Here are your tasks:\n"
                    response += "\n".join(
                        f"  - #{i + 1}: {task['title']}"
                        for i, task in enumerate(tasks)
                    )

                return {
                    "response": response,
                    "handled_locally": True
                }

            elif intent == IntentType.COMPLETE_TASK:
                task_id = self._extract_task_id(message)
                result = complete_task(user_id=user_id, task_id=task_id)
                return {
                    "response": f"Task completed: {result['title']}",
                    "handled_locally": True
                }

            elif intent == IntentType.DELETE_TASK:
                task_id = self._extract_task_id(message)
                result = delete_task(user_id=user_id, task_id=task_id)
                return {
                    "response": f"Task deleted: {result['title']}",
                    "handled_locally": True
                }

            elif intent == IntentType.UPDATE_TASK:
                task_id = self._extract_task_id(message)
                title_match = re.search(r'to\s+["\'](.+?)["\']', message)
                if title_match:
                    new_title = title_match.group(1)
                    result = update_task(user_id=user_id, task_id=task_id, title=new_title)
                    return {
                        "response": f"Task updated: {result['title']}",
                        "handled_locally": True
                    }

            return None

        except (ValidationError, TaskNotFoundError, AuthorizationError) as e:
            return {
                "response": str(e),
                "handled_locally": True
            }
        except Exception:
            return {
                "response": "An unexpected error occurred while processing your request.",
                "handled_locally": True
            }


task_intelligence_service = TaskIntelligenceService()