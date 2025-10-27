#!/bin/bash

# Start services with production build for frontend

echo "Starting services with production frontend..."

# Navigate to project
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

# Kill existing
pkill -9 -f "python3 main.py" 2>/dev/null || true
pkill -9 -f "npm run dev" 2>/dev/null || true
pkill -9 -f "vite" 2>/dev/null || true
pkill -9 -f "npx" 2>/dev/null || true
sleep 2

# Start backend
echo "Starting backend..."
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
sleep 8

if curl -s http://localhost:9000/docs > /dev/null 2>&1; then
    echo "✓ Backend running"
else
    echo "✗ Backend failed"
fi

# Build and serve frontend in production mode
cd frontend

echo "Building frontend for production..."
npm run build 2>&1 | tail -20

echo "Serving frontend..."
nohup npx serve -s dist -l 3001 > ../frontend.log 2>&1 &
cd ..

sleep 5

if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✓ Frontend running on port 3001"
else
    echo "✗ Frontend check logs"
    tail -20 frontend.log
fi

echo ""
echo "========================================="
echo "Services Started!"
echo "Access: http://44.202.138.57:3001"
echo "========================================="

