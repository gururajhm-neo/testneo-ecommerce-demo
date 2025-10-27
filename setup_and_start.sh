#!/bin/bash

# Complete setup and start script for EC2

echo "=========================================="
echo "E-commerce App Setup on EC2"
echo "=========================================="
echo ""

# Navigate to project
if [ -d "testneo-ecommerce-demo" ]; then
    cd testneo-ecommerce-demo
elif [ -d "/home/ubuntu/ecom-app/testneo-ecommerce-demo" ]; then
    cd /home/ubuntu/ecom-app/testneo-ecommerce-demo
fi

PROJECT_DIR=$(pwd)
echo "Project directory: $PROJECT_DIR"
echo ""

# Step 1: Open firewall ports
echo "Step 1: Opening firewall ports..."
sudo ufw allow 9000/tcp
sudo ufw allow 3001/tcp
echo "✓ Ports opened"
echo ""

# Step 2: Stop existing services
echo "Step 2: Stopping existing services..."
pkill -9 -f "python3 main.py" 2>/dev/null
pkill -9 -f "npm run dev" 2>/dev/null
pkill -9 -f "vite" 2>/dev/null
sleep 2
echo "✓ Services stopped"
echo ""

# Step 3: Setup Python virtual environment
echo "Step 3: Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Step 4: Install Python dependencies
echo "Step 4: Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Python dependencies installed"
echo ""

# Step 5: Install Node.js dependencies
echo "Step 5: Installing Node.js dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
    echo "✓ Node.js dependencies installed"
else
    echo "✓ Node.js dependencies already installed"
fi
cd ..
echo ""

# Step 6: Start backend
echo "Step 6: Starting backend on port 9000..."
cd "$PROJECT_DIR"
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
sleep 8

# Check backend
if curl -s http://localhost:9000/docs > /dev/null 2>&1; then
    echo "✓ Backend is running and responding"
else
    echo "✗ Backend not responding - checking logs..."
    tail -30 backend.log | grep -i error || echo "No errors in last 30 lines"
fi
echo ""

# Step 7: Start frontend
echo "Step 7: Starting frontend on port 3001..."
cd "$PROJECT_DIR/frontend"
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd "$PROJECT_DIR"
echo "Frontend PID: $FRONTEND_PID"
sleep 8
echo ""

# Step 8: Verify services
echo "Step 8: Verifying services..."
echo ""

# Check if processes are running
echo "Running processes:"
ps aux | grep -E "python3 main.py|npm run dev" | grep -v grep
echo ""

# Test backend
if curl -s http://localhost:9000/docs > /dev/null 2>&1; then
    echo "✓ Backend responding on localhost:9000"
else
    echo "✗ Backend not responding"
    echo "Backend logs:"
    tail -20 backend.log
fi

# Test frontend
if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✓ Frontend responding on localhost:3001"
else
    echo "✗ Frontend not responding"
    echo "Frontend logs:"
    tail -20 frontend.log
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Access URLs:"
echo "  Frontend: http://44.202.138.57:3001"
echo "  Backend: http://44.202.138.57:9000"
echo "  Admin: http://44.202.138.57:3001/admin"
echo ""
echo "Login credentials:"
echo "  Email: admin@ecommerce.com"
echo "  Password: admin123"
echo ""
echo "View logs:"
echo "  tail -f $PROJECT_DIR/backend.log"
echo "  tail -f $PROJECT_DIR/frontend.log"
echo ""
echo "Stop services:"
echo "  pkill -f 'python3 main.py'"
echo "  pkill -f 'npm run dev'"
echo ""
echo "=========================================="

