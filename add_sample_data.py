"""
Add comprehensive sample data to the database
"""
from database import SessionLocal, init_db
from models import Product, ProductCategory
from datetime import datetime

def add_comprehensive_products():
    """Add detailed product data for e-commerce demo"""
    init_db()
    db = SessionLocal()
    
    try:
        # Check if products already exist
        if db.query(Product).count() > 5:
            print("Products already exist, skipping...")
            return
        
        products = []
        
        # Electronics
        p1 = Product(
            name="Apple MacBook Pro 16-inch",
            price=2499.99,
            category="electronics",
            sku="MBP-16-M3-PRO",
            description="16-inch MacBook Pro with M3 Pro chip, 18-core CPU, 40-core GPU, and 36GB unified memory. Perfect for professional work.",
            brand="Apple"
        )
        p1.sale_price = 2299.99
        p1.cost_price = 1800.00
        p1.manufacturer = "Apple Inc."
        p1.stock_quantity = 25
        p1.min_stock_level = 5
        p1.is_featured = True
        p1.is_bestseller = True
        p1.weight = 4.7
        p1.dimensions = {"length": 35.57, "width": 24.81, "height": 1.68}
        p1.color = "Space Gray"
        p1.images = [
            "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400",
            "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400"
        ]
        p1.thumbnail = "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=300"
        p1.tags = ["laptop", "macbook", "apple", "professional"]
        p1.keywords = ["macbook", "laptop", "apple", "computer"]
        p1.warranty_period = 365
        p1.return_period = 30
        products.append(p1)
            Product(
                name="Sony WH-1000XM5 Wireless Headphones",
                description="Premium noise canceling headphones with industry-leading sound quality and 30-hour battery life.",
                price=399.99,
                sale_price=349.99,
                cost_price=250.00,
                category=ProductCategory.ELECTRONICS,
                sku="SONY-WH1000XM5",
                brand="Sony",
                manufacturer="Sony Corporation",
                stock_quantity=75,
                min_stock_level=20,
                is_featured=True,
                weight=0.25,
                color="Black",
                images=[
                    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300",
                tags=["headphones", "wireless", "noise-canceling", "audio"],
                keywords=["sony", "headphones", "wireless", "audio"],
                warranty_period=365,
                return_period=30
            ),
            
            # Clothing
            Product(
                name="Nike Air Force 1 '07",
                description="Classic basketball shoe with durable leather upper and Air cushioning for all-day comfort.",
                price=90.00,
                sale_price=75.00,
                cost_price=40.00,
                category=ProductCategory.CLOTHING,
                sku="NIKE-AF1-07",
                brand="Nike",
                manufacturer="Nike Inc.",
                stock_quantity=200,
                min_stock_level=50,
                is_featured=True,
                is_bestseller=True,
                weight=0.4,
                size="10",
                color="White/White",
                images=[
                    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300",
                tags=["sneakers", "nike", "classic", "casual"],
                keywords=["nike", "shoes", "sneakers", "classic"],
                warranty_period=90,
                return_period=30
            ),
            Product(
                name="Levi's 511 Slim Fit Jeans",
                description="Slim fit jeans made from stretch denim for comfortable, versatile wear.",
                price=79.50,
                cost_price=30.00,
                category=ProductCategory.CLOTHING,
                sku="LEVIS-511-SLIM",
                brand="Levi's",
                manufacturer="Levi Strauss & Co.",
                stock_quantity=150,
                min_stock_level=40,
                is_bestseller=True,
                weight=0.35,
                size="32x32",
                color="Midnight Blue",
                images=[
                    "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1542272604-787c3835535d?w=300",
                tags=["jeans", "denim", "slim-fit", "casual"],
                keywords=["levis", "jeans", "denim", "casual"],
                return_period=30
            ),
            
            # Books
            Product(
                name="The 7 Habits of Highly Effective People",
                description="Powerful lessons in personal change from Stephen Covey, one of the most respected business leaders of our time.",
                price=16.99,
                sale_price=12.99,
                cost_price=5.00,
                category=ProductCategory.BOOKS,
                sku="BOOK-7HABITS",
                brand="Simon & Schuster",
                manufacturer="Simon & Schuster",
                stock_quantity=300,
                min_stock_level=100,
                is_bestseller=True,
                weight=0.4,
                dimensions={"length": 20, "width": 13, "height": 2.5},
                color="Blue",
                images=[
                    "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300",
                tags=["business", "self-help", "motivation", "leadership"],
                keywords=["self-help", "business", "success", "motivation"],
                return_period=30
            ),
            
            # Sports & Outdoors
            Product(
                name="Nike Dri-FIT Running Shorts",
                description="Lightweight, breathable running shorts with built-in liner for maximum comfort during workouts.",
                price=35.00,
                sale_price=28.99,
                cost_price=12.00,
                category=ProductCategory.SPORTS,
                sku="NIKE-DRIFIT-SHORTS",
                brand="Nike",
                manufacturer="Nike Inc.",
                stock_quantity=180,
                min_stock_level=50,
                weight=0.1,
                size="Medium",
                color="Black",
                material="Dri-FIT",
                images=[
                    "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=300",
                tags=["running", "athletic", "shorts", "nike"],
                keywords=["nike", "shorts", "running", "athletic"],
                warranty_period=90,
                return_period=30
            ),
            
            # Health & Beauty
            Product(
                name="Oral-B Pro 1000 Electric Toothbrush",
                description="Clinically proven to reduce more plaque than a regular manual toothbrush.",
                price=49.99,
                sale_price=39.99,
                cost_price=20.00,
                category=ProductCategory.HEALTH_BEAUTY,
                sku="ORALB-PRO-1000",
                brand="Oral-B",
                manufacturer="Procter & Gamble",
                stock_quantity=120,
                min_stock_level=30,
                weight=0.3,
                color="White",
                images=[
                    "https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=300",
                tags=["toothbrush", "dental", "health", "electric"],
                keywords=["oral-b", "toothbrush", "electric", "dental"],
                warranty_period=365,
                return_period=30
            ),
            
            # Home & Kitchen
            Product(
                name="Ninja BL610 Professional Blender",
                description="1100-watt professional blender with six blades and three speeds for smoothies and more.",
                price=99.99,
                sale_price=79.99,
                cost_price=40.00,
                category=ProductCategory.HOME_KITCHEN,
                sku="NINJA-BL610",
                brand="Ninja",
                manufacturer="SharkNinja",
                stock_quantity=80,
                min_stock_level=20,
                is_featured=True,
                weight=4.5,
                dimensions={"length": 20, "width": 10, "height": 45},
                color="Gray",
                images=[
                    "https://images.unsplash.com/photo-1568559926197-3d7c8dc4d1e6?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1568559926197-3d7c8dc4d1e6?w=300",
                tags=["blender", "kitchen", "appliance", "ninja"],
                keywords=["blender", "ninja", "kitchen", "smoothie"],
                warranty_period=365,
                return_period=30
            ),
            
            # Toys & Games
            Product(
                name="LEGO Creator Expert Ford Mustang",
                description="Build and display this authentic replica of the classic 1965 Ford Mustang featuring V8 engine details.",
                price=149.99,
                sale_price=124.99,
                cost_price=60.00,
                category=ProductCategory.TOYS_GAMES,
                sku="LEGO-MUSTANG",
                brand="LEGO",
                manufacturer="LEGO Group",
                stock_quantity=45,
                min_stock_level=10,
                is_featured=True,
                weight=2.5,
                images=[
                    "https://images.unsplash.com/photo-1596755387247-23310d6d80d5?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1596755387247-23310d6d80d5?w=300",
                tags=["lego", "building", "mustang", "creator"],
                keywords=["lego", "mustang", "building", "toys"],
                warranty_period=None,
                return_period=90
            ),
            
            # Automotive
            Product(
                name="WeatherTech All-Weather Floor Liners",
                description="Premium laser-measured floor liners that provide ultimate protection for your vehicle's interior.",
                price=109.99,
                cost_price=50.00,
                category=ProductCategory.AUTOMOTIVE,
                sku="WEATHER-FLOOR",
                brand="WeatherTech",
                manufacturer="WeatherTech",
                stock_quantity=90,
                min_stock_level=25,
                weight=15.0,
                color="Black",
                material="Rubber",
                images=[
                    "https://images.unsplash.com/photo-1502161254066-6c74afbf07ca?w=400"
                ],
                thumbnail="https://images.unsplash.com/photo-1502161254066-6c74afbf07ca?w=300",
                tags=["automotive", "floor-mats", "protection", "accessories"],
                keywords=["weathertech", "floor-mats", "automotive", "protection"],
                warranty_period=365,
                return_period=30
            )
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        print(f"✅ Added {len(products)} comprehensive products to database!")
        
    except Exception as e:
        print(f"Error adding products: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_comprehensive_products()

