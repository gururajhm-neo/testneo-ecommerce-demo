#!/usr/bin/env bash
# One-button ecom agent → TestNeo gate demo
# Run from anywhere: ./agents/scripts/demo_e2e.sh
set -euo pipefail

AGENTS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # .../agents
REPO_ROOT="$(cd "$AGENTS_ROOT/.." && pwd)"        # .../testneo-ecommerce-demo
cd "$REPO_ROOT"

if [[ ! -f "$AGENTS_ROOT/.env" ]]; then
  echo "Missing agents/.env — copy agents/.env.example and set TESTNEO_API_KEY + TESTNEO_PROJECT_ID"
  exit 1
fi

# Prefer repo venv, then agents venv
PY="$REPO_ROOT/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  PY="$AGENTS_ROOT/.venv/bin/python"
fi
if [[ ! -x "$PY" ]]; then
  PY="python3"
fi

export PYTHONPATH="${REPO_ROOT}${PYTHONPATH:+:$PYTHONPATH}"

echo "==> Health check ecom API"
if ! curl -sf "http://127.0.0.1:9000/health" >/dev/null; then
  echo "Ecom API down. Start with: ./start_backend.sh (or ./start_all.sh)"
  exit 1
fi

echo "==> Seed delivered order (for refund scenarios)"
"$PY" -m agents.scripts.seed_demo_state

echo "==> Full E2E: checkout OK → refund BREAK → memory BREAK"
"$PY" -m agents.scripts.run_demo_e2e --scenario all

echo "==> Artifacts in agents/artifacts/"
ls -1 agents/artifacts/*_latest.json 2>/dev/null || true
