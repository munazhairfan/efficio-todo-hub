# Frontend Chat Integration - End-to-End Testing

This document outlines the end-to-end testing scenarios for the frontend chat integration feature, covering all three user stories.

## User Story 1: Send Messages to Chatbot

### Test Scenario 1: Basic Message Sending
1. User opens the chat interface on the dashboard
2. User types a message in the input field
3. User clicks the send button or presses Enter
4. The message appears immediately in the chat window with "sent" status
5. The loading indicator appears
6. The assistant's response appears in the chat window with "delivered" status
7. The conversation ID is stored in localStorage

### Test Scenario 2: Error Handling
1. User types a message and sends it
2. If there's a network error, the message shows an error status
3. The user can see an error message and retry functionality

### Test Scenario 3: Input Validation
1. User attempts to send an empty message
2. The system prevents sending and shows an error
3. User attempts to send a message that exceeds the character limit
4. The system prevents sending and shows an error

## User Story 2: Manage Conversation Context

### Test Scenario 1: Conversation Persistence
1. User starts a new conversation
2. The system generates a conversation ID
3. Multiple messages are exchanged in the same conversation
4. The conversation ID is consistently passed with each request
5. User refreshes the page
6. The conversation context is restored from localStorage

### Test Scenario 2: New Conversation Creation
1. User clears the conversation context
2. A new conversation is started with a new ID
3. The new ID is stored and used for subsequent messages

## User Story 3: Display Chat Responses

### Test Scenario 1: Message Formatting
1. User sends a message
2. The message appears with proper styling for user messages
3. Assistant's response appears with proper styling for assistant messages
4. Timestamps are displayed correctly
5. Status indicators are shown appropriately

### Test Scenario 2: Message History
1. User engages in a multi-message conversation
2. All messages are displayed in chronological order
3. The chat interface scrolls to the bottom automatically
4. Message history persists across page refreshes

## Comprehensive End-to-End Test Flow

1. User navigates to the dashboard
2. ChatInterface component loads with the user's ID
3. User sees the welcome message and empty chat history
4. User types "Hello, how are you?" and sends the message
5. The message appears immediately with timestamp and "sent" status
6. Loading indicator appears
7. Assistant responds with "Hi! I'm doing well. How can I help you?"
8. Response appears with timestamp and "delivered" status
9. Conversation ID is stored in localStorage
10. User sends another message "Can you help me create a todo list?"
11. The conversation continues with the same conversation ID
12. User refreshes the page
13. Previous conversation is restored from localStorage
14. User can continue the conversation seamlessly
15. User sends a very long message (>2000 characters)
16. System prevents sending and shows character count in red
17. User sends a message with special characters and formatting
18. Message displays correctly without issues
19. User presses Escape to clear the input field
20. Input field is cleared as expected

## Error Conditions Tested

1. Network timeout - Retry mechanism kicks in
2. Rate limiting - Appropriate error message shown
3. Invalid conversation ID - New conversation started
4. Empty message submission - Validation prevents sending
5. Browser storage unavailable - Graceful degradation

## Performance Considerations

1. Messages appear instantly in the UI without waiting for server response
2. Loading states prevent duplicate submissions
3. Efficient rendering of message history
4. Proper cleanup of event listeners and resources