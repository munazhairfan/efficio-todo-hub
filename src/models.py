from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Task:
    """
    Represents a todo item with ID, title, description, and completion status.
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __str__(self) -> str:
        """
        Return a string representation of the task for console display.
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title} - {self.description}"


class TaskList:
    """
    Collection of tasks stored in-memory that supports add, view, update, delete, and mark operations.
    """

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the list with a unique ID and default incomplete status.

        Args:
            title: The title of the task
            description: The description of the task (optional)

        Returns:
            The created Task object
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(id=self.next_id, title=title.strip(), description=description.strip())
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object

        Raises:
            KeyError: If no task with the given ID exists
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"Task with ID {task_id} not found")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update task details by ID.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if update was successful, False otherwise
        """
        try:
            task = self.get_task(task_id)
            if title is not None:
                if not title.strip():
                    raise ValueError("Task title cannot be empty")
                task.title = title.strip()
            if description is not None:
                task.description = description.strip()
            return True
        except KeyError:
            return False

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            task = self.get_task(task_id)
            self.tasks.remove(task)
            return True
        except KeyError:
            return False

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete by ID.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            True if marking was successful, False otherwise
        """
        try:
            task = self.get_task(task_id)
            task.completed = True
            return True
        except KeyError:
            return False

    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete by ID.

        Args:
            task_id: The ID of the task to mark incomplete

        Returns:
            True if marking was successful, False otherwise
        """
        try:
            task = self.get_task(task_id)
            task.completed = False
            return True
        except KeyError:
            return False

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all Task objects
        """
        return self.tasks.copy()

    def get_completed_tasks(self) -> List[Task]:
        """
        Retrieve only completed tasks.

        Returns:
            List of completed Task objects
        """
        return [task for task in self.tasks if task.completed]

    def get_pending_tasks(self) -> List[Task]:
        """
        Retrieve only pending tasks.

        Returns:
            List of pending Task objects
        """
        return [task for task in self.tasks if not task.completed]