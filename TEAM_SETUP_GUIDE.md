# Team Setup Guide

This repository contains a FastAPI backend and a React/Vite frontend for the TestNeo e-commerce demo.

## What is included
- Backend API: FastAPI + SQLAlchemy + SQLite
- Frontend UI: React + Vite
- Seeded demo data including admin, moderator, and customer accounts
- Simple scripts to start/stop the services

## Default login credentials
The seed data creates these accounts automatically on first backend startup:

- Admin: admin@ecommerce.com / admin123
- Moderator: moderator@ecommerce.com / moderator123
- Customer sample: john@test.com / john123

You can also create new users through the registration flow.

## Prerequisites
Install these tools first:
- Python 3.13+ (3.14 also works for this repo)
- Node.js 18+
- Git

## 1) Clone and enter the repo
```bash
git clone <repo-url>
cd testneo-ecommerce-demo
```

## 2) Create the Python virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Install frontend dependencies
```bash
cd frontend
npm install
cd ..
```

## 4) Start the backend
From the repo root:
```bash
./start_backend.sh
```

The backend will run on:
- http://127.0.0.1:9000
- API docs: http://127.0.0.1:9000/docs

## 5) Start the frontend
From the repo root:
```bash
./start_frontend.sh
```

The frontend will run on:
- http://127.0.0.1:3001

## 6) Start both services together
```bash
./start_all.sh
```

## 7) Stop both services
```bash
./stop_all.sh
```

## 8) Quick health check
Backend:
```bash
python3 check_backend.py
```

Frontend:
```bash
curl http://127.0.0.1:3001
```

## 9) Useful endpoints
- Health: http://127.0.0.1:9000/health
- Products: http://127.0.0.1:9000/products
- Login: POST http://127.0.0.1:9000/auth/login

Example login request:
```bash
curl -X POST http://127.0.0.1:9000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecommerce.com","password":"admin123"}'
```

## 10) Repo structure overview
- main.py - FastAPI entry point
- populate_mock_data.py - Seed data generation
- models/ - Database models
- schemas/ - API request/response schemas
- services/ - Auth and business logic
- frontend/ - React/Vite app

## Troubleshooting
If the backend does not start:
```bash
./stop_all.sh
./start_backend.sh
```

If the frontend does not start:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
cd ..
./start_frontend.sh
```

If you want to reseed demo data, run:
```bash
./.venv/bin/python populate_mock_data.py
```
