#!/bin/bash

# Update Frontend with EC2 IP and Restart Services
# Run this on EC2

echo "=========================================="
echo "Updating Frontend API URL and Restarting Services"
echo "=========================================="

# Navigate to project directory
cd ~/ecom-app/testneo-ecommerce-demo || exit 1

# Pull latest changes
echo "Pulling latest code..."
git pull origin main || echo "Not a git repo or already up to date"

# Activate virtual environment
source venv/bin/activate

# Kill existing services
echo "Stopping existing services..."
pkill -f "python3 main.py" || true
pkill -f "npm" || true
pkill -f "serve" || true
sleep 2

# Rebuild frontend
echo "Rebuilding frontend..."
cd frontend
npm run build
cd ..

# Start backend
echo "Starting backend on port 9000..."
nohup python3 main.py > backend.log 2>&1 &
sleep 5

# Check if backend started
if sudo lsof -i :9000 > /dev/null 2>&1; then
    echo "✓ Backend started successfully"
else
    echo "✗ Backend failed to start - check backend.log"
fi

# Start frontend
echo "Starting frontend on port 3001..."
cd frontend
nohup npm start > ../frontend.log 2>&1 &
cd ..
sleep 10

# Check if frontend started
if sudo lsof -i :3001 > /dev/null 2>&1; then
    echo "✓ Frontend started successfully"
else
    echo "✗ Frontend failed to start - check frontend.log"
fi

echo "=========================================="
echo "Services Restarted!"
echo "=========================================="
echo "Access URLs:"
echo "  Frontend: http://44.202.138.57:3001"
echo "  Admin: http://44.202.138.57:3001/admin"
echo "  Backend API: http://44.202.138.57:9000"
echo ""
echo "Admin Credentials:"
echo "  Email: admin@ecommerce.com"
echo "  Password: admin123"
echo ""
echo "To view logs:"
echo "  tail -f backend.log"
echo "  tail -f frontend.log"
echo "=========================================="

