from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from api.models.error_context import (
    ErrorContext, ErrorContextCreate, ErrorContextUpdate, ErrorContextResponse, ErrorTypeEnum
)
from src.services.error_service import ErrorService
from src.repositories.error_repository import ErrorRepository
from src.database import get_session


router = APIRouter(prefix="/api/error", tags=["error"])


@router.post("/handle", response_model=Dict[str, Any])
async def handle_error(
    *,
    session: Session = Depends(get_session),
    data: Dict[str, Any]
):
    """
    Report an error and get user-friendly response.
    """
    # Extract required fields
    error_type_str = data.get("errorType")
    original_request = data.get("originalRequest", {})
    technical_details = data.get("technicalDetails", "")

    # Validate error type
    try:
        error_type = ErrorTypeEnum(error_type_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid errorType. Must be one of: {[e.value for e in ErrorTypeEnum]}"
        )

    # Validate required fields
    if not error_type_str:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="errorType is required"
        )

    # Initialize services
    error_service = ErrorService(session)

    # Generate user-friendly message based on error type
    user_messages = {
        ErrorTypeEnum.USER_INPUT: "I didn't understand your request. Could you rephrase that?",
        ErrorTypeEnum.SYSTEM_FAILURE: "Something went wrong on my end. I'm looking into it.",
        ErrorTypeEnum.NETWORK_ISSUE: "I'm having trouble connecting. Please try again in a moment.",
        ErrorTypeEnum.VALIDATION_ERROR: "Some of the information you provided isn't quite right. Could you check it?"
    }

    user_message = user_messages.get(error_type, "An unexpected error occurred. Let me try to help.")

    # Generate suggested actions based on error type
    suggested_actions = []
    if error_type == ErrorTypeEnum.USER_INPUT:
        suggested_actions = [
            "Try rephrasing your request with more specific details",
            "Break your request into smaller, more specific parts"
        ]
    elif error_type == ErrorTypeEnum.VALIDATION_ERROR:
        suggested_actions = [
            "Check the format of your request",
            "Verify that all required information is provided"
        ]
    elif error_type in [ErrorTypeEnum.SYSTEM_FAILURE, ErrorTypeEnum.NETWORK_ISSUE]:
        suggested_actions = [
            "Wait a moment and try again",
            "Check your internet connection if the problem persists"
        ]

    # Create error context with user-friendly information
    error_data = ErrorContextCreate(
        error_type=error_type,
        original_request=original_request,
        error_message=user_message,
        suggested_actions=suggested_actions,
        technical_details=technical_details
    )

    error_context = error_service.create_error_context(error_data)

    # Prepare response
    response_data = {
        "userMessage": user_message,
        "suggestedActions": suggested_actions,
        "canRetry": error_type in [ErrorTypeEnum.SYSTEM_FAILURE, ErrorTypeEnum.NETWORK_ISSUE],
        "errorId": error_context.id,
        "handled": True
    }

    return response_data


@router.get("/{error_id}", response_model=ErrorContextResponse)
async def get_error_context(
    error_id: str,
    session: Session = Depends(get_session)
):
    """
    Get error context by ID.
    """
    error_repo = ErrorRepository(session)
    error_context = error_repo.get_by_id(error_id)

    if not error_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error context not found"
        )

    # Convert to response model
    response = ErrorContextResponse(
        id=error_context.id,
        error_type=error_context.error_type,
        original_request=error_context.original_request,
        error_message=error_context.error_message,
        suggested_actions=error_context.suggested_actions,
        timestamp=error_context.timestamp,
        handled=error_context.handled,
        technical_details=error_context.technical_details
    )

    return response


@router.put("/{error_id}/mark-handled", response_model=ErrorContextResponse)
async def mark_error_as_handled(
    error_id: str,
    session: Session = Depends(get_session)
):
    """
    Mark an error as handled.
    """
    error_repo = ErrorRepository(session)
    error_context = error_repo.mark_as_handled(error_id)

    if not error_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error context not found"
        )

    # Convert to response model
    response = ErrorContextResponse(
        id=error_context.id,
        error_type=error_context.error_type,
        original_request=error_context.original_request,
        error_message=error_context.error_message,
        suggested_actions=error_context.suggested_actions,
        timestamp=error_context.timestamp,
        handled=error_context.handled,
        technical_details=error_context.technical_details
    )

    return response


