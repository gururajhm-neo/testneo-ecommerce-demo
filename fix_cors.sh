#!/bin/bash

# Fix CORS and Restart Services on EC2

echo "=========================================="
echo "Fixing CORS and Restarting Services"
echo "=========================================="

# Navigate to project directory
cd ~/ecom-app/testneo-ecommerce-demo || exit 1

# Pull latest changes
echo "Pulling latest code..."
git pull origin main || echo "Note: Push changes first from local"

# Activate virtual environment
source venv/bin/activate

# Kill existing backend
echo "Stopping existing backend..."
pkill -f "python3 main.py" || true
sleep 2

# Start backend with new CORS settings
echo "Starting backend with updated CORS..."
nohup python3 main.py > backend.log 2>&1 &
sleep 5

# Check if backend started
if sudo lsof -i :9000 > /dev/null 2>&1; then
    echo "✓ Backend restarted successfully"
else
    echo "✗ Backend failed to start - check backend.log"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Backend restarted with CORS fixes!"
echo "=========================================="
echo ""
echo "Access URLs:"
echo "  Frontend: http://44.202.138.57:3001"
echo "  Admin Panel: http://44.202.138.57:3001/admin"
echo ""
echo "Admin Login:"
echo "  Email: admin@ecommerce.com"
echo "  Password: admin123"
echo ""
echo "To view logs:"
echo "  tail -f backend.log"
echo "=========================================="

