#!/usr/bin/env bash
# Create agents/.env from example if missing (does not overwrite).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "$ROOT/.env" ]]; then
  echo "agents/.env already exists"
  exit 0
fi
cp "$ROOT/.env.example" "$ROOT/.env"
echo "Created agents/.env — edit TESTNEO_API_KEY and TESTNEO_PROJECT_ID"
