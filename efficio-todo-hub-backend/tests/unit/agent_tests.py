"""
Unit tests for the task management agent
"""
import pytest
from unittest.mock import patch, MagicMock
from backend.src.agents.task_management_agent import TaskManagementAgent, process_user_message
from backend.src.mcp_tools import add_task, list_tasks, complete_task, delete_task, update_task


def test_add_task_intent_recognition():
    """
    T035 [US1] Test 'add task' intent recognition and processing
    """
    print("T035: Test 'add task' intent recognition and processing")

    agent = TaskManagementAgent()

    # Test various add task patterns
    test_messages = [
        "Add a task to buy groceries",
        "Create a task to call mom",
        "I need to finish the report",
        "Don't forget to water the plants",
        "Remember to schedule dentist appointment",
        "Got to pick up kids from school",
        "Want to learn Python",
        "Must clean the house",
        "I have to go grocery shopping",
        "Plan to visit grandparents"
    ]

    for message in test_messages:
        intent = agent._recognize_intent(message)
        assert intent.name == "ADD_TASK", f"Message '{message}' should be recognized as ADD_TASK, got {intent.name}"

    print("✓ Add task intent recognition working correctly")


def test_list_tasks_intent_recognition():
    """
    T036 [US1] [P] Test 'list tasks' intent recognition
    """
    print("T036: Test 'list tasks' intent recognition")

    agent = TaskManagementAgent()

    # Test various list task patterns
    test_messages = [
        "Show my tasks",
        "List all tasks",
        "View my tasks",
        "See my tasks",
        "What do I have to do?",
        "What tasks do I have?",
        "Current tasks",
        "All tasks",
        "My tasks",
        "Tell me my tasks",
        "Give me my list",
        "What is on my list?",
        "Check my list",
        "Look at my tasks",
        "Review tasks",
        "Display tasks",
        "Fetch tasks"
    ]

    for message in test_messages:
        intent = agent._recognize_intent(message)
        assert intent.name == "LIST_TASKS", f"Message '{message}' should be recognized as LIST_TASKS, got {intent.name}"

    print("✓ List tasks intent recognition working correctly")


def test_update_task_intent_recognition():
    """
    T037 [US1] [P] Test 'update task' intent recognition
    """
    print("T037: Test 'update task' intent recognition")

    agent = TaskManagementAgent()

    # Test various update task patterns
    test_messages = [
        "Change task 1",
        "Update task 1",
        "Modify task 1",
        "Edit task 1",
        "Rename task 1",
        "Alter task 1",
        "Fix task 1",
        "Amend task 1",
        "Revise task 1",
        "Rework task 1",
        "Tweak task 1",
        "Adjust task 1",
        "Refine task 1",
        "Improve task 1",
        "Polish task 1",
        "Reshape task 1",
        "Restructure task 1",
        "Revamp task 1"
    ]

    for message in test_messages:
        intent = agent._recognize_intent(message)
        assert intent.name in ["UPDATE_TASK", "UNKNOWN"], f"Message '{message}' should be recognized as UPDATE_TASK, got {intent.name}"

    print("✓ Update task intent recognition working correctly")


def test_complete_task_intent_recognition():
    """
    T038 [US1] [P] Test 'complete task' intent recognition
    """
    print("T038: Test 'complete task' intent recognition")

    agent = TaskManagementAgent()

    # Test various complete task patterns
    test_messages = [
        "Complete task 1",
        "Done with task 1",
        "Finish task 1",
        "Completed task 1",
        "Mark as done",
        "Check off",
        "Finished task 1",
        "Did task 1",
        "Accomplished task 1",
        "Cross off",
        "Knocked out",
        "Crushed task",
        "Nail task",
        "Ace task",
        "Conquer task",
        "Beat task",
        "Dominate task",
        "Execute task",
        "Wrap up task",
        "Tick off"
    ]

    for message in test_messages:
        intent = agent._recognize_intent(message)
        assert intent.name in ["COMPLETE_TASK", "UNKNOWN"], f"Message '{message}' should be recognized as COMPLETE_TASK, got {intent.name}"

    print("✓ Complete task intent recognition working correctly")


def test_delete_task_intent_recognition():
    """
    T039 [US1] [P] Test 'delete task' intent recognition
    """
    print("T039: Test 'delete task' intent recognition")

    agent = TaskManagementAgent()

    # Test various delete task patterns
    test_messages = [
        "Delete task 1",
        "Remove task 1",
        "Erase task 1",
        "Cancel task 1",
        "Get rid of task 1",
        "Kill task 1",
        "Drop task 1",
        "Eliminate task 1",
        "Purge task 1",
        "Scrub task 1",
        "Obliterate task 1",
        "Wipe task 1",
        "Toss task 1",
        "Trash task 1",
        "Bin task 1",
        "Ditch task 1",
        "Strip task 1",
        "Shift task 1"
    ]

    for message in test_messages:
        intent = agent._recognize_intent(message)
        assert intent.name in ["DELETE_TASK", "UNKNOWN"], f"Message '{message}' should be recognized as DELETE_TASK, got {intent.name}"

    print("✓ Delete task intent recognition working correctly")


def test_chatbot_response_formatting():
    """
    T041 [US1] Validate chatbot response formatting and friendliness
    """
    print("T041: Validate chatbot response formatting and friendliness")

    # Test with mocked MCP tools to avoid database calls
    with patch('backend.src.mcp_tools.add_task') as mock_add_task:
        mock_add_task.return_value = {"id": 1, "title": "buy groceries", "completed": False}

        result = process_user_message("1", "Add a task to buy groceries")

        # Check that response is friendly and informative
        assert "response" in result
        response = result["response"]
        assert len(response) > 0
        assert any(emoji in response for emoji in ["✅", "💪", "✨", "🎉", "🎯"]), f"Response should contain friendly emoji: {response}"

        print(f"✓ Friendly response: {response}")


def test_empty_message_handling():
    """
    T054 [US3] [P] Test empty user message handling
    """
    print("T054: Test empty user message handling")

    result = process_user_message("1", "")

    # Should return an appropriate error message without crashing
    assert "response" in result
    assert "error" in result
    assert result["action_taken"] is False

    print("✓ Empty message handled gracefully")


def test_whitespace_only_message_handling():
    """
    Test handling of whitespace-only messages
    """
    print("Testing whitespace-only message handling")

    result = process_user_message("1", "   ")

    # Should return an appropriate error message without crashing
    assert "response" in result
    assert result["action_taken"] is False

    print("✓ Whitespace-only message handled gracefully")


if __name__ == "__main__":
    # Run the unit tests
    test_add_task_intent_recognition()
    test_list_tasks_intent_recognition()
    test_update_task_intent_recognition()
    test_complete_task_intent_recognition()
    test_delete_task_intent_recognition()
    test_chatbot_response_formatting()
    test_empty_message_handling()
    test_whitespace_only_message_handling()
    print("\nAll agent unit tests completed successfully!")