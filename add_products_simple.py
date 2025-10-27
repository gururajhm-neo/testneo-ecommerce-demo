"""
Quick script to add products via SQL
"""
import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Check if products exist
cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
count = cursor.fetchone()[0]

if count > 0:
    print(f"Products already exist: {count} active products")
else:
    print("Adding sample products...")
    
    products = [
        ('iPhone 15 Pro Max', 'Latest iPhone with advanced features and titanium design', 1199.99, 1099.99, 'electronics', 'IPHONE-15-PRO-MAX', 'Apple', 50, 10, 100, 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=300'),
        ('Nike Air Max 270', 'Comfortable running shoes with Air Max technology', 129.99, 99.99, 'clothing', 'NIKE-AIR-MAX-270', 'Nike', 100, 20, 1000, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300'),
        ('The Great Gatsby', 'Classic American novel by F. Scott Fitzgerald', 12.99, None, 'books', 'BOOK-GATSBY', 'Scribner', 200, 50, 1000, 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300'),
        ('Samsung 4K Smart TV', '55-inch 4K Ultra HD Smart TV with HDR', 699.99, None, 'electronics', 'SAMSUNG-TV-55-4K', 'Samsung', 25, 5, 100, 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=300'),
        ('Levi\'s 501 Original', 'Classic straight fit jeans with button fly', 59.99, 49.99, 'clothing', 'LEVIS-501', 'Levi\'s', 150, 30, 1000, 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=300')
    ]
    
    now = datetime.now().isoformat()
    
    for name, desc, price, sale_price, cat, sku, brand, stock, min_stock, max_stock, thumb in products:
        cursor.execute("""
            INSERT INTO products 
            (name, description, price, sale_price, category, sku, brand, stock_quantity, min_stock_level, max_stock_level, is_active, is_featured, thumbnail, created_at, updated_at, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1, ?, ?, ?, ?)
        """, (name, desc, price, sale_price, cat, sku, brand, stock, min_stock, max_stock, thumb, now, now, now))
    
    conn.commit()
    print(f"Added {len(products)} products!")

conn.close()

