# TestNeo E-Commerce Demo

This repository contains a full-stack e-commerce demo with a FastAPI backend and a React/Vite frontend for local testing, demos, and team walkthroughs.

## Features

- FastAPI backend with SQLite
- React/Vite storefront
- User authentication and registration
- Product catalog, cart, checkout, and orders
- Reviews, coupons, wishlist, and admin views
- Seeded demo data for immediate testing

## Prerequisites

- Python 3.13+ (3.14 is also supported here)
- Node.js 18+
- Git

## Local setup

### 1) Clone and enter the repo
```bash
git clone <repo-url>
cd testneo-ecommerce-demo
```

### 2) Create and activate a Python virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Install frontend dependencies
```bash
cd frontend
npm install
cd ..
```

### 4) Start the backend
```bash
./start_backend.sh
```

The backend runs at:
- http://127.0.0.1:9000
- API docs: http://127.0.0.1:9000/docs

### 5) Start the frontend
```bash
./start_frontend.sh
```

The frontend runs at:
- http://127.0.0.1:3001
- http://localhost:3001

### 6) Start both together
```bash
./start_all.sh
```

### 7) Stop both services
```bash
./stop_all.sh
```

### 8) Seed the demo data
The demo data is created automatically when the backend starts. If you want to seed it manually, run:

```bash
./.venv/bin/python populate_mock_data.py
```

## Demo login credentials

The app seeds these accounts automatically on first backend startup:

- Admin: admin@ecommerce.com / admin123
- Moderator: moderator@ecommerce.com / moderator123
- Customer: john@test.com / john123

## Quick health checks

Backend:
```bash
python3 check_backend.py
```

Frontend:
```bash
curl http://127.0.0.1:3001
```

## Useful endpoints

- Health: http://127.0.0.1:9000/health
- Products: http://127.0.0.1:9000/products
- Login: POST http://127.0.0.1:9000/auth/login

## Project structure

```text
testneo-ecommerce-demo/
├── main.py                  # FastAPI application
├── populate_mock_data.py    # Demo seed data
├── start_backend.sh         # Backend launcher
├── start_frontend.sh        # Frontend launcher
├── start_all.sh             # Launch both services
├── stop_all.sh              # Stop both services
├── frontend/                # React/Vite app
├── models/                  # SQLAlchemy models
├── schemas/                 # Pydantic schemas
├── services/                # Business logic
└── README.md                # This guide
```

## Demo purpose

This project is intended for:
- Demo environments
- UI and API testing
- Team walkthroughs
- CI/CD and automation examples

