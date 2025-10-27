"""
Populate database with comprehensive test data for admin use cases
Run this script to add products, coupons, reviews, and orders for testing
"""
import requests
import json
from datetime import datetime, timedelta

API_URL = "http://localhost:9000"

# Admin credentials
ADMIN_LOGIN = {
    "email": "admin@ecommerce.com",
    "password": "admin123"
}

def login():
    """Login as admin"""
    response = requests.post(f"{API_URL}/auth/login", json=ADMIN_LOGIN)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("[OK] Admin login successful")
        return token
    print(f"[FAILED] Login failed: {response.text}")
    return None

def add_products(token):
    """Add diverse products"""
    headers = {"Authorization": f"Bearer {token}"}
    
    products = [
        {
            "name": "Samsung Galaxy S24 Ultra",
            "description": "Latest Samsung flagship with 200MP camera and AI features",
            "price": 1299.99,
            "sale_price": 1199.99,
            "cost_price": 900.00,
            "category": "electronics",
            "sku": "SAMSUNG-GALAXY-S24",
            "brand": "Samsung",
            "manufacturer": "Samsung Electronics",
            "stock_quantity": 75,
            "min_stock_level": 10,
            "max_stock_level": 200,
            "is_featured": True,
            "is_bestseller": True,
            "weight": 0.233,
            "dimensions": {"length": 16.26, "width": 7.9, "height": 0.89},
            "color": "Titanium Black",
            "tags": ["smartphone", "android", "premium", "5g"],
            "keywords": ["samsung", "galaxy", "smartphone", "android"]
        },
        {
            "name": "Sony WH-1000XM5 Headphones",
            "description": "Industry-leading noise cancellation with premium sound",
            "price": 399.99,
            "sale_price": 349.99,
            "cost_price": 250.00,
            "category": "electronics",
            "sku": "SONY-WH1000XM5",
            "brand": "Sony",
            "manufacturer": "Sony Corporation",
            "stock_quantity": 120,
            "min_stock_level": 20,
            "max_stock_level": 300,
            "is_featured": True,
            "is_bestseller": True,
            "weight": 0.25,
            "dimensions": {"length": 26, "width": 19, "height": 7},
            "color": "Black",
            "tags": ["headphones", "audio", "noise-cancelling", "premium"],
            "keywords": ["sony", "headphones", "audio", "wireless"]
        },
        {
            "name": "Adidas Ultraboost 24",
            "description": "Premium running shoes with superior cushioning",
            "price": 189.99,
            "sale_price": 149.99,
            "cost_price": 80.00,
            "category": "clothing",
            "sku": "ADIDAS-ULTRA24",
            "brand": "Adidas",
            "manufacturer": "Adidas AG",
            "stock_quantity": 200,
            "min_stock_level": 30,
            "max_stock_level": 400,
            "is_featured": True,
            "weight": 0.6,
            "dimensions": {"length": 28, "width": 10, "height": 5},
            "color": "White/Black",
            "size": "M 10",
            "tags": ["running", "shoes", "athletic", "comfortable"],
            "keywords": ["adidas", "running", "shoes", "athletic"]
        },
        {
            "name": "Dell XPS 15 Laptop",
            "description": "15-inch premium laptop with 4K display",
            "price": 1999.99,
            "sale_price": 1799.99,
            "cost_price": 1200.00,
            "category": "electronics",
            "sku": "DELL-XPS-15",
            "brand": "Dell",
            "manufacturer": "Dell Technologies",
            "stock_quantity": 45,
            "min_stock_level": 5,
            "max_stock_level": 100,
            "is_featured": True,
            "weight": 1.92,
            "dimensions": {"length": 35.7, "width": 25.9, "height": 1.8},
            "color": "Platinum Silver",
            "tags": ["laptop", "computer", "premium", "business"],
            "keywords": ["dell", "laptop", "xps", "computer"]
        },
        {
            "name": "iPad Pro 12.9-inch",
            "description": "Latest iPad Pro with M4 chip",
            "price": 1199.99,
            "cost_price": 800.00,
            "category": "electronics",
            "sku": "APPLE-IPADPRO-12",
            "brand": "Apple",
            "manufacturer": "Apple Inc.",
            "stock_quantity": 60,
            "min_stock_level": 10,
            "max_stock_level": 150,
            "is_featured": True,
            "weight": 0.682,
            "dimensions": {"length": 28.06, "width": 21.5, "height": 0.66},
            "color": "Space Gray",
            "tags": ["tablet", "apple", "premium", "productivity"],
            "keywords": ["ipad", "tablet", "apple", "pro"]
        },
        {
            "name": "Microsoft Surface Pro 9",
            "description": "Versatile 2-in-1 tablet with Windows 11",
            "price": 1099.99,
            "sale_price": 999.99,
            "cost_price": 650.00,
            "category": "electronics",
            "sku": "MSFT-SURFACE-PRO9",
            "brand": "Microsoft",
            "manufacturer": "Microsoft Corporation",
            "stock_quantity": 55,
            "min_stock_level": 10,
            "max_stock_level": 150,
            "is_featured": False,
            "weight": 0.879,
            "dimensions": {"length": 28.7, "width": 20.9, "height": 0.93},
            "color": "Platinum",
            "tags": ["tablet", "windows", "2-in-1", "business"],
            "keywords": ["surface", "tablet", "windows", "microsoft"]
        },
        {
            "name": "Canon EOS R5 Camera",
            "description": "Professional mirrorless camera with 45MP sensor",
            "price": 3899.99,
            "sale_price": 3599.99,
            "cost_price": 2800.00,
            "category": "electronics",
            "sku": "CANON-EOS-R5",
            "brand": "Canon",
            "manufacturer": "Canon Inc.",
            "stock_quantity": 25,
            "min_stock_level": 5,
            "max_stock_level": 50,
            "is_featured": True,
            "weight": 0.65,
            "dimensions": {"length": 13.8, "width": 9.8, "height": 8.8},
            "color": "Black",
            "tags": ["camera", "photography", "professional", "mirrorless"],
            "keywords": ["canon", "camera", "photography", "professional"]
        },
        {
            "name": "LG C3 OLED 65-inch TV",
            "description": "Premium OLED TV with 4K resolution and HDR",
            "price": 2499.99,
            "sale_price": 1999.99,
            "cost_price": 1400.00,
            "category": "electronics",
            "sku": "LG-C3-65OLED",
            "brand": "LG",
            "manufacturer": "LG Electronics",
            "stock_quantity": 30,
            "min_stock_level": 5,
            "max_stock_level": 60,
            "is_featured": True,
            "weight": 23.1,
            "dimensions": {"length": 144.9, "width": 83.1, "height": 5.9},
            "color": "Black",
            "tags": ["tv", "oled", "4k", "entertainment"],
            "keywords": ["lg", "tv", "oled", "4k", "hdr"]
        },
        {
            "name": "Nintendo Switch OLED",
            "description": "Gaming console with 7-inch OLED screen",
            "price": 349.99,
            "cost_price": 220.00,
            "category": "electronics",
            "sku": "NIN-SWITCH-OLED",
            "brand": "Nintendo",
            "manufacturer": "Nintendo Co. Ltd",
            "stock_quantity": 150,
            "min_stock_level": 30,
            "max_stock_level": 300,
            "is_featured": True,
            "is_bestseller": True,
            "weight": 0.42,
            "dimensions": {"length": 23.9, "width": 10.2, "height": 1.39},
            "color": "White",
            "tags": ["gaming", "console", "portable", "nintendo"],
            "keywords": ["nintendo", "switch", "gaming", "console"]
        },
        {
            "name": "Dyson V15 Detect Vacuum",
            "description": "Latest cordless vacuum with laser technology",
            "price": 749.99,
            "sale_price": 649.99,
            "cost_price": 400.00,
            "category": "electronics",
            "sku": "DYSON-V15-DET",
            "brand": "Dyson",
            "manufacturer": "Dyson Ltd",
            "stock_quantity": 80,
            "min_stock_level": 15,
            "max_stock_level": 200,
            "is_featured": True,
            "weight": 2.6,
            "dimensions": {"length": 108.5, "width": 25.6, "height": 25.6},
            "color": "Yellow/Nickel",
            "tags": ["vacuum", "home", "cordless", "premium"],
            "keywords": ["dyson", "vacuum", "cleaner", "cordless"]
        }
    ]
    
    print("\n>>> Adding products...")
    added = 0
    for product in products:
        try:
            response = requests.post(f"{API_URL}/products", json=product, headers=headers)
            if response.status_code == 201:
                added += 1
                print(f"  [OK] {product['name']}")
            else:
                print(f"  [FAILED] {product['name']}: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {product['name']}: {e}")
    
    print(f"\n[SUCCESS] Added {added}/{len(products)} products")

