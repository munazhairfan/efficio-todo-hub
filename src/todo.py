"""
Task management functions for the Todo In-Memory Console App.
"""
from typing import List, Optional
from .models import Task, TaskList


def add_task(task_list: TaskList, title: str, description: str = "") -> int:
    """
    Add a new task with title and description validation.

    Args:
        task_list: The TaskList instance to add the task to
        title: The title of the task
        description: The description of the task (optional)

    Returns:
        The ID of the newly created task

    Raises:
        ValueError: If title is empty or invalid
    """
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    task = task_list.add_task(title, description)
    return task.id


def get_task(task_list: TaskList, task_id: int) -> dict:
    """
    Retrieve a task by its ID and return as dictionary.

    Args:
        task_list: The TaskList instance to get the task from
        task_id: The ID of the task to retrieve

    Returns:
        Dictionary representation of the task
    """
    task = task_list.get_task(task_id)
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed
    }


def update_task(task_list: TaskList, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
    """
    Update task details by ID.

    Args:
        task_list: The TaskList instance to update the task in
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        True if update was successful, False otherwise
    """
    return task_list.update_task(task_id, title, description)


def delete_task(task_list: TaskList, task_id: int) -> bool:
    """
    Remove a task by ID.

    Args:
        task_list: The TaskList instance to delete the task from
        task_id: The ID of the task to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    return task_list.delete_task(task_id)


def toggle_complete(task_list: TaskList, task_id: int) -> bool:
    """
    Toggle the completion status of a task.

    Args:
        task_list: The TaskList instance containing the task
        task_id: The ID of the task to toggle

    Returns:
        True if toggle was successful, False otherwise
    """
    try:
        task = task_list.get_task(task_id)
        if task.completed:
            return task_list.mark_incomplete(task_id)
        else:
            return task_list.mark_complete(task_id)
    except KeyError:
        return False


def mark_complete(task_list: TaskList, task_id: int) -> bool:
    """
    Mark a task as complete.

    Args:
        task_list: The TaskList instance containing the task
        task_id: The ID of the task to mark complete

    Returns:
        True if marking was successful, False otherwise
    """
    return task_list.mark_complete(task_id)


def mark_incomplete(task_list: TaskList, task_id: int) -> bool:
    """
    Mark a task as incomplete.

    Args:
        task_list: The TaskList instance containing the task
        task_id: The ID of the task to mark incomplete

    Returns:
        True if marking was successful, False otherwise
    """
    return task_list.mark_incomplete(task_id)


def get_all_tasks(task_list: TaskList) -> List[dict]:
    """
    Retrieve all tasks as a list of dictionaries.

    Args:
        task_list: The TaskList instance to get tasks from

    Returns:
        List of dictionary representations of all tasks
    """
    tasks = task_list.get_all_tasks()
    return [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        }
        for task in tasks
    ]


def get_completed_tasks(task_list: TaskList) -> List[dict]:
    """
    Retrieve only completed tasks as a list of dictionaries.

    Args:
        task_list: The TaskList instance to get tasks from

    Returns:
        List of dictionary representations of completed tasks
    """
    tasks = task_list.get_completed_tasks()
    return [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        }
        for task in tasks
    ]


def get_pending_tasks(task_list: TaskList) -> List[dict]:
    """
    Retrieve only pending tasks as a list of dictionaries.

    Args:
        task_list: The TaskList instance to get tasks from

    Returns:
        List of dictionary representations of pending tasks
    """
    tasks = task_list.get_pending_tasks()
    return [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        }
        for task in tasks
    ]