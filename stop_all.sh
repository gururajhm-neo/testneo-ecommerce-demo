#!/usr/bin/env bash
set -euo pipefail

# Stop ONLY this demo's listeners (ports 9000 / 3001).
# Do NOT pkill npm/vite/serve/python globally — that can kill main TestNeo.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

kill_port() {
  local port="$1"
  if command -v fuser >/dev/null 2>&1; then
    fuser -k "${port}/tcp" 2>/dev/null || true
  elif command -v lsof >/dev/null 2>&1; then
    local pids
    pids="$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)"
    if [ -n "$pids" ]; then
      # shellcheck disable=SC2086
      kill $pids 2>/dev/null || true
      sleep 1
      pids="$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)"
      if [ -n "$pids" ]; then
        # shellcheck disable=SC2086
        kill -9 $pids 2>/dev/null || true
      fi
    fi
  else
    echo "Install lsof or psmisc (fuser) to stop by port."
    return 1
  fi
}

echo "Stopping ecommerce demo on ports 9000 and 3001..."
kill_port 9000
kill_port 3001

# Also stop this repo's logged start_all children if still around
pkill -f "$ROOT_DIR/start_backend.sh" 2>/dev/null || true
pkill -f "$ROOT_DIR/start_frontend.sh" 2>/dev/null || true
pkill -f "$ROOT_DIR/frontend/.*vite --host 0.0.0.0 --port 3001" 2>/dev/null || true
pkill -f "serve -s dist -l tcp://0.0.0.0:3001" 2>/dev/null || true

echo "Stopped ecommerce demo only (main TestNeo on 3000/8000/8001 untouched)."
