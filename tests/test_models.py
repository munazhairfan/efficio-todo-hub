"""
Unit tests for the Task model and TaskList class.
"""
import pytest
from src.models import Task, TaskList


class TestTask:
    """Tests for the Task dataclass."""

    def test_task_creation(self):
        """Test creating a new task with valid parameters."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_default_values(self):
        """Test creating a task with default values."""
        task = Task(id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_task_string_representation(self):
        """Test the string representation of a task."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=True)
        expected = "[✓] 1. Test Task - Test Description"
        assert str(task) == expected

        task = Task(id=2, title="Test Task", description="Test Description", completed=False)
        expected = "[○] 2. Test Task - Test Description"
        assert str(task) == expected


class TestTaskList:
    """Tests for the TaskList class."""

    def test_tasklist_initialization(self):
        """Test initializing a TaskList."""
        task_list = TaskList()
        assert task_list.tasks == []
        assert task_list.next_id == 1

    def test_add_task_success(self):
        """Test adding a task successfully."""
        task_list = TaskList()
        task = task_list.add_task("Test Title", "Test Description")

        assert len(task_list.tasks) == 1
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task_list.next_id == 2

    def test_add_task_without_description(self):
        """Test adding a task without providing a description."""
        task_list = TaskList()
        task = task_list.add_task("Test Title")

        assert len(task_list.tasks) == 1
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_empty_title_error(self):
        """Test that adding a task with empty title raises ValueError."""
        task_list = TaskList()
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_list.add_task("")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_list.add_task("   ")

    def test_get_task_success(self):
        """Test retrieving a task by ID."""
        task_list = TaskList()
        added_task = task_list.add_task("Test Title")

        retrieved_task = task_list.get_task(added_task.id)

        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title
        assert retrieved_task.description == added_task.description
        assert retrieved_task.completed == added_task.completed

    def test_get_task_not_found(self):
        """Test that retrieving a non-existent task raises KeyError."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        with pytest.raises(KeyError, match="Task with ID 999 not found"):
            task_list.get_task(999)

    def test_update_task_success(self):
        """Test updating a task successfully."""
        task_list = TaskList()
        original_task = task_list.add_task("Original Title", "Original Description")

        success = task_list.update_task(original_task.id, "New Title", "New Description")

        assert success is True
        updated_task = task_list.get_task(original_task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_task_partial(self):
        """Test updating only title or description."""
        task_list = TaskList()
        original_task = task_list.add_task("Original Title", "Original Description")

        # Update only title
        success = task_list.update_task(original_task.id, title="New Title")
        assert success is True

        updated_task = task_list.get_task(original_task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged

        # Update only description
        success = task_list.update_task(original_task.id, description="Newer Description")
        assert success is True

        updated_task = task_list.get_task(original_task.id)
        assert updated_task.title == "New Title"  # Should remain unchanged
        assert updated_task.description == "Newer Description"

    def test_update_task_invalid_id(self):
        """Test updating a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = task_list.update_task(999, "New Title")
        assert success is False

    def test_update_task_empty_title_error(self):
        """Test that updating a task with empty title raises ValueError."""
        task_list = TaskList()
        original_task = task_list.add_task("Original Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_list.update_task(original_task.id, title="   ")

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        task_list = TaskList()
        task_to_delete = task_list.add_task("Test Title")

        success = task_list.delete_task(task_to_delete.id)

        assert success is True
        assert len(task_list.tasks) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = task_list.delete_task(999)
        assert success is False
        assert len(task_list.tasks) == 1

    def test_mark_complete_success(self):
        """Test marking a task as complete."""
        task_list = TaskList()
        task = task_list.add_task("Test Title")

        success = task_list.mark_complete(task.id)

        assert success is True
        updated_task = task_list.get_task(task.id)
        assert updated_task.completed is True

    def test_mark_complete_not_found(self):
        """Test marking a non-existent task as complete."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = task_list.mark_complete(999)
        assert success is False

    def test_mark_incomplete_success(self):
        """Test marking a task as incomplete."""
        task_list = TaskList()
        task = task_list.add_task("Test Title")
        task_list.mark_complete(task.id)  # First mark as complete

        success = task_list.mark_incomplete(task.id)

        assert success is True
        updated_task = task_list.get_task(task.id)
        assert updated_task.completed is False

    def test_mark_incomplete_not_found(self):
        """Test marking a non-existent task as incomplete."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = task_list.mark_incomplete(999)
        assert success is False

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")

        all_tasks = task_list.get_all_tasks()

        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks

    def test_get_completed_tasks(self):
        """Test retrieving only completed tasks."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")
        task_list.mark_complete(task2.id)

        completed_tasks = task_list.get_completed_tasks()

        assert len(completed_tasks) == 1
        assert task2 in completed_tasks
        assert task1 not in completed_tasks

    def test_get_pending_tasks(self):
        """Test retrieving only pending tasks."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")
        task_list.mark_complete(task2.id)

        pending_tasks = task_list.get_pending_tasks()

        assert len(pending_tasks) == 1
        assert task1 in pending_tasks
        assert task2 not in pending_tasks