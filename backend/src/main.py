"""Main FastAPI application."""

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chat import router as chat_router
from .middleware.rate_limiter import RateLimitMiddleware
# Import conversation router from the backend.api.routes module
from api.routes.conversation import router as conversation_router

# Create the FastAPI app
app = FastAPI(
    title="Efficio Todo Hub - Chat API",
    description="API for chat and conversation handling",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Include API routes
app.include_router(chat_router)
app.include_router(conversation_router)

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"message": "Efficio Todo Hub Chat API is running!"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}