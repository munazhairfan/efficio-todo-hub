"""
Example usage of the Chat API.

This script demonstrates how to interact with the Chat API programmatically.
"""

import requests
import json
from typing import Dict, Optional


class ChatAPIClient:
    """Client for interacting with the Chat API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')

    def send_message(self, user_id: int, message: str, conversation_id: Optional[int] = None) -> Dict:
        """
        Send a message to the chat API.

        Args:
            user_id: The ID of the user sending the message
            message: The message content
            conversation_id: ID of existing conversation, or None for new conversation

        Returns:
            Response from the API as a dictionary
        """
        url = f"{self.base_url}/api/{user_id}/chat"

        payload = {
            "message": message,
            "conversation_id": conversation_id
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    def start_conversation(self, user_id: int, initial_message: str) -> Dict:
        """
        Start a new conversation.

        Args:
            user_id: The ID of the user
            initial_message: The first message in the conversation

        Returns:
            Response from the API with new conversation details
        """
        return self.send_message(user_id, initial_message, conversation_id=None)

    def continue_conversation(self, user_id: int, conversation_id: int, message: str) -> Dict:
        """
        Continue an existing conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the existing conversation
            message: The message to add to the conversation

        Returns:
            Response from the API
        """
        return self.send_message(user_id, message, conversation_id=conversation_id)


def demo_usage():
    """Demonstrate usage of the Chat API."""
    print("💬 Chat API Usage Demo")
    print("=" * 50)

    # Initialize the client
    client = ChatAPIClient("http://localhost:8000")  # Adjust URL as needed

    try:
        print("\n1. Starting a new conversation...")
        response = client.start_conversation(
            user_id=1,
            initial_message="Hello, I need help organizing my tasks!"
        )

        print(f"   ✓ New conversation created: #{response['conversation_id']}")
        print(f"   ✓ AI Response: {response['response'][:60]}...")
        print(f"   ✓ Has Tool Calls: {response['has_tool_calls']}")

        conversation_id = response['conversation_id']

        print(f"\n2. Continuing conversation #{conversation_id}...")
        response = client.continue_conversation(
            user_id=1,
            conversation_id=conversation_id,
            message="Can you help me create a todo list for the week?"
        )

        print(f"   ✓ Continued conversation: #{response['conversation_id']}")
        print(f"   ✓ AI Response: {response['response'][:60]}...")
        print(f"   ✓ Has Tool Calls: {response['has_tool_calls']}")

        if response['has_tool_calls']:
            print(f"   ✓ Detected tool calls: {len(response['tool_calls'])}")
            for i, tool_call in enumerate(response['tool_calls']):
                print(f"     {i+1}. {tool_call['tool_name']}: {tool_call['parameters']}")

        print(f"\n3. Testing tool call detection...")
        response = client.continue_conversation(
            user_id=1,
            conversation_id=conversation_id,
            message="Add 'Buy groceries' to my todo list"
        )

        print(f"   ✓ Response: {response['response'][:60]}...")
        print(f"   ✓ Has Tool Calls: {response['has_tool_calls']}")

        if response['has_tool_calls']:
            print(f"   ✓ Tool calls detected! This would trigger the todo manager.")

        print("\n✅ Demo completed successfully!")
        print("\n💡 Tips for using the API:")
        print("   • Use conversation_id=null to start a new conversation")
        print("   • Use conversation_id=# to continue an existing conversation")
        print("   • Messages mentioning 'todo', 'weather', 'calculate' may trigger tool calls")
        print("   • All conversations are tied to user_id for access control")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("\nThe API server might not be running. Start it with:")
        print("   cd backend && uvicorn src.main:app --reload")


if __name__ == "__main__":
    demo_usage()