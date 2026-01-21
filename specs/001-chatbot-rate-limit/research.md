# Research: Chatbot Rate Limiting Implementation

## Overview
Research for implementing rate limiting for chatbot endpoints to protect against abuse and API exhaustion.

## Decision: Rate Limiting Strategy
**Rationale**: Selected token bucket algorithm for rate limiting as it provides smooth rate limiting with burst capability while being simple to implement. This allows users to send up to 10 messages rapidly if they haven't sent any recently, but averages to 10 messages per minute over time.

**Alternatives considered**:
- Fixed window: Simple but allows bursts at window boundaries
- Sliding window: More accurate but requires more storage per user
- Token bucket: Allows controlled bursts while maintaining average rate (selected)

## Decision: Storage Mechanism
**Rationale**: Using in-memory storage with TTL (Time To Live) for rate limit records. For distributed deployments, Redis will be used if needed. This approach minimizes database load and provides fast access times.

**Alternatives considered**:
- Database storage: Persistent but slower and adds load to database
- In-memory with TTL: Fast access and low overhead (selected)
- Redis: Good for distributed systems but requires additional infrastructure

## Decision: Authentication Integration
**Rationale**: Leverage existing JWT authentication system to identify users. Extract user ID from JWT token to apply rate limiting per user. This respects the constraint of not changing existing JWT auth logic.

**Alternatives considered**:
- Modify JWT system: Would violate non-goal constraint
- Session-based identification: Would require additional infrastructure
- Use existing JWT system: Maintains current architecture (selected)

## Decision: Middleware Approach
**Rationale**: Implement rate limiting as FastAPI middleware that intercepts requests to chatbot endpoints. This allows centralized rate limiting logic without modifying existing endpoint code.

**Alternatives considered**:
- Decorator approach: Would require modification of each endpoint
- Middleware approach: Centralized and non-intrusive (selected)
- Endpoint-level checks: Would duplicate logic across endpoints

## Decision: Rate Limit Reset Mechanism
**Rationale**: Implement automatic reset after 60 seconds using sliding window approach. Each user's rate limit window starts from their first request and refreshes every 60 seconds.

**Alternatives considered**:
- Calendar-aligned windows: Would reset at specific times (e.g., :00 every minute)
- Rolling window: Continuous 60-second window from last request (selected)
- Fixed intervals: Simpler but less fair for users

## Decision: Error Response Format
**Rationale**: Return a friendly error message as specified in requirements: "You're sending messages too fast. Please wait a moment." with HTTP 429 status code to indicate rate limiting.

**Alternatives considered**:
- Generic error message: Less user-friendly
- Specified message: Matches requirements exactly (selected)
- Different HTTP codes: 429 is standard for rate limiting