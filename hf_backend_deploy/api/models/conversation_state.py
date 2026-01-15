from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, JSON
import uuid
from enum import Enum


class ConversationState(SQLModel, table=True):
    """
    Represents the current context of the user interaction, including pending clarifications and user intent
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    session_id: str = Field(index=True)
    current_intent: Optional[str] = Field(default=None)
    pending_clarifications: List[str] = Field(default=[], sa_column=Column('pending_clarifications', JSON))
    context_data: Dict[str, Any] = Field(default={}, sa_column=Column('context_data', JSON))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow))
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'created_at' not in kwargs or kwargs['created_at'] is None:
            self.created_at = datetime.utcnow()
        if 'updated_at' not in kwargs or kwargs['updated_at'] is None:
            self.updated_at = datetime.utcnow()


# Pydantic model for API requests/responses
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ConversationStateCreate(BaseModel):
    session_id: str
    current_intent: Optional[str] = None
    pending_clarifications: List[str] = []
    context_data: Dict[str, Any] = {}


class ConversationStateUpdate(BaseModel):
    current_intent: Optional[str] = None
    pending_clarifications: Optional[List[str]] = None
    context_data: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None


class ConversationStateResponse(BaseModel):
    id: str
    session_id: str
    current_intent: Optional[str]
    pending_clarifications: List[str]
    context_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    expires_at: datetime