#!/bin/bash
# Check Node.js version for this project (Vite 7 needs 20.19+ or 22.12+)
echo "Current Node.js version:"
node --version 2>/dev/null || echo "not installed"
echo ""
echo "Current npm version:"
npm --version 2>/dev/null || echo "not installed"
echo ""
echo "Required: Node.js 20.19+ or 22.12+ (Vite 7)"
echo ""

if [ -s "$HOME/.nvm/nvm.sh" ]; then
    echo "✓ nvm is available at ~/.nvm"
else
    echo "✗ nvm not found — run: bash upgrade_node_ec2.sh"
fi
