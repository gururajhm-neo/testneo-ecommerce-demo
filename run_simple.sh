#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo "Virtual environment not found. Create it with: python3 -m venv .venv"
  exit 1
fi

source .venv/bin/activate

python -m pip install --upgrade pip >/dev/null 2>&1 || true
python -m pip install -r requirements.txt >/dev/null 2>&1 || true

echo "Starting backend on http://127.0.0.1:9000"
python -m uvicorn main:app --host 0.0.0.0 --port 9000
