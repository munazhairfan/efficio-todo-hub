import os
from fastapi import FastAPI
from dotenv import load_dotenv
from core.auth.jwt_handler import SECRET_KEY
from core.config.config import settings
from sqlmodel import SQLModel
from db import engine
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Efficio Todo App - aligned with UI component architecture",
    version="1.0.0"
)

# Add CORS middleware
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")  # Default to localhost for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import models to register them with SQLModel
from models.user import User
from models.todo import Todo

# Create database tables on startup
@app.on_event("startup")
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Import and include routes
from api.auth.handlers import router as auth_router
from api.users.handlers import router as user_router
from api.todos.handlers import router as todos_router

app.include_router(auth_router, prefix=settings.api_v1_prefix, tags=["authentication"])
app.include_router(user_router, prefix=settings.api_v1_prefix, tags=["users"])
app.include_router(todos_router)

# Additional documentation for UI integration
app.openapi_tags = [
    {
        "name": "authentication",
        "description": "Authentication endpoints for UI login/logout functionality"
    },
    {
        "name": "users",
        "description": "User profile and protected endpoints for authenticated users"
    },
    {
        "name": "todos",
        "description": "Todo management endpoints for UI todo list functionality"
    }
]

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API with Authentication"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "auth_secret_configured": bool(SECRET_KEY)}
