# UI Components to Backend Endpoints Mapping Plan

## Overview
This document maps the UI components in the `/ui` folder to the corresponding backend endpoints in the existing todo application. The goal is to ensure the beautiful UI can interact with all backend functionality while preserving existing functionality.

## Current UI Structure Analysis
The UI in the `/ui` folder is a landing page built with Next.js App Router featuring:
- Landing page with navigation, hero section, features, and call-to-action
- Modern styling with custom color palette and animations
- Components like buttons, cards, and navigation elements

## Backend API Endpoints Available

### Authentication Endpoints
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate existing user
- `POST /api/auth/verify` - Verify JWT token validity

### Todo Management Endpoints
- `GET /api/todos` - Retrieve all todos for authenticated user
- `POST /api/todos` - Create new todo item
- `GET /api/todos/{todo_id}` - Retrieve specific todo by ID
- `PUT /api/todos/{todo_id}` - Update specific todo by ID
- `DELETE /api/todos/{todo_id}` - Delete specific todo by ID

### Protected Endpoints
- `GET /api/protected` - Example protected endpoint
- `GET /api/profile` - Get user profile information

## Required New UI Pages for Todo Functionality

The current `/ui` folder contains only a landing page. To fully integrate with the backend, we need to create additional UI pages:

### 1. Authentication Pages
- **Sign Up Page** (`/signup`)
  - Component: Form with email and password fields
  - Backend Endpoint: `POST /api/auth/signup`
  - UI Components: Input fields, buttons, form validation

- **Sign In Page** (`/signin`)
  - Component: Form with email and password fields
  - Backend Endpoint: `POST /api/auth/signin`
  - UI Components: Input fields, buttons, form validation

- **Profile Page** (`/profile`)
  - Component: Display user information
  - Backend Endpoint: `GET /api/profile`
  - UI Components: User info display, logout button

### 2. Todo Management Pages
- **Dashboard/Todos Page** (`/dashboard` or `/todos`)
  - Component: Todo list display with create/update/delete functionality
  - Backend Endpoints:
    - `GET /api/todos` (to fetch todos)
    - `POST /api/todos` (to create new todo)
    - `PUT /api/todos/{todo_id}` (to update todo)
    - `DELETE /api/todos/{todo_id}` (to delete todo)
  - UI Components: Todo cards, form inputs, buttons, lists

## Implementation Strategy

### Phase 1: Landing Page Integration
- Keep existing landing page as `/ui/app/page.tsx`
- Add navigation to authentication pages

### Phase 2: Authentication Integration
- Create new pages in `/ui/app/auth/` directory:
  - `/ui/app/auth/signup/page.tsx`
  - `/ui/app/auth/signin/page.tsx`
- Implement authentication forms using UI components
- Add token management and redirect logic

### Phase 3: Todo Functionality Integration
- Create dashboard in `/ui/app/dashboard/page.tsx`
- Implement todo CRUD operations using backend API
- Use existing UI components (cards, buttons) with new functionality

## UI Components Reuse Strategy

### Reusable Components from `/ui/components`
- `Button` - For all form submissions and navigation
- `Card` - For displaying todo items
- `Input` - For todo title/description fields
- `Navbar` - For consistent navigation across pages
- `FeatureCard` - Potentially for displaying todo features

## Backend Code Comments Mapping

When restructuring the backend, add comments mapping endpoints to UI components:

```python
# UI Component: TodoListPage -> Backend Endpoint: GET /api/todos
@router.get("/", response_model=TodoListResponse)
async def get_todos(...):
    ...

# UI Component: TodoForm -> Backend Endpoint: POST /api/todos
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(...):
    ...
```

## Frontend API Integration Points

### API Client Updates
The existing frontend has an API client in `frontend/lib/api.ts`. We'll need to:
1. Update the API client to handle the new UI structure
2. Ensure it works with the App Router pattern
3. Add proper error handling for all endpoints

### Authentication Context
The existing AuthProvider in `frontend/components/auth/AuthProvider.tsx` will need to be:
1. Adapted to work with the new UI structure
2. Updated to maintain compatibility with the backend
3. Potentially restructured to match UI patterns

## Data Flow Mapping

### User Authentication Flow
1. User visits landing page
2. User clicks "Sign Up" or "Sign In"
3. User fills authentication form using UI components
4. Request sent to `/api/auth/signup` or `/api/auth/signin`
5. JWT token received and stored
6. User redirected to dashboard

### Todo Management Flow
1. User accesses dashboard page
2. UI fetches todos via `GET /api/todos`
3. User creates/updates/deletes todos using UI components
4. Requests sent to appropriate todo endpoints
5. UI updates based on API responses

## Compatibility Requirements

### API Response Format
- Ensure backend responses match UI data expectations
- Maintain consistent data structure across all endpoints
- Handle error responses appropriately in UI

### Authentication Integration
- JWT tokens must be properly handled by UI
- User state must be maintained across UI components
- Protected routes must work with backend auth middleware

## Implementation Notes

1. The UI uses App Router while the current frontend uses Pages Router
2. Need to decide whether to migrate existing frontend or create parallel UI
3. All existing backend functionality must remain intact
4. Database models and relationships should not change
5. API endpoints should remain the same for compatibility