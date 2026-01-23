"""Main FastAPI application."""

import sys
import os
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import Dict, Any
import uuid

# Import using relative imports from within src package
from .api.chat import router as chat_router
from .middleware.rate_limiter import RateLimitMiddleware

# Import conversation components directly
from api.models.conversation_state import (
    ConversationState, ConversationStateCreate, ConversationStateUpdate, ConversationStateResponse
)
from services.conversation_service import ConversationService
from utils.intent_detector import get_intent_detector
from utils.question_generator import get_question_generator
from utils.ambiguous_pattern_matcher import get_ambiguous_pattern_matcher
from utils.vague_term_detector import get_vague_term_detector
from database import get_session
from src.services.task_intelligence_service import task_intelligence_service

# Create the FastAPI app
app = FastAPI(
    title="Efficio Todo Hub - Chat API",
    description="API for chat and conversation handling",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware temporarily disabled due to asyncpg import issues
# app.add_middleware(RateLimitMiddleware)

# Add middleware to normalize URL paths (fix double slashes)
@app.middleware("http")
async def normalize_url_middleware(request, call_next):
    # Normalize double slashes in the URL path
    if '//' in request.url.path:
        normalized_path = request.url.path.replace('//', '/')
        # Update the request URL with the normalized path
        request.scope['path'] = normalized_path

    response = await call_next(request)
    return response

# Include API routes
app.include_router(chat_router)

# Import and include API chat routes
try:
    from api.routes.chat import router as api_chat_router
    app.include_router(api_chat_router)
except ImportError:
    print("Could not import API chat router - this may be expected depending on the deployment environment")

# Directly add the conversation clarify endpoint to ensure it's available
from src.core.dependencies import get_current_user
from src.models.user import User

@app.post("/api/conversation/clarify", response_model=Dict[str, Any])
async def clarify_conversation_direct(
    data: Dict[str, Any],
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a request that requires clarification or submit clarifying information.
    Direct implementation to ensure endpoint availability.
    """
    # Extract fields with more flexible handling
    session_id = data.get("sessionId") or data.get("session_id") or str(uuid.uuid4())
    user_input = data.get("input", data.get("message", data.get("text", "")))
    context = data.get("context", data.get("ctx", {}))

    # More flexible validation - generate a session ID if not provided
    if not user_input:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="input is required"
        )

    # Initialize services
    conv_service = ConversationService(session)

    # Use authenticated user's ID if available, otherwise try context, then mark as unauthenticated
    if current_user and hasattr(current_user, 'id') and current_user.id:
        user_id = str(current_user.id)
    else:
        # Extract user ID from context if available
        user_id = context.get("user_id")
        if not user_id or user_id in ["temp_user", "guest_user", "null", "undefined", "", "None"]:
            # If no valid user_id in context, default to indicating unauthenticated state
            user_id = "unauthenticated_user"

    # First, try to process the user input through the task intelligence service
    # This handles task-related requests with specific logic
    task_result = task_intelligence_service.process_task_request(str(user_id), user_input)

    if task_result and task_result.get("handled_locally"):
        # The request was handled by the task intelligence service
        # Return the response directly
        response_data = {
            "responseType": "success",
            "message": task_result["response"],
            "clarifyingQuestions": [],
            "suggestedActions": [],
            "conversationId": None,
            "analysis": {
                "intent": {"is_ambiguous": False},
                "ambiguity": {"is_ambiguous": False},
                "vagueness": {"is_vague": False}
            }
        }
        return response_data

    # If the task intelligence service didn't handle it, fall back to the old detection system
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

# Import conversation router with error handling - try different import paths
try:
    # Try relative import from package structure (going up from src to backend root)
    from ..api.routes.conversation import router as conversation_router
    app.include_router(conversation_router)
except ImportError as e:
    try:
        # Try absolute import assuming backend is in Python path
        from api.routes.conversation import router as conversation_router
        app.include_router(conversation_router)
    except ImportError as e2:
        print(f"Warning: Could not import conversation router: {e}, {e2}")
        print(f"Error details: {type(e2).__name__}: {e2}")

# Import error router with error handling - try different import paths
try:
    # Try relative import from package structure (going up from src to backend root)
    from ..api.routes.error import router as error_router
    app.include_router(error_router)
except ImportError as e:
    try:
        # Try absolute import assuming backend is in Python path
        from api.routes.error import router as error_router
        app.include_router(error_router)
    except ImportError as e2:
        print(f"Warning: Could not import error router: {e}, {e2}")
        print(f"Error details: {type(e2).__name__}: {e2}")

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"message": "Efficio Todo Hub Chat API is running!"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# Additional endpoints for Hugging Face Spaces compatibility
@app.get("/startup-health")
def startup_health():
    """Startup health check for Hugging Face Spaces."""
    try:
        # Verify required environment variables are available
        required_vars = ["DATABASE_URL"]
        missing_vars = []

        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            return {
                "status": "unhealthy",
                "missing_environment_variables": missing_vars,
                "timestamp": datetime.utcnow()
            }

        return {
            "status": "healthy",
            "environment_ok": True,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }