from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
import uuid
from datetime import datetime
from typing import Optional
import pytz
from .base import BaseUUIDModel
from pydantic import field_validator


class Todo(BaseUUIDModel, table=True):
    """
    Todo model with user association per data-model.md specifications
    """
    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            PostgresUUID(as_uuid=True),
            primary_key=True,
            server_default=func.gen_random_uuid(),
            nullable=False
        )
    )

    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(
        sa_column=Column(
            PostgresUUID(as_uuid=True),
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