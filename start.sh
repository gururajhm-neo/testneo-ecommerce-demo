#!/bin/bash

# Simple start script for EC2
# This script starts both backend and frontend

echo "Starting E-commerce Application..."

# Kill existing processes
echo "Killing existing services..."
pkill -f "python main.py" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# Start backend
echo "Starting backend on port 9000..."
nohup python main.py > backend.log 2>&1 &
sleep 5

# Start frontend on port 3001
echo "Starting frontend on port 3001..."
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
cd ..
sleep 5

echo ""
echo "=========================================="
echo "Services Started!"
echo "Backend: http://44.202.138.57:9000"
echo "Frontend: http://44.202.138.57:3001"
echo "Admin Panel: http://44.202.138.57:3001/admin"
echo "=========================================="
echo ""

