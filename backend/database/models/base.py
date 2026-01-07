from sqlmodel import SQLModel
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
import uuid
from datetime import datetime
from typing import Optional
import pytz


class BaseUUIDModel(SQLModel):
    """
    Base model with UUID primary key support per data-model.md specifications
    and timezone-aware timestamp fields per research.md
    """
    pass  # Simple base class without fields that can be extended