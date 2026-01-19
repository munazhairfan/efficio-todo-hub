"""Task service for handling task-related operations."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime

from src.models.task import Task, TaskCreate, TaskUpdate
from src.database.session import get_db


class TaskService:
    """
    Service class to handle task-related operations
    """

    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_data: TaskCreate) -> Task:
        """
        Create a new task
        """
        try:
            task = Task(
                user_id=task_data.user_id,
                title=task_data.title,
                description=task_data.description,
                completed=task_data.completed
            )
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get task by ID
        """
        try:
            return self.db.query(Task).filter(Task.id == task_id).first()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_tasks_by_user(
        self,
        user_id: int,
        status_filter: Optional[str] = "all"
    ) -> List[Task]:
        """
        Get all tasks for a user with optional status filter
        """
        try:
            query = self.db.query(Task).filter(Task.user_id == user_id)

            if status_filter == "pending":
                query = query.filter(Task.completed == False)
            elif status_filter == "completed":
                query = query.filter(Task.completed == True)
            # If status_filter is "all", return all tasks

            return query.order_by(Task.created_at.desc()).all()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update task with provided data
        """
        try:
            task = self.get_task_by_id(task_id)
            if task:
                # Update only the fields that are provided
                if task_data.title is not None:
                    task.title = task_data.title
                if task_data.description is not None:
                    task.description = task_data.description
                if task_data.completed is not None:
                    task.completed = task_data.completed

                task.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(task)
            return task
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_task(self, task_id: int) -> bool:
        """
        Delete task by ID
        """
        try:
            task = self.get_task_by_id(task_id)
            if task:
                self.db.delete(task)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark task as completed
        """
        try:
            task = self.get_task_by_id(task_id)
            if task:
                task.completed = True
                task.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(task)
            return task
        except SQLAlchemyError:
            self.db.rollback()
            raise