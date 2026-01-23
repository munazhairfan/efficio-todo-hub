"""Task model for the todo application."""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Represents a single item in a user's to-do list, containing id, title, description, status, and user association
    """
    __tablename__ = "todos"  # Use 'todos' table name to match existing database schema

    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, index=True))
    user_id: str = Field(sa_column=Column(String, nullable=False, index=True))  # Foreign key to users table (matches frontend User.id format)
    title: str = Field(sa_column=Column(String, nullable=False))  # Title of the task
    description: Optional[str] = Field(sa_column=Column(Text, nullable=True))  # Detailed description of the task
    completed: bool = Field(sa_column=Column(Boolean, default=False, nullable=False))  # Whether the task is completed or not
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))

    # Relationship to user (if user model exists)
    # user = relationship("User", back_populates="tasks")


# SQLModel models for API
from sqlmodel import SQLModel
from typing import Optional


class TaskCreate(SQLModel):
    user_id: str
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(SQLModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime