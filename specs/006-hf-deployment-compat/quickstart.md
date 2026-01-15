# Quickstart: Hugging Face Deployment Compatibility

**Feature**: Hugging Face Deployment Compatibility
**Date**: 2026-01-15
**Status**: Complete

## Overview

This guide provides instructions for deploying the FastAPI chatbot backend to Hugging Face Spaces.

## Prerequisites

- FastAPI application with existing functionality
- Proper requirements.txt file
- Health check endpoint available

## Deployment Steps

### 1. Prepare the Application

1. Ensure the `server.py` file exists with Hugging Face compatible startup configuration
2. Verify that the application binds to `0.0.0.0` and reads the `PORT` environment variable
3. Confirm the `/health` endpoint is available

### 2. Hugging Face Space Configuration

1. Create a new Space on Hugging Face
2. Choose the "Docker" option for custom deployment
3. Add the following to your Dockerfile:

```Dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["python", "backend/server.py"]
```

### 3. Alternative: Python Server Option

If using Hugging Face's Python server option:

1. Ensure the `server.py` file is in the root directory or properly referenced
2. The application will automatically use the PORT environment variable
3. Make sure the server binds to 0.0.0.0

### 4. Verification

1. After deployment, check the application logs for startup messages
2. Visit the `/health` endpoint to verify the application is running
3. Test the chat functionality to ensure all features work as expected

## Local Testing

To test locally with the same configuration as Hugging Face:

```bash
PORT=8000 python backend/server.py
```

Then visit `http://localhost:8000/health` to verify the health endpoint.

## Troubleshooting

- If the application crashes on startup, check that it binds to `0.0.0.0` and not `localhost`
- If the health check fails, verify that the `/health` endpoint returns a proper JSON response
- If environment variables aren't working, ensure the PORT variable is properly passed to the application