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
    """Types of intents the AI agent can recognize"""
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"
    UNKNOWN = "unknown"


class TaskIntelligenceService:
    """
    Service that provides intent detection and task processing logic
    for the OpenRouter-based assistant
    """

    def __init__(self):
        # Define patterns for recognizing different intents
        self.patterns = {
            IntentType.ADD_TASK: [
                r'add.*task',
                r'create.*task',
                r'make.*task',
                r'new.*task',
                r'add.*to.*list',
                r'put.*on.*list',
                r'need.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'i.*should\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'don\'t.*forget.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'remember.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'add.*a.*',
                r'create.*a.*',
                r'got.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'gotta\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'want.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'would.*like.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'must\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'i\s+have\s+to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)(?!.*what\s+do\s+i\s+have\s+to\s+do)',
                r'schedule.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
                r'plan.*to\s+(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read|purchase|attend|prepare|organize|clean|fix|build|create|learn|practice|apply|setup|install|configure)',
            ],
            IntentType.LIST_TASKS: [
                r'show.*task',
                r'list.*task',
                r'view.*task',
                r'see.*task',
                r'what.*do.*i.*have.*to.*do',
                r'what.*tasks.*do.*i.*have',
                r'current.*task',
                r'all.*task',
                r'my.*task',
                r'what.*to.*do',
                r'tell.*me.*my.*task',
                r'give.*me.*my.*list',
                r'what.*is.*on.*my.*list',
                r'check.*my.*list',
                r'look.*at.*my.*tasks',
                r'browse.*tasks',
                r'review.*tasks',
                r'display.*tasks',
                r'fetch.*tasks',
                r'what.*is.*on.*my.*list',
            ],
            IntentType.COMPLETE_TASK: [
                r'complete.*task',
                r'done.*with.*task',
                r'finish.*task',
                r'completed.*task',
                r'mark.*as.*done',
                r'check.*off',
                r'finished.*task',
                r'did.*task',
                r'accomplished.*task',
                r'cross.*off',
                r'knocked.*out',
                r'crushed.*task',
                r'nail.*task',
                r'ace.*task',
                r'conquer.*task',
                r'beat.*task',
                r'dominate.*task',
                r'execute.*task',
                r'wrap.*up.*task',
                r'tick.*off',
            ],
            IntentType.DELETE_TASK: [
                r'delete.*task',
                r'remove.*task',
                r'erase.*task',
                r'cancel.*task',
                r'get.*rid.*of.*task',
                r'kill.*task',
                r'drop.*task',
                r'eliminate.*task',
                r'purge.*task',
                r'scrub.*task',
                r'obliterate.*task',
                r'wipe.*task',
                r'toss.*task',
                r'trash.*task',
                r'bin.*task',
                r'ditch.*task',
                r'strip.*task',
                r'shift.*task',
            ],
            IntentType.UPDATE_TASK: [
                r'change.*task',
                r'update.*task',
                r'modify.*task',
                r'edit.*task',
                r'rename.*task',
                r'alter.*task',
                r'fix.*task',
                r'amend.*task',
                r'revise.*task',
                r'rework.*task',
                r'tweak.*task',
                r'adjust.*task',
                r'refine.*task',
                r'improve.*task',
                r'polish.*task',
                r'reshape.*task',
                r'restructure.*task',
                r'revamp.*task',
            ]
        }

        # Compile regex patterns for better performance
        self.compiled_patterns = {}
        for intent_type, patterns in self.patterns.items():
            compiled_patterns = []
            for pattern in patterns:
                compiled_patterns.append(re.compile(pattern, re.IGNORECASE))
            self.compiled_patterns[intent_type] = compiled_patterns

    def _extract_task_id(self, message: str) -> Optional[int]:
        """
        Extract task ID from message using common patterns
        """
        # Look for patterns like "task #1", "task 1", "#1", etc.
        patterns = [
            r'task\s*#(\d+)',
            r'task\s+(\d+)',
            r'#(\d+)',
            r'number\s+(\d+)',
            r'item\s*#(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                try:
                    task_id = int(match.group(1))
                    # Safety guard: Validate that the task ID is reasonable (positive and not excessively large)
                    if task_id > 0 and task_id < 1000000:  # Reasonable upper limit
                        return task_id
                except ValueError:
                    continue

        return None

    def _extract_task_details(self, message: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract task title and description from message
        """
        # Remove common phrases that indicate task creation
        clean_message = re.sub(r'^(add|create|make|new)\s+(a\s+)?(task\s+to|task|to)\s*', '', message, flags=re.IGNORECASE)

        # If the message still contains common task-related phrases, extract the core task
        if re.search(r'(buy|get|do|complete|finish|start|stop|go|visit|call|send|write|read)', clean_message, re.IGNORECASE):
            # Look for the main action/object
            parts = re.split(r'[.,!?;]', clean_message)
            title = parts[0].strip()
            description = ' '.join(parts[1:]).strip() if len(parts) > 1 else None
            return title, description

        # If no clear action pattern, use the cleaned message as title
        return clean_message.strip(), None

    def _recognize_intent(self, message: str) -> IntentType:
        """
        Recognize the intent from the user message
        """
        message_lower = message.lower()

        # Check for each intent type
        for intent_type, compiled_patterns in self.compiled_patterns.items():
            for pattern in compiled_patterns:
                if pattern.search(message_lower):
                    return intent_type

        # If no pattern matches, return unknown
        return IntentType.UNKNOWN

    def process_task_request(self, user_id: str, message: str) -> Optional[Dict[str, Any]]:
        """
        Process a task-related request and return structured data for MCP tools.

        Returns None if the request is not task-related or if it should be handled by OpenRouter directly.
        """
        intent = self._recognize_intent(message)

        # If intent is unknown, let OpenRouter handle it normally
        if intent == IntentType.UNKNOWN:
            # Check if it's a general conversation starter that should be handled locally
            message_lower = message.lower()

            # Handle common casual conversation patterns that should be handled locally
            if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'howdy']):
                return {
                    "response": "Hi there! I'm your friendly task management assistant. You can ask me to add, list, complete, delete, or update tasks. What would you like to do today?",
                    "handled_locally": True
                }
            elif 'how are you' in message_lower or 'how do you do' in message_lower:
                return {
                    "response": "I'm doing great, thank you for asking! I'm here to help you manage your tasks. Would you like to add, list, complete, delete, or update any tasks?",
                    "handled_locally": True
                }
            elif 'thank' in message_lower:
                return {
                    "response": "You're welcome! I'm happy to help. Is there anything else I can assist you with regarding your tasks?",
                    "handled_locally": True
                }
            elif any(bye_word in message_lower for bye_word in ['bye', 'goodbye', 'see you', 'farewell']):
                return {
                    "response": "Goodbye! Feel free to come back anytime you need help managing your tasks! Have a great day!",
                    "handled_locally": True
                }
            elif 'name' in message_lower and ('what' in message_lower or 'who' in message_lower):
                return {
                    "response": "I'm your friendly task management assistant! I can help you add, list, complete, delete, or update tasks. How can I assist you today?",
                    "handled_locally": True
                }
            elif 'help' in message_lower:
                return {
                    "response": "I'm here to help you manage your tasks! You can ask me to:\n• Add a task (e.g., 'add a task to buy groceries')\n• List your tasks (e.g., 'show me my tasks')\n• Complete a task (e.g., 'complete task #1')\n• Delete a task (e.g., 'delete task #1')\n• Update a task (e.g., 'update task #1 to new title')\n\nWhat would you like to do?",
                    "handled_locally": True
                }
            else:
                # Not a task-related intent, let OpenRouter handle it
                return None

        # Process the recognized intent
        try:
            if intent == IntentType.ADD_TASK:
                title, description = self._extract_task_details(message)
                if not title or not title.strip():
                    # If we couldn't extract a title, ask for clarification
                    return {
                        "response": "I'm not sure what task you'd like to add. Could you please specify what task you want to create? 😊",
                        "handled_locally": True
                    }

                # Validate task title length
                if len(title.strip()) < 2:
                    return {
                        "response": "The task title seems too short. Please provide a more detailed task description. 🤔",
                        "handled_locally": True
                    }

                # Validate and sanitize title
                sanitized_title = title.strip()
                result = add_task(user_id=user_id, title=sanitized_title, description=description)
                return {
                    "response": f"Great! I've added the task '{result['title']}' to your list! It's now ready to tackle.",
                    "handled_locally": True,
                    "tool_call": {
                        "name": "add_task",
                        "arguments": {"user_id": user_id, "title": sanitized_title, "description": description}
                    }
                }

            elif intent == IntentType.LIST_TASKS:
                # Check if user wants specific status
                status = "all"
                if "pending" in message.lower() or "incomplete" in message.lower():
                    status = "pending"
                elif "completed" in message.lower():
                    status = "completed"

                tasks = list_tasks(user_id=user_id, status=status)
                if not tasks:
                    status_text = status if status != "all" else "current"
                    return {
                        "response": f"You don't have any {status_text} tasks right now. Would you like to add some?",
                        "handled_locally": True
                    }

                # Format response with better formatting
                if status == "all":
                    pending_tasks = [task for task in tasks if task['status'] == 'pending']
                    completed_tasks = [task for task in tasks if task['status'] == 'completed']

                    if pending_tasks and completed_tasks:
                        pending_list = "\n".join([f"  • #{task['id']}: {task['title']}" for task in pending_tasks])
                        completed_list = "\n".join([f"  • #{task['id']}: {task['title']}" for task in completed_tasks])
                        response = f"Here are your tasks:\n\nPending ({len(pending_tasks)}):\n{pending_list}"
                        if completed_tasks:
                            response += f"\n\nCompleted ({len(completed_tasks)}):\n{completed_list}"
                    elif pending_tasks:
                        task_list = "\n".join([f"  • #{task['id']}: {task['title']}" for task in pending_tasks])
                        response = f"Here are your {len(pending_tasks)} pending tasks:\n{task_list}"
                    elif completed_tasks:
                        task_list = "\n".join([f"  • #{task['id']}: {task['title']}" for task in completed_tasks])
                        response = f"Here are your {len(completed_tasks)} completed tasks:\n{task_list}"
                    else:
                        response = f"Here are your {len(tasks)} tasks:\n" + "\n".join([f"  • #{task['id']}: {task['title']}" for task in tasks])
                else:
                    task_list = "\n".join([f"  • #{task['id']}: {task['title']}" for task in tasks])
                    status_display = "pending" if status == "pending" else status
                    response = f"Here are your {len(tasks)} {status_display} tasks:\n{task_list}"

                return {
                    "response": response,
                    "handled_locally": True,
                    "tool_call": {
                        "name": "list_tasks",
                        "arguments": {"user_id": user_id, "status": status}
                    },
                    "tasks": tasks
                }

            elif intent == IntentType.COMPLETE_TASK:
                task_id = self._extract_task_id(message)
                if not task_id:
                    # Try to extract a task title if no ID is found
                    # Look for patterns like "complete 'buy groceries'"
                    title_match = re.search(r"(complete|done with|finished|finish|mark as done).*['\"]([^'\"]+)['\"]", message, re.IGNORECASE)
                    if title_match:
                        task_title = title_match.group(2)
                        # We would need to implement a way to find task by title, but for now we'll ask for ID
                        return {
                            "response": f"To complete '{task_title}', I need the task number. Could you please specify which task number corresponds to '{task_title}'?",
                            "handled_locally": True
                        }

                    return {
                        "response": "Which task would you like to mark as complete? Please specify the task number (e.g., 'complete task #1').",
                        "handled_locally": True
                    }

                # Validate that the task ID is positive
                if task_id <= 0:
                    return {
                        "response": "Task numbers must be positive. Please specify a valid task number. 📝",
                        "handled_locally": True
                    }

                result = complete_task(user_id=user_id, task_id=task_id)
                return {
                    "response": f"Excellent! I've marked task '#{result['id']}: {result['title']}' as completed! Great job!",
                    "handled_locally": True,
                    "tool_call": {
                        "name": "complete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id}
                    }
                }

            elif intent == IntentType.DELETE_TASK:
                task_id = self._extract_task_id(message)
                if not task_id:
                    # Try to extract a task title if no ID is found
                    title_match = re.search(r"(delete|remove|kill|drop|get rid of).*['\"]([^'\"]+)['\"]", message, re.IGNORECASE)
                    if title_match:
                        task_title = title_match.group(2)
                        return {
                            "response": f"To delete '{task_title}', I need the task number. Could you please specify which task number corresponds to '{task_title}'?",
                            "handled_locally": True
                        }

                    return {
                        "response": "Which task would you like to delete? Please specify the task number (e.g., 'delete task #1').",
                        "handled_locally": True
                    }

                # Validate that the task ID is positive
                if task_id <= 0:
                    return {
                        "response": "Task numbers must be positive. Please specify a valid task number.",
                        "handled_locally": True
                    }

                result = delete_task(user_id=user_id, task_id=task_id)
                return {
                    "response": f"Got it! I've deleted task '#{result['id']}: {result['title']}'. It's gone forever!",
                    "handled_locally": True,
                    "tool_call": {
                        "name": "delete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id}
                    }
                }

            elif intent == IntentType.UPDATE_TASK:
                task_id = self._extract_task_id(message)
                if not task_id:
                    # Try to extract a task title if no ID is found
                    title_match = re.search(r"(change|update|modify|edit|rename|alter|fix).*['\"]([^'\"]+)['\"]", message, re.IGNORECASE)
                    if title_match:
                        task_title = title_match.group(2)
                        return {
                            "response": f"To update '{task_title}', I need the task number. Could you please specify which task number corresponds to '{task_title}'?",
                            "handled_locally": True
                        }

                    return {
                        "response": "Which task would you like to update? Please specify the task number (e.g., 'update task #1').",
                        "handled_locally": True
                    }

                # Validate that the task ID is positive
                if task_id <= 0:
                    return {
                        "response": "Task numbers must be positive. Please specify a valid task number.",
                        "handled_locally": True
                    }

                # Try to extract new title/description from the message
                # Look for patterns like "change task #1 to 'new title'"
                title_match = re.search(r"(to|as|be|into)['\s]+['\"]([^'\"]+)['\"]", message, re.IGNORECASE)
                if title_match:
                    new_title = title_match.group(2)

                    # Validate new title length
                    if len(new_title.strip()) < 2:
                        return {
                            "response": "The new title seems too short. Please provide a more detailed task description. 🤔",
                            "handled_locally": True
                        }

                    result = update_task(user_id=user_id, task_id=task_id, title=new_title)
                    return {
                        "response": f"Perfect! I've updated task #{result['id']} to '{result['title']}'. Looks much better!",
                        "handled_locally": True,
                        "tool_call": {
                            "name": "update_task",
                            "arguments": {"user_id": user_id, "task_id": task_id, "title": new_title}
                        }
                    }
                else:
                    return {
                        "response": f"What would you like to update about task #{task_id}? Please specify the new title or description (e.g., 'update task #{task_id} to \"new title\"').",
                        "handled_locally": True
                    }
        except ValidationError as e:
            return {
                "response": f"I couldn't process your request: {str(e)}. Please check your input and try again.",
                "handled_locally": True,
                "error": str(e)
            }
        except TaskNotFoundError as e:
            return {
                "response": f"I couldn't find that task. It might have been deleted or the task number might be incorrect. Please check the task number and try again.",
                "handled_locally": True,
                "error": str(e)
            }
        except AuthorizationError as e:
            return {
                "response": f"You're not authorized to perform that action. This might be because the task belongs to another user.",
                "handled_locally": True,
                "error": str(e)
            }
        except Exception as e:
            return {
                "response": f"An unexpected error occurred while processing your request. Please try again. If the problem persists, contact support.",
                "handled_locally": True,
                "error": str(e)
            }

        # If we get here, return None to let OpenRouter handle it
        return None


# Global instance for easy access
task_intelligence_service = TaskIntelligenceService()