# 🚀 EC2 Deployment Complete Guide

Complete guide for deploying and using the E-Commerce Application on AWS EC2.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Access URLs](#access-urls)
3. [Initial Setup](#initial-setup)
4. [Service Management](#service-management)
5. [Populate Data](#populate-data)
6. [Troubleshooting](#troubleshooting)
7. [Complete Command Reference](#complete-command-reference)

---

## 🚀 Quick Start

### SSH into EC2
```bash
ssh ubuntu@44.202.138.57
```

### Navigate to Project
```bash
cd ~/ecom-app/testneo-ecommerce-demo
```

### Start Services
```bash
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
cd frontend && nohup npm start > ../frontend.log 2>&1 &
```

### Populate Data
```bash
python3 populate_mock_data.py
```

---

## 🌐 Access URLs

### Frontend & Admin Panel
- **Homepage**: http://44.202.138.57:3001
- **Products**: http://44.202.138.57:3001/products
- **Admin Dashboard**: http://44.202.138.57:3001/admin
- **Admin Login**: http://44.202.138.57:3001/login

### Backend API
- **API Base**: http://44.202.138.57:9000
- **API Docs**: http://44.202.138.57:9000/docs
- **OpenAPI Spec**: http://44.202.138.57:9000/openapi.json

---

## 🔐 Admin Credentials

### Default Admin User
- **Email**: `admin@ecommerce.com`
- **Password**: `admin123`

### Additional Test Users
- **Customer**: `customer@test.com` / `customer123`
- **Moderator**: `moderator@ecommerce.com` / `moderator123`

---

## 🛠️ Initial Setup

### 1. First-Time Deployment

```bash
# Navigate to project
cd ~/ecom-app/testneo-ecommerce-demo

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies (if not already installed)
pip install -r requirements.txt

# Install Node.js dependencies (if not already installed)
cd frontend
npm install
cd ..

# Build frontend
cd frontend
npm run build
cd ..
```

### 2. Configure Firewall (UFW)

```bash
# Allow ports 9000 (backend) and 3001 (frontend)
sudo ufw allow 9000/tcp
sudo ufw allow 3001/tcp
sudo ufw allow 22/tcp  # SSH (if not already allowed)
sudo ufw status
```

### 3. Start Services

```bash
# Start backend
nohup python3 main.py > backend.log 2>&1 &

# Start frontend (production)
cd frontend
nohup npm start > ../frontend.log 2>&1 &
cd ..
```

### 4. Verify Services are Running

```bash
# Check if ports are listening
sudo lsof -i :9000  # Backend
sudo lsof -i :3001  # Frontend

# Check processes
ps aux | grep python3 | grep main.py
ps aux | grep npm | grep -v grep
```

---

## 📊 Populate Data

### Add Comprehensive Test Data

```bash
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate
python3 populate_mock_data.py
```

This will add:
- ✅ 15+ Products across multiple categories
- ✅ Multiple test customers
- ✅ Sample orders with different statuses
- ✅ Product reviews and ratings
- ✅ Coupons and discount codes

---

## 🎛️ Service Management

### Check Service Status

```bash
# Check backend
ps aux | grep python3 | grep main.py
sudo lsof -i :9000

# Check frontend
ps aux | grep npm | grep -v grep
sudo lsof -i :3001
```

### View Logs

```bash
# Backend logs
tail -f ~/ecom-app/testneo-ecommerce-demo/backend.log

# Frontend logs
tail -f ~/ecom-app/testneo-ecommerce-demo/frontend.log

# Last 50 lines of each
tail -n 50 backend.log
tail -n 50 frontend.log
```

### Stop Services

```bash
# Stop backend
pkill -f "python3 main.py"

# Stop frontend
pkill -f "npm"
pkill -f "serve"
```

### Restart Services

```bash
# Stop existing services
pkill -f "python3 main.py"
pkill -f "npm"

# Wait a moment
sleep 2

# Start backend
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &

# Start frontend
cd frontend
nohup npm start > ../frontend.log 2>&1 &
cd ..
```

---

## 🔧 Troubleshooting

### Issue: Frontend not loading

**Check if frontend is running:**
```bash
ps aux | grep npm
sudo lsof -i :3001
```

**Rebuild and restart:**
```bash
cd ~/ecom-app/testneo-ecommerce-demo/frontend
npm run build
cd ..
cd frontend
nohup npm start > ../frontend.log 2>&1 &
cd ..
```

### Issue: Backend not responding

**Check if backend is running:**
```bash
ps aux | grep python3
sudo lsof -i :9000
```

**Restart backend:**
```bash
pkill -f "python3 main.py"
sleep 2
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
```

**Check for errors:**
```bash
tail -n 100 backend.log
```

### Issue: Database errors

**Check database file exists:**
```bash
ls -lh ~/ecom-app/testneo-ecommerce-demo/*.db
```

**Recreate database (CAUTION: This deletes all data):**
```bash
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate
python3 -c "from database import drop_db, init_db; drop_db(); init_db(); print('Database recreated')"
```

### Issue: CORS errors

**Verify CORS is configured in config.py:**
```bash
grep -A 15 "cors_origins" config.py
```

**Should include:**
- `http://44.202.138.57:3001`
- `http://44.202.138.57:3000`

**Restart backend after CORS changes:**
```bash
pkill -f "python3 main.py"
sleep 2
nohup python3 main.py > backend.log 2>&1 &
```

### Issue: Empty data in admin panel

**Populate database with test data:**
```bash
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate
python3 populate_mock_data.py
```

**Check database content:**
```bash
# Count users
sqlite3 ~/ecom-app/testneo-ecommerce-demo/ecommerce.db "SELECT COUNT(*) FROM users"

# Count products
sqlite3 ~/ecom-app/testneo-ecommerce-demo/ecommerce.db "SELECT COUNT(*) FROM products"

# Count orders
sqlite3 ~/ecom-app/testneo-ecommerce-demo/ecommerce.db "SELECT COUNT(*) FROM orders"
```

---

## 📚 Complete Command Reference

### Database Management

```bash
# View all users
sqlite3 ~/ecom-app/testneo-ecommerce-demo/ecommerce.db "SELECT email, username, role FROM users"

# View all products
sqlite3 ~/ecom-app/testneo-ecommerce-demo/ecommerce.db "SELECT name, price, stock_quantity FROM products LIMIT 10"

# View orders
sqlite3 ~/ecom-app/testneo-ecommerce-demo/ecommerce.db "SELECT id, total_price, status FROM orders LIMIT 10"

# Database size
ls -lh ~/ecom-app/testneo-ecommerce-demo/ecommerce.db
```

### API Testing

```bash
# Test login API
curl -X POST http://localhost:9000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "admin@ecommerce.com", "password": "admin123"}'

# Get products (no auth required)
curl http://localhost:9000/products

# Get admin stats (requires token)
curl http://localhost:9000/admin/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Git Operations

```bash
# Pull latest changes
cd ~/ecom-app/testneo-ecommerce-demo
git pull origin main

# Check current commit
git log --oneline -5

# Check for local changes
git status
```

### System Monitoring

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep -E "python|node|npm"

# Check listening ports
sudo netstat -tulpn | grep -E "9000|3001"
```

---

## 🎯 Admin Panel Features

### Dashboard
- View total users, products, orders, revenue
- Sales charts and analytics
- Inventory alerts for low stock
- Recent activity and statistics

### Products Management
- ✅ View all products
- ✅ Add new products
- ✅ Edit existing products
- ✅ Delete products
- ✅ Search and filter
- ✅ Export to CSV
- ✅ Bulk operations

### Orders Management
- ✅ View all orders
- ✅ Update order status
- ✅ View order details
- ✅ Cancel orders
- ✅ Search and filter
- ✅ Export to CSV
- ✅ Pagination

### Users Management
- ✅ View all users
- ✅ Add new users
- ✅ Edit user details
- ✅ Delete users
- ✅ Search and filter
- ✅ Export to CSV

### Reviews Management
- ✅ View all reviews
- ✅ Approve/reject reviews
- ✅ Delete reviews
- ✅ Search and filter
- ✅ Pagination

### Coupons Management
- ✅ View all coupons
- ✅ Add new coupons
- ✅ Edit existing coupons
- ✅ Delete coupons
- ✅ Toggle active status
- ✅ Search and filter

---

## 🔄 Update and Deploy New Changes

### Pull Latest Code

```bash
cd ~/ecom-app/testneo-ecommerce-demo
git pull origin main
```

### Update Python Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Update Frontend Dependencies

```bash
cd frontend
npm install
npm run build
cd ..
```

### Restart Services

```bash
# Stop services
pkill -f "python3 main.py"
pkill -f "npm"

# Wait
sleep 3

# Start services
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &

cd frontend
nohup npm start > ../frontend.log 2>&1 &
cd ..
```

---

## 📝 Useful One-Liners

```bash
# Quick restart everything
cd ~/ecom-app/testneo-ecommerce-demo && source venv/bin/activate && pkill -f "python3 main.py" && pkill -f "npm" && sleep 2 && nohup python3 main.py > backend.log 2>&1 & cd frontend && nohup npm start > ../frontend.log 2>&1 & cd ..

# Check service status
echo "Backend:" && (ps aux | grep "python3 main.py" | grep -v grep && echo "Running") || echo "Not Running" && echo "Frontend:" && (ps aux | grep "npm" | grep -v grep && echo "Running") || echo "Not Running"

# View latest logs
tail -n 20 backend.log frontend.log

# Database statistics
sqlite3 ~/ecom-app/testneo-ecommerce-demo/ecommerce.db "SELECT 'Users' as Type, COUNT(*) as Count FROM users UNION SELECT 'Products', COUNT(*) FROM products UNION SELECT 'Orders', COUNT(*) FROM orders UNION SELECT 'Reviews', COUNT(*) FROM reviews"
```

---

## ✅ Summary

### URLs
- **Frontend**: http://44.202.138.57:3001
- **Admin Panel**: http://44.202.138.57:3001/admin
- **API Docs**: http://44.202.138.57:9000/docs

### Credentials
- **Admin**: admin@ecommerce.com / admin123

### Quick Commands
```bash
# Start services
cd ~/ecom-app/testneo-ecommerce-demo && source venv/bin/activate && nohup python3 main.py > backend.log 2>&1 & cd frontend && nohup npm start > ../frontend.log 2>&1 & cd ..

# Populate data
cd ~/ecom-app/testneo-ecommerce-demo && source venv/bin/activate && python3 populate_mock_data.py

# View logs
tail -f backend.log frontend.log

# Stop services
pkill -f "python3 main.py" && pkill -f "npm"
```

---

**Happy Testing! 🎉**

