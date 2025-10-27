#!/bin/bash

# Kill and restart services script

echo "=========================================="
echo "Restarting E-commerce Services"
echo "=========================================="
echo ""

# Find correct directory
if [ -f "main.py" ]; then
    PROJ_DIR=$(pwd)
elif [ -f "../main.py" ]; then
    cd ..
    PROJ_DIR=$(pwd)
elif [ -d "/home/ubuntu/ecom-app/testneo-ecommerce-demo" ]; then
    cd /home/ubuntu/ecom-app/testneo-ecommerce-demo
    PROJ_DIR=$(pwd)
else
    echo "Error: Could not find project directory"
    exit 1
fi

echo "Working directory: $PROJ_DIR"
echo ""

# Kill existing services
echo "Stopping existing services..."
pkill -9 -f "python3 main.py" 2>/dev/null || true
pkill -9 -f "npm run dev" 2>/dev/null || true
pkill -9 -f "vite" 2>/dev/null || true
sleep 3
echo "✓ Services stopped"
echo ""

# Start backend
echo "Starting backend on port 9000..."
cd "$PROJ_DIR"
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
sleep 8

if curl -s http://localhost:9000/docs > /dev/null 2>&1; then
    echo "✓ Backend started"
else
    echo "✗ Backend failed"
    tail -10 backend.log
fi
echo ""

# Start frontend
echo "Starting frontend on port 3001..."
cd "$PROJ_DIR/frontend"
nohup npm run dev > ../frontend.log 2>&1 &
cd "$PROJ_DIR"
sleep 8

if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✓ Frontend started"
else
    echo "✗ Frontend failed"
    tail -10 frontend.log
fi
echo ""

echo "=========================================="
echo "Services Restarted!"
echo "=========================================="
echo "Access URLs:"
echo "  http://44.202.138.57:3001"
echo "  http://44.202.138.57:3001/admin"
echo ""
echo "To view logs:"
echo "  tail -f backend.log"
echo "  tail -f frontend.log"
echo ""
