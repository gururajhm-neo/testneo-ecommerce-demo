#!/usr/bin/env python3
"""
Script to create or update admin user on EC2
Run this on your EC2 instance to ensure admin user exists
"""
from database import SessionLocal, init_db
from models.user import User, UserRole
from services.auth_service import get_password_hash
from datetime import datetime

def create_or_update_admin():
    """Create or update admin user"""
    # Ensure database is initialized
    init_db()
    
    db = SessionLocal()
    try:
        admin_email = "admin@ecommerce.com"
        admin_password = "admin123"
        
        admin_user = db.query(User).filter(User.email == admin_email).first()

        if admin_user:
            # Update existing user to admin
            admin_user.role = UserRole.ADMIN
            admin_user.is_active = True
            admin_user.is_verified = True
            admin_user.is_email_verified = True
            # Update password hash
            admin_user.password_hash = get_password_hash(admin_password)
            db.commit()
            print("✓ Updated existing user to admin")
        else:
            # Create new admin user
            admin_user = User(
                email=admin_email,
                username="admin",
                password=admin_password,  # Plain password, User.__init__ will hash it
                first_name="Admin",
                last_name="User",
                phone="123-456-7890",
                role=UserRole.ADMIN
            )
            admin_user.is_active = True
            admin_user.is_verified = True
            admin_user.is_email_verified = True
            db.add(admin_user)
            db.commit()
            print("✓ Created new admin user")
        
        db.refresh(admin_user)
        
        print("\n============================================================")
        print("ADMIN USER READY!")
        print("============================================================")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        print(f"User ID: {admin_user.id}")
        print(f"Role: {admin_user.role.value}")
        print(f"Active: {admin_user.is_active}")
        print(f"Verified: {admin_user.is_verified}")
        print("\nYou can now login to the admin panel at:")
        print("http://44.202.138.57:3001/login")
        print("============================================================")

    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_or_update_admin()

