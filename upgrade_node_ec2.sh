#!/bin/bash
# Install Node.js 20 for THIS demo only (does NOT change the system default Node).
# Safe to run on the same EC2 as the main TestNeo product.
# Run: bash upgrade_node_ec2.sh

set -e

echo "=========================================="
echo "Install Node 20 for ecommerce demo only"
echo "=========================================="
echo ""
echo "This uses nvm and does NOT change your default Node."
echo "Main TestNeo can keep using system/default Node 18."
echo ""

CURRENT_NODE=$(node --version 2>/dev/null || echo "not installed")
echo "Current shell Node.js: $CURRENT_NODE"
echo ""

if [ ! -d "$HOME/.nvm" ]; then
    echo "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi

export NVM_DIR="$HOME/.nvm"
# shellcheck disable=SC1091
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

echo "Installing Node.js 20 (side-by-side; default left unchanged)..."
nvm install 20

# Do NOT run: nvm alias default 20
# That would change Node for the whole ubuntu user and could affect main TestNeo.

echo ""
echo "=========================================="
echo "Verification"
echo "=========================================="
nvm exec 20 node --version
nvm exec 20 npm --version

echo ""
echo "✓ Node 20 installed alongside your existing Node."
echo "  Default Node is unchanged: $(nvm version default 2>/dev/null || echo 'system/default')"
echo ""
echo "Next:"
echo "  cd ~/testneo-ecommerce-demo"
echo "  ./stop_all.sh"
echo "  ./start_all.sh"
