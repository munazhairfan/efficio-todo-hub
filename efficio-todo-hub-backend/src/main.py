"""Main FastAPI application."""

import sys
import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import using relative imports from within src package
from .api.chat import router as chat_router
from .middleware.rate_limiter import RateLimitMiddleware

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

# Import conversation router with error handling - try different import paths
try:
    # Try relative import from package structure
    from ..api.routes.conversation import router as conversation_router
    app.include_router(conversation_router)
except ImportError as e:
    try:
        # Try absolute import assuming backend is in Python path
        from api.routes.conversation import router as conversation_router
        app.include_router(conversation_router)
    except ImportError as e2:
        print(f"Warning: Could not import conversation router: {e}, {e2}")
        print(f"Error details: {type(e2).__name__}: {e2}")

# Import error router with error handling - try different import paths
try:
    # Try relative import from package structure
    from ..api.routes.error import router as error_router
    app.include_router(error_router)
except ImportError as e:
    try:
        # Try absolute import assuming backend is in Python path
        from api.routes.error import router as error_router
        app.include_router(error_router)
    except ImportError as e2:
        print(f"Warning: Could not import error router: {e}, {e2}")
        print(f"Error details: {type(e2).__name__}: {e2}")

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"message": "Efficio Todo Hub Chat API is running!"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# Additional endpoints for Hugging Face Spaces compatibility
@app.get("/startup-health")
def startup_health():
    """Startup health check for Hugging Face Spaces."""
    try:
        # Verify required environment variables are available
        required_vars = ["DATABASE_URL"]
        missing_vars = []

        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            return {
                "status": "unhealthy",
                "missing_environment_variables": missing_vars,
                "timestamp": datetime.utcnow()
            }

        return {
            "status": "healthy",
            "environment_ok": True,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }