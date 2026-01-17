"""
Helper functions for testing
"""
import json
from typing import Dict, Any, List
import re


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """
    Validate data against a basic JSON schema
    Returns list of validation errors
    """
    errors = []

    # Check required fields
    if "required" in schema:
        for field in schema["required"]:
            if field not in data:
                errors.append(f"Missing required field: {field}")

    # Check field types
    if "properties" in schema:
        for field, field_spec in schema["properties"].items():
            if field in data:
                expected_type = field_spec.get("type")
                if expected_type:
                    actual_value = data[field]
                    if expected_type == "string" and not isinstance(actual_value, str):
                        errors.append(f"Field {field} should be string, got {type(actual_value).__name__}")
                    elif expected_type == "integer" and not isinstance(actual_value, int):
                        errors.append(f"Field {field} should be integer, got {type(actual_value).__name__}")
                    elif expected_type == "boolean" and not isinstance(actual_value, bool):
                        errors.append(f"Field {field} should be boolean, got {type(actual_value).__name__}")
                    elif expected_type == "array" and not isinstance(actual_value, list):
                        errors.append(f"Field {field} should be array, got {type(actual_value).__name__}")
                    elif expected_type == "object" and not isinstance(actual_value, dict):
                        errors.append(f"Field {field} should be object, got {type(actual_value).__name__}")

    return errors


def validate_chat_response(response: Dict[str, Any]) -> List[str]:
    """
    Validate chat API response structure
    """
    schema = {
        "required": ["conversation_id", "response", "message_id"],
        "properties": {
            "conversation_id": {"type": "integer"},
            "response": {"type": "string"},
            "message_id": {"type": "integer"},
            "conversation_title": {"type": "string"},
            "has_tool_calls": {"type": "boolean"},
            "tool_calls": {"type": "array"}
        }
    }
    return validate_json_schema(response, schema)


def validate_todo_response(response: Dict[str, Any]) -> List[str]:
    """
    Validate todo API response structure
    """
    schema = {
        "required": ["id", "title", "completed", "user_id", "created_at", "updated_at"],
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "completed": {"type": "boolean"},
            "user_id": {"type": "integer"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        }
    }
    return validate_json_schema(response, schema)


def validate_error_response(response: Dict[str, Any]) -> List[str]:
    """
    Validate error response structure
    """
    schema = {
        "required": ["detail"],
        "properties": {
            "detail": {"type": "string"}
        }
    }
    return validate_json_schema(response, schema)


def check_response_headers(response_headers: Dict[str, str], expected_headers: List[str]) -> List[str]:
    """
    Check if response contains expected headers
    """
    errors = []
    for header in expected_headers:
        if header.lower() not in [h.lower() for h in response_headers.keys()]:
            errors.append(f"Missing expected header: {header}")
    return errors


def validate_jwt_token_format(token: str) -> bool:
    """
    Basic validation of JWT token format (3 parts separated by dots)
    """
    parts = token.split('.')
    return len(parts) == 3


def extract_task_ids_from_response(response_text: str) -> List[int]:
    """
    Extract task IDs from response text using regex
    """
    # Look for patterns like "task #1", "task 1", "#1", etc.
    patterns = [
        r'task\s*#(\d+)',
        r'task\s+(\d+)',
        r'#(\d+)',
        r'number\s+(\d+)'
    ]

    task_ids = []
    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        for match in matches:
            try:
                task_id = int(match)
                if task_id > 0:
                    task_ids.append(task_id)
            except ValueError:
                continue

    return list(set(task_ids))  # Remove duplicates


def validate_task_data(task_data: Dict[str, Any]) -> List[str]:
    """
    Validate task data structure and content
    """
    errors = []

    if "title" not in task_data or not isinstance(task_data["title"], str) or len(task_data["title"].strip()) == 0:
        errors.append("Task must have a valid title")

    if "completed" in task_data and not isinstance(task_data["completed"], bool):
        errors.append("Task completed field must be boolean")

    if "description" in task_data and task_data["description"] is not None and not isinstance(task_data["description"], str):
        errors.append("Task description must be string or null")

    if "user_id" not in task_data or not isinstance(task_data["user_id"], int) or task_data["user_id"] <= 0:
        errors.append("Task must have a valid user_id")

    return errors


def compare_task_objects(task1: Dict[str, Any], task2: Dict[str, Any], ignore_fields: List[str] = []) -> bool:
    """
    Compare two task objects, ignoring specified fields
    """
    task1_filtered = {k: v for k, v in task1.items() if k not in ignore_fields}
    task2_filtered = {k: v for k, v in task2.items() if k not in ignore_fields}

    return task1_filtered == task2_filtered


def validate_timestamp_format(timestamp_str: str) -> bool:
    """
    Validate ISO 8601 timestamp format
    """
    import re
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})?$'
    return bool(re.match(pattern, timestamp_str))


def extract_conversation_id_from_response(response: Dict[str, Any]) -> int:
    """
    Extract conversation ID from chat response
    """
    if "conversation_id" in response:
        return response["conversation_id"]
    return None