# TestNeo E-Commerce Demo API

This is a clean, standalone e-commerce API for testing and demo purposes.

## Features

- FastAPI-based RESTful API
- User authentication
- Product management
- Shopping cart
- Orders
- Wishlist
- Reviews
- Coupons
- SQLite database

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
```bash
python main.py
```

3. Access the API:
- API: http://localhost:9000
- Swagger Docs: http://localhost:9000/docs

## Default Credentials

- Email: `customer@test.com`
- Password: `customer123`

## Project Structure

```
testneo-ecommerce-demo/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── database.py          # Database connection
├── requirements.txt     # Python dependencies
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
└── services/            # Business logic services
```

## Demo Purpose

This API is designed for:
- Test automation demos
- E2E testing demonstrations
- API testing showcases
- CI/CD pipeline examples

## Deployment

Ready for deployment to:
- Railway (recommended for API)
- Vercel (for frontend integration)
- Docker
- AWS/Azure/GCP

