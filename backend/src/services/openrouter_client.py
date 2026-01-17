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

            # Check if the response contains tool calls
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]

                # Check if the AI wants to call a tool
                if "tool_calls" in choice["message"]:
                    # Import the tools here to avoid circular imports
                    from ..mcp_tools import add_task, list_tasks, complete_task, delete_task, update_task

                    # Process each tool call
                    tool_call_results = []
                    for tool_call in choice["message"]["tool_calls"]:
                        function_name = tool_call["function"]["name"]
                        import json
                        function_args = json.loads(tool_call["function"]["arguments"])  # Safely parse the arguments

                        try:
                            # Execute the appropriate tool function
                            if function_name == "add_task":
                                result = add_task(**function_args)
                            elif function_name == "list_tasks":
                                result = list_tasks(**function_args)
                            elif function_name == "complete_task":
                                result = complete_task(**function_args)
                            elif function_name == "delete_task":
                                result = delete_task(**function_args)
                            elif function_name == "update_task":
                                result = update_task(**function_args)
                            else:
                                result = {"error": f"Unknown function: {function_name}"}

                            tool_call_results.append({
                                "tool_call_id": tool_call["id"],
                                "role": "tool",
                                "name": function_name,
                                "content": str(result)
                            })
                        except Exception as e:
                            tool_call_results.append({
                                "tool_call_id": tool_call["id"],
                                "role": "tool",
                                "name": function_name,
                                "content": f"Error executing tool: {str(e)}"
                            })

                    # Send the tool results back to the model for a final response
                    # First add the assistant message that contained the tool calls
                    assistant_message_with_tool_calls = {
                        "role": "assistant",
                        "content": choice["message"].get("content"),
                        "tool_calls": choice["message"]["tool_calls"]
                    }
                    updated_messages = messages + [assistant_message_with_tool_calls] + tool_call_results

                    # Make a second API call with the tool results
                    payload["messages"] = updated_messages
                    response = client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        json=payload,
                        headers=headers
                    )

                    response.raise_for_status()
                    data = response.json()

                    if "choices" in data and len(data["choices"]) > 0:
                        content = data["choices"][0]["message"]["content"]
                        return content.strip() if content else ""
                    else:
                        logger.error(f"No choices found in OpenRouter response: {data}")
                        return "I'm having trouble responding right now. Please try again."
                else:
                    # No tool calls, return the content directly
                    content = choice["message"]["content"]
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