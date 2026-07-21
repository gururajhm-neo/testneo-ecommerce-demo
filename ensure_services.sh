#!/usr/bin/env bash
# Start/repair ecommerce demo services on EC2 (safe beside main TestNeo).
# Usage: bash ensure_services.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

mkdir -p /tmp
unset CORS_ORIGINS || true
unset PORT || true
export ECOM_PORT="${ECOM_PORT:-9000}"
export ECOM_HOST="${ECOM_HOST:-0.0.0.0}"

echo "==> Checking frontend :3001"
if ! curl -sf -m 2 http://127.0.0.1:3001/ >/dev/null; then
  echo "Frontend down — starting..."
  ./stop_all.sh || true
  nohup ./start_frontend.sh > /tmp/testneo-frontend.log 2>&1 &
  sleep 2
else
  echo "Frontend OK"
fi

echo "==> Checking backend :9000"
if ! curl -sf -m 2 http://127.0.0.1:9000/health >/dev/null; then
  echo "Backend down — starting..."
  if [ -d .venv ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  elif [ -d venv ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
  else
    echo "ERROR: no .venv/venv. Create with: python3 -m venv .venv && pip install -r requirements.txt"
    exit 1
  fi

  # Free only demo backend port
  if command -v fuser >/dev/null 2>&1; then
    fuser -k 9000/tcp 2>/dev/null || true
  fi

  nohup python main.py > /tmp/testneo-backend.log 2>&1 &
  sleep 3
else
  echo "Backend OK"
fi

echo "==> Local health"
curl -sS -m 3 http://127.0.0.1:9000/health || {
  echo "Backend still failing. Last log lines:"
  tail -40 /tmp/testneo-backend.log || true
  exit 1
}
echo
curl -sS -m 3 -o /dev/null -w "frontend:%{http_code}\n" http://127.0.0.1:3001/

echo "==> Via nginx (if configured)"
curl -sS -m 3 -o /dev/null -w "domain_ui:%{http_code}\n" http://testneo-ecom.testneo.ai/ || true
curl -sS -m 3 -o /dev/null -w "domain_api:%{http_code}\n" http://testneo-ecom.testneo.ai/api/health || true

echo
echo "Done. Login: http://testneo-ecom.testneo.ai/login"
echo "Admin: admin@ecommerce.com / admin123"
