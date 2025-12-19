#!/usr/bin/env python3
"""
Test login functionality on EC2
Run this to debug login issues
"""
import sys
from database import SessionLocal, init_db
from models.user import User, UserRole
from services.auth_service import authenticate_user, login_user
from schemas.user import UserLogin

def test_login():
    """Test login functionality"""
    print("=" * 60)
    print("Testing Login Functionality")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_email = "admin@ecommerce.com"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        
        if not admin_user:
            print(f"✗ Admin user not found: {admin_email}")
            print("  Run: python3 create_admin_ec2.py")
            return False
        
        print(f"✓ Found admin user: {admin_user.email}")
        print(f"  - ID: {admin_user.id}")
        print(f"  - Username: {admin_user.username}")
        print(f"  - Role: {admin_user.role} (value: {admin_user.role.value})")
        print(f"  - Active: {admin_user.is_active}")
        print(f"  - Verified: {admin_user.is_verified}")
        print(f"  - Has password_hash: {bool(admin_user.password_hash)}")
        
        # Test authentication
        print("\n" + "=" * 60)
        print("Testing Authentication")
        print("=" * 60)
        
        try:
            authenticated_user = authenticate_user(db, admin_email, "admin123")
            if authenticated_user:
                print("✓ Authentication successful!")
            else:
                print("✗ Authentication failed - incorrect password")
                return False
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test login_user function
        print("\n" + "=" * 60)
        print("Testing login_user Function")
        print("=" * 60)
        
        try:
            login_data = UserLogin(email=admin_email, password="admin123")
            token_response = login_user(db, login_data)
            
            print("✓ Login successful!")
            print(f"  - Access token: {token_response.access_token[:50]}...")
            print(f"  - Token type: {token_response.token_type}")
            print(f"  - Expires in: {token_response.expires_in} seconds")
            print(f"  - User ID: {token_response.user.id}")
            print(f"  - User email: {token_response.user.email}")
            print(f"  - User role: {token_response.user.role}")
            
            return True
            
        except Exception as e:
            print(f"✗ Login error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)

