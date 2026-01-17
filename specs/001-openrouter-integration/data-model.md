# Data Model: OpenRouter Integration

## Entities

### OpenRouter Request
- **model**: String - The AI model identifier (e.g., "openai/gpt-3.5-turbo")
- **messages**: Array of Message objects - The conversation history including system, user, and assistant messages
- **temperature**: Float - Controls randomness of AI responses (0.0-1.0)
- **max_tokens**: Integer - Maximum number of tokens to generate (optional)

### Message
- **role**: String - The speaker role ("system", "user", "assistant")
- **content**: String - The message content

### OpenRouter Response
- **id**: String - Unique identifier for the response
- **choices**: Array of Choice objects - The AI-generated responses
- **usage**: Usage object - Token usage statistics
- **created**: Integer - Unix timestamp of when the response was created

### Choice
- **index**: Integer - Index of the choice in the response
- **message**: Message object - The AI-generated message
- **finish_reason**: String - Why the model stopped generating (e.g., "stop", "length")

### Usage
- **prompt_tokens**: Integer - Number of tokens in the prompt
- **completion_tokens**: Integer - Number of tokens in the completion
- **total_tokens**: Integer - Total number of tokens used

### OpenRouterClientConfig
- **api_key**: String - The OpenRouter API key (read from environment variables)
- **base_url**: String - The API base URL (default: "https://openrouter.ai/api/v1")
- **timeout**: Integer - Request timeout in seconds (default: 30)
- **default_model**: String - Default model to use if none specified