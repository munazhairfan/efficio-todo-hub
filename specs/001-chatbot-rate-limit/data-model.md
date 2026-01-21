# Data Model: Chatbot Rate Limiting

## Entities

### RateLimitRecord
Represents a user's current rate limit state

**Fields**:
- userId: String - Unique identifier for authenticated user
- requestCount: Integer - Number of requests made in current window (default: 0)
- windowStart: DateTime - Timestamp when current rate limit window began
- lastRequestTime: DateTime - Timestamp of the most recent request

**Relationships**: None (temporary in-memory storage)

**Validation Rules**:
- userId must be non-empty
- requestCount must be >= 0
- windowStart must be in the past
- requestCount must not exceed 10 for the window

### RateLimitConfiguration
Defines the rate limiting parameters

**Fields**:
- maxRequests: Integer - Maximum number of requests allowed (value: 10)
- timeWindowSeconds: Integer - Duration of rate limit window in seconds (value: 60)
- isEnabled: Boolean - Whether rate limiting is active (default: true)

**Relationships**: None

**Validation Rules**:
- maxRequests must be > 0
- timeWindowSeconds must be > 0
- isEnabled must be boolean

## State Transitions

### RateLimitRecord
- **Initial State**: New user makes first request → Record created with requestCount=1, windowStart=current_time
- **Within Window**: User makes request while in current window → requestCount incremented
- **Window Expired**: User makes request after window expires → New window starts, requestCount=1
- **Limit Exceeded**: requestCount > maxRequests → Rate limit exceeded, request blocked
- **Window Reset**: After timeWindowSeconds → Record can be cleared or reused

## Data Flows

1. **Incoming Request**: Extract userId from JWT → Check RateLimitRecord → Validate against Configuration → Allow/Block → Update Record
2. **Cleanup**: Periodic cleanup of expired RateLimitRecords to prevent memory growth