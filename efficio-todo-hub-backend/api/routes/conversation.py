from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..models.conversation_state import (
    ConversationState, ConversationStateCreate, ConversationStateUpdate, ConversationStateResponse
)
from ..services.conversation_service import ConversationService
from ..utils.intent_detector import get_intent_detector
from ..utils.question_generator import get_question_generator
from ..utils.ambiguous_pattern_matcher import get_ambiguous_pattern_matcher
from ..utils.vague_term_detector import get_vague_term_detector
from ..database import get_session


router = APIRouter(prefix="/api/conversation", tags=["conversation"])


@router.post("/clarify", response_model=Dict[str, Any])
async def clarify_conversation(
    *,
    session: Session = Depends(get_session),
    data: Dict[str, Any]
):
    """
    Submit a request that requires clarification or submit clarifying information.
    """
    # Extract required fields
    session_id = data.get("sessionId")
    user_input = data.get("input", "")
    context = data.get("context", {})

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="sessionId is required"
        )

    if not user_input:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="input is required"
        )

    # Initialize services
    conv_service = ConversationService(session)
    intent_detector = get_intent_detector()
    question_generator = get_question_generator()
    pattern_matcher = get_ambiguous_pattern_matcher()
    vague_detector = get_vague_term_detector()

    # Get existing conversation state or create new one
    conversation = conv_service.get_conversation_state(session_id)
    if not conversation:
        # Create new conversation state
        conv_create = ConversationStateCreate(
            session_id=session_id,
            current_intent=user_input,
            context_data=context
        )
        conversation = conv_service.create_conversation_state(conv_create)

    # Analyze the user input
    intent_result = intent_detector.classify_input(user_input)
    ambiguity_analysis = pattern_matcher.analyze_ambiguity(user_input)
    vagueness_analysis = vague_detector.analyze_vagueness(user_input)

    # Determine response type based on analysis
    response_type = "success"  # default
    message = ""
    clarifying_questions = []
    suggested_actions = []

    # Check if input is ambiguous or needs clarification
    if intent_result['is_ambiguous'] or ambiguity_analysis['is_ambiguous'] or vagueness_analysis['is_vague']:
        response_type = "clarification"

        # Generate clarifying questions based on analysis
        if ambiguity_analysis['clarification_questions']:
            clarifying_questions.extend(ambiguity_analysis['clarification_questions'])
        elif vagueness_analysis['suggestions']:
            # Convert suggestions to questions
            for suggestion in vagueness_analysis['suggestions'][:2]:
                question = f"To be clear: {suggestion.replace('?', '').replace('.', '')}?"
                clarifying_questions.append(question)
        else:
            # Generate generic clarifying questions
            clarifying_questions = question_generator.generate_for_ambiguity_analysis(ambiguity_analysis)

        # Limit to 3 questions to avoid overwhelming the user
        clarifying_questions = clarifying_questions[:3]

        message = "I need some clarification to help you better."
    else:
        # Input is clear, process normally
        response_type = "success"
        message = f"I understand you want to: {user_input}"

        # Update the conversation state with the current intent
        update_data = ConversationStateUpdate(current_intent=user_input)
        conv_service.update_conversation_state(session_id, update_data)

    # Check if confirmation is needed for critical actions
    if intent_detector.requires_confirmation(user_input):
        response_type = "clarification"
        confirmation_question = question_generator.generate_confirmation_question()
        clarifying_questions.insert(0, confirmation_question)
        message = "This action requires confirmation."

    # Prepare response
    response_data = {
        "responseType": response_type,
        "message": message,
        "clarifyingQuestions": clarifying_questions,
        "suggestedActions": suggested_actions,
        "conversationId": conversation.id if conversation else None,
        "analysis": {
            "intent": intent_result,
            "ambiguity": ambiguity_analysis,
            "vagueness": vagueness_analysis
        }
    }

    return response_data


@router.get("/state/{session_id}", response_model=ConversationStateResponse)
async def get_conversation_state(
    session_id: str,
    session: Session = Depends(get_session)
):
    """
    Retrieve the current state of a conversation.
    """
    conv_service = ConversationService(session)
    conversation = conv_service.get_conversation_state(session_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation state not found"
        )

    # Convert to response model
    response = ConversationStateResponse(
        id=conversation.id,
        session_id=conversation.session_id,
        current_intent=conversation.current_intent,
        pending_clarifications=conversation.pending_clarifications,
        context_data=conversation.context_data,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        expires_at=conversation.expires_at
    )

    return response


@router.post("/state/{session_id}", response_model=ConversationStateResponse)
async def update_conversation_state(
    session_id: str,
    *,
    session: Session = Depends(get_session),
    data: ConversationStateUpdate
):
    """
    Update the conversation state.
    """
    conv_service = ConversationService(session)
    conversation = conv_service.update_conversation_state(session_id, data)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation state not found"
        )

    # Convert to response model
    response = ConversationStateResponse(
        id=conversation.id,
        session_id=conversation.session_id,
        current_intent=conversation.current_intent,
        pending_clarifications=conversation.pending_clarifications,
        context_data=conversation.context_data,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        expires_at=conversation.expires_at
    )

    return response


@router.delete("/state/{session_id}")
async def delete_conversation_state(
    session_id: str,
    session: Session = Depends(get_session)
):
    """
    Delete the conversation state.
    """
    conv_service = ConversationService(session)
    deleted = conv_service.delete_conversation_state(session_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation state not found"
        )

    return {"message": "Conversation state deleted successfully"}


@router.post("/clear-expired")
async def clear_expired_conversations(
    session: Session = Depends(get_session)
):
    """
    Manually clear all expired conversation states.
    """
    conv_service = ConversationService(session)
    deleted_count = conv_service.clear_expired_conversations()

    return {"deleted_count": deleted_count, "message": f"Cleared {deleted_count} expired conversations"}


# Additional helper endpoints

@router.post("/analyze-input")
async def analyze_user_input(
    *,
    data: Dict[str, Any]
):
    """
    Analyze user input for ambiguity, vagueness, and intent without storing conversation state.
    """
    user_input = data.get("input", "")
    if not user_input:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="input is required"
        )

    intent_detector = get_intent_detector()
    pattern_matcher = get_ambiguous_pattern_matcher()
    vague_detector = get_vague_term_detector()
    question_generator = get_question_generator()

    # Perform analyses
    intent_result = intent_detector.classify_input(user_input)
    ambiguity_analysis = pattern_matcher.analyze_ambiguity(user_input)
    vagueness_analysis = vague_detector.analyze_vagueness(user_input)

    # Generate clarifying questions if needed
    clarifying_questions = []
    if intent_result['is_ambiguous'] or ambiguity_analysis['is_ambiguous'] or vagueness_analysis['is_vague']:
        clarifying_questions = question_generator.generate_for_ambiguity_analysis(ambiguity_analysis)

    return {
        "input": user_input,
        "analysis": {
            "intent": intent_result,
            "ambiguity": ambiguity_analysis,
            "vagueness": vagueness_analysis
        },
        "needs_clarification": intent_result['is_ambiguous'] or ambiguity_analysis['is_ambiguous'] or vagueness_analysis['is_vague'],
        "clarifying_questions": clarifying_questions[:3]  # Limit to 3 questions
    }