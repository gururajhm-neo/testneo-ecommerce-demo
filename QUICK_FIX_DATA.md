# 🚀 Quick Fix - Populate Data on EC2

## ⚡ Run These Commands on Your EC2 Server

### 1. Pull Latest Code
```bash
cd ~/ecom-app/testneo-ecommerce-demo
git pull origin main
```

### 2. Populate Database with Test Data
```bash
source venv/bin/activate
python3 populate_mock_data.py
```

### 3. Wait for Data to Load
You should see output like:
```
============================================================
POPULATING DATABASE WITH MOCK DATA
============================================================

[1/5] Creating Users...
[OK] Created 4 customer users

[2/5] Creating Products...
[OK] Created 15 products

[3/5] Creating Orders...
[OK] Created 20 orders

[4/5] Creating Reviews...
[OK] Created 30 reviews

[5/5] Creating Coupons...
[OK] Created 4 coupons

============================================================
DATABASE POPULATION COMPLETE!
============================================================
Total Users: 7
Total Products: 18
Total Orders: 20
Total Reviews: 30
Total Coupons: 7
```

### 4. Refresh Admin Panel
Go to: **http://44.202.138.57:3001/admin**

Login with:
- **Email**: `admin@ecommerce.com`
- **Password**: `admin123`

---

## ✅ After This You Will See:

- ✅ **Products**: 18+ products with images
- ✅ **Users**: 7 users (admin, moderator, 4 customers)
- ✅ **Orders**: 20 orders with different statuses
- ✅ **Reviews**: 30 product reviews
- ✅ **Coupons**: 4 active discount codes
- ✅ **Dashboard**: Complete analytics and charts

---

## 🎯 All Features Now Available

### Dashboard
- Sales statistics
- Revenue charts
- Inventory alerts
- Recent activity

### Products
- Add/Edit/Delete products
- Search and filter
- Export CSV
- Pagination

### Orders
- View/Update/Cancel orders
- Status management
- Search and filter
- Export CSV

### Users
- Add/Edit/Delete users
- Search and filter
- Export CSV

### Reviews
- Approve/Reject/Delete
- Search and filter

### Coupons
- Add/Edit/Delete coupons
- Toggle active status

---

**That's it! Refresh your browser and enjoy all the features! 🎉**

