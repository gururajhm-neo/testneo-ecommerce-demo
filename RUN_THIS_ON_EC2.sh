#!/bin/bash

# Simple script to run on EC2 - fixes the path issues

echo "=========================================="
echo "E-commerce App Setup"
echo "=========================================="
echo ""

# Get the correct directory (handles nested directories)
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

# Step 1: Open firewall
echo "Opening firewall ports..."
sudo ufw allow 9000/tcp 2>/dev/null || true
sudo ufw allow 3001/tcp 2>/dev/null || true
echo "✓ Firewall configured"
echo ""

# Step 2: Kill existing services
echo "Stopping existing services..."
pkill -9 -f "python3 main.py" 2>/dev/null || true
pkill -9 -f "npm run dev" 2>/dev/null || true
pkill -9 -f "vite" 2>/dev/null || true
sleep 2
echo "✓ Services stopped"
echo ""

# Step 3: Setup venv if not exists
echo "Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
echo "✓ Virtual environment ready"
echo ""

# Step 4: Install Python deps
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    echo "✓ Python dependencies installed"
else
    echo "✗ requirements.txt not found"
    exit 1
fi
echo ""

# Step 5: Install Node deps
echo "Installing Node.js dependencies..."
if [ -d "frontend" ]; then
    cd frontend
    if [ ! -d "node_modules" ]; then
        npm install
        echo "✓ Node.js dependencies installed"
    else
        echo "✓ Node.js dependencies already installed"
    fi
    cd ..
else
    echo "✗ frontend directory not found"
    exit 1
fi
echo ""

# Step 6: Start backend
echo "Starting backend..."
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
sleep 8

if curl -s http://localhost:9000/docs > /dev/null 2>&1; then
    echo "✓ Backend is running"
else
    echo "✗ Backend failed to start"
    echo "Last 20 lines of backend.log:"
    tail -20 backend.log
fi
echo ""

# Step 7: Start frontend
echo "Starting frontend..."
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
cd ..
sleep 8

if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✓ Frontend is running"
else
    echo "✗ Frontend failed to start"
    echo "Last 20 lines of frontend.log:"
    tail -20 frontend.log
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo "Access your app:"
echo "  Frontend: http://44.202.138.57:3001"
echo "  Backend: http://44.202.138.57:9000"
echo "  Admin: http://44.202.138.57:3001/admin"
echo ""
echo "Login: admin@ecommerce.com / admin123"
echo ""

