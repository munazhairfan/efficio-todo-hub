from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select
from api.models.conversation_state import ConversationState


class ConversationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, conversation_state: ConversationState) -> ConversationState:
        """Create a new conversation state in the database"""
        self.session.add(conversation_state)
        self.session.commit()
        self.session.refresh(conversation_state)
        return conversation_state

    def get_by_session_id(self, session_id: str) -> Optional[ConversationState]:
        """Get conversation state by session ID"""
        statement = select(ConversationState).where(ConversationState.session_id == session_id)
        return self.session.exec(statement).first()

    def get_by_id(self, id: str) -> Optional[ConversationState]:
        """Get conversation state by ID"""
        statement = select(ConversationState).where(ConversationState.id == id)
        return self.session.exec(statement).first()

    def update(self, conversation_state: ConversationState) -> ConversationState:
        """Update an existing conversation state"""
        self.session.add(conversation_state)
        self.session.commit()
        self.session.refresh(conversation_state)
        return conversation_state

    def delete_by_session_id(self, session_id: str) -> bool:
        """Delete conversation state by session ID"""
        conversation = self.get_by_session_id(session_id)
        if not conversation:
            return False

        self.session.delete(conversation)
        self.session.commit()
        return True

    def delete_by_id(self, id: str) -> bool:
        """Delete conversation state by ID"""
        conversation = self.get_by_id(id)
        if not conversation:
            return False

        self.session.delete(conversation)
        self.session.commit()
        return True

    def get_all_expired(self) -> List[ConversationState]:
        """Get all expired conversation states"""
        statement = select(ConversationState).where(ConversationState.expires_at < datetime.utcnow())
        return self.session.exec(statement).all()

    def delete_expired(self) -> int:
        """Delete all expired conversation states and return count of deleted items"""
        expired_conversations = self.get_all_expired()
        count = 0
        for conversation in expired_conversations:
            self.session.delete(conversation)
            count += 1

        self.session.commit()
        return count

    def get_all_by_session_ids(self, session_ids: List[str]) -> List[ConversationState]:
        """Get all conversation states for a list of session IDs"""
        statement = select(ConversationState).where(ConversationState.session_id.in_(session_ids))
        return self.session.exec(statement).all()