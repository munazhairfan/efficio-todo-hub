"""
Command-line interface for the Todo In-Memory Console App.
"""
from typing import Optional
from .models import TaskList
from .todo import add_task


def get_user_input(prompt: str) -> str:
    """
    Get input from the user with a prompt.

    Args:
        prompt: The prompt to display to the user

    Returns:
        The user's input as a string
    """
    return input(prompt).strip()


def cli_add_task(task_list: TaskList) -> bool:
    """
    CLI function for adding tasks.

    Args:
        task_list: The TaskList instance to add the task to

    Returns:
        True if task was added successfully, False otherwise
    """
    print("\n--- Add New Task ---")
    title = get_user_input("Enter task title: ")

    if not title:
        print("Error: Task title cannot be empty.")
        return False

    description = get_user_input("Enter task description (optional): ")

    try:
        task_id = add_task(task_list, title, description)
        print(f"✓ Task added successfully with ID: {task_id}")
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False


def cli_view_tasks(task_list: TaskList):
    """
    CLI function for viewing all tasks.

    Args:
        task_list: The TaskList instance to view tasks from
    """
    print("\n--- All Tasks ---")
    all_tasks = task_list.get_all_tasks()

    if not all_tasks:
        print("No tasks found.")
        return

    for task in all_tasks:
        status = "✓" if task.completed else "○"
        print(f"[{status}] {task.id}. {task.title} - {task.description}")


def cli_update_task(task_list: TaskList):
    """
    CLI function for updating tasks.

    Args:
        task_list: The TaskList instance to update tasks in
    """
    print("\n--- Update Task ---")
    try:
        task_id_str = get_user_input("Enter task ID to update: ")
        task_id = int(task_id_str)
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
        return

    # Check if task exists
    try:
        current_task = task_list.get_task(task_id)
    except KeyError:
        print(f"Error: Task with ID {task_id} not found.")
        return

    print(f"Current task: {current_task}")

    new_title = get_user_input(f"Enter new title (current: '{current_task.title}', press Enter to keep current): ")
    new_description = get_user_input(f"Enter new description (current: '{current_task.description}', press Enter to keep current): ")

    # Use current values if user didn't provide new ones
    title = new_title if new_title else current_task.title
    description = new_description if new_description else current_task.description

    try:
        success = task_list.update_task(task_id, title, description)
        if success:
            print(f"✓ Task {task_id} updated successfully.")
        else:
            print(f"✗ Failed to update task {task_id}.")
    except ValueError as e:
        print(f"Error: {e}")


def cli_delete_task(task_list: TaskList):
    """
    CLI function for deleting tasks.

    Args:
        task_list: The TaskList instance to delete tasks from
    """
    print("\n--- Delete Task ---")
    try:
        task_id_str = get_user_input("Enter task ID to delete: ")
        task_id = int(task_id_str)
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
        return

    # Check if task exists
    try:
        current_task = task_list.get_task(task_id)
        print(f"Task to delete: {current_task}")
    except KeyError:
        print(f"Error: Task with ID {task_id} not found.")
        return

    confirm = get_user_input(f"Are you sure you want to delete task {task_id}? (y/N): ")
    if confirm.lower() in ['y', 'yes']:
        success = task_list.delete_task(task_id)
        if success:
            print(f"✓ Task {task_id} deleted successfully.")
        else:
            print(f"✗ Failed to delete task {task_id}.")
    else:
        print("Task deletion cancelled.")


def cli_toggle_task_status(task_list: TaskList):
    """
    CLI function for toggling task status.

    Args:
        task_list: The TaskList instance containing the task
    """
    print("\n--- Toggle Task Status ---")
    try:
        task_id_str = get_user_input("Enter task ID to toggle status: ")
        task_id = int(task_id_str)
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
        return

    # Check if task exists
    try:
        current_task = task_list.get_task(task_id)
        print(f"Current task: {current_task}")
    except KeyError:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Toggle the status
    if current_task.completed:
        success = task_list.mark_incomplete(task_id)
        new_status = "incomplete"
    else:
        success = task_list.mark_complete(task_id)
        new_status = "complete"

    if success:
        print(f"✓ Task {task_id} marked as {new_status}.")
    else:
        print(f"✗ Failed to update task {task_id} status.")