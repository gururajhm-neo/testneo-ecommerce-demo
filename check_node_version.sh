#!/bin/bash
# Check Node.js version
echo "Current Node.js version:"
node --version
echo ""
echo "Current npm version:"
npm --version
echo ""
echo "Required: Node.js 18+ for Vite"
echo ""

# Check if nvm is installed
if command -v nvm &> /dev/null || [ -s "$HOME/.nvm/nvm.sh" ]; then
    echo "✓ nvm is available"
else
    echo "✗ nvm not found"
fi

