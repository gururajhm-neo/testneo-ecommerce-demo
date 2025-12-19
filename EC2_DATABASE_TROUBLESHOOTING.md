# EC2 Database Troubleshooting Guide

## Problem: 500 Internal Server Error on Login

If you're getting a 500 error when trying to login to the admin panel on EC2, follow these steps:

## Step 1: Check if Database Exists

SSH into your EC2 instance and run:

```bash
cd /path/to/your/project
ls -la ecommerce.db
```

If the file doesn't exist, the database needs to be initialized.

## Step 2: Check Database Contents

Run the check script:

```bash
chmod +x check_and_fix_database_ec2.sh
./check_and_fix_database_ec2.sh
```

Or manually check with Python:

```bash
python3 << EOF
from database import SessionLocal, init_db
from models.user import User

# Initialize database if needed
init_db()

# Check users
db = SessionLocal()
users = db.query(User).all()
print(f"Total users: {len(users)}")
for user in users:
    print(f"  - {user.email} ({user.role.value}) - Active: {user.is_active}")
db.close()
EOF
```

## Step 3: Create Admin User

If no admin user exists, create one:

```bash
python3 create_admin_ec2.py
```

This will create an admin user with:
- **Email**: `admin@ecommerce.com`
- **Password**: `admin123`

## Step 4: Check Server Logs

Check the FastAPI server logs for detailed error messages:

```bash
# If running with systemd
sudo journalctl -u your-service-name -f

# If running directly
# Check the terminal where you started the server
# Or check log files if you're logging to a file
```

## Step 5: Verify Database Permissions

Make sure the database file has correct permissions:

```bash
chmod 644 ecommerce.db
chown $USER:$USER ecommerce.db
```

## Step 6: Test Database Connection

Test if Python can connect to the database:

```bash
python3 << EOF
from database import SessionLocal, engine
from sqlalchemy import text

try:
    db = SessionLocal()
    result = db.execute(text("SELECT 1"))
    print("✓ Database connection successful")
    db.close()
except Exception as e:
    print(f"✗ Database connection failed: {e}")
EOF
```

## Step 7: Check SQLite Installation

Verify SQLite is installed:

```bash
sqlite3 --version
```

If not installed:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install sqlite3

# Amazon Linux
sudo yum install sqlite
```

## Step 8: Manual Database Query

Query the database directly:

```bash
sqlite3 ecommerce.db << EOF
.tables
SELECT * FROM users WHERE role IN ('admin', 'ADMIN');
SELECT COUNT(*) FROM users;
EOF
```

## Step 9: Restart the Server

After fixing the database, restart your FastAPI server:

```bash
# If using systemd
sudo systemctl restart your-service-name

# If running directly
# Stop the current process (Ctrl+C) and restart:
python3 main.py
```

## Step 10: Test Login

Try logging in again with:
- **Email**: `admin@ecommerce.com`
- **Password**: `admin123`

## Common Issues and Solutions

### Issue 1: Database file not found
**Solution**: Run `init_db()` from Python or restart the server (it auto-initializes)

### Issue 2: No admin user
**Solution**: Run `python3 create_admin_ec2.py`

### Issue 3: Permission denied
**Solution**: 
```bash
chmod 644 ecommerce.db
chown $USER:$USER ecommerce.db
```

### Issue 4: Database locked
**Solution**: Make sure only one instance of the server is running

### Issue 5: Import errors
**Solution**: Make sure you're in the correct directory and all dependencies are installed:
```bash
pip3 install -r requirements.txt
```

## Quick Fix Script

Run this complete fix script:

```bash
#!/bin/bash
cd /path/to/your/project

# Initialize database
python3 << EOF
from database import init_db
init_db()
print("Database initialized")
EOF

# Create admin user
python3 create_admin_ec2.py

# Check status
python3 << EOF
from database import SessionLocal
from models.user import User
db = SessionLocal()
admins = db.query(User).filter(User.role.in_([UserRole.ADMIN])).all()
print(f"Admin users: {len(admins)}")
for admin in admins:
    print(f"  - {admin.email}")
db.close()
EOF
```

## Still Having Issues?

1. Check server logs for the exact error message
2. Verify all environment variables are set correctly
3. Ensure all Python dependencies are installed
4. Check that the server is running on the correct port (9000)
5. Verify firewall rules allow connections on port 9000

