"""
OpenRouter Client Module

This module provides functionality to interact with the OpenRouter API
to generate AI responses for the chatbot.
"""

import os
import httpx
import logging
from typing import List, Dict, Any, Optional

# Try different import paths for different environments
try:
    from src.core.config import settings
except ImportError:
    try:
        from core.config import settings
    except ImportError:
        try:
            from api.core.config import settings
        except ImportError:
            # Create a mock settings object with default values for Hugging Face environment
            class MockSettings:
                secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
                algorithm = os.getenv("ALGORITHM", "HS256")
                access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

            settings = MockSettings()


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
    # Load the API key from settings (with fallback to environment variable)
    print(f"DEBUG: OPENROUTER_API_KEY from os.getenv: {'SET' if os.getenv('OPENROUTER_API_KEY') else 'NOT SET'}")
    print(f"DEBUG: OPENROUTER_API_KEY length: {len(os.getenv('OPENROUTER_API_KEY')) if os.getenv('OPENROUTER_API_KEY') else 0}")

    # Try multiple possible configuration paths for the API key
    api_key = getattr(settings, 'openrouter_api_key', None) or os.getenv("OPENROUTER_API_KEY")

    print(f"DEBUG: Final API key from settings: {'SET' if api_key else 'NOT SET'}")
    if api_key:
        print(f"DEBUG: API key length: {len(api_key)}")
        print(f"DEBUG: API key first 10 chars: {api_key[:10]}...")

    if not api_key:
        logger.error("OpenRouter API key is not configured in settings or environment")
        raise ValueError("OpenRouter API key is required")

    # Basic payload with only essential fields
    payload = {
        "model": "google/gemma-2-2b-it:free",
        "messages": messages
    }

    # Add optional fields only if needed
    if tools is not None and len(tools) > 0:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    else:
        # Add basic parameters for general conversation
        payload["temperature"] = 0.7
        payload["max_tokens"] = 1000

    # Essential headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "Efficio Todo Hub"
    }

    try:
        print(f"DEBUG: OpenRouter API request - Model: {payload['model']}")
        print(f"DEBUG: OpenRouter API request - Message count: {len(messages)}")

        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )

            print(f"DEBUG: OpenRouter API response status: {response.status_code}")

            if response.status_code != 200:
                print(f"DEBUG: OpenRouter error response: {response.text}")
                return "I'm having trouble responding right now. Please try again."

            data = response.json()

            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content.strip() if content else ""
            else:
                logger.error(f"No choices found in OpenRouter response: {data}")
                return "I'm having trouble responding right now. Please try again."

    except Exception as e:
        logger.error(f"OpenRouter API call failed: {str(e)}")
        return "I'm having trouble responding right now. Please try again."