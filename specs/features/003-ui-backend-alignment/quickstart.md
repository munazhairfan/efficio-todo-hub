# Quickstart: Backend UI Alignment

## Overview
This guide provides a quick setup and testing approach for the backend UI alignment feature. This restructuring maintains all existing functionality while organizing the backend code to match UI patterns.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for UI development)
- PostgreSQL database
- Environment variables configured (DATABASE_URL, BETTER_AUTH_SECRET)

## Setup

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
```

### 3. Database Setup
```bash
cd backend
alembic upgrade head
```

## Running the Application

### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### UI
```bash
cd ui
npm install
npm run dev
```

## Testing the Feature

### 1. Verify API Endpoints
After restructuring, all existing endpoints should continue to work:
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/verify` - Token verification
- `GET /api/todos` - Get user's todos
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo

### 2. Test Authentication Flow
1. Register a new user via `/api/auth/signup`
2. Login with the new user via `/api/auth/signin`
3. Verify the token works with `/api/auth/verify`
4. Use the token to access protected endpoints

### 3. Test Todo Operations
1. Authenticate and get a token
2. Create a new todo via `POST /api/todos`
3. Retrieve todos via `GET /api/todos`
4. Update a todo via `PUT /api/todos/{id}`
5. Delete a todo via `DELETE /api/todos/{id}`

## Key Changes in Restructure

### Before
```
backend/
├── routes/
├── auth/
├── database/
├── main.py
└── dependencies.py
```

### After
```
backend/
├── api/
│   ├── auth/
│   ├── todos/
│   └── users/
├── core/
│   ├── auth/
│   ├── security/
│   └── config/
├── models/
├── services/
├── database/
├── utils/
├── dependencies/
├── main.py
└── config.py
```

## Verification Checklist

- [ ] All existing API endpoints continue to work as before
- [ ] Authentication flow functions correctly
- [ ] Todo CRUD operations work properly
- [ ] Database models remain unchanged
- [ ] JWT tokens continue to work
- [ ] No breaking changes to existing functionality
- [ ] New structure follows UI component organization patterns

## Troubleshooting

### Endpoints Not Working
- Check that import paths are updated after restructuring
- Verify that route registration in main.py is correct

### Authentication Issues
- Ensure JWT secret is properly configured
- Verify token validation functions are working

### Database Connection Issues
- Confirm DATABASE_URL is correctly set
- Check that database is running and accessible