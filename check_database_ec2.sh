#!/bin/bash
# Script to check SQLite database on EC2

echo "=========================================="
echo "SQLite Database Check on EC2"
echo "=========================================="
echo ""

# Check if database file exists
DB_FILE="./ecommerce.db"
if [ -f "$DB_FILE" ]; then
    echo "✓ Database file exists: $DB_FILE"
    echo "  File size: $(du -h $DB_FILE | cut -f1)"
    echo "  Last modified: $(stat -c %y $DB_FILE)"
else
    echo "✗ Database file NOT found: $DB_FILE"
    echo "  Current directory: $(pwd)"
    echo "  Files in current directory:"
    ls -la | head -20
fi

echo ""
echo "=========================================="
echo "Checking Database Contents"
echo "=========================================="
echo ""

# Check if sqlite3 is installed
if command -v sqlite3 &> /dev/null; then
    echo "✓ sqlite3 is installed"
    
    if [ -f "$DB_FILE" ]; then
        echo ""
        echo "--- Users Table ---"
        sqlite3 $DB_FILE "SELECT COUNT(*) as user_count FROM users;" 2>/dev/null || echo "Error querying users table"
        sqlite3 $DB_FILE "SELECT id, email, username, role, is_active, is_verified FROM users LIMIT 5;" 2>/dev/null || echo "Error querying users"
        
        echo ""
        echo "--- Admin Users ---"
        sqlite3 $DB_FILE "SELECT id, email, username, role FROM users WHERE role = 'admin' OR role = 'ADMIN';" 2>/dev/null || echo "Error querying admin users"
        
        echo ""
        echo "--- Products Table ---"
        sqlite3 $DB_FILE "SELECT COUNT(*) as product_count FROM products;" 2>/dev/null || echo "Error querying products table"
        
        echo ""
        echo "--- Orders Table ---"
        sqlite3 $DB_FILE "SELECT COUNT(*) as order_count FROM orders;" 2>/dev/null || echo "Error querying orders table"
        
        echo ""
        echo "--- All Tables ---"
        sqlite3 $DB_FILE ".tables" 2>/dev/null || echo "Error listing tables"
    else
        echo "✗ Cannot check database contents - file not found"
    fi
else
    echo "✗ sqlite3 is not installed"
    echo "  Install with: sudo apt-get install sqlite3"
fi

echo ""
echo "=========================================="
echo "Python Database Check"
echo "=========================================="
echo ""

# Check with Python
python3 << EOF
import sqlite3
import os

db_file = "./ecommerce.db"
if os.path.exists(db_file):
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
        for admin in admins:
            print(f"  - ID: {admin[0]}, Email: {admin[1]}, Username: {admin[2]}, Role: {admin[3]}")
        
        # Check if database is accessible
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✓ Tables in database: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        conn.close()
    except Exception as e:
        print(f"✗ Error accessing database: {e}")
else:
    print(f"✗ Database file not found: {db_file}")
EOF

echo ""
echo "=========================================="
echo "Check Complete"
echo "=========================================="

