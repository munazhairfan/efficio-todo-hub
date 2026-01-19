"""Task model for the todo application."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.models import BaseModel


class Task(BaseModel):
    """
    Represents a single item in a user's to-do list, containing id, title, description, status, and user association
    """
    __tablename__ = "tasks"

    user_id = Column(Integer, nullable=False, index=True)  # Foreign key to users table
    title = Column(String, nullable=False)  # Title of the task
    description = Column(Text, nullable=True)  # Detailed description of the task
    completed = Column(Boolean, default=False, nullable=False)  # Whether the task is completed or not
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to user (if user model exists)
    # user = relationship("User", back_populates="tasks")


# Pydantic models for API
from pydantic import BaseModel as PydanticBaseModel
from typing import Optional


class TaskCreate(PydanticBaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

    class Config:
        from_attributes = True


class TaskUpdate(PydanticBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        from_attributes = True


class TaskResponse(PydanticBaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True