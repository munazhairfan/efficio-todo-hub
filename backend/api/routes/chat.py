"""
Chat API Routes
Handles chatbot functionality with rate limiting and authentication
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from typing import Dict, Any
import uuid
from datetime import datetime
from src.core.dependencies import get_current_user

from api.models.conversation_state import (
    ConversationState, ConversationStateCreate, ConversationStateUpdate, ConversationStateResponse
)
from services.conversation_service import ConversationService
from utils.intent_detector import get_intent_detector
from utils.question_generator import get_question_generator
from utils.ambiguous_pattern_matcher import get_ambiguous_pattern_matcher
from utils.vague_term_detector import get_vague_term_detector

# Direct import for proper session handling
from src.database.session import get_db as get_session

from src.services.task_intelligence_service import task_intelligence_service
from services.rate_limiter import rate_limiter
from src.services.openrouter_client import call_openrouter


router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=Dict[str, Any])
async def chat_endpoint(
    data: Dict[str, Any],
    session: Session = Depends(get_session),
    authorization: str = Header(None)
):
    """
    Main chat endpoint that handles both conversational and task requests.
    """
    print(f"DEBUG: Chat endpoint called with data: {data}")

    # Extract message with flexible handling
    user_input = data.get("message", data.get("input", data.get("text", "")))
    conversation_id = data.get("conversationId") or data.get("conversation_id")
    context = data.get("context", data.get("ctx", {}))

    print(f"DEBUG: Extracted user_input: {user_input}")
    print(f"DEBUG: Extracted conversation_id: {conversation_id}")
    print(f"DEBUG: Extracted context: {context}")

    if not user_input:
        print("DEBUG: No user input provided")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message is required"
        )

    # Extract user ID from context if available
    user_id = context.get("user_id")
    print(f"DEBUG: Initial user_id from context: {user_id}")

    # If user_id is not found in context OR if it's the special 'auth_extract' value,
    # try to get user ID from authorization header using existing auth system
    if not user_id or user_id == "auth_extract":
        # Try to get user ID from authorization header using existing auth system
        # This would require the request to have proper authorization header
        # For now, we'll check if there's an authorization header and extract user info

        # In the actual request processing, we need to extract the user from the authorization header
        # Since we don't have direct access to the header here, we'll need to modify the approach
        # Let's look for authorization in the context or data
        auth_header = context.get("authorization") or data.get("authorization") or authorization
        print(f"DEBUG: Auth header found: {bool(auth_header)}")

        if auth_header:
            # Process the authorization header to extract user ID
            import re
            # Handle "Bearer <token>" format
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                print("DEBUG: Extracted token from Bearer header")
            else:
                token = auth_header
                print("DEBUG: Using raw auth header as token")

            # Decode JWT token to get user ID (similar to get_current_user logic)
            try:
                from jose import jwt
                from src.core.config import settings
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
                user_id = payload.get("sub") or payload.get("user_id")
                print(f"DEBUG: Decoded user_id from JWT: {user_id}")

                if user_id is None:
                    user_id = "temp_user"
                    print("DEBUG: Setting user_id to temp_user (no sub/user_id found in JWT)")
                else:
                    user_id = str(user_id)  # Ensure it's a string
                    print(f"DEBUG: Converted user_id to string: {user_id}")
            except Exception as e:
                print(f"DEBUG: JWT decode failed: {str(e)}")
                # If token decoding fails, fall back to temp_user
                user_id = "temp_user"
                print("DEBUG: Setting user_id to temp_user due to JWT decode error")
        else:
            # If no authorization provided, default to temp_user
            user_id = "temp_user"
            print("DEBUG: No auth header provided, setting user_id to temp_user")
    # else: user_id already has a value from context, continue with original logic

    print(f"DEBUG: Final user_id: {user_id}")

    # Check rate limit
    print(f"DEBUG: Checking rate limit for user: {user_id}")
    is_allowed, error_msg = rate_limiter.is_allowed(str(user_id))
    if not is_allowed:
        print(f"DEBUG: Rate limit exceeded: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_msg
        )
    else:
        print("DEBUG: Rate limit check passed")

    # Initialize services
    print("DEBUG: Initializing ConversationService")
    try:
        conv_service = ConversationService(session)
        print("DEBUG: ConversationService initialized successfully")
    except Exception as e:
        print(f"DEBUG: ConversationService initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

    # First, try to process through task intelligence service
    print(f"DEBUG: Calling task_intelligence_service with user_id: {user_id}, input: {user_input}")
    try:
        task_result = task_intelligence_service.process_task_request(str(user_id), user_input)
        print(f"DEBUG: Task result received: {task_result}")
    except Exception as e:
        print(f"DEBUG: task_intelligence_service threw exception: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return error response
        return {
            "response": f"Task processing error: {str(e)}",
            "conversationId": str(uuid.uuid4()),
            "type": "error_response"
        }

    if task_result and task_result.get("handled_locally"):
        print("DEBUG: Task was handled locally, returning task response")
        # Task was handled locally, return response directly
        return {
            "response": task_result["response"],
            "conversationId": str(uuid.uuid4()),
            "type": "task_response"
        }

    print("DEBUG: Task not handled locally, proceeding to AI response")
    # For conversation-based responses, use AI
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Respond naturally to the user's messages. If they want to manage tasks, let them know you can help with that. Be friendly and engaging."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    try:
        print("DEBUG: Calling OpenRouter AI service")
        # Call the AI service for a proper conversational response
        ai_response = call_openrouter(messages)
        print(f"DEBUG: OpenRouter response received: {ai_response[:100]}...")

        return {
            "response": ai_response,
            "conversationId": conversation_id or str(uuid.uuid4()),
            "type": "chat_response"
        }
    except Exception as e:
        print(f"DEBUG: OpenRouter call failed: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback if AI call fails
        return {
            "response": f"I understand you said: '{user_input}'. How can I assist you further?",
            "conversationId": conversation_id or str(uuid.uuid4()),
            "type": "fallback_response"
        }


@router.post("/conversation/clarify", response_model=Dict[str, Any])
async def clarify_conversation(
    data: Dict[str, Any],
    session: Session = Depends(get_session)
):
    """
    Submit a request that requires clarification or submit clarifying information.
    """
    print(f"DEBUG: Clarify endpoint called with data: {data}")

    # Extract fields with more flexible handling
    session_id = data.get("sessionId") or data.get("session_id") or str(uuid.uuid4())
    user_input = data.get("input", data.get("message", data.get("text", "")))
    context = data.get("context", data.get("ctx", {}))

    print(f"DEBUG: Clarify - Extracted session_id: {session_id}")
    print(f"DEBUG: Clarify - Extracted user_input: {user_input}")
    print(f"DEBUG: Clarify - Extracted context: {context}")

    # More flexible validation - generate a session ID if not provided
    if not user_input:
        print("DEBUG: Clarify - No user input provided")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="input is required"
        )

    # Extract user ID from context if available
    user_id = context.get("user_id")
    print(f"DEBUG: Clarify - Initial user_id from context: {user_id}")

    # If user_id is not found in context OR if it's the special 'auth_extract' value,
    # try to get user ID from authorization header using existing auth system
    if not user_id or user_id == "auth_extract":
        # Try to get user ID from authorization header using existing auth system
        # Import the existing auth dependency
        from src.core.dependencies import get_current_user
        # This would require the request to have proper authorization header
        # For now, we'll check if there's an authorization header and extract user info

        # In the actual request processing, we need to extract the user from the authorization header
        # Since we don't have direct access to the header here, we'll need to modify the approach
        # Let's look for authorization in the context, data, or parameter
        auth_header = context.get("authorization") or data.get("authorization") or authorization

        print(f"DEBUG: Clarify - Auth header found: {bool(auth_header)}")

        if auth_header:
            # Process the authorization header to extract user ID
            import re
            # Handle "Bearer <token>" format
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                print("DEBUG: Clarify - Extracted token from Bearer header")
            else:
                token = auth_header
                print("DEBUG: Clarify - Using raw auth header as token")

            # Decode JWT token to get user ID (similar to get_current_user logic)
            try:
                from jose import jwt
                from src.core.config import settings
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
                user_id = payload.get("sub") or payload.get("user_id")
                print(f"DEBUG: Clarify - Decoded user_id from JWT: {user_id}")

                if user_id is None:
                    user_id = "temp_user"
                    print("DEBUG: Clarify - Setting user_id to temp_user (no sub/user_id found in JWT)")
                else:
                    user_id = str(user_id)  # Ensure it's a string
                    print(f"DEBUG: Clarify - Converted user_id to string: {user_id}")
            except Exception as e:
                print(f"DEBUG: Clarify - JWT decode failed: {str(e)}")
                # If token decoding fails, fall back to temp_user
                user_id = "temp_user"
                print("DEBUG: Clarify - Setting user_id to temp_user due to JWT decode error")
        else:
            # If no authorization provided, default to temp_user
            user_id = "temp_user"
            print("DEBUG: Clarify - No auth header provided, setting user_id to temp_user")
    # else: user_id already has a value from context, continue with original logic

    print(f"DEBUG: Clarify - Final user_id: {user_id}")

    # Check rate limit for authenticated user
    print(f"DEBUG: Clarify - Checking rate limit for user: {user_id}")
    is_allowed, error_msg = rate_limiter.is_allowed(str(user_id))
    if not is_allowed:
        print(f"DEBUG: Clarify - Rate limit exceeded: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_msg
        )
    else:
        print("DEBUG: Clarify - Rate limit check passed")

    # Initialize services
    print("DEBUG: Clarify - Initializing ConversationService")
    try:
        conv_service = ConversationService(session)
        print("DEBUG: Clarify - ConversationService initialized successfully")
    except Exception as e:
        print(f"DEBUG: Clarify - ConversationService initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

    # First, try to process the user input through the task intelligence service
    # This handles task-related requests with specific logic
    print(f"DEBUG: Clarify - Calling task_intelligence_service with user_id: {user_id}, input: {user_input}")
    try:
        task_result = task_intelligence_service.process_task_request(str(user_id), user_input)
        print(f"DEBUG: Clarify - Task result received: {task_result}")
    except Exception as e:
        print(f"DEBUG: Clarify - task_intelligence_service threw exception: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return error response
        return {
            "responseType": "error",
            "message": f"Task processing error: {str(e)}",
            "clarifyingQuestions": [],
            "suggestedActions": [],
            "conversationId": None,
            "analysis": {
                "intent": {"is_ambiguous": False},
                "ambiguity": {"is_ambiguous": False},
                "vagueness": {"is_vague": False}
            }
        }

    if task_result and task_result.get("handled_locally"):
        # The request was handled by the task intelligence service
        # Return the response directly
        print("DEBUG: Clarify - Task was handled locally, returning task response")
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

    print("DEBUG: Clarify - Task not handled locally, proceeding to fallback system")
    # If the task intelligence service didn't handle it, fall back to the old detection system
    intent_detector = get_intent_detector()
    question_generator = get_question_generator()
    pattern_matcher = get_ambiguous_pattern_matcher()
    vague_detector = get_vague_term_detector()

    # Get existing conversation state or create new one
    print("DEBUG: Clarify - Getting conversation state")
    conversation = conv_service.get_conversation_state(session_id)
    if not conversation:
        print("DEBUG: Clarify - No existing conversation, creating new one")
        # Create new conversation state
        conv_create = ConversationStateCreate(
            session_id=session_id,
            current_intent=user_input,
            context_data=context
        )
        conversation = conv_service.create_conversation_state(conv_create)
        print("DEBUG: Clarify - New conversation created")
    else:
        print("DEBUG: Clarify - Existing conversation found")

    # Analyze the user input
    print("DEBUG: Clarify - Analyzing user input")
    intent_result = intent_detector.classify_input(user_input)
    ambiguity_analysis = pattern_matcher.analyze_ambiguity(user_input)
    vagueness_analysis = vague_detector.analyze_vagueness(user_input)

    print(f"DEBUG: Clarify - Analysis results - intent: {intent_result}, ambiguity: {ambiguity_analysis}, vagueness: {vagueness_analysis}")

    # Determine response type based on analysis
    response_type = "success"  # default
    message = ""
    clarifying_questions = []
    suggested_actions = []

    # Check if input is ambiguous or needs clarification
    if intent_result['is_ambiguous'] or ambiguity_analysis['is_ambiguous'] or vagueness_analysis['is_vague']:
        print("DEBUG: Clarify - Input is ambiguous, generating clarifying questions")
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
        print("DEBUG: Clarify - Input is clear, calling OpenRouter AI")
        # Input is clear, but instead of just acknowledging, let's call the AI for a proper response
        # This handles general conversation that doesn't need task management
        from src.services.openrouter_client import call_openrouter

        # Build conversation history for context
        # Since we don't have a direct way to get conversation history here, we'll use a simple approach
        # In a real implementation, we'd want to fetch actual conversation history
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Respond naturally to the user's messages. If they want to manage tasks, let them know you can help with that. Be friendly and engaging."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        try:
            # Call the AI service for a proper conversational response
            print("DEBUG: Clarify - Calling OpenRouter AI service")
            ai_response = call_openrouter(messages)
            print(f"DEBUG: Clarify - OpenRouter response received: {ai_response[:100]}...")
            message = ai_response
        except Exception as e:
            print(f"DEBUG: Clarify - OpenRouter call failed: {str(e)}")
            # Fallback if AI call fails
            message = f"I understand you said: '{user_input}'. How can I assist you further?"

        # Update the conversation state with the current intent
        print("DEBUG: Clarify - Updating conversation state")
        update_data = ConversationStateUpdate(current_intent=user_input)
        conv_service.update_conversation_state(session_id, update_data)

    # Check if confirmation is needed for critical actions
    if intent_detector.requires_confirmation(user_input):
        print("DEBUG: Clarify - Confirmation required for action")
        response_type = "clarification"
        confirmation_question = question_generator.generate_confirmation_question()
        clarifying_questions.insert(0, confirmation_question)
        message = "This action requires confirmation."

    # Prepare response
    print("DEBUG: Clarify - Preparing final response")
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

    print(f"DEBUG: Clarify - Returning response: {response_data}")
    return response_data