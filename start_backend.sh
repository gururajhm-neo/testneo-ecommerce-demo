#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo "Python virtual environment not found. Run: python3 -m venv .venv"
  exit 1
fi

source .venv/bin/activate

# Do not inherit main TestNeo PORT=8000 on shared EC2
unset PORT || true
export ECOM_HOST="${ECOM_HOST:-0.0.0.0}"
export ECOM_PORT="${ECOM_PORT:-9000}"

echo "Starting ecommerce backend on ${ECOM_HOST}:${ECOM_PORT}"
python main.py
