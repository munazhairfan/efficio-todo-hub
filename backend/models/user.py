from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func
import uuid
from datetime import datetime
from typing import Optional
import pytz
from pydantic import EmailStr


class User(SQLModel, table=True):
    """
    User model with identity reference for data isolation per data-model.md
    """
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    email: EmailStr = Field(unique=True, nullable=False, max_length=255)
    password: str = Field(nullable=False, max_length=255)  # Hashed password
    name: Optional[str] = Field(default=None, max_length=255)  # User's full name

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )