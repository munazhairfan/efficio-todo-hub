# Backend API for Efficio Todo App

This backend is structured to align with the UI component architecture found in the `/ui` folder, following modern patterns for clean separation of concerns.

## Architecture

The backend follows a modular architecture similar to the UI patterns:

```
backend/
├── api/                 # API route handlers organized by feature
│   ├── auth/           # Authentication endpoints
│   ├── todos/          # Todo endpoints
│   └── users/          # User endpoints
├── core/               # Core functionality
│   ├── auth/          # Authentication utilities
│   ├── security/      # Security utilities
│   └── config/        # Configuration settings
├── models/             # Database models
├── services/           # Business logic services
├── database/           # Database connection and session management
├── utils/              # Utility functions
├── dependencies/       # FastAPI dependency functions
└── main.py             # FastAPI application entry point
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate existing user
- `POST /api/auth/verify` - Verify JWT token

### User Management
- `GET /api/protected` - Example protected endpoint
- `GET /api/profile` - Get user profile information

### Todo Management
- `GET /api/todos` - Get all todos for authenticated user
- `POST /api/todos` - Create new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update specific todo
- `DELETE /api/todos/{id}` - Delete specific todo

## UI Integration

This backend is designed to work seamlessly with the UI in the `/ui` folder:

- All endpoints return data structures compatible with modern UI frameworks
- Authentication follows standard JWT patterns
- Response formats are optimized for UI consumption
- Proper error handling for UI feedback

## Service Layer

Business logic is separated into services for better maintainability:

- `services/auth_service.py` - Authentication logic
- `services/todo_service.py` - Todo management logic
- `services/user_service.py` - User management logic

## Compatibility

- Maintains 100% backward compatibility with existing API endpoints
- Preserves all existing functionality
- Follows the same data models and response formats