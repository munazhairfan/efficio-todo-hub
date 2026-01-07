# Efficio Todo App - Frontend

## Overview
This is the frontend implementation of the Efficio Todo application, built with Next.js 14, TypeScript, and Tailwind CSS. The UI visually matches the reference design while connecting to an existing backend API.

## Features
- User authentication (sign up, sign in, sign out)
- Todo management (create, read, update, delete)
- Responsive design with visually appealing UI
- JWT-based authentication with token management
- User profile management

## Tech Stack
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Server Components
- Shadcn/ui components

## Project Structure
```
frontend/
├── app/                 # Next.js App Router pages
│   ├── (auth)/          # Authentication pages (sign up, sign in)
│   ├── dashboard/       # Main dashboard with todos
│   ├── profile/         # User profile page
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Landing page
│   └── not-found.tsx    # 404 error page
├── components/          # Reusable UI components
│   ├── ui/              # Base UI components (buttons, inputs, etc.)
│   ├── auth/            # Authentication components
│   ├── todo/            # Todo-specific components
│   └── navigation/      # Navigation components
├── lib/                 # Utility functions and API client
│   ├── api.ts           # API client for backend communication
│   └── auth.ts          # Authentication utilities
├── styles/              # Global styles and Tailwind config
│   └── globals.css      # Global CSS and Tailwind imports
├── types/               # TypeScript type definitions
│   └── index.ts         # Shared type definitions
└── public/              # Static assets
```

## API Integration
The frontend connects to the backend API as configured in environment variables:
- `NEXT_PUBLIC_API_URL` - Base URL for the backend API

## Environment Variables
Create a `.env.local` file in the frontend directory:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Getting Started
1. Install dependencies: `npm install` or `yarn install`
2. Set up environment variables
3. Run the development server: `npm run dev` or `yarn dev`
4. Visit `http://localhost:3000`

## Authentication Flow
1. Users can sign up or sign in via the `/auth` page
2. JWT tokens are stored in localStorage
3. Tokens are automatically attached to API requests
4. Protected routes (`/dashboard`, `/profile`) require authentication

## Todo Management
- Users can create, read, update, and delete todos
- Todos are isolated by user (each user sees only their todos)
- Todos have title, description, and completion status
- Loading states and error handling are implemented

## Styling
The application uses Tailwind CSS with custom styling that matches the reference UI design. Color palette, typography, and spacing follow the design specification.

## Error Handling
- Network errors are caught and displayed to users
- Form validation prevents invalid submissions
- Authentication errors redirect to sign-in page
- Loading states provide feedback during API calls