"""Service class to handle message-related operations."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime

from src.models.message import Message, MessageCreate
from src.models.conversation import Conversation


class MessageService:
    """
    Service class to handle message-related operations
    """

    def __init__(self, db: Session):
        self.db = db

    def create_message(self, message_data: MessageCreate) -> Message:
        """
        Create a new message
        """
        try:
            message = Message(
                conversation_id=message_data.conversation_id,
                user_id=message_data.user_id,
                role=message_data.role,
                content=message_data.content
            )
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            return message
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """
        Get message by ID
        """
        try:
            return self.db.query(Message).filter(Message.id == message_id).first()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_messages_by_conversation(self, conversation_id: int) -> List[Message]:
        """
        Get all messages for a conversation
        """
        try:
            return (
                self.db.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.timestamp.asc())
                .all()
            )
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_recent_messages(self, conversation_id: int, limit: int = 10) -> List[Message]:
        """
        Get recent messages for a conversation (most recent first)
        """
        try:
            return (
                self.db.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.timestamp.desc())
                .limit(limit)
                .all()
            )
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_message(self, message_id: int) -> bool:
        """
        Delete a message by ID
        """
        try:
            message = self.get_message_by_id(message_id)
            if message:
                self.db.delete(message)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_message_content(self, message_id: int, content: str) -> Optional[Message]:
        """
        Update message content
        """
        try:
            message = self.get_message_by_id(message_id)
            if message:
                message.content = content
                message.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(message)
            return message
        except SQLAlchemyError:
            self.db.rollback()
            raise