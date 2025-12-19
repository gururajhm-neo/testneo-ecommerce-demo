# EC2 Login 500 Error - Fix Guide

## Problem
Getting `{"detail":"Internal server error"}` when trying to login with `admin@ecommerce.com` / `admin123`

## Quick Fix Steps

### Step 1: Test Login Locally on EC2

SSH into your EC2 instance and run:

```bash
cd /path/to/your/project
python3 test_login_ec2.py
```

This will test the login function and show you exactly where it's failing.

### Step 2: Check Server Logs

Check your FastAPI server logs for the detailed error:

```bash
# If running with systemd
sudo journalctl -u your-service-name -n 50 --no-pager

# If running in a screen/tmux session
# Check the terminal where the server is running

# If logging to a file
tail -n 50 /path/to/logfile.log
```

### Step 3: Verify Admin User Exists

```bash
python3 << EOF
from database import SessionLocal, init_db
from models.user import User, UserRole

init_db()
db = SessionLocal()
admin = db.query(User).filter(User.email == "admin@ecommerce.com").first()
if admin:
    print(f"✓ Admin found: {admin.email}")
    print(f"  Role: {admin.role.value}")
    print(f"  Active: {admin.is_active}")
    print(f"  Has password: {bool(admin.password_hash)}")
else:
    print("✗ Admin not found - run: python3 create_admin_ec2.py")
db.close()
EOF
```

### Step 4: Recreate Admin User

If the admin user doesn't exist or has issues:

```bash
python3 create_admin_ec2.py
```

### Step 5: Restart Server

After making changes, restart your server:

```bash
# Stop current server (Ctrl+C or kill process)
# Then restart:
python3 main.py
```

## Common Issues

### Issue 1: Enum Conversion Error
**Error**: `'admin' is not among the defined enum values`

**Fix**: The code now properly converts enum values. Make sure you've pulled the latest code.

### Issue 2: UserResponse.from_orm() Failing
**Error**: `from_orm() got an unexpected keyword argument`

**Fix**: The code now manually converts the user object instead of using `from_orm()`.

### Issue 3: Database Connection Error
**Error**: `database is locked` or connection errors

**Fix**: 
- Make sure only one instance of the server is running
- Check database file permissions: `chmod 644 ecommerce.db`

### Issue 4: Missing Dependencies
**Error**: Import errors

**Fix**: Install all dependencies:
```bash
pip3 install -r requirements.txt
```

## Testing the Fix

After applying the fix, test with:

```bash
# Test login function
python3 test_login_ec2.py

# Test via API (if server is running)
curl -X POST http://localhost:9000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ecommerce.com", "password": "admin123"}'
```

## What Was Fixed

1. **Better Error Handling**: Login function now catches and logs all errors
2. **Enum Conversion**: Properly converts model enum to schema enum
3. **Manual UserResponse Creation**: Instead of using `from_orm()`, manually creates the response object
4. **Detailed Logging**: Server logs now show the exact error and stack trace

## Still Not Working?

1. Run `python3 test_login_ec2.py` and share the output
2. Check server logs and share the error message
3. Verify database file exists: `ls -la ecommerce.db`
4. Check Python version: `python3 --version` (should be 3.8+)
5. Verify all imports work: `python3 -c "from services.auth_service import login_user; print('OK')"`

