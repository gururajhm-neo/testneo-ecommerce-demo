#!/bin/bash

# Quick Fix for EC2 - Run This Script

echo "=========================================="
echo "Quick Fix for EC2 Issues"
echo "=========================================="
echo ""

# Step 1: Open UFW firewall ports
echo "Step 1: Opening firewall ports..."
sudo ufw allow 9000/tcp
sudo ufw allow 3001/tcp
sudo ufw allow 3000/tcp
echo "✓ Ports opened"
echo ""

# Step 2: Kill existing processes
echo "Step 2: Stopping existing services..."
pkill -9 -f "python" 2>/dev/null
pkill -9 -f "npm run dev" 2>/dev/null
pkill -9 -f "vite" 2>/dev/null
sleep 3
echo "✓ Services stopped"
echo ""

# Step 3: Navigate to project
if [ -f "main.py" ]; then
    PROJECT_DIR=$(pwd)
elif [ -d "testneo-ecommerce-demo" ]; then
    cd testneo-ecommerce-demo
    PROJECT_DIR=$(pwd)
elif [ -d "/home/ubuntu/ecom-app/testneo-ecommerce-demo" ]; then
    cd /home/ubuntu/ecom-app/testneo-ecommerce-demo
    PROJECT_DIR=/home/ubuntu/ecom-app/testneo-ecommerce-demo
fi

echo "Project directory: $PROJECT_DIR"
echo ""

# Step 4: Start backend with python3
echo "Step 4: Starting backend on port 9000..."
cd "$PROJECT_DIR"
nohup python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
sleep 8

# Check backend
if curl -s http://localhost:9000/docs > /dev/null; then
    echo "✓ Backend is running"
else
    echo "✗ Backend not responding - check backend.log"
    tail -20 backend.log
fi
echo ""

# Step 5: Start frontend
echo "Step 5: Starting frontend on port 3001..."
cd "$PROJECT_DIR/frontend"
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd "$PROJECT_DIR"
echo "Frontend PID: $FRONTEND_PID"
sleep 8
echo ""

# Step 6: Verify
echo "Step 6: Verifying services..."
echo ""

# Check ports using ss instead of netstat
echo "Backend:"
ss -tuln | grep ":9000 " || echo "Not listening on 9000"

echo ""
echo "Frontend:"
ss -tuln | grep ":3001 " || echo "Not listening on 3001"

echo ""

# Test connections
echo "Testing connections..."
if curl -s -o /dev/null -w "Backend: %{http_code}\n" http://localhost:9000/docs; then
    echo "✓ Backend responding"
else
    echo "✗ Backend not responding"
fi

if curl -s -o /dev/null -w "Frontend: %{http_code}\n" http://localhost:3001; then
    echo "✓ Frontend responding"
else
    echo "✗ Frontend not responding"
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
echo "Check logs:"
echo "  tail -f backend.log"
echo "  tail -f frontend.log"
echo ""
echo "Check status:"
echo "  ps aux | grep python3"
echo "  ps aux | grep 'npm run dev'"
echo ""
echo "=========================================="

