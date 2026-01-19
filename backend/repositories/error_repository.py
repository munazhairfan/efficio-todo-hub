from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select
from api.models.error_context import ErrorContext, ErrorTypeEnum


class ErrorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, error_context: ErrorContext) -> ErrorContext:
        """Create a new error context in the database"""
        self.session.add(error_context)
        self.session.commit()
        self.session.refresh(error_context)
        return error_context

    def get_by_id(self, id: str) -> Optional[ErrorContext]:
        """Get error context by ID"""
        statement = select(ErrorContext).where(ErrorContext.id == id)
        return self.session.exec(statement).first()

    def update(self, error_context: ErrorContext) -> ErrorContext:
        """Update an existing error context"""
        self.session.add(error_context)
        self.session.commit()
        self.session.refresh(error_context)
        return error_context

    def delete(self, id: str) -> bool:
        """Delete error context by ID"""
        error_context = self.get_by_id(id)
        if not error_context:
            return False

        self.session.delete(error_context)
        self.session.commit()
        return True

    def get_all_unhandled(self) -> List[ErrorContext]:
        """Get all unhandled error contexts"""
        statement = select(ErrorContext).where(ErrorContext.handled == False)
        return self.session.exec(statement).all()

    def get_by_error_type(self, error_type: ErrorTypeEnum) -> List[ErrorContext]:
        """Get all error contexts of a specific type"""
        statement = select(ErrorContext).where(ErrorContext.error_type == error_type)
        return self.session.exec(statement).all()

    def get_recent_errors(self, hours: int = 24) -> List[ErrorContext]:
        """Get all error contexts from the last specified hours"""
        from datetime import timedelta
        time_threshold = datetime.utcnow() - timedelta(hours=hours)

        statement = select(ErrorContext).where(ErrorContext.timestamp >= time_threshold)
        return self.session.exec(statement).all()

    def mark_as_handled(self, id: str) -> Optional[ErrorContext]:
        """Mark an error context as handled"""
        error_context = self.get_by_id(id)
        if not error_context:
            return None

        error_context.handled = True
        return self.update(error_context)

    def get_all(self) -> List[ErrorContext]:
        """Get all error contexts"""
        statement = select(ErrorContext)
        return self.session.exec(statement).all()

    def delete_all_unhandled(self) -> int:
        """Delete all unhandled error contexts and return count of deleted items"""
        unhandled_errors = self.get_all_unhandled()
        count = 0
        for error in unhandled_errors:
            self.session.delete(error)
            count += 1

        self.session.commit()
        return count