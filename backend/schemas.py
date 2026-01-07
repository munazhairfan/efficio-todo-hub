from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class TodoCreate(BaseModel):
    """
    Schema for creating a new todo item.
    Based on data-model.md requirements for TodoCreate.
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=False)


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo item.
    Based on data-model.md requirements for TodoUpdate.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TodoResponse(BaseModel):
    """
    Schema for todo response.
    Based on data-model.md requirements for TodoResponse.
    """
    id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID


class TodoListResponse(BaseModel):
    """
    Schema for todo list response.
    """
    todos: list[TodoResponse]