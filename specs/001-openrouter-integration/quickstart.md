# Quickstart Guide: OpenRouter Integration

## Overview
This guide explains how to set up and use the OpenRouter AI integration for the chatbot functionality.

## Prerequisites
- Python 3.11+
- OpenRouter account with API key
- Environment variables configured for API access

## Setup

### 1. Environment Variables
Set the required environment variables:
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key-here"
export DATABASE_URL="your-database-url-here"
```

### 2. Dependencies
Ensure required dependencies are installed:
```bash
pip install httpx
```

## Implementation Steps

### 1. Create OpenRouter Client
Create a client service that handles communication with OpenRouter API:
- Reads API key from environment variables
- Builds proper request payloads with conversation context
- Handles API responses and errors appropriately

### 2. Update Chat Endpoint
Modify the chat endpoint to:
- Use the OpenRouter client instead of mock responses
- Pass conversation history as context to the AI
- Maintain fallback to local agent if OpenRouter fails

### 3. Test Integration
Test the integration by:
- Sending sample messages to the chat endpoint
- Verifying AI responses are returned from OpenRouter
- Confirming fallback mechanism works when OpenRouter is unavailable

## Usage
Once configured, the chatbot will automatically:
- Send user messages to OpenRouter for AI processing
- Return AI-generated responses to users
- Handle API errors gracefully with fallback responses
- Maintain conversation context across messages

## Testing
Test the OpenRouter integration by:
1. Making chat requests and verifying AI responses
2. Testing error scenarios (invalid API key, network timeouts)
3. Confirming fallback responses work when OpenRouter is unavailable
4. Verifying conversation history is properly passed to OpenRouter