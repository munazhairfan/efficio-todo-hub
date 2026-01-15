# Quickstart: Frontend UI Reimplementation

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (running on localhost:8000 by default)
- Git for version control

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd efficio-todo-hub
```

### 2. Navigate to Frontend Directory
```bash
cd frontend
```

### 3. Install Dependencies
```bash
npm install
# or
yarn install
```

### 4. Environment Configuration
Create a `.env.local` file in the frontend directory with the following:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 5. Start Development Server
```bash
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`

## Key Features

### Authentication
- User signup and signin flows
- JWT token management
- Protected routes for authenticated users

### Todo Management
- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- View all user todos in a list

### UI Components
- Reusable UI components matching the reference UI
- Responsive design patterns
- Consistent styling with Tailwind CSS

## API Integration

The frontend connects to the existing backend API at the configured `NEXT_PUBLIC_API_URL`. All authentication and data operations use the existing backend endpoints without modification.

## Development Workflow

1. **Component Development**: Create new components in the `/components` directory
2. **Page Creation**: Add new pages in the `/app` directory using Next.js App Router
3. **API Integration**: Use the API client in `/lib/api.ts` for backend communication
4. **Styling**: Apply Tailwind CSS classes following the reference UI patterns
5. **Testing**: Add tests in the `/tests` directory following Next.js testing patterns