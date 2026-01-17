"""
API Client wrapper for making test requests to backend endpoints
"""
import requests
import json
from typing import Optional, Dict, Any


class APIClient:
    """Wrapper for making API requests during testing"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def set_auth_token(self, token: str):
        """Set the authorization header with JWT token"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def post_chat(self, user_id: int, message: str, conversation_id: Optional[int] = None) -> Dict[Any, Any]:
        """Send a chat message to the chat endpoint"""
        url = f"{self.base_url}/api/{user_id}/chat"

        payload = {
            "message": message
        }

        if conversation_id is not None:
            payload["conversation_id"] = conversation_id

        response = self.session.post(url, json=payload)
        return {
            "status_code": response.status_code,
            "json": response.json() if response.content else {},
            "headers": dict(response.headers)
        }

    def get_todos(self, user_id: int) -> Dict[Any, Any]:
        """Get all todos for a user"""
        url = f"{self.base_url}/api/users/{user_id}/todos"
        response = self.session.get(url)
        return {
            "status_code": response.status_code,
            "json": response.json() if response.content else {},
        }

    def create_todo(self, user_id: int, title: str, description: Optional[str] = None) -> Dict[Any, Any]:
        """Create a new todo for a user"""
        url = f"{self.base_url}/api/users/{user_id}/todos"
        payload = {
            "title": title,
            "description": description
        }
        response = self.session.post(url, json=payload)
        return {
            "status_code": response.status_code,
            "json": response.json() if response.content else {},
        }


# Helper functions for JWT token generation
def generate_test_token(user_id: int, secret: str = "test-secret") -> str:
    """Generate a test JWT token for authenticated test scenarios"""
    import jwt
    from datetime import datetime, timedelta

    payload = {
        "sub": str(user_id),
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token