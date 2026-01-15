from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message
from datetime import datetime


class ConversationService:
    """
    Service class to handle conversation-related operations
    """

    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """
        Create a new conversation
        """
        try:
            conversation = Conversation(
                user_id=conversation_data.user_id,
                title=conversation_data.title
            )
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            return conversation
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_conversation_by_id(self, conversation_id: int) -> Optional[Conversation]:
        """
        Get conversation by ID
        """
        try:
            return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_conversation_messages(self, conversation_id: int) -> list[Message]:
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

    def update_conversation_title(self, conversation_id: int, title: str) -> Optional[Conversation]:
        """
        Update conversation title
        """
        try:
            conversation = self.get_conversation_by_id(conversation_id)
            if conversation:
                conversation.title = title
                conversation.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(conversation)
            return conversation
        except SQLAlchemyError:
            self.db.rollback()
            raise