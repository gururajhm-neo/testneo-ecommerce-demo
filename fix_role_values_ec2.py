#!/usr/bin/env python3
"""
Fix role values in database - convert uppercase to lowercase
Run this on EC2 to fix any uppercase role values in the database
"""
from database import SessionLocal, init_db
from models.user import User, UserRole
from sqlalchemy import text

def fix_role_values():
    """Fix role values in database"""
    print("=" * 60)
    print("Fixing Role Values in Database")
    print("=" * 60)
    
    init_db()
    db = SessionLocal()
    
    try:
        # Check current roles
        print("\nChecking current roles...")
        users = db.query(User).all()
        for user in users:
            print(f"  User {user.id} ({user.email}): role = {user.role} (type: {type(user.role)})")
            if hasattr(user.role, 'value'):
                print(f"    - Enum value: {user.role.value}")
            if hasattr(user.role, 'name'):
                print(f"    - Enum name: {user.role.name}")
        
        # Fix roles using raw SQL to ensure lowercase
        print("\nFixing roles in database...")
        
        # Update all roles to lowercase
        db.execute(text("""
            UPDATE users 
            SET role = LOWER(role)
            WHERE role != LOWER(role)
        """))
        
        db.commit()
        print("✓ Roles updated to lowercase")
        
        # Verify the fix
        print("\nVerifying fix...")
        users = db.query(User).all()
        for user in users:
            role_value = user.role.value if hasattr(user.role, 'value') else str(user.role)
            print(f"  User {user.id} ({user.email}): role = {role_value}")
            if role_value.upper() == role_value and role_value != role_value.lower():
                print(f"    ⚠ Still uppercase: {role_value}")
            else:
                print(f"    ✓ Correct: {role_value}")
        
        print("\n" + "=" * 60)
        print("Fix Complete!")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    fix_role_values()

