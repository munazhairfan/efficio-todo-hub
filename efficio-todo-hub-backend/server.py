import os
import sys
import uvicorn

# Add the current directory (backend) to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Also add the parent directory to allow imports like 'backend.api.routes'
parent_dir = os.path.dirname(backend_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.main import app

if __name__ == "__main__":
    import logging

    # Set up basic logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Get port from environment variable (Hugging Face Spaces sets this)
        port = int(os.environ.get("PORT", 7860))  # Use 7860 as default as requested

        logger.info(f"Starting server on port {port}")

        # Hugging Face Spaces requires binding to 0.0.0.0
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise