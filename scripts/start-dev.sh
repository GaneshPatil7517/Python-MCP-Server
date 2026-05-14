#!/bin/bash
# Start development server with hot reload

echo "🚀 Starting MCP Server in development mode..."

# Load environment
if [ -f ".env" ]; then
    export $(cat .env | grep -v '#' | xargs)
else
    echo "⚠️  .env file not found. Using defaults."
fi

# Run server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
