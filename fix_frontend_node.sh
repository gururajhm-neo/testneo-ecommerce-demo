#!/bin/bash
# Fix frontend Node.js issues
# Run: bash fix_frontend_node.sh

set -e

echo "=========================================="
echo "Fixing Frontend Node.js Issues"
echo "=========================================="
echo ""

cd ~/ecom-app/testneo-ecommerce-demo/frontend

# Check Node version
echo "Current Node version: $(node --version)"
echo "Node path: $(which node)"
echo ""

# Clean install
echo "Cleaning node_modules and package-lock.json..."
rm -rf node_modules package-lock.json

echo "Installing dependencies with Node $(node --version)..."
npm install

echo ""
echo "=========================================="
echo "Testing Vite..."
echo "=========================================="
echo ""

# Test if Vite works
if npm run dev -- --version 2>&1 | head -1; then
    echo "✓ Vite is working!"
else
    echo "✗ Vite still has issues"
    echo ""
    echo "Trying to fix Vite version..."
    npm install vite@latest --save-dev
fi

echo ""
echo "=========================================="
echo "Fix Complete!"
echo "=========================================="
echo ""
echo "Now try: npm run dev"

