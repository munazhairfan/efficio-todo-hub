from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import conversation, error, users
from middleware.error_handler import setup_error_handling
from database import get_engine
from api.models.conversation_state import ConversationState
from api.models.error_context import ErrorContext
from src.models.user import User
from src.models.task import Task
from sqlmodel import SQLModel


# Create FastAPI app
app = FastAPI(title="Todo App API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handling middleware
setup_error_handling(app)

# Include API routes
app.include_router(conversation.router)
app.include_router(error.router)
app.include_router(users.router)

# Create all tables
@app.on_event("startup")
def on_startup():
    engine = get_engine()
    # Create tables for SQLAlchemy models (using declarative base from session)
    from src.database.session import Base as SQLAlchemyBase
    SQLAlchemyBase.metadata.create_all(bind=engine)
    # Create tables for SQLModel models
    SQLModel.metadata.create_all(bind=engine)

# Removed blocking database initialization from startup to prevent hanging
# Database tables will be created when first accessed

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-app-api"}

if __name__ == "__main__":
    import uvicorn
    import os
    # Get port from environment variable (Hugging Face Spaces sets this)
    port = int(os.environ.get("PORT", 7860))  # Default to 7860 as requested

    # Hugging Face Spaces requires binding to 0.0.0.0
    uvicorn.run(app, host="0.0.0.0", port=port)