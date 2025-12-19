# Quick Fix: Database Role Values

## Problem
Database has uppercase role values ('ADMIN') but SQLAlchemy expects lowercase ('admin')

## Solution: Run SQLite Commands

### Option 1: Quick Script (Recommended)

```bash
cd ~/ecom-app/testneo-ecommerce-demo
chmod +x fix_database_quick.sh
./fix_database_quick.sh
```

### Option 2: Manual SQLite Commands

```bash
cd ~/ecom-app/testneo-ecommerce-demo

# Connect to database
sqlite3 ecommerce.db
```

Then run these SQL commands inside sqlite3:

```sql
-- See current roles
SELECT id, email, role FROM users;

-- Fix all roles to lowercase
UPDATE users SET role = lower(role);

-- Verify the fix
SELECT id, email, role FROM users;

-- Check admin user specifically
SELECT id, email, role FROM users WHERE email = 'admin@ecommerce.com';

-- Exit sqlite3
.quit
```

### Option 3: One-Line Command

```bash
cd ~/ecom-app/testneo-ecommerce-demo
sqlite3 ecommerce.db "UPDATE users SET role = lower(role); SELECT id, email, role FROM users;"
```

## Verify Fix

After running the fix, verify it worked:

```bash
python3 << EOF
from database import SessionLocal
from models.user import User

db = SessionLocal()
admin = db.query(User).filter(User.email == "admin@ecommerce.com").first()
if admin:
    print(f"✓ Role: {admin.role.value}")
    print(f"✓ Type: {type(admin.role)}")
else:
    print("✗ Admin user not found")
db.close()
EOF
```

You should see `Role: admin` without any errors.

## Restart Server

After fixing the database:

```bash
# Stop current server (Ctrl+C or kill process)
# Then restart:
python3 main.py
```

## Test Login

Try logging in with:
- Email: `admin@ecommerce.com`
- Password: `admin123`

