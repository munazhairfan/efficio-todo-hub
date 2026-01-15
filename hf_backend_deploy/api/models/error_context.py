from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, JSON, String
import uuid
from enum import Enum


class ErrorTypeEnum(str, Enum):
    USER_INPUT = "user_input"
    SYSTEM_FAILURE = "system_failure"
    NETWORK_ISSUE = "network_issue"
    VALIDATION_ERROR = "validation_error"


class ErrorContext(SQLModel, table=True):
    """
    Information about failures that occurred, including type and suggested remediation paths
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    error_type: ErrorTypeEnum = Field(sa_column=Column('error_type', String, nullable=False))
    original_request: Dict[str, Any] = Field(default={}, sa_column=Column('original_request', JSON))
    error_message: str = Field()
    suggested_actions: List[str] = Field(default=[], sa_column=Column('suggested_actions', JSON))
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow))
    handled: bool = Field(default=False)
    technical_details: Optional[str] = Field(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'timestamp' not in kwargs or kwargs['timestamp'] is None:
            self.timestamp = datetime.utcnow()


# Pydantic model for API requests/responses
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ErrorContextCreate(BaseModel):
    error_type: ErrorTypeEnum
    original_request: Dict[str, Any] = {}
    error_message: str
    suggested_actions: List[str] = []
    technical_details: Optional[str] = None


class ErrorContextUpdate(BaseModel):
    error_message: Optional[str] = None
    suggested_actions: Optional[List[str]] = None
    handled: Optional[bool] = None
    technical_details: Optional[str] = None


class ErrorContextResponse(BaseModel):
    id: str
    error_type: ErrorTypeEnum
    original_request: Dict[str, Any]
    error_message: str
    suggested_actions: List[str]
    timestamp: datetime
    handled: bool
    technical_details: Optional[str]