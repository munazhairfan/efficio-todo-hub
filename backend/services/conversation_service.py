from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select
from api.models.conversation_state import ConversationState, ConversationStateCreate, ConversationStateUpdate


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation_state(self, conversation_data: ConversationStateCreate) -> ConversationState:
        """Create a new conversation state"""
        # Set expiration time (e.g., 1 hour from creation)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        conversation_state = ConversationState(
            session_id=conversation_data.session_id,
            current_intent=conversation_data.current_intent,
            pending_clarifications=conversation_data.pending_clarifications,
            context_data=conversation_data.context_data,
            expires_at=expires_at
        )

        self.session.add(conversation_state)
        self.session.commit()
        self.session.refresh(conversation_state)

        return conversation_state

    def get_conversation_state(self, session_id: str) -> Optional[ConversationState]:
        """Get conversation state by session ID"""
        statement = select(ConversationState).where(ConversationState.session_id == session_id)
        conversation = self.session.exec(statement).first()

        # Check if conversation has expired
        if conversation and conversation.expires_at < datetime.utcnow():
            self.delete_conversation_state(session_id)
            return None

        return conversation

    def update_conversation_state(self, session_id: str, update_data: ConversationStateUpdate) -> Optional[ConversationState]:
        """Update conversation state by session ID"""
        conversation = self.get_conversation_state(session_id)
        if not conversation:
            return None

        # Update fields if provided
        if update_data.current_intent is not None:
            conversation.current_intent = update_data.current_intent
        if update_data.pending_clarifications is not None:
            conversation.pending_clarifications = update_data.pending_clarifications
        if update_data.context_data is not None:
            conversation.context_data = update_data.context_data
        if update_data.expires_at is not None:
            conversation.expires_at = update_data.expires_at

        conversation.updated_at = datetime.utcnow()

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def delete_conversation_state(self, session_id: str) -> bool:
        """Delete conversation state by session ID"""
        conversation = self.get_conversation_state(session_id)
        if not conversation:
            return False

        self.session.delete(conversation)
        self.session.commit()
        return True

    def clear_expired_conversations(self) -> int:
        """Remove all expired conversation states and return count of deleted items"""
        statement = select(ConversationState).where(ConversationState.expires_at < datetime.utcnow())
        expired_conversations = self.session.exec(statement).all()

        count = 0
        for conversation in expired_conversations:
            self.session.delete(conversation)
            count += 1

        self.session.commit()
        return count

    def add_pending_clarification(self, session_id: str, clarification: str) -> Optional[ConversationState]:
        """Add a clarification to the pending list"""
        conversation = self.get_conversation_state(session_id)
        if not conversation:
            return None

        if clarification not in conversation.pending_clarifications:
            conversation.pending_clarifications.append(clarification)

        conversation.updated_at = datetime.utcnow()
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def remove_pending_clarification(self, session_id: str, clarification: str) -> Optional[ConversationState]:
        """Remove a clarification from the pending list"""
        conversation = self.get_conversation_state(session_id)
        if not conversation:
            return None

        if clarification in conversation.pending_clarifications:
            conversation.pending_clarifications.remove(clarification)

        conversation.updated_at = datetime.utcnow()
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def get_active_conversation_state(self, session_id: str) -> Optional[ConversationState]:
        """Get conversation state only if it's not expired"""
        conversation = self.get_conversation_state(session_id)
        if conversation and conversation.expires_at >= datetime.utcnow():
            return conversation
        return None