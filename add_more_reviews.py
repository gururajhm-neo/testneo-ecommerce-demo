"""Add more reviews to the database"""
from database import SessionLocal
from models.review import Review
from models.product import Product
from models.user import User
from sqlalchemy import func
import random

def add_more_reviews():
    db = SessionLocal()
    try:
        # Get all products and users
        products = db.query(Product).all()
        users = db.query(User).all()
        
        # Review templates
        review_templates = [
            ("Great product!", "Excellent quality and fast shipping. Highly recommend!"),
            ("Very satisfied", "Works perfectly as described. Great value for money."),
            ("Amazing!", "Exceeded my expectations. Will definitely buy again!"),
            ("Good value", "Decent product for the price. Does what it's supposed to do."),
            ("Outstanding quality", "One of the best purchases I've made. Quality is top notch."),
            ("Highly recommended", "Great product, great service, great price. What more could you ask for?"),
            ("Fast delivery", "Product arrived quickly and works perfectly. Very happy with my purchase."),
            ("Perfect fit", "Exactly as described. Very satisfied with this purchase."),
            ("Great quality", "Well made and durable. Worth every penny."),
            ("Love it!", "This product is amazing. I use it every day and it never disappoints."),
            ("Excellent service", "Great customer service and the product quality is outstanding."),
            ("Good purchase", "Nice product. Good value for the money. Would recommend to others."),
            ("Impressive", "Really impressed with the quality and performance. Great buy!"),
            ("Sturdy and reliable", "Built to last. Very pleased with this purchase."),
            ("Beautiful product", "Looks great and functions perfectly. Very happy customer."),
        ]
        
        # Get existing reviews count
        existing_count = db.query(Review).count()
        print(f"Current reviews: {existing_count}")
        
        if existing_count > 30:
            print("Already have enough reviews!")
            return
        
        # Add more reviews
        reviews_to_add = 50 - existing_count
        print(f"Adding {reviews_to_add} more reviews...")
        
        for i in range(reviews_to_add):
            product = random.choice(products)
            user = random.choice(users)
            
            # Check if user already reviewed this product
            existing_review = db.query(Review).filter(
                Review.user_id == user.id,
                Review.product_id == product.id
            ).first()
            
            if existing_review:
                continue
            
            title, comment = random.choice(review_templates)
            rating = random.choice([4, 5, 5, 5, 4, 5])  # Mostly positive
            
            review = Review(
                user_id=user.id,
                product_id=product.id,
                rating=rating,
                title=title,
                comment=comment
            )
            
            # Set additional properties
            review.is_verified_purchase = random.choice([True, True, False])  # Mostly verified
            review.is_approved = random.choice([True, False])  # Mix of approved/pending
            
            db.add(review)
        
        db.commit()
        print(f"[OK] Added {reviews_to_add} reviews successfully!")
        
        # Print final count
        final_count = db.query(Review).count()
        print(f"Total reviews now: {final_count}")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_more_reviews()

