#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

chmod +x start_backend.sh start_frontend.sh stop_all.sh

./start_backend.sh > /tmp/testneo-backend.log 2>&1 &
BACKEND_PID=$!

./start_frontend.sh > /tmp/testneo-frontend.log 2>&1 &
FRONTEND_PID=$!

cat <<EOF
Started services.
Backend PID: $BACKEND_PID
Frontend PID: $FRONTEND_PID

Open (local):
- http://127.0.0.1:9000
- http://127.0.0.1:3001

Open (EC2 public):
- http://34.229.255.219:9000
- http://34.229.255.219:3001
- http://34.229.255.219:3001/login

Stop them with:
- ./stop_all.sh
EOF
