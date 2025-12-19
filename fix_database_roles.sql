-- SQLite commands to fix role values in database
-- Run these commands using: sqlite3 ecommerce.db < fix_database_roles.sql
-- Or run them interactively: sqlite3 ecommerce.db

-- Step 1: Check current roles (see what's in the database)
SELECT id, email, role FROM users;

-- Step 2: Fix all roles to lowercase
UPDATE users SET role = lower(role);

-- Step 3: Verify the fix (should show lowercase roles)
SELECT id, email, role FROM users;

-- Step 4: Check specifically for admin user
SELECT id, email, role FROM users WHERE email = 'admin@ecommerce.com';

