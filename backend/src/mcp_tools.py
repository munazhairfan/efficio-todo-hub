"""Model Context Protocol (MCP) tools for AI agents to manage user tasks."""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.task import Task, TaskCreate
from .services.task_service import TaskService
from .utils.errors import (
    TaskNotFoundError,
    AuthenticationError,
    ValidationError,
    AuthorizationError,
    handle_mcp_error
)
from .database.session import get_db, get_session_local


def _get_db_session() -> Session:
    """Get a database session for MCP tools"""
    from .database import get_session
    # Use the generator and get the session
    db_gen = get_session()
    db = next(db_gen)
    return db


def _validate_user_ownership(user_id: str, task: Task) -> None:
    """Validate that the user owns the task"""
    if str(task.user_id) != user_id:
        raise AuthorizationError("User is not authorized to access this task")


def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for a user.

    Args:
        user_id: The ID of the user requesting the operation (string)
        title: The title of the task to create (string, required)
        description: Detailed description of the task (string, optional)

    Returns:
        Dict with task_id (integer), status (string), and title (string)
    """
    try:
        # Input validation
        if not user_id:
            raise ValidationError("user_id is required")
        if not title or not title.strip():
            raise ValidationError("title is required and cannot be empty")

        # Use user_id as string for database operations (consistent with User model)
        user_id_str = str(user_id)

        # Get database session
        db = _get_db_session()
        task_service = TaskService(db)

        try:
            # Create task data
            task_create_data = TaskCreate(
                user_id=user_id_str,
                title=title.strip(),
                description=description.strip() if description else None
            )

            # Create the task
            task = task_service.create_task(task_create_data)

            # Return standardized response
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
        finally:
            db.close()

    except Exception as e:
        error_response = handle_mcp_error(e)
        raise e  # Re-raise the exception as MCP tools typically handle errors at a higher level


def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """
    Retrieve tasks for a user.

    Args:
        user_id: The ID of the user requesting the operation (string, required)
        status: Filter by status ("all", "pending", "completed") (string, optional)

    Returns:
        Array of task objects with properties: id, title, description, status, created_at
    """
    try:
        # Input validation
        if not user_id:
            raise ValidationError("user_id is required")

        # Validate status parameter
        valid_statuses = ["all", "pending", "completed"]
        if status not in valid_statuses:
            status = "all"  # Default to "all" if invalid status provided

        # Use user_id as string for database operations (consistent with User model)
        user_id_str = str(user_id)

        # Get database session
        db = _get_db_session()
        task_service = TaskService(db)

        try:
            # Get tasks for the user with status filter
            tasks = task_service.get_tasks_by_user(user_id_str, status)

            # Convert tasks to response format
            result = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": "completed" if task.completed else "pending",
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                result.append(task_dict)

            return result
        finally:
            db.close()

    except Exception as e:
        error_response = handle_mcp_error(e)
        raise e  # Re-raise the exception as MCP tools typically handle errors at a higher level


def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        user_id: The ID of the user requesting the operation (string, required)
        task_id: The ID of the task to complete (integer, required)

    Returns:
        Dict with task_id (integer), status (string), and title (string)
    """
    try:
        # Input validation
        if not user_id:
            raise ValidationError("user_id is required")
        if not task_id:
            raise ValidationError("task_id is required")

        # Use user_id as string for database operations (consistent with User model)
        user_id_str = str(user_id)

        # Get database session
        db = _get_db_session()
        task_service = TaskService(db)

        try:
            # Get the task to check if it exists and if user owns it
            task = task_service.get_task_by_id(task_id)
            if not task:
                raise TaskNotFoundError(task_id)

            # Verify user ownership
            if str(task.user_id) != user_id_str:
                raise AuthorizationError("User is not authorized to modify this task")

            # Complete the task
            completed_task = task_service.complete_task(task_id)

            # Return standardized response
            return {
                "task_id": completed_task.id,
                "status": "completed",
                "title": completed_task.title
            }
        finally:
            db.close()

    except Exception as e:
        error_response = handle_mcp_error(e)
        raise e  # Re-raise the exception as MCP tools typically handle errors at a higher level


def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Remove a task.

    Args:
        user_id: The ID of the user requesting the operation (string, required)
        task_id: The ID of the task to delete (integer, required)

    Returns:
        Dict with task_id (integer), status (string), and title (string)
    """
    try:
        # Input validation
        if not user_id:
            raise ValidationError("user_id is required")
        if not task_id:
            raise ValidationError("task_id is required")

        # Use user_id as string for database operations (consistent with User model)
        user_id_str = str(user_id)

        # Get database session
        db = _get_db_session()
        task_service = TaskService(db)

        try:
            # Get the task to check if it exists and if user owns it
            task = task_service.get_task_by_id(task_id)
            if not task:
                raise TaskNotFoundError(task_id)

            # Verify user ownership
            if str(task.user_id) != user_id_str:
                raise AuthorizationError("User is not authorized to delete this task")

            # Store task details before deletion for response
            task_title = task.title
            task_id_result = task.id

            # Delete the task
            deleted = task_service.delete_task(task_id)

            if not deleted:
                raise TaskNotFoundError(task_id)

            # Return standardized response
            return {
                "task_id": task_id_result,
                "status": "deleted",
                "title": task_title
            }
        finally:
            db.close()

    except Exception as e:
        error_response = handle_mcp_error(e)
        raise e  # Re-raise the exception as MCP tools typically handle errors at a higher level


def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update task title or description.

    Args:
        user_id: The ID of the user requesting the operation (string, required)
        task_id: The ID of the task to update (integer, required)
        title: New title for the task (string, optional)
        description: New description for the task (string, optional)

    Returns:
        Dict with task_id (integer), status (string), and title (string)
    """
    try:
        # Input validation
        if not user_id:
            raise ValidationError("user_id is required")
        if not task_id:
            raise ValidationError("task_id is required")
        if title is None and description is None:
            raise ValidationError("At least one of title or description must be provided")

        # Use user_id as string for database operations (consistent with User model)
        user_id_str = str(user_id)

        # Get database session
        db = _get_db_session()
        task_service = TaskService(db)

        try:
            # Get the task to check if it exists and if user owns it
            task = task_service.get_task_by_id(task_id)
            if not task:
                raise TaskNotFoundError(task_id)

            # Verify user ownership
            if str(task.user_id) != user_id_str:
                raise AuthorizationError("User is not authorized to update this task")

            # Prepare update data
            from .models.task import TaskUpdate
            task_update_data = TaskUpdate(
                title=title.strip() if title else None,
                description=description.strip() if description else None
            )

            # Update the task
            updated_task = task_service.update_task(task_id, task_update_data)

            # Return standardized response
            return {
                "task_id": updated_task.id,
                "status": "updated",
                "title": updated_task.title
            }
        finally:
            db.close()

    except Exception as e:
        error_response = handle_mcp_error(e)
        raise e  # Re-raise the exception as MCP tools typically handle errors at a higher level