@router.get("/", response_model=List[ErrorContextResponse])
async def get_all_errors(
    session: Session = Depends(get_session),
    handled: Optional[bool] = None,
    error_type: Optional[str] = None
):
    """
    Get all errors with optional filters.
    """
    error_repo = ErrorRepository(session)

    if handled is not None:
        errors = error_repo.get_all_unhandled() if not handled else error_repo.get_all()
    else:
        errors = error_repo.get_all()

    # Filter by error type if specified
    if error_type:
        try:
            error_type_enum = ErrorTypeEnum(error_type)
            errors = [error for error in errors if error.error_type == error_type_enum]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid errorType. Must be one of: {[e.value for e in ErrorTypeEnum]}"
            )

    # Convert to response models
    response_list = []
    for error in errors:
        response = ErrorContextResponse(
            id=error.id,
            error_type=error.error_type,
            original_request=error.original_request,
            error_message=error.error_message,
            suggested_actions=error.suggested_actions,
            timestamp=error.timestamp,
            handled=error.handled,
            technical_details=error.technical_details
        )
        response_list.append(response)

    return response_list


@router.delete("/{error_id}")
async def delete_error_context(
    error_id: str,
    session: Session = Depends(get_session)
):
    """
    Delete error context by ID.
    """
    error_repo = ErrorRepository(session)
    deleted = error_repo.delete(error_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error context not found"
        )

    return {"message": "Error context deleted successfully"}


@router.post("/batch-handle", response_model=List[Dict[str, Any]])
async def batch_handle_errors(
    *,
    session: Session = Depends(get_session),
    errors: List[Dict[str, Any]]
):
    """
    Handle multiple errors in a batch.
    """
    error_service = ErrorService(session)
    results = []

    for error_data in errors:
        # Extract required fields
        error_type_str = error_data.get("errorType")
        original_request = error_data.get("originalRequest", {})
        technical_details = error_data.get("technicalDetails", "")

        # Validate error type
        try:
            error_type = ErrorTypeEnum(error_type_str)
        except ValueError:
            results.append({
                "success": False,
                "error": f"Invalid errorType: {error_type_str}",
                "original_data": error_data
            })
            continue

        # Validate required fields
        if not error_type_str:
            results.append({
                "success": False,
                "error": "errorType is required",
                "original_data": error_data
            })
            continue

        # Generate user-friendly message based on error type
        user_messages = {
            ErrorTypeEnum.USER_INPUT: "I didn't understand your request. Could you rephrase that?",
            ErrorTypeEnum.SYSTEM_FAILURE: "Something went wrong on my end. I'm looking into it.",
            ErrorTypeEnum.NETWORK_ISSUE: "I'm having trouble connecting. Please try again in a moment.",
            ErrorTypeEnum.VALIDATION_ERROR: "Some of the information you provided isn't quite right. Could you check it?"
        }

        user_message = user_messages.get(error_type, "An unexpected error occurred. Let me try to help.")

        # Generate suggested actions based on error type
        suggested_actions = []
        if error_type == ErrorTypeEnum.USER_INPUT:
            suggested_actions = [
                "Try rephrasing your request with more specific details",
                "Break your request into smaller, more specific parts"
            ]
        elif error_type == ErrorTypeEnum.VALIDATION_ERROR:
            suggested_actions = [
                "Check the format of your request",
                "Verify that all required information is provided"
            ]
        elif error_type in [ErrorTypeEnum.SYSTEM_FAILURE, ErrorTypeEnum.NETWORK_ISSUE]:
            suggested_actions = [
                "Wait a moment and try again",
                "Check your internet connection if the problem persists"
            ]

        # Create error context with user-friendly information
        error_context_data = ErrorContextCreate(
            error_type=error_type,
            original_request=original_request,
            error_message=user_message,
            suggested_actions=suggested_actions,
            technical_details=technical_details
        )

        error_context = error_service.create_error_context(error_context_data)

        results.append({
            "success": True,
            "userMessage": user_message,
            "suggestedActions": suggested_actions,
            "canRetry": error_type in [ErrorTypeEnum.SYSTEM_FAILURE, ErrorTypeEnum.NETWORK_ISSUE],
            "errorId": error_context.id,
            "handled": True
        })

    return results