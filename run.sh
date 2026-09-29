#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "⚡ Starting EdgeShield AI Services..."

# 1. Start Backend on port 8000 if not active
if ! lsof -i :8000 > /dev/null 2>&1; then
    echo "Starting FastAPI Backend on port 8000..."
    PYTHONPATH=backend nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    sleep 2
else
    echo "✓ Backend is already running on port 8000."
fi

# 2. Start Frontend on port 5173 if not active
if ! lsof -i :5173 > /dev/null 2>&1; then
    echo "Starting Vite Frontend on port 5173..."
    (cd "$DIR/frontend" && nohup ./node_modules/.bin/vite --host 0.0.0.0 --port 5173 > "$DIR/frontend.log" 2>&1 &)
    sleep 2
else
    echo "✓ Frontend is already running on port 5173."
fi

echo ""
echo "🚀 EdgeShield AI is live and ready!"
echo "   Frontend Dashboard: http://localhost:5173"
echo "   Backend API:        http://localhost:8000"
echo "   API Docs:           http://localhost:8000/docs"
echo ""

# Open default browser on macOS
if command -v open > /dev/null 2>&1; then
    open http://localhost:5173
fi
