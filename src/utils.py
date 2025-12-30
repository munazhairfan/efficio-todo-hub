"""
Utility functions for the Todo In-Memory Console App.
"""


def generate_id() -> int:
    """
    This function is a placeholder for ID generation.
    In the current implementation, ID generation is handled by the TaskList class.
    This function exists to satisfy the architectural plan but isn't currently used.
    """
    # This would be used if we needed a separate ID generation mechanism
    # For now, TaskList handles ID generation internally
    raise NotImplementedError("ID generation is handled by TaskList class")


def format_task_display(task) -> str:
    """
    Format a task for console display with clear status indicators.

    Args:
        task: A Task object to format

    Returns:
        Formatted string representation of the task
    """
    status = "✓" if getattr(task, 'completed', False) else "○"
    task_id = getattr(task, 'id', 'N/A')
    title = getattr(task, 'title', 'No Title')
    description = getattr(task, 'description', '')
    return f"[{status}] {task_id}. {title} - {description}"


def format_task_list_display(tasks) -> str:
    """
    Format a list of tasks for console display.

    Args:
        tasks: List of Task objects to format

    Returns:
        Formatted string representation of the task list
    """
    if not tasks:
        return "No tasks found."

    formatted_tasks = []
    for task in tasks:
        formatted_tasks.append(format_task_display(task))

    return "\n".join(formatted_tasks)


def validate_task_input(title: str, description: str = "") -> bool:
    """
    Validate task input for required fields.

    Args:
        title: Task title to validate
        description: Task description to validate

    Returns:
        True if input is valid, False otherwise
    """
    if not title or not title.strip():
        return False
    return True