#!/bin/bash
# Upgrade Node.js to version 20+ on EC2 (required by Vite 7)
# Run: bash upgrade_node_ec2.sh

set -e

echo "=========================================="
echo "Upgrading Node.js for Vite 7 Compatibility"
echo "=========================================="
echo ""

CURRENT_NODE=$(node --version 2>/dev/null || echo "not installed")
echo "Current Node.js: $CURRENT_NODE"
echo ""

# Install nvm if not present
if [ ! -d "$HOME/.nvm" ]; then
    echo "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi

export NVM_DIR="$HOME/.nvm"
# shellcheck disable=SC1091
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
# shellcheck disable=SC1091
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

echo "Installing Node.js 20 (LTS)..."
nvm install 20
nvm use 20
nvm alias default 20

echo ""
echo "=========================================="
echo "Verification"
echo "=========================================="
node --version
npm --version

echo ""
echo "✓ Node.js upgraded successfully!"
echo "Next:"
echo "  cd ~/testneo-ecommerce-demo/frontend"
echo "  rm -rf node_modules"
echo "  npm install"
echo "  cd .. && ./stop_all.sh && ./start_all.sh"
