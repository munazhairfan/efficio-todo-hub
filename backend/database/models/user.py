from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
import uuid
from datetime import datetime
from typing import Optional
import pytz
from .base import BaseUUIDModel
from pydantic import EmailStr


class User(BaseUUIDModel, table=True):
    """
    User model with identity reference for data isolation per data-model.md
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

    email: EmailStr = Field(unique=True, nullable=False, max_length=255)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(pytz.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )