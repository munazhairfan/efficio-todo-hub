# Quickstart: User Authentication

## Setup Instructions

### Frontend Setup
1. Install Better Auth dependencies:
   ```bash
   cd frontend
   npm install @better-auth/react @better-auth/node
   ```

2. Configure Better Auth in `auth.config.ts`:
   ```typescript
   import { createAuthClient } from "@better-auth/client";

   export const auth = createAuthClient({
     baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
     plugins: [
       // Enable JWT plugin
     ]
   });
   ```

3. Set up authentication context in `_app.tsx`:
   ```tsx
   import { AuthProvider } from '../components/auth/AuthProvider';

   function MyApp({ Component, pageProps }) {
     return (
       <AuthProvider>
         <Component {...pageProps} />
       </AuthProvider>
     );
   }
   ```

### Backend Setup
1. Install required dependencies:
   ```bash
   cd backend
   pip install pyjwt[crypto] python-jose[cryptography]
   ```

2. Create JWT verification utility in `auth/jwt_handler.py`:
   ```python
   from fastapi import HTTPException, status
   import jwt
   from jwt import PyJWKClient

   SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
   ALGORITHM = "HS256"

   def verify_jwt_token(token: str):
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           user_id: str = payload.get("sub")
           if user_id is None:
               raise HTTPException(
                   status_code=status.HTTP_401_UNAUTHORIZED,
                   detail="Could not validate credentials"
               )
           return {"user_id": user_id}
       except jwt.JWTError:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Could not validate credentials"
           )
   ```

3. Create authentication dependency in `auth/middleware.py`:
   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

   security = HTTPBearer()

   async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
       token = credentials.credentials
       return verify_jwt_token(token)
   ```

## Running the Application

### Development
1. Start the backend:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

### Environment Variables
Create `.env` files in both frontend and backend with:
- `BETTER_AUTH_SECRET`: Your JWT signing secret
- `NEXT_PUBLIC_API_URL`: Backend API URL (e.g., http://localhost:8000)

## Key Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Login and get JWT token
- `POST /api/auth/verify` - Verify JWT token validity

### Protected Routes
- All routes under `/api/*` (except auth routes) require valid JWT token
- Token should be passed in `Authorization: Bearer <token>` header