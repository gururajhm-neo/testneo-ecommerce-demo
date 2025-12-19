#!/bin/bash
# Upgrade Node.js to version 18+ on EC2
# Run: bash upgrade_node_ec2.sh

set -e

echo "=========================================="
echo "Upgrading Node.js for Vite Compatibility"
echo "=========================================="
echo ""

# Check current version
CURRENT_NODE=$(node --version 2>/dev/null || echo "not installed")
echo "Current Node.js: $CURRENT_NODE"
echo ""

# Install nvm if not present
if [ ! -d "$HOME/.nvm" ]; then
    echo "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js 18 (LTS)
echo "Installing Node.js 18 (LTS)..."
nvm install 18
nvm use 18
nvm alias default 18

# Verify installation
echo ""
echo "=========================================="
echo "Verification"
echo "=========================================="
node --version
npm --version

echo ""
echo "✓ Node.js upgraded successfully!"
echo "Now run: cd frontend && npm install && npm run dev"

