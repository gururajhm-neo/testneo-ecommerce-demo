#!/bin/bash
# Script to check and fix SQLite database on EC2

echo "=========================================="
echo "SQLite Database Check & Fix on EC2"
echo "=========================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DB_FILE="./ecommerce.db"

# Check if database file exists
if [ -f "$DB_FILE" ]; then
    echo "✓ Database file exists: $DB_FILE"
    echo "  File size: $(du -h $DB_FILE | cut -f1)"
    echo "  Last modified: $(stat -c %y $DB_FILE 2>/dev/null || stat -f '%Sm' $DB_FILE 2>/dev/null)"
else
    echo "✗ Database file NOT found: $DB_FILE"
    echo "  Current directory: $(pwd)"
    echo ""
    echo "Creating database by running Python init script..."
    python3 << EOF
from database import init_db
init_db()
print("✓ Database initialized")
EOF
fi

echo ""
echo "=========================================="
echo "Checking Database Contents"
echo "=========================================="
echo ""

# Check with Python
python3 << 'PYEOF'
import sqlite3
import os
import sys

db_file = "./ecommerce.db"
if not os.path.exists(db_file):
    print(f"✗ Database file not found: {db_file}")
    sys.exit(1)

try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Check users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"✓ Users in database: {user_count}")
    
    # Check admin users
    cursor.execute("SELECT id, email, username, role FROM users WHERE role IN ('admin', 'ADMIN')")
    admins = cursor.fetchall()
    print(f"✓ Admin users: {len(admins)}")
    if admins:
        for admin in admins:
            print(f"  - ID: {admin[0]}, Email: {admin[1]}, Username: {admin[2]}, Role: {admin[3]}")
    else:
        print("  ⚠ No admin users found!")
    
    # Check all users
    cursor.execute("SELECT id, email, username, role, is_active, is_verified FROM users LIMIT 10")
    all_users = cursor.fetchall()
    print(f"\n✓ All users (first 10):")
    for user in all_users:
        print(f"  - ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Role: {user[3]}, Active: {user[4]}, Verified: {user[5]}")
    
    # Check if database is accessible
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n✓ Tables in database: {len(tables)}")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count} rows")
    
    conn.close()
    print("\n✓ Database is accessible and working")
    
except Exception as e:
    print(f"✗ Error accessing database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

echo ""
echo "=========================================="
echo "Check Complete"
echo "=========================================="

