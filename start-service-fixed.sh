#!/bin/bash
# Start E-commerce Services (Fixed for Node.js 18+)
set -e

echo "Starting E-commerce Services..."
echo ""

# Check Node version
NODE_VERSION=$(node --version 2>/dev/null || echo "not found")
echo "Using Node: $NODE_VERSION"

if [[ ! "$NODE_VERSION" =~ ^v1[89]\. ]]; then
    echo "⚠ Warning: Node.js 18+ required for Vite"
    echo "Current version: $NODE_VERSION"
fi

# Activate Python venv
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Python venv activated"
fi

# Check for existing services
echo ""
echo "Checking for existing services..."

# Kill existing backend
if lsof -ti:9000 > /dev/null 2>&1; then
    echo "Killing existing backend on port 9000..."
    lsof -ti:9000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Kill existing frontend
if lsof -ti:3001 > /dev/null 2>&1; then
    echo "Killing existing frontend on port 3001..."
    lsof -ti:3001 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start backend
echo ""
echo "Starting backend..."
if [ -f "main.py" ]; then
    nohup python3 main.py > backend.log 2>&1 &
    BACKEND_PID=$!
    echo "Backend started with PID: $BACKEND_PID"
    
    # Wait a moment and check
    sleep 3
    if curl -s http://localhost:9000/health > /dev/null 2>&1; then
        echo "✓ Backend is running on port 9000"
    else
        echo "⚠ Backend may still be starting..."
    fi
else
    echo "✗ main.py not found in current directory"
    exit 1
fi

# Start frontend
echo ""
echo "Starting frontend..."
cd frontend

# Ensure node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Check Node version before starting
NODE_VER=$(node --version)
echo "Using Node: $NODE_VER for frontend"

# Start frontend dev server
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

# Wait and check
sleep 5
if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✓ Frontend is running on port 3001"
else
    echo "✗ Frontend failed to start"
    echo "Check frontend.log for errors:"
    echo "  tail -f frontend.log"
    echo ""
    echo "Common fix:"
    echo "  cd frontend"
    echo "  rm -rf node_modules package-lock.json"
    echo "  npm install"
fi

cd ..

echo ""
echo "=========================================="
echo "Services Status"
echo "=========================================="
echo "Backend:  http://localhost:9000"
echo "Frontend: http://localhost:3001"
echo ""
echo "Logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo "=========================================="

