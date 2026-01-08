from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func, ForeignKey
import uuid
from datetime import datetime
from typing import Optional
import pytz
from pydantic import field_validator


class Todo(SQLModel, table=True):
    """
    Todo model with user association per data-model.md specifications
    """
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(
        sa_column=Column(
            ForeignKey("user.id"),
            nullable=False
        )
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )

    @field_validator('title')
    def validate_title(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Title must not be empty')
        return v