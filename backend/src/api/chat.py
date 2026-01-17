"""Chat API endpoint implementation."""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, validator
from jose import jwt
from jose.jwt import JWTError
import logging

logger = logging.getLogger(__name__)

from ..core.dependencies import get_db_session
from ..core.config import settings
from ..models.conversation import ConversationCreate, ConversationResponse
from ..models.message import MessageCreate, MessageResponse
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..services.openrouter_client import call_openrouter

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


def verify_jwt_token(authorization: str = Header(None)) -> dict:
    """
    Verify JWT token from Authorization header and extract user information.

    Args:
        authorization: Authorization header in format "Bearer <token>"

    Returns:
        dict: User information extracted from token payload

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is required")

    # Check if authorization header starts with "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format. Expected 'Bearer <token>'")

    # Extract the token part after "Bearer "
    token = authorization[7:]  # Remove "Bearer " prefix

    try:
        # Decode the JWT token using the secret key and algorithm from settings
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")


# Pydantic model for the chat request with validation
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[int] = None  # None for new conversation

    @validator('message')
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 1000:  # Set limit to 1000 characters as per requirements
            raise ValueError('Message too long, must be 1000 characters or less')
        return v.strip()

    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Conversation ID must be a positive integer')
        return v


# Enhanced response model to support potential tool call information
class ToolCallInfo(BaseModel):
    """Information about a tool call that the AI might make."""
    tool_name: str
    parameters: dict
    execution_status: Optional[str] = None  # pending, executed, failed


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    message_id: int
    conversation_title: Optional[str] = None
    # Additional fields for potential tool call information (for future use)
    tool_calls: Optional[list[ToolCallInfo]] = []
    has_tool_calls: bool = False


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    user_id: int,
    chat_request: ChatRequest,
    db: Session = Depends(get_db_session),
    authorization: str = Header(None)
):
    """
    Handle chat messages and return AI responses.

    This endpoint supports:
    1. Starting a new conversation (when conversation_id is None)
    2. Continuing an existing conversation (when conversation_id is provided)

    Args:
        user_id: The ID of the user making the request (path parameter)
        chat_request: The chat request containing the message and optional conversation_id
        authorization: Authorization header with Bearer token
    """
    # Validate user_id
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer")

    # Validate the JWT token and extract user information
    token_payload = verify_jwt_token(authorization)

    # Extract user_id from the token payload
    token_user_id = token_payload.get("user_id") or token_payload.get("id")

    if not token_user_id:
        logger.warning(f"Invalid token: user ID not found in token for user_id: {user_id}")
        raise HTTPException(status_code=401, detail="Invalid token: user ID not found in token")

    # Validate that the user_id in the token matches the user_id in the path parameter
    if str(token_user_id) != str(user_id):
        logger.warning(f"Unauthorized access attempt: token user_id {token_user_id} != path user_id {user_id}")
        raise HTTPException(status_code=403, detail="Not authorized to access this user's conversations")

    conversation_service = ConversationService(db)
    message_service = MessageService(db)

    # Determine if we're starting a new conversation or continuing an existing one
    if chat_request.conversation_id is None:
        # Create a new conversation
        conversation_data = ConversationCreate(
            user_id=user_id,
            title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"  # Auto-generate title
        )
        conversation = conversation_service.create_conversation(conversation_data)
        conversation_id = conversation.id
    else:
        # Verify the conversation exists and belongs to the user
        existing_conversation = conversation_service.get_conversation_by_id(chat_request.conversation_id)
        if not existing_conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        if existing_conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this conversation")

        conversation_id = chat_request.conversation_id
        conversation = existing_conversation  # For title access later

    # Create the user's message
    user_message_data = MessageCreate(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=chat_request.message
    )
    user_message = message_service.create_message(user_message_data)

    # Fetch conversation history to provide context to the AI agent
    conversation_history = message_service.get_messages_by_conversation(conversation_id)

    # Build messages for OpenRouter API
    # Include system instruction, conversation history, and current user message
    messages = [
        {
            "role": "system",
            "content": "You are a helpful task management assistant. Help users manage their tasks and be friendly and encouraging."
        }
    ]

    # Add conversation history
    for msg in conversation_history:
        role = "assistant" if msg.role == "assistant" else "user"
        messages.append({
            "role": role,
            "content": msg.content
        })

    # Add current user message
    messages.append({
        "role": "user",
        "content": chat_request.message
    })

    # Prepare MCP tools schema for potential use by the AI
    mcp_tools_schemas = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "title": {"type": "string", "description": "The title of the task to create"},
                        "description": {"type": "string", "description": "Detailed description of the task (optional)"}
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "status": {"type": "string", "description": "Filter by status ('all', 'pending', 'completed'), defaults to 'all'"}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Remove a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task (optional)"},
                        "description": {"type": "string", "description": "New description for the task (optional)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    ]

    # Call OpenRouter to get AI response
    ai_response_content = call_openrouter(messages, tools=mcp_tools_schemas)

    # Create the AI's response message
    ai_message_data = MessageCreate(
        conversation_id=conversation_id,
        user_id=user_id,  # In a real app, this might be the AI's ID or 0
        role="assistant",
        content=ai_response_content
    )
    ai_message = message_service.create_message(ai_message_data)

    # Check if the AI response suggests potential tool usage
    has_tool_calls, tool_calls = analyze_for_potential_tool_calls(chat_request.message, ai_response_content)

    # Prepare the response
    response = ChatResponse(
        conversation_id=conversation_id,
        response=ai_response_content,
        message_id=ai_message.id,
        conversation_title=conversation.title if chat_request.conversation_id is None else None,
        has_tool_calls=has_tool_calls,
        tool_calls=tool_calls
    )

    # Log successful message processing
    logger.info(f"Successfully processed message for user_id: {user_id}, conversation_id: {conversation_id}")

    return response


def analyze_for_potential_tool_calls(user_message: str, ai_response: str) -> tuple[bool, list]:
    """
    Analyze the user message and AI response to determine if there are potential tool calls.

    Returns a tuple of (has_tool_calls: bool, tool_calls: list[ToolCallInfo])
    """
    import re

    tool_calls = []

    # Look for keywords that might indicate potential tool usage
    user_lower = user_message.lower()

    # Check for todo/task related keywords
    if any(word in user_lower for word in ["todo", "task", "list", "add", "complete", "done"]):
        tool_calls.append(ToolCallInfo(
            tool_name="todo_manager",
            parameters={"action": "suggest", "query": user_message[:100]}
        ))

    # Check for weather related keywords
    if any(word in user_lower for word in ["weather", "temperature", "forecast", "rain", "sun"]):
        tool_calls.append(ToolCallInfo(
            tool_name="weather_service",
            parameters={"location": "user_location", "query": user_message[:100]}
        ))

    # Check for calculation related keywords
    if any(word in user_lower for word in ["calculate", "math", "sum", "multiply", "divide", "subtract"]):
        tool_calls.append(ToolCallInfo(
            tool_name="calculator",
            parameters={"expression": user_message[:100]}
        ))

    # Check for time/date related keywords
    if any(word in user_lower for word in ["time", "date", "schedule", "calendar", "appointment"]):
        tool_calls.append(ToolCallInfo(
            tool_name="calendar_service",
            parameters={"query": user_message[:100]}
        ))

    # Return whether there are tool calls and the list of tool calls
    return len(tool_calls) > 0, tool_calls


def generate_mock_ai_response(user_message: str) -> str:
    """
    Generate a mock AI response based on the user's message.

    This is a placeholder implementation that will be replaced with actual AI integration.
    For now, it returns structured responses that could simulate AI tool usage.
    """
    import random

    # Sample responses that simulate AI with potential tool usage
    basic_responses = [
        f"I understand you said: '{user_message}'. This is a simulated AI response.",
        f"Thanks for your message: '{user_message}'. I'm processing this with my AI capabilities.",
        f"I've received your input about '{user_message[:50]}{'...' if len(user_message) > 50 else ''}'. Analyzing now..."
    ]

    # Simulate potential tool responses based on keywords
    user_lower = user_message.lower()

    if any(word in user_lower for word in ["todo", "task", "list", "add"]):
        # Simulate a response that might trigger a tool call
        return f"I can help you manage your tasks! I've noted your request about '{user_message[:30]}{'...' if len(user_message) > 30 else ''}'. Would you like me to add this to your todo list?"
    elif any(word in user_lower for word in ["weather", "temperature", "forecast"]):
        return f"You asked about weather. I can fetch current weather information for you. For '{user_message}', I would typically call a weather API."
    elif any(word in user_lower for word in ["time", "date", "now"]):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current time is {current_time}. Regarding your query about '{user_message[:30]}{'...' if len(user_message) > 30 else ''}', I can assist further if needed."
    elif any(word in user_lower for word in ["calculate", "math", "sum", "multiply"]):
        return f"I can help with calculations. For your request '{user_message[:30]}{'...' if len(user_message) > 30 else ''}', I would typically call a calculator tool."
    elif "hello" in user_lower or "hi" in user_lower:
        return "Hello there! How can I assist you today? I'm your AI assistant ready to help with tasks, questions, and more."
    elif "how are you" in user_lower:
        return "I'm functioning optimally, thank you for asking! I'm here to help you with your tasks and questions. What can I assist you with today?"
    elif "thank" in user_lower:
        return "You're welcome! I'm glad I could help. Is there anything else I can assist you with?"
    elif "bye" in user_lower or "goodbye" in user_lower:
        return "Goodbye! Feel free to come back if you have more questions. I'm always here to help when you need assistance."
    else:
        # Return a random basic response
        return random.choice(basic_responses)