#!/bin/bash

# Simple start script that works with production build

echo "Starting services..."

cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

# Kill existing
pkill -9 -f "python3 main.py" 2>/dev/null || true
pkill -9 -f "npm" 2>/dev/null || true
pkill -9 -f "vite" 2>/dev/null || true
sleep 2

# Start backend
echo "Starting backend..."
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
sleep 5

# Build and serve frontend
echo "Building frontend..."
cd frontend
npm run build
echo "Starting frontend server..."
npx serve -s dist -l 3001 > ../frontend.log 2>&1 &
cd ..

sleep 5

echo ""
echo "Services started!"
echo "Access: http://44.202.138.57:3001"
echo ""
echo "Check status:"
curl -s -o /dev/null -w "Backend: %{http_code}\n" http://localhost:9000/docs
curl -s -o /dev/null -w "Frontend: %{http_code}\n" http://localhost:3001

