"""
Unit tests for the task management functions in todo.py.
"""
import pytest
from src.models import TaskList
from src.todo import (
    add_task, get_task, update_task, delete_task,
    toggle_complete, mark_complete, mark_incomplete,
    get_all_tasks, get_completed_tasks, get_pending_tasks
)


class TestAddTask:
    """Tests for the add_task function."""

    def test_add_task_success(self):
        """Test adding a task successfully."""
        task_list = TaskList()
        task_id = add_task(task_list, "Test Title", "Test Description")

        assert task_id == 1
        task = task_list.get_task(task_id)
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        task_list = TaskList()
        task_id = add_task(task_list, "Test Title")

        assert task_id == 1
        task = task_list.get_task(task_id)
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_empty_title_error(self):
        """Test that adding a task with empty title raises ValueError."""
        task_list = TaskList()
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            add_task(task_list, "")


class TestGetTask:
    """Tests for the get_task function."""

    def test_get_task_success(self):
        """Test retrieving a task successfully."""
        task_list = TaskList()
        original_task = task_list.add_task("Test Title", "Test Description")

        task_dict = get_task(task_list, original_task.id)

        assert task_dict['id'] == original_task.id
        assert task_dict['title'] == original_task.title
        assert task_dict['description'] == original_task.description
        assert task_dict['completed'] == original_task.completed

    def test_get_task_not_found(self):
        """Test that retrieving a non-existent task raises KeyError."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        with pytest.raises(KeyError):
            get_task(task_list, 999)


class TestUpdateTask:
    """Tests for the update_task function."""

    def test_update_task_success(self):
        """Test updating a task successfully."""
        task_list = TaskList()
        original_task = task_list.add_task("Original Title", "Original Description")

        success = update_task(task_list, original_task.id, "New Title", "New Description")

        assert success is True
        updated_task = task_list.get_task(original_task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_task_partial(self):
        """Test updating only title or description."""
        task_list = TaskList()
        original_task = task_list.add_task("Original Title", "Original Description")

        # Update only title
        success = update_task(task_list, original_task.id, title="New Title")
        assert success is True

        updated_task = task_list.get_task(original_task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = update_task(task_list, 999, "New Title")
        assert success is False


class TestDeleteTask:
    """Tests for the delete_task function."""

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        task_list = TaskList()
        task_to_delete = task_list.add_task("Test Title")

        success = delete_task(task_list, task_to_delete.id)

        assert success is True
        with pytest.raises(KeyError):
            task_list.get_task(task_to_delete.id)

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = delete_task(task_list, 999)
        assert success is False
        assert len(task_list.tasks) == 1


class TestToggleComplete:
    """Tests for the toggle_complete function."""

    def test_toggle_complete_to_incomplete(self):
        """Test toggling a completed task to incomplete."""
        task_list = TaskList()
        task = task_list.add_task("Test Title")
        task_list.mark_complete(task.id)

        success = toggle_complete(task_list, task.id)

        assert success is True
        updated_task = task_list.get_task(task.id)
        assert updated_task.completed is False

    def test_toggle_incomplete_to_complete(self):
        """Test toggling an incomplete task to complete."""
        task_list = TaskList()
        task = task_list.add_task("Test Title")

        success = toggle_complete(task_list, task.id)

        assert success is True
        updated_task = task_list.get_task(task.id)
        assert updated_task.completed is True

    def test_toggle_task_not_found(self):
        """Test toggling a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = toggle_complete(task_list, 999)
        assert success is False


class TestMarkComplete:
    """Tests for the mark_complete function."""

    def test_mark_complete_success(self):
        """Test marking a task as complete."""
        task_list = TaskList()
        task = task_list.add_task("Test Title")

        success = mark_complete(task_list, task.id)

        assert success is True
        updated_task = task_list.get_task(task.id)
        assert updated_task.completed is True

    def test_mark_complete_not_found(self):
        """Test marking a non-existent task as complete."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = mark_complete(task_list, 999)
        assert success is False


class TestMarkIncomplete:
    """Tests for the mark_incomplete function."""

    def test_mark_incomplete_success(self):
        """Test marking a task as incomplete."""
        task_list = TaskList()
        task = task_list.add_task("Test Title")
        task_list.mark_complete(task.id)  # First mark as complete

        success = mark_incomplete(task_list, task.id)

        assert success is True
        updated_task = task_list.get_task(task.id)
        assert updated_task.completed is False

    def test_mark_incomplete_not_found(self):
        """Test marking a non-existent task as incomplete."""
        task_list = TaskList()
        task_list.add_task("Test Title")

        success = mark_incomplete(task_list, 999)
        assert success is False


class TestGetAllTasks:
    """Tests for the get_all_tasks function."""

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")

        all_tasks = get_all_tasks(task_list)

        assert len(all_tasks) == 2
        task_ids = [task['id'] for task in all_tasks]
        assert task1.id in task_ids
        assert task2.id in task_ids


class TestGetCompletedTasks:
    """Tests for the get_completed_tasks function."""

    def test_get_completed_tasks(self):
        """Test retrieving only completed tasks."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")
        task_list.mark_complete(task2.id)

        completed_tasks = get_completed_tasks(task_list)

        assert len(completed_tasks) == 1
        assert completed_tasks[0]['id'] == task2.id
        assert completed_tasks[0]['completed'] is True


class TestGetPendingTasks:
    """Tests for the get_pending_tasks function."""

    def test_get_pending_tasks(self):
        """Test retrieving only pending tasks."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")
        task_list.mark_complete(task2.id)

        pending_tasks = get_pending_tasks(task_list)

        assert len(pending_tasks) == 1
        assert pending_tasks[0]['id'] == task1.id
        assert pending_tasks[0]['completed'] is False