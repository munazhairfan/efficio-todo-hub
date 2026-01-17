from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select
from ..api.models.error_context import ErrorContext, ErrorTypeEnum, ErrorContextCreate, ErrorContextUpdate


class ErrorService:
    def __init__(self, session: Session):
        self.session = session

    def create_error_context(self, error_data: ErrorContextCreate) -> ErrorContext:
        """Create a new error context"""
        error_context = ErrorContext(
            error_type=error_data.error_type,
            original_request=error_data.original_request,
            error_message=error_data.error_message,
            suggested_actions=error_data.suggested_actions,
            technical_details=error_data.technical_details
        )

        self.session.add(error_context)
        self.session.commit()
        self.session.refresh(error_context)

        return error_context

    def get_error_context(self, error_id: str) -> Optional[ErrorContext]:
        """Get error context by ID"""
        statement = select(ErrorContext).where(ErrorContext.id == error_id)
        return self.session.exec(statement).first()

    def update_error_context(self, error_id: str, update_data: ErrorContextUpdate) -> Optional[ErrorContext]:
        """Update error context by ID"""
        error_context = self.get_error_context(error_id)
        if not error_context:
            return None

        # Update fields if provided
        if update_data.error_message is not None:
            error_context.error_message = update_data.error_message
        if update_data.suggested_actions is not None:
            error_context.suggested_actions = update_data.suggested_actions
        if update_data.handled is not None:
            error_context.handled = update_data.handled
        if update_data.technical_details is not None:
            error_context.technical_details = update_data.technical_details

        self.session.add(error_context)
        self.session.commit()
        self.session.refresh(error_context)

        return error_context

    def mark_error_as_handled(self, error_id: str) -> Optional[ErrorContext]:
        """Mark an error as handled"""
        return self.update_error_context(error_id, ErrorContextUpdate(handled=True))

    def get_unhandled_errors(self) -> List[ErrorContext]:
        """Get all unhandled errors"""
        statement = select(ErrorContext).where(ErrorContext.handled == False)
        return self.session.exec(statement).all()

    def delete_error_context(self, error_id: str) -> bool:
        """Delete error context by ID"""
        error_context = self.get_error_context(error_id)
        if not error_context:
            return False

        self.session.delete(error_context)
        self.session.commit()
        return True

    def get_errors_by_type(self, error_type: ErrorTypeEnum) -> List[ErrorContext]:
        """Get all errors of a specific type"""
        statement = select(ErrorContext).where(ErrorContext.error_type == error_type)
        return self.session.exec(statement).all()

    def create_user_friendly_error(
        self,
        error_type: ErrorTypeEnum,
        original_request: Dict[str, Any],
        user_message: str,
        suggested_actions: List[str] = None,
        technical_details: str = None
    ) -> ErrorContext:
        """Create an error context with user-friendly message"""
        if suggested_actions is None:
            suggested_actions = []

        error_data = ErrorContextCreate(
            error_type=error_type,
            original_request=original_request,
            error_message=user_message,
            suggested_actions=suggested_actions,
            technical_details=technical_details
        )

        return self.create_error_context(error_data)