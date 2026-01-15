from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from .session import Base


class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamps"""

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BaseModel(Base, TimestampMixin):
    """Base model with common functionality"""
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)