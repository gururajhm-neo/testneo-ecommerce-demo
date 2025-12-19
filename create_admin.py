"""
Script to create or update an admin user
"""
from database import SessionLocal
from models.user import User, UserRole
from services.auth_service import get_password_hash
from datetime import datetime

def create_or_update_admin():
    """Create admin user or update existing user to admin"""
    db = SessionLocal()
    try:
        # Find admin role enum
        admin_role = None
        for role in UserRole:
            if role.value == "admin":
                admin_role = role
                break
        
        if not admin_role:
            print("Error: Could not find ADMIN role enum")
            return
        
        # Check if admin user exists using raw SQL to avoid enum conversion issues
        from sqlalchemy import text
        result = db.execute(text("SELECT id FROM users WHERE email = :email"), {"email": "admin@ecommerce.com"})
        existing_user = result.fetchone()
        
        if existing_user:
            # Update existing user using raw SQL to avoid enum issues
            user_id = existing_user[0]
            db.execute(
                text("UPDATE users SET role = :role, is_active = :is_active, is_verified = :is_verified, is_email_verified = :is_email_verified WHERE id = :id"),
                {"role": "admin", "is_active": True, "is_verified": True, "is_email_verified": True, "id": user_id}
            )
            print("✓ Updated existing user to admin")
        else:
            # Create new admin user
            admin_user = User(
                email="admin@ecommerce.com",
                username="admin",
                password="admin123",
                first_name="Admin",
                last_name="User",
                role=admin_role
            )
            admin_user.is_active = True
            admin_user.is_verified = True
            admin_user.is_email_verified = True
            db.add(admin_user)
            print("✓ Created new admin user")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("ADMIN USER READY!")
        print("=" * 60)
        print("Email: admin@ecommerce.com")
        print("Password: admin123")
        print("\nYou can now login to the admin panel at:")
        print("http://localhost:3001/login")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_or_update_admin()

