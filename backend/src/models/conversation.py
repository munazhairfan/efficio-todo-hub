from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.models import BaseModel


class Conversation(BaseModel):
    """
    Represents a thread of messages between a user and the AI assistant
    """
    __tablename__ = "conversations"

    user_id = Column(Integer, nullable=False, index=True)  # Foreign key to users table
    title = Column(String(100), nullable=True)  # Auto-generated title based on initial message

    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


# Pydantic models for API
from pydantic import BaseModel as PydanticBaseModel
from typing import Optional


class ConversationCreate(PydanticBaseModel):
    user_id: int
    title: Optional[str] = None


class ConversationResponse(PydanticBaseModel):
    id: int
    user_id: int
    title: Optional[str] = None

    class Config:
        from_attributes = True