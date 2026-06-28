#!/usr/bin/env bash
set -euo pipefail

for pid in $(pgrep -f "python main.py|vite --host 0.0.0.0 --port 3001"); do
  kill "$pid" 2>/dev/null || true
done

echo "Stopped TestNeo services."
