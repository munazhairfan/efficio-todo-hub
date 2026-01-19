from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.models import BaseModel


class Message(BaseModel):
    """
    Represents a single exchange in a conversation, containing the user's input and the AI's response
    """
    __tablename__ = "messages"

    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Foreign key to users table
    role = Column(String(20), nullable=False)  # Either "user" or "assistant"
    content = Column(Text, nullable=False)  # The actual content of the message
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    metadata_json = Column(String, nullable=True)  # Additional information about the message (for future tool usage)

    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")


# Pydantic models for API
from pydantic import BaseModel as PydanticBaseModel, validator
from typing import Optional


class MessageCreate(PydanticBaseModel):
    conversation_id: Optional[int] = None  # Optional for new conversations
    user_id: int
    role: str
    content: str

    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'assistant']:
            raise ValueError('Role must be either "user" or "assistant"')
        return v

    @validator('content')
    def validate_content(cls, v):
        if len(v) < 1 or len(v) > 10000:
            raise ValueError('Content must be between 1 and 10000 characters')
        return v


class MessageResponse(PydanticBaseModel):
    id: int
    conversation_id: int
    user_id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True