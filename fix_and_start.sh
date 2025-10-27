#!/bin/bash

# Fix common issues and start services

echo "=========================================="
echo "Fixing Common Issues and Starting Services"
echo "=========================================="
echo ""

# Step 1: Navigate to project directory
if [ -f "main.py" ]; then
    echo "✓ Found main.py in current directory"
elif [ -d "testneo-ecommerce-demo" ]; then
    cd testneo-ecommerce-demo
    echo "✓ Moved to testneo-ecommerce-demo"
elif [ -d "/home/ubuntu/ecom-app/testneo-ecommerce-demo" ]; then
    cd /home/ubuntu/ecom-app/testneo-ecommerce-demo
    echo "✓ Moved to /home/ubuntu/ecom-app/testneo-ecommerce-demo"
else
    echo "✗ Could not find project directory"
    exit 1
fi

echo "Current directory: $(pwd)"
echo ""

# Step 2: Disable UFW firewall (if running)
echo "Step 2: Checking firewall..."
if sudo ufw status | grep -q "Status: active"; then
    echo "⚠ Firewall is active, temporarily disabling for testing..."
    sudo ufw allow 9000/tcp
    sudo ufw allow 3001/tcp
    echo "✓ Ports added to UFW"
else
    echo "✓ UFW is not active"
fi
echo ""

# Step 3: Kill existing processes
echo "Step 3: Stopping existing services..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 3
echo "✓ Existing services stopped"
echo ""

# Step 4: Install dependencies if needed
echo "Step 4: Checking dependencies..."
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠ Frontend dependencies not found, installing..."
    cd frontend
    npm install
    cd ..
fi
echo "✓ Dependencies checked"
echo ""

# Step 5: Start backend
echo "Step 5: Starting backend..."
nohup python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
sleep 5

# Check if backend started
if ps -p $BACKEND_PID > /dev/null; then
    echo "✓ Backend is running"
else
    echo "✗ Backend failed to start. Check backend.log"
    cat backend.log
    exit 1
fi
echo ""

# Step 6: Start frontend
echo "Step 6: Starting frontend..."
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "Frontend PID: $FRONTEND_PID"
sleep 5
echo ""

# Step 7: Verify services
echo "Step 7: Verifying services..."
echo ""

# Check if ports are listening
if netstat -tuln 2>/dev/null | grep -q ":9000 "; then
    echo "✓ Backend listening on port 9000"
else
    echo "✗ Backend not listening on port 9000"
fi

if netstat -tuln 2>/dev/null | grep -q ":3001 "; then
    echo "✓ Frontend listening on port 3001"
else
    echo "✗ Frontend not listening on port 3001"
fi

echo ""

# Step 8: Test local connections
echo "Step 8: Testing local connections..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/docs)
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001)

if [ "$BACKEND_STATUS" = "200" ]; then
    echo "✓ Backend responding (HTTP $BACKEND_STATUS)"
else
    echo "✗ Backend not responding (HTTP $BACKEND_STATUS)"
fi

if [ "$FRONTEND_STATUS" = "200" ]; then
    echo "✓ Frontend responding (HTTP $FRONTEND_STATUS)"
else
    echo "✗ Frontend not responding (HTTP $FRONTEND_STATUS)"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo "Backend URL: http://44.202.138.57:9000"
echo "Frontend URL: http://44.202.138.57:3001"
echo "Admin Panel: http://44.202.138.57:3001/admin"
echo ""
echo "To view logs:"
echo "  tail -f backend.log"
echo "  tail -f frontend.log"
echo "=========================================="

