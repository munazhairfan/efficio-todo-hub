"""
OpenRouter Client Module

This module provides functionality to interact with the OpenRouter API
to generate AI responses for the chatbot.
"""

import os
import httpx
import logging
from typing import List, Dict, Any, Optional
from ..core.config import settings


logger = logging.getLogger(__name__)


def call_openrouter(messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, timeout: int = 30) -> str:
    """
    Call the OpenRouter API to get an AI response based on the provided messages and tools.

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        tools: Optional list of tool schemas for the AI to potentially use
        timeout: Request timeout in seconds (default: 30)

    Returns:
        str: The AI-generated response content

    Raises:
        Exception: If the API call fails or returns an invalid response
    """
    # Load the API key from environment variables
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        logger.error("OPENROUTER_API_KEY environment variable is not set")
        raise ValueError("OPENROUTER_API_KEY environment variable is required")

    # Prepare the request payload
    payload = {
        "model": "openai/gpt-3.5-turbo",  # Using a stable, chat-capable model with tool calling support
        "messages": messages,
        "temperature": 0.7,  # Balanced between creativity and coherence
        "max_tokens": 1000,   # Reasonable limit for chat responses
        "tools": tools if tools is not None else [],  # MCP tool schemas when provided
        "tool_choice": "auto"  # Allow AI to decide when to use tools
    }

    # Prepare headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "efficio-todo-hub",
        "X-Title": "Efficio Todo Hub"
    }

    try:
        # Make the API request using httpx
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )

            # Check if the request was successful
            response.raise_for_status()

            # Parse the response
            data = response.json()

            # Extract the AI response content
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content.strip() if content else ""
            else:
                logger.error(f"No choices found in OpenRouter response: {data}")
                return "I'm having trouble responding right now. Please try again."

    except httpx.TimeoutException:
        logger.error("OpenRouter API request timed out")
        return "I'm having trouble responding right now. Please try again."

    except httpx.RequestError as e:
        logger.error(f"OpenRouter API request error: {str(e)}")
        return "I'm having trouble responding right now. Please try again."

    except KeyError as e:
        logger.error(f"Unexpected response format from OpenRouter: {str(e)}")
        return "I'm having trouble responding right now. Please try again."

    except Exception as e:
        logger.error(f"Unexpected error during OpenRouter API call: {str(e)}")
        return "I'm having trouble responding right now. Please try again."