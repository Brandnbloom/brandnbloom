#!/bin/bash
# Start script for Render deployment

cd backend
uvicorn server:app --host 0.0.0.0 --port ${PORT:-8001}
