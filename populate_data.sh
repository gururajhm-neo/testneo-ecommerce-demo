#!/bin/bash

# Populate Database with Mock Data
# Run this on EC2 to add comprehensive test data

echo "=========================================="
echo "Populating Database with Mock Data"
echo "=========================================="

# Navigate to project directory
cd ~/ecom-app/testneo-ecommerce-demo || exit 1

# Activate virtual environment
source venv/bin/activate

# Run populate script
echo "Running populate_mock_data.py..."
python3 populate_mock_data.py

echo ""
echo "=========================================="
echo "✓ Database populated with mock data!"
echo "=========================================="
echo ""
echo "You can now refresh the admin panel to see:"
echo "  - Products"
echo "  - Users"  
echo "  - Orders"
echo "  - Reviews"
echo "  - Coupons"
echo "=========================================="

