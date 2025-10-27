"""
Comprehensive Mock Data Generator for E-Commerce
Populates database with realistic test data
"""
import sys
from database import SessionLocal, init_db, drop_db
from models.user import User
from models.product import Product, ProductCategory
from models.order import Order, PaymentMethod, OrderStatus, ShippingMethod, PaymentStatus
from models.order import OrderItem
from models.review import Review
from models.coupon import Coupon, DiscountType
from datetime import datetime, timedelta
from passlib.context import CryptContext
import random
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def create_mock_data():
    """Create comprehensive mock data"""
    print("=" * 60)
    print("POPULATING DATABASE WITH MOCK DATA")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Always populate if less than 20 products
        if db.query(Product).count() > 20:
            print("\nData already exists. Skipping population.")
            return
        
        print("\n[1/5] Creating Users...")
        # Create additional users
        customers = [
            {"email": "john@test.com", "username": "john_doe", "password": "john123", "first_name": "John", "last_name": "Doe"},
            {"email": "jane@test.com", "username": "jane_smith", "password": "jane123", "first_name": "Jane", "last_name": "Smith"},
            {"email": "bob@test.com", "username": "bob_wilson", "password": "bob123", "first_name": "Bob", "last_name": "Wilson"},
            {"email": "alice@test.com", "username": "alice_brown", "password": "alice123", "first_name": "Alice", "last_name": "Brown"},
        ]
        
        for customer in customers:
            if not db.query(User).filter(User.email == customer["email"]).first():
                user = User(
                    email=customer["email"],
                    username=customer["username"],
                    password=customer["password"],
                    first_name=customer["first_name"],
                    last_name=customer["last_name"]
                )
                user.is_active = True
                user.is_verified = True
                db.add(user)
        
        db.commit()
        print(f"[OK] Created {len(customers)} customer users")
        
        print("\n[2/5] Creating Products...")
        # Products data
        products_data = [
            {"name": "iPhone 15 Pro Max", "description": "Latest iPhone with titanium design", "price": 1199.99, "sale_price": 1099.99, "category": "ELECTRONICS", "sku": "IPH-15PM", "brand": "Apple", "stock_quantity": 50, "is_featured": True, "is_bestseller": True},
            {"name": "Samsung Galaxy S24 Ultra", "description": "Premium Android flagship", "price": 899.99, "sale_price": 799.99, "category": "ELECTRONICS", "sku": "SGS24U", "brand": "Samsung", "stock_quantity": 30, "is_featured": True, "is_bestseller": True},
            {"name": "MacBook Pro 16-inch", "description": "Professional laptop with M3 chip", "price": 2499.99, "sale_price": 2299.99, "category": "ELECTRONICS", "sku": "MBP16", "brand": "Apple", "stock_quantity": 20, "is_featured": True},
            {"name": "AirPods Pro 2", "description": "Noise canceling wireless earbuds", "price": 249.99, "sale_price": 199.99, "category": "ELECTRONICS", "sku": "APP2", "brand": "Apple", "stock_quantity": 100},
            {"name": "Nike Air Max 270", "description": "Comfortable running shoes", "price": 129.99, "sale_price": 99.99, "category": "CLOTHING", "sku": "NAM270", "brand": "Nike", "stock_quantity": 75, "is_bestseller": True},
            {"name": "Levi's 501 Jeans", "description": "Classic straight fit jeans", "price": 59.99, "sale_price": 49.99, "category": "CLOTHING", "sku": "LVS501", "brand": "Levi's", "stock_quantity": 120},
            {"name": "Samsung 4K Smart TV", "description": "55-inch 4K Ultra HD Smart TV", "price": 699.99, "category": "ELECTRONICS", "sku": "SS55TV", "brand": "Samsung", "stock_quantity": 25, "is_featured": True},
            {"name": "The Great Gatsby", "description": "Classic American novel", "price": 12.99, "category": "BOOKS", "sku": "BK001", "brand": "Scribner", "stock_quantity": 200, "is_bestseller": True},
            {"name": "Dyson V15 Vacuum", "description": "Powerful cordless vacuum cleaner", "price": 649.99, "sale_price": 599.99, "category": "ELECTRONICS", "sku": "DYSV15", "brand": "Dyson", "stock_quantity": 40, "is_featured": True},
            {"name": "Instant Pot Duo", "description": "7-in-1 pressure cooker", "price": 99.99, "sale_price": 79.99, "category": "HOME_GARDEN", "sku": "IPDUO", "brand": "Instant Pot", "stock_quantity": 60},
            {"name": "Adidas Ultraboost 22", "description": "High-performance running shoes", "price": 180.00, "sale_price": 150.00, "category": "CLOTHING", "sku": "ADUB22", "brand": "Adidas", "stock_quantity": 85, "is_bestseller": True},
            {"name": "Ray-Ban Aviator Sunglasses", "description": "Classic aviator style sunglasses", "price": 154.00, "category": "CLOTHING", "sku": "RBAV", "brand": "Ray-Ban", "stock_quantity": 50},
            {"name": "iPad Pro 12.9", "description": "Professional tablet with M2 chip", "price": 1099.99, "sale_price": 999.99, "category": "ELECTRONICS", "sku": "IPP129", "brand": "Apple", "stock_quantity": 35, "is_featured": True},
            {"name": "Bose QuietComfort 45", "description": "Premium noise canceling headphones", "price": 329.00, "category": "ELECTRONICS", "sku": "BOSQC45", "brand": "Bose", "stock_quantity": 70},
            {"name": "KitchenAid Stand Mixer", "description": "5-quart stand mixer", "price": 379.99, "category": "HOME_GARDEN", "sku": "KAMIX", "brand": "KitchenAid", "stock_quantity": 45, "is_featured": True},
        ]
        
        for p_data in products_data:
            sku = p_data["sku"]
            
            # Check if product with this SKU already exists
            if db.query(Product).filter(Product.sku == sku).first():
                continue
            
            # Extract required fields
            name = p_data["name"]
            price = p_data["price"]
            category_str = p_data["category"]
            description = p_data.get("description", "")
            brand = p_data.get("brand", "")
            
            # Convert category string to ProductCategory enum value
            category = ProductCategory[category_str].value if isinstance(category_str, str) else category_str
            
            # Create product with required fields
            product = Product(
                name=name,
                price=price,
                category=category,
                sku=sku,
                description=description,
                brand=brand
            )
            
            # Set optional fields
            if "sale_price" in p_data:
                product.sale_price = p_data["sale_price"]
            if "stock_quantity" in p_data:
                product.stock_quantity = p_data["stock_quantity"]
                product.min_stock_level = p_data.get("min_stock_level", 10)
                product.max_stock_level = p_data.get("max_stock_level", 1000)
            if "is_featured" in p_data:
                product.is_featured = p_data["is_featured"]
            if "is_bestseller" in p_data:
                product.is_bestseller = p_data["is_bestseller"]
            
            db.add(product)
        
        db.commit()
        print(f"[OK] Created {len(products_data)} products")
        
        print("\n[3/5] Creating Orders...")
        # Get users
        users = db.query(User).all()
        products = db.query(Product).all()
        
        if users and products:
            # Create more realistic orders
            order_statuses = [OrderStatus.PENDING, OrderStatus.PROCESSING, OrderStatus.SHIPPED, 
                            OrderStatus.DELIVERED, OrderStatus.CONFIRMED, OrderStatus.CANCELLED]
            
            cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
                     "San Antonio", "San Diego", "Dallas", "San Jose"]
            
            states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
            
            for i in range(25):  # Create 25 orders
                user = random.choice(users)
                
                # Create order with proper dates
                order_date = datetime.utcnow() - timedelta(days=random.randint(0, 90))
                
                order = Order(
                    user_id=user.id,
                    payment_method=random.choice(list(PaymentMethod)),
                    shipping_address={"street": f"{random.randint(100, 9999)} Main St", 
                                     "city": random.choice(cities), 
                                     "state": random.choice(states), 
                                     "postal_code": f"{random.randint(10000, 99999)}", 
                                     "country": "US"},
                    billing_address={"street": f"{random.randint(100, 9999)} Main St", 
                                     "city": random.choice(cities), 
                                     "state": random.choice(states), 
                                     "postal_code": f"{random.randint(10000, 99999)}", 
                                     "country": "US"}
                )
                
                # Set timestamps
                order.created_at = order_date
                order.updated_at = order_date
                
                # Random order status (weighted towards delivered/completed)
                if i < 15:
                    order.status = random.choice([OrderStatus.DELIVERED, OrderStatus.CONFIRMED, OrderStatus.SHIPPED, OrderStatus.OUT_FOR_DELIVERY])
                elif i < 20:
                    order.status = random.choice([OrderStatus.PROCESSING, OrderStatus.PENDING, OrderStatus.CONFIRMED])
                else:
                    order.status = random.choice([OrderStatus.CANCELLED, OrderStatus.REFUNDED])
                
                order.shipping_method = random.choice(list(ShippingMethod))
                
                # Add random number of items to calculate realistic totals
                num_items = random.randint(1, 4)
                selected_products = random.sample(products, min(num_items, len(products)))
                
                subtotal = 0
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    subtotal += (product.price * quantity)
                
                # Add shipping and tax
                shipping_cost = 5.0 if subtotal < 50 else 0.0
                tax_rate = 0.10
                tax_amount = subtotal * tax_rate
                order.total_amount = subtotal + shipping_cost + tax_amount
                order.subtotal = subtotal
                order.shipping_cost = shipping_cost
                order.tax_amount = tax_amount
                
                db.add(order)
                db.flush()
                
                # Add order items
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=product.price
                    )
                    # Set total price after initialization
                    order_item.total_price = product.price * quantity
                    db.add(order_item)
                
                db.commit()
            
            print(f"[OK] Created 25 orders")
        
        print("\n[4/5] Creating Reviews...")
        # Create reviews
        if users and products:
            review_texts = [
                ("Amazing product!", "Really happy with this purchase. Quality is excellent."),
                ("Great value!", "Best bang for your buck. Highly recommend!"),
                ("Works as expected", "Exactly what I needed. Very satisfied."),
                ("Not bad", "Does the job but could be better."),
                ("Outstanding!", "Exceeded my expectations in every way."),
                ("Love it!", "This product is fantastic. Worth every penny."),
                ("Perfect fit", "Exactly what I was looking for. Great quality."),
            ]
            
            for i in range(20):
                user = random.choice(users)
                product = random.choice(products)
                comment_text, title = random.choice(review_texts)
                
                review = Review(
                    user_id=user.id,
                    product_id=product.id,
                    rating=random.randint(3, 5),
                    title=title,
                    comment=comment_text
                )
                # Set additional properties after initialization
                review.is_verified_purchase = random.choice([True, False])
                review.is_approved = random.choice([True, False])
                db.add(review)
            
            db.commit()
            print("[OK] Created 20 reviews")
        
        print("\n[5/5] Creating Coupons...")
        # Create coupons
        coupons_data = [
            {"code": "SAVE10", "name": "Save 10%", "discount_type": "percentage", "discount_value": 10, "valid_from": datetime.utcnow(), "valid_until": datetime.utcnow() + timedelta(days=30), "minimum_order_amount": 50},
            {"code": "SAVE20", "name": "Save 20%", "discount_type": "percentage", "discount_value": 20, "valid_from": datetime.utcnow(), "valid_until": datetime.utcnow() + timedelta(days=30), "minimum_order_amount": 100},
            {"code": "FLAT50", "name": "$50 Off", "discount_type": "fixed", "discount_value": 50, "valid_from": datetime.utcnow(), "valid_until": datetime.utcnow() + timedelta(days=30), "minimum_order_amount": 200},
            {"code": "NEWUSER", "name": "New User Discount", "discount_type": "percentage", "discount_value": 15, "valid_from": datetime.utcnow(), "valid_until": datetime.utcnow() + timedelta(days=90), "minimum_order_amount": 0},
        ]
        
        for c_data in coupons_data:
            coupon = Coupon(**c_data)
            db.add(coupon)
        
        db.commit()
        print(f"[OK] Created {len(coupons_data)} coupons")
        
        print("\n" + "=" * 60)
        print("DATABASE POPULATION COMPLETE!")
        print("=" * 60)
        print(f"Total Users: {db.query(User).count()}")
        print(f"Total Products: {db.query(Product).count()}")
        print(f"Total Orders: {db.query(Order).count()}")
        print(f"Total Reviews: {db.query(Review).count()}")
        print(f"Total Coupons: {db.query(Coupon).count()}")
        print("\nYou can now test all features!")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to populate database: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_mock_data()
