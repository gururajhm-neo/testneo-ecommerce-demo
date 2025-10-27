#!/bin/bash

echo "Fixing frontend issues..."

# Navigate to project
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

echo "Current directory: $(pwd)"

# Kill frontend
pkill -9 -f "npm run dev" 2>/dev/null || true
pkill -9 -f "vite" 2>/dev/null || true
sleep 2

# Remove node_modules and reinstall
echo "Reinstalling frontend dependencies..."
cd frontend
rm -rf node_modules package-lock.json

# Reinstall with compatible versions
npm install --legacy-peer-deps

echo "Starting frontend..."
nohup npm run dev > ../frontend.log 2>&1 &
sleep 10

if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✓ Frontend is working!"
else
    echo "✗ Frontend still failing. Check logs:"
    tail -20 ../frontend.log
fi

echo ""
echo "Check status:"
curl -s -o /dev/null -w "Backend: %{http_code}\n" http://localhost:9000/docs
curl -s -o /dev/null -w "Frontend: %{http_code}\n" http://localhost:3001

