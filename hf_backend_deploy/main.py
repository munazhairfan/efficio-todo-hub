from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import conversation, error
from backend.middleware.error_handler import setup_error_handling
from backend.database import engine
from backend.api.models.conversation_state import ConversationState
from backend.api.models.error_context import ErrorContext
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

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-app-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)