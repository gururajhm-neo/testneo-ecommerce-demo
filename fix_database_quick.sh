#!/bin/bash
# Quick script to fix database roles
# Run: bash fix_database_quick.sh

DB_FILE="ecommerce.db"

if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file $DB_FILE not found!"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "=========================================="
echo "Fixing Role Values in Database"
echo "=========================================="
echo ""

echo "Step 1: Checking current roles..."
sqlite3 "$DB_FILE" "SELECT id, email, role FROM users;"

echo ""
echo "Step 2: Fixing roles to lowercase..."
sqlite3 "$DB_FILE" "UPDATE users SET role = lower(role);"

echo ""
echo "Step 3: Verifying fix..."
sqlite3 "$DB_FILE" "SELECT id, email, role FROM users;"

echo ""
echo "Step 4: Checking admin user..."
sqlite3 "$DB_FILE" "SELECT id, email, role FROM users WHERE email = 'admin@ecommerce.com';"

echo ""
echo "=========================================="
echo "Fix Complete!"
echo "=========================================="

