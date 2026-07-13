#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR/frontend"

# Prefer nvm Node 20+ when available (Vite 7 requires Node 20.19+ / 22.12+)
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [ -s "$NVM_DIR/nvm.sh" ]; then
  # shellcheck disable=SC1090
  . "$NVM_DIR/nvm.sh"
  nvm use 20 >/dev/null 2>&1 || nvm use --lts >/dev/null 2>&1 || true
fi

NODE_MAJOR="$(node -p "process.versions.node.split('.')[0]" 2>/dev/null || echo 0)"
if [ "$NODE_MAJOR" -lt 20 ]; then
  echo "ERROR: Node.js 20+ required for Vite 7 (found $(node --version 2>/dev/null || echo 'none'))."
  echo "On EC2 run: bash \"$ROOT_DIR/upgrade_node_ec2.sh\""
  exit 1
fi

if [ ! -d node_modules ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

# EC2 / production default: build once and serve static files (less RAM than vite dev)
# Local hot-reload: FRONTEND_MODE=dev ./start_frontend.sh
if [ "${FRONTEND_MODE:-prod}" = "dev" ]; then
  npm run dev -- --host 0.0.0.0 --port 3001
else
  echo "Building frontend for production..."
  npm run build
  echo "Serving frontend on 0.0.0.0:3001..."
  npx --yes serve -s dist -l tcp://0.0.0.0:3001
fi
