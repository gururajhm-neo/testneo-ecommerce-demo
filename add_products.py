"""
Quick script to add realistic product data
"""
import requests
import json

API_URL = "http://localhost:9000"

# Test credentials
LOGIN_DATA = {
    "email": "admin@ecommerce.com",
    "password": "admin123"
}

def login():
    """Login to get admin token"""
    response = requests.post(f"{API_URL}/auth/login", json=LOGIN_DATA)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def add_product(token, product_data):
    """Add a single product"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/products", json=product_data, headers=headers)
    if response.status_code != 201:
        print(f"Error: {response.text}")
    return response.status_code == 201

def main():
    print("Logging in as admin...")
    token = login()
    
    if not token:
        print("Failed to login")
        return
    
    print("Logged in successfully!")
    
    products = [
        {
            "name": "Apple MacBook Pro 16-inch",
            "description": "16-inch MacBook Pro with M3 Pro chip, 18-core CPU, 40-core GPU",
            "price": 2499.99,
            "sale_price": 2299.99,
            "cost_price": 1800.00,
            "category": "electronics",
            "sku": "MBP16-M3",
            "brand": "Apple",
            "manufacturer": "Apple Inc.",
            "stock_quantity": 25,
            "min_stock_level": 5,
            "max_stock_level": 100,
            "is_featured": True,
            "is_bestseller": True,
            "weight": 4.7,
            "dimensions": {"length": 35.57, "width": 24.81, "height": 1.68},
            "color": "Space Gray",
            "images": [
                "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400"
            ],
            "thumbnail": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=300",
            "tags": ["laptop", "macbook", "apple", "professional"],
            "keywords": ["macbook", "laptop", "apple", "computer"]
        },
        {
            "name": "Sony WH-1000XM5 Headphones",
            "description": "Premium noise canceling headphones with industry-leading sound quality",
            "price": 399.99,
            "sale_price": 349.99,
            "cost_price": 250.00,
            "category": "electronics",
            "sku": "SONY-WH1000XM5",
            "brand": "Sony",
            "manufacturer": "Sony Corporation",
            "stock_quantity": 75,
            "min_stock_level": 20,
            "max_stock_level": 500,
            "is_featured": True,
            "weight": 0.25,
            "color": "Black"
        },
        {
            "name": "Nike Air Force 1 '07",
            "description": "Classic basketball shoe with durable leather upper and Air cushioning",
            "price": 90.00,
            "sale_price": 75.00,
            "cost_price": 40.00,
            "category": "clothing",
            "sku": "NIKE-AF1-07",
            "brand": "Nike",
            "manufacturer": "Nike Inc.",
            "stock_quantity": 200,
            "min_stock_level": 50,
            "max_stock_level": 1000,
            "is_featured": True,
            "is_bestseller": True,
            "weight": 0.4,
            "size": "10",
            "color": "White"
        },
        {
            "name": "The 7 Habits of Highly Effective People",
            "description": "Powerful lessons in personal change from Stephen Covey",
            "price": 16.99,
            "sale_price": 12.99,
            "cost_price": 5.00,
            "category": "books",
            "sku": "BOOK-7HABITS",
            "brand": "Simon & Schuster",
            "manufacturer": "Simon & Schuster",
            "stock_quantity": 300,
            "min_stock_level": 100,
            "max_stock_level": 1000,
            "is_bestseller": True,
            "weight": 0.4
        }
    ]
    
    print(f"Adding {len(products)} products...")
    
    for product in products:
        if add_product(token, product):
            print(f"Added: {product['name']}")
        else:
            print(f"Failed: {product['name']}")
    
    print("\nDone! Check http://localhost:3000 to see your products!")

if __name__ == "__main__":
    main()

