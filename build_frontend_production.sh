#!/bin/bash
# Build frontend for production (alternative to dev server)
# This builds static files that can be served with nginx or any web server

set -e

echo "=========================================="
echo "Building Frontend for Production"
echo "=========================================="
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Building production bundle..."
npm run build

echo ""
echo "=========================================="
echo "Build Complete!"
echo "=========================================="
echo ""
echo "Built files are in: frontend/dist"
echo ""
echo "To serve with nginx, point to: frontend/dist"
echo "Or use a simple HTTP server:"
echo "  cd frontend/dist && python3 -m http.server 3001"