def add_coupons(token):
    """Add various coupons"""
    headers = {"Authorization": f"Bearer {token}"}
    
    coupons = [
        {
            "code": "WELCOME10",
            "discount_type": "percentage",
            "discount_value": 10,
            "minimum_purchase": 50.00,
            "maximum_discount": 100.00,
            "valid_from": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=30)).isoformat(),
            "usage_limit": 100,
            "description": "Welcome 10% off for new customers"
        },
        {
            "code": "SAVE50",
            "discount_type": "fixed",
            "discount_value": 50.00,
            "minimum_purchase": 200.00,
            "valid_from": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=60)).isoformat(),
            "usage_limit": 50,
            "description": "Save $50 on orders over $200"
        },
        {
            "code": "FREESHIP",
            "discount_type": "free_shipping",
            "discount_value": 10.00,
            "minimum_purchase": 100.00,
            "valid_from": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=90)).isoformat(),
            "usage_limit": 200,
            "description": "Free shipping on orders over $100"
        },
        {
            "code": "FLASH25",
            "discount_type": "percentage",
            "discount_value": 25,
            "minimum_purchase": 150.00,
            "maximum_discount": 200.00,
            "valid_from": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=7)).isoformat(),
            "usage_limit": 30,
            "description": "Flash sale 25% off"
        },
        {
            "code": "VIP20",
            "discount_type": "percentage",
            "discount_value": 20,
            "minimum_purchase": 300.00,
            "maximum_discount": 150.00,
            "valid_from": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=365)).isoformat(),
            "usage_limit": 10,
            "description": "VIP members exclusive 20% off"
        }
    ]
    
    print("\n>>> Adding coupons...")
    added = 0
    for coupon in coupons:
        try:
            response = requests.post(f"{API_URL}/coupons", json=coupon, headers=headers)
            if response.status_code == 201:
                added += 1
                print(f"  [OK] {coupon['code']}")
            else:
                print(f"  [FAILED] {coupon['code']}: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {coupon['code']}: {e}")
    
    print(f"\n[SUCCESS] Added {added}/{len(coupons)} coupons")

def main():
    print("=" * 60)
    print("POPULATING DATABASE WITH ADMIN TEST DATA")
    print("=" * 60)
    
    token = login()
    if not token:
        print("❌ Failed to login as admin")
        return
    
    add_products(token)
    add_coupons(token)
    
    print("\n" + "=" * 60)
    print("[SUCCESS] DATABASE POPULATION COMPLETE")
    print("=" * 60)
    print("\nYou can now test admin features with:")
    print("  - Email: admin@ecommerce.com")
    print("  - Password: admin123")
    print("\nAccess the API documentation at: http://localhost:9000/docs")

if __name__ == "__main__":
    main()

