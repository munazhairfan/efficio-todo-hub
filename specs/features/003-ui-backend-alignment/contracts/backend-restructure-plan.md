# Backend Restructuring Plan: Align with UI Style

## Overview
This document outlines how to restructure the backend folder organization to match the clean, modular patterns seen in the UI folder structure, while maintaining all existing functionality.

## Current Backend Structure vs UI Patterns

### Current Backend Structure
```
backend/
├── auth/                 # Authentication logic
├── database/            # Database models and connections
├── routes/              # API route handlers
├── main.py              # FastAPI app entry point
├── dependencies.py      # Dependency injection functions
├── db.py                # Database connection setup
├── schemas.py           # Pydantic models
└── ...
```

### UI Structure Pattern (to emulate)
```
ui/
├── app/                 # Application pages and layout
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components
│   └── custom/         # Custom business components
├── lib/                # Shared utilities
├── hooks/              # React hooks
└── styles/             # Styling definitions
```

## Proposed Backend Restructure

### New Backend Structure
```
backend/
├── api/                 # API route handlers (replaces routes/)
│   ├── auth/           # Authentication endpoints
│   ├── todos/          # Todo endpoints
│   ├── users/          # User endpoints
│   └── __init__.py     # API router aggregation
├── core/               # Core application logic
│   ├── auth/          # Authentication utilities
│   ├── security/      # Security-related utilities
│   └── config/        # Configuration
├── models/             # Data models (replaces database/models/)
│   ├── base.py        # Base model definitions
│   ├── user.py        # User model
│   ├── todo.py        # Todo model
│   └── __init__.py    # Model exports
├── schemas/            # Pydantic schemas (request/response models)
├── services/           # Business logic services
│   ├── auth_service.py # Authentication business logic
│   ├── todo_service.py # Todo business logic
│   └── user_service.py # User business logic
├── database/           # Database connection and session management
├── utils/              # Utility functions
│   ├── validators.py  # Input validation utilities
│   ├── helpers.py     # General helper functions
│   └── decorators.py  # Custom decorators
├── dependencies/       # FastAPI dependency functions
├── main.py             # FastAPI app entry point
├── config.py           # Configuration settings
└── __init__.py         # Package initialization
```

## Detailed Restructuring Steps

### 1. Move Route Handlers to API Directory
**Current**: `backend/routes/*.py`
**Target**: `backend/api/*/handlers.py`

- `backend/routes/auth.py` → `backend/api/auth/handlers.py`
- `backend/routes/todos.py` → `backend/api/todos/handlers.py`
- `backend/routes/protected.py` → `backend/api/users/handlers.py`

### 2. Create Services Layer
Create a new `services/` directory for business logic:

```
backend/services/
├── auth_service.py      # Authentication business logic
├── todo_service.py      # Todo CRUD operations
├── user_service.py      # User management operations
└── __init__.py
```

**auth_service.py** will contain:
- User signup logic
- User signin logic
- Token creation/validation logic

**todo_service.py** will contain:
- Todo creation logic
- Todo retrieval logic
- Todo update logic
- Todo deletion logic

### 3. Restructure Core Components
Create a `core/` directory for core functionality:

```
backend/core/
├── auth/
│   ├── jwt_handler.py  # JWT token handling
│   ├── middleware.py   # Authentication middleware
│   └── user_extractor.py # User extraction utilities
├── security/
│   ├── password.py    # Password utilities
│   └── validation.py  # Security validation
└── config/
    ├── settings.py    # Application settings
    └── constants.py   # Application constants
```

### 4. Enhance Models Organization
Move and organize models with better structure:

```
backend/models/
├── base.py             # Base model classes
├── user.py             # User model
├── todo.py             # Todo model
├── relationships.py    # Model relationships
└── __init__.py         # Export all models
```

### 5. Create Dependencies Module
Separate dependency functions:

```
backend/dependencies/
├── auth_deps.py        # Authentication dependencies
├── db_deps.py          # Database dependencies
├── user_deps.py        # User-related dependencies
└── __init__.py
```

### 6. Add Utility Functions
Create utility modules:

```
backend/utils/
├── validators.py       # Input validation
├── helpers.py          # General helpers
├── decorators.py       # Custom decorators
├── exceptions.py       # Custom exceptions
└── formatters.py       # Data formatting utilities
```

## Implementation Strategy

### Phase 1: Create New Directory Structure
1. Create all new directories
2. Move files gradually to maintain functionality
3. Update imports in all files

### Phase 2: Extract Business Logic
1. Move business logic from route handlers to service layer
2. Create service functions that route handlers will call
3. Maintain backward compatibility of API endpoints

### Phase 3: Refactor Dependencies
1. Separate dependency functions into their own modules
2. Create dependency injection patterns that match service layer

### Phase 4: Update Main Application
1. Update `main.py` to use new structure
2. Update import paths throughout the application
3. Maintain all existing endpoints and functionality

## Code Comments for UI Mapping

Add comments in restructured code to map to UI components:

```python
# UI Component: TodoListPage -> Service: todo_service.get_user_todos()
async def get_user_todos(user_id: UUID, db: AsyncSession) -> List[TodoResponse]:
    ...

# UI Component: TodoCreateForm -> Service: todo_service.create_todo()
async def create_todo(todo_data: TodoCreate, user_id: UUID, db: AsyncSession) -> TodoResponse:
    ...
```

## Backward Compatibility Requirements

1. **API Endpoints**: Keep all existing API endpoints unchanged
   - `/api/auth/signup` → remains the same
   - `/api/auth/signin` → remains the same
   - `/api/todos` → remains the same
   - All HTTP methods and URL patterns remain unchanged

2. **Response Formats**: Maintain existing response schemas
   - Keep `schemas.py` with existing Pydantic models
   - Ensure all responses match current format

3. **Database Models**: Keep models unchanged
   - No changes to database schema
   - Maintain all existing relationships

4. **Authentication**: Keep JWT implementation unchanged
   - Same token format and validation
   - Same middleware behavior

## Benefits of New Structure

1. **Modularity**: Clear separation of concerns
2. **Maintainability**: Easier to locate and modify specific functionality
3. **Scalability**: Easy to add new features in organized way
4. **Testability**: Services can be tested independently
5. **Consistency**: Matches patterns seen in modern UI frameworks

## Files to Update

1. `main.py` - Update import paths
2. All route files - Update imports to use services
3. `dependencies.py` - Move to dependencies/ directory
4. `schemas.py` - Potentially reorganize if needed
5. Configuration files - Move to core/config/

## Risk Mitigation

1. **Gradual Migration**: Move files one by one with testing
2. **Maintain Endpoints**: Keep all API endpoints unchanged
3. **Thorough Testing**: Test all endpoints after each change
4. **Backup Strategy**: Keep original structure accessible during transition
5. **Documentation**: Update all import paths in comments