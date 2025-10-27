#!/usr/bin/env python3
"""
Create admin user for the e-commerce API
"""
import sys
from database import SessionLocal
from models.user import User, UserRole
from services.auth_service import create_user

def create_admin():
    """Create admin user if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@ecommerce.com").first()
        
        if admin:
            print(f"✅ Admin user already exists:")
            print(f"   Email: {admin.email}")
            print(f"   Username: {admin.username}")
            print(f"   Role: {admin.role}")
            print(f"   Active: {admin.is_active}")
            return
        
        # Create admin user
        print("Creating admin user...")
        admin_data = {
            "email": "admin@ecommerce.com",
            "username": "admin",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "User",
            "role": UserRole.ADMIN
        }
        
        admin = create_user(db, **admin_data)
        admin.is_active = True
        admin.is_verified = True
        admin.is_email_verified = True
        db.commit()
        
        print("✅ Admin user created successfully!")
        print(f"   Email: admin@ecommerce.com")
        print(f"   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()

