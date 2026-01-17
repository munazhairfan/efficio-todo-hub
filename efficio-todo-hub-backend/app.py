# Hugging Face Space entry point
# This file is used by Hugging Face Spaces as the main application entry point

import os
import uvicorn
from src.main import app

if __name__ == "__main__":
    # Get port from environment variable (Hugging Face Spaces sets this)
    port = int(os.environ.get("PORT", 8000))

    # Hugging Face Spaces requires binding to 0.0.0.0
    uvicorn.run(app, host="0.0.0.0", port=port)