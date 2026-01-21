# Quickstart Guide: Chatbot Rate Limiting

## Overview
Quick start guide for implementing and using the chatbot rate limiting feature.

## Development Setup

### Prerequisites
- Python 3.11
- FastAPI
- Redis (optional, for distributed deployments)
- Existing JWT authentication system

### Environment Variables
```bash
# Rate limiting configuration
RATE_LIMIT_MAX_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
RATE_LIMIT_ENABLED=true

# Redis configuration (optional)
REDIS_URL=redis://localhost:6379
```

## Integration Steps

### 1. Add Rate Limiting Middleware
Include the rate limiting middleware in your FastAPI application:

```python
from backend.src.middleware.rate_limiter import RateLimitMiddleware

app = FastAPI()
app.add_middleware(RateLimitMiddleware)
```

### 2. Apply to Chatbot Endpoints Only
Configure rate limiting to apply only to chatbot endpoints, not to Todo CRUD or authentication endpoints.

### 3. User Identification
The system leverages existing JWT authentication to identify users and apply rate limits per authenticated user.

## Usage Examples

### Normal Usage
Authenticated users can send up to 10 messages per minute:
```javascript
// This will work normally (first 10 messages in a minute)
fetch('/api/conversation/clarify', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <jwt-token>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({input: "Hello, how are you?"})
});
```

### Rate Limit Exceeded
When users exceed the limit, they receive a friendly error:
```javascript
// After 10 messages in the last minute, this returns:
{
  "error": "You're sending messages too fast. Please wait a moment.",
  "retryAfter": 60
}
```

## Testing

### Unit Tests
```bash
pytest tests/unit/test_rate_limiter.py
```

### Integration Tests
```bash
pytest tests/integration/test_rate_limit_integration.py
```

## Deployment Notes

### Single Instance
For single-server deployments, in-memory storage is sufficient.

### Distributed Systems
For distributed deployments, configure Redis for shared rate limit state:
```python
# Configure Redis as the storage backend
rate_limiter = RateLimiter(storage_backend='redis', redis_url=os.getenv('REDIS_URL'))
```

## Troubleshooting

### Common Issues
1. **Rate limits not applying**: Check that middleware is added and endpoints are correctly identified
2. **Memory usage**: Monitor memory usage in high-concurrency scenarios
3. **Clock drift**: Ensure system clocks are synchronized in distributed deployments