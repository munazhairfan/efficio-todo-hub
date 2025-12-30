"""
Unit tests for the CLI functions.
These tests focus on the logic of CLI functions, not the actual user input/output.
"""
from unittest.mock import patch, MagicMock
from src.models import TaskList
from src.cli import cli_add_task, cli_view_tasks, cli_update_task, cli_delete_task, cli_toggle_task_status


class TestCLIAddTask:
    """Tests for the cli_add_task function."""

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_add_task_success(self, mock_print, mock_get_user_input):
        """Test successful task addition via CLI."""
        # Mock user inputs
        mock_get_user_input.side_effect = ['Test Title', 'Test Description']

        task_list = TaskList()
        result = cli_add_task(task_list)

        assert result is True
        assert len(task_list.tasks) == 1
        assert task_list.tasks[0].title == 'Test Title'
        assert task_list.tasks[0].description == 'Test Description'
        assert task_list.tasks[0].completed is False

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_add_task_empty_title(self, mock_print, mock_get_user_input):
        """Test CLI add task with empty title."""
        # Mock user inputs - empty title
        mock_get_user_input.side_effect = ['', 'Test Description']

        task_list = TaskList()
        result = cli_add_task(task_list)

        assert result is False
        assert len(task_list.tasks) == 0

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_add_task_no_description(self, mock_print, mock_get_user_input):
        """Test CLI add task without description."""
        # Mock user inputs - no description
        mock_get_user_input.side_effect = ['Test Title', '']

        task_list = TaskList()
        result = cli_add_task(task_list)

        assert result is True
        assert len(task_list.tasks) == 1
        assert task_list.tasks[0].title == 'Test Title'
        assert task_list.tasks[0].description == ''


class TestCLIViewTasks:
    """Tests for the cli_view_tasks function."""

    @patch('builtins.print')
    def test_cli_view_tasks_with_tasks(self, mock_print):
        """Test viewing tasks when tasks exist."""
        task_list = TaskList()
        task_list.add_task('Task 1', 'Description 1')
        task_list.add_task('Task 2', 'Description 2')

        cli_view_tasks(task_list)

        # Check that print was called (at least once for the header)
        assert mock_print.call_count >= 1

    @patch('builtins.print')
    def test_cli_view_tasks_empty_list(self, mock_print):
        """Test viewing tasks when no tasks exist."""
        task_list = TaskList()

        cli_view_tasks(task_list)

        # Check that the "No tasks found" message was printed
        mock_print.assert_any_call("No tasks found.")


class TestCLIUpdateTask:
    """Tests for the cli_update_task function."""

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_update_task_success(self, mock_print, mock_get_user_input):
        """Test successful task update via CLI."""
        task_list = TaskList()
        task = task_list.add_task('Original Title', 'Original Description')

        # Mock user inputs: task ID, new title, new description
        mock_get_user_input.side_effect = [
            str(task.id),           # task ID
            'New Title',           # new title
            'New Description'      # new description
        ]

        cli_update_task(task_list)

        # Verify the task was updated
        updated_task = task_list.get_task(task.id)
        assert updated_task.title == 'New Title'
        assert updated_task.description == 'New Description'

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_update_task_invalid_id(self, mock_print, mock_get_user_input):
        """Test updating a task with invalid ID."""
        task_list = TaskList()
        task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: invalid task ID
        mock_get_user_input.side_effect = [
            '999',                 # invalid task ID
        ]

        cli_update_task(task_list)

        # Verify the error message was printed
        mock_print.assert_any_call("Error: Task with ID 999 not found.")

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_update_task_invalid_number(self, mock_print, mock_get_user_input):
        """Test updating a task with invalid number input."""
        task_list = TaskList()
        task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: non-numeric task ID
        mock_get_user_input.side_effect = [
            'abc',                 # invalid task ID (not a number)
        ]

        cli_update_task(task_list)

        # Verify the error message was printed
        mock_print.assert_any_call("Error: Please enter a valid task ID (number).")


class TestCLIDeleteTask:
    """Tests for the cli_delete_task function."""

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_delete_task_success(self, mock_print, mock_get_user_input):
        """Test successful task deletion via CLI."""
        task_list = TaskList()
        task = task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: task ID, confirmation
        mock_get_user_input.side_effect = [
            str(task.id),           # task ID
            'y'                    # confirm deletion
        ]

        cli_delete_task(task_list)

        # Verify the task was deleted
        assert len(task_list.tasks) == 0

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_delete_task_cancelled(self, mock_print, mock_get_user_input):
        """Test task deletion cancelled by user."""
        task_list = TaskList()
        task = task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: task ID, no confirmation
        mock_get_user_input.side_effect = [
            str(task.id),           # task ID
            'n'                    # cancel deletion
        ]

        cli_delete_task(task_list)

        # Verify the task was not deleted
        assert len(task_list.tasks) == 1

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_delete_task_invalid_id(self, mock_print, mock_get_user_input):
        """Test deleting a task with invalid ID."""
        task_list = TaskList()
        task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: invalid task ID
        mock_get_user_input.side_effect = [
            '999',                 # invalid task ID
        ]

        cli_delete_task(task_list)

        # Verify the error message was printed
        mock_print.assert_any_call("Error: Task with ID 999 not found.")


class TestCLIToggleTaskStatus:
    """Tests for the cli_toggle_task_status function."""

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_toggle_task_status_success(self, mock_print, mock_get_user_input):
        """Test successful task status toggle via CLI."""
        task_list = TaskList()
        task = task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: task ID
        mock_get_user_input.side_effect = [
            str(task.id),           # task ID
        ]

        cli_toggle_task_status(task_list)

        # Verify the task status was toggled
        updated_task = task_list.get_task(task.id)
        assert updated_task.completed is True

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_toggle_task_status_invalid_id(self, mock_print, mock_get_user_input):
        """Test toggling status of a task with invalid ID."""
        task_list = TaskList()
        task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: invalid task ID
        mock_get_user_input.side_effect = [
            '999',                 # invalid task ID
        ]

        cli_toggle_task_status(task_list)

        # Verify the error message was printed
        mock_print.assert_any_call("Error: Task with ID 999 not found.")

    @patch('src.cli.get_user_input')
    @patch('builtins.print')
    def test_cli_toggle_task_status_invalid_number(self, mock_print, mock_get_user_input):
        """Test toggling status with invalid number input."""
        task_list = TaskList()
        task_list.add_task('Test Title', 'Test Description')

        # Mock user inputs: non-numeric task ID
        mock_get_user_input.side_effect = [
            'abc',                 # invalid task ID (not a number)
        ]

        cli_toggle_task_status(task_list)

        # Verify the error message was printed
        mock_print.assert_any_call("Error: Please enter a valid task ID (number).")