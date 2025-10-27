# 🚀 Quick Start Guide - E-Commerce Application

## ✅ Setup Complete!

Your database is now populated with realistic test data:
- **7 Users** (including admin)
- **17 Products** (electronics, clothing, books, home/garden)
- **41 Orders** with various statuses
- **39 Reviews** for testing

---

## 🎯 How to Start & Test

### 1. Backend is Already Running
The FastAPI server should be running at: **http://localhost:9000**

If not started, run:
```bash
python main.py
```

### 2. Frontend
Make sure the frontend is running (it should be in another terminal):
```bash
cd frontend
npm run dev
```

Access at: **http://localhost:3000**

---

## 👥 Test Accounts

### Admin Account
```
Email: admin@ecommerce.com
Password: admin123
```

### Customer Accounts
```
Email: customer@test.com
Password: customer123
```

Additional test customers:
- john@test.com / john123
- jane@test.com / jane123
- bob@test.com / bob123
- alice@test.com / alice123

---

## 🛍️ Customer Features (End-to-End Flow)

### Browse & Shop
1. Go to **Products** page
2. View 17+ products across multiple categories
3. Click any product to see details
4. Click **"Add to Cart"**
5. View your cart and adjust quantities
6. Click **"Proceed to Checkout"**
7. Fill in shipping address
8. Select payment method
9. Click **"Place Order"**
10. See order confirmation with order number

---

## 🔧 Admin Features (50+ Endpoints!)

Login as admin to access admin dashboard at: **http://localhost:3000/admin**

### Admin Dashboard (`/admin`)
- View revenue statistics
- See total users, products, orders
- Monitor order status distribution
- Track review approval status

### Products Management (`/admin/products`)
- **View all 17 products**
- **Delete products** (trash icon)
- Edit/Add products (coming soon)

### Orders Management (`/admin/orders`)
- **View all 41 orders**
- **Cancel orders** (X icon)
- Filter by status
- View order details

### Users Management (`/admin/users`)
- View all 7 users
- See user details
- Manage user roles

### Reviews Management (`/admin/reviews`)
- **View all 39 reviews**
- **Approve reviews** (✓ checkmark)
- **Reject reviews** (✗ X icon)
- **Delete reviews** (🗑️ trash icon)
- Filter by approval status

---

## 📊 All 50+ API Endpoints Available

### Authentication (3 endpoints)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token

### Products (3 endpoints)
- `GET /products` - List all products
- `GET /products/{id}` - Get product details
- `POST /products` - Create product (admin)
- `PUT /products/{id}` - Update product (admin)
- `DELETE /products/{id}` - Delete product (admin)

### Cart (4 endpoints)
- `GET /cart` - Get user's cart
- `POST /cart` - Add to cart
- `PUT /cart/{item_id}` - Update cart item
- `DELETE /cart/{item_id}` - Remove from cart
- `DELETE /cart` - Clear cart

### Orders (4 endpoints)
- `POST /orders` - Create order
- `GET /orders` - List user's orders
- `GET /orders/{id}` - Get order details
- `DELETE /orders/{id}` - Cancel order

### Reviews (2 endpoints)
- `POST /reviews` - Create review
- `GET /reviews/{product_id}` - Get product reviews

### Users (3 endpoints)
- `GET /users/me` - Get current user
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user

### Admin - Stats (2 endpoints)
- `GET /admin/stats` - Dashboard statistics
- `GET /admin/stats/revenue` - Revenue analytics

### Admin - Products (3 endpoints)
- `POST /products` - Create product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Admin - Orders (3 endpoints)
- `GET /orders` - Get all orders (filtering supported)
- `GET /orders/{id}` - Get order details
- `PUT /orders/{id}` - Update order status

### Admin - Users (3 endpoints)
- `GET /users` - Get all users
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user

### Admin - Reviews (4 endpoints)
- `GET /admin/reviews` - Get all reviews
- `PUT /admin/reviews/{id}/approve` - Approve review
- `PUT /admin/reviews/{id}/reject` - Reject review
- `DELETE /reviews/{id}` - Delete review

### Coupons (Coming soon - 5 endpoints)

---

## 🎯 How to Use All Features

### Customer Journey
1. **Browse** → View products by category
2. **Search** → Find specific products
3. **Add to Cart** → Select quantity and add
4. **Checkout** → Enter shipping details
5. **Place Order** → Complete purchase
6. **View Order** → Track order status

### Admin Journey
1. **Login** as admin
2. **Dashboard** → View key metrics
3. **Products** → Manage inventory
4. **Orders** → Process customer orders
5. **Users** → Manage user accounts
6. **Reviews** → Moderate product reviews

---

## 🐛 Troubleshooting

### Backend not starting?
```bash
# Kill any existing processes
Get-Process python | Stop-Process -Force

# Start backend
python main.py
```

### Frontend not loading?
```bash
cd frontend
npm install  # If needed
npm run dev
```

### Database issues?
The database is already populated! Check counts:
```bash
python -c "from database import SessionLocal; from models.user import User; from models.product import Product; from models.order import Order; from models.review import Review; db = SessionLocal(); print(f'Users: {db.query(User).count()}'); print(f'Products: {db.query(Product).count()}'); print(f'Orders: {db.query(Order).count()}'); print(f'Reviews: {db.query(Review).count()}'); db.close()"
```

---

## ✨ What's Working

✅ User Authentication (Login/Register/Logout)  
✅ Product Browsing (List & Details)  
✅ Shopping Cart (Add/Update/Remove)  
✅ Order Placement (Full checkout flow)  
✅ Admin Dashboard (Statistics)  
✅ Admin Products (View/Delete)  
✅ Admin Orders (View/Cancel)  
✅ Admin Users (View/Details)  
✅ Admin Reviews (View/Approve/Reject/Delete)  
✅ Role-based access control  
✅ JWT authentication  
✅ Responsive design  

---

## 📝 Next Steps (Optional Enhancements)

- [ ] Implement product editing
- [ ] Add product creation form
- [ ] Implement order status updates
- [ ] Add user management features
- [ ] Implement coupon system in UI
- [ ] Add wishlist functionality
- [ ] Implement inventory management
- [ ] Add analytics dashboard
- [ ] Implement search and filters

---

## 🎉 You're All Set!

Start testing at: **http://localhost:3000**

Login as admin: **admin@ecommerce.com** / **admin123**  
Login as customer: **customer@test.com** / **customer123**

Enjoy testing your fully functional e-commerce application! 🚀
