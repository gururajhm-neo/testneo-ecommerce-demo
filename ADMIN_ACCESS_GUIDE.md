# Admin Access Guide

## 🎯 Current Admin Access (API Only)

Currently, **admin functionality is only available via the API** - there's no admin UI frontend yet.

---

## 🔐 How to Access Admin Functions

### Option 1: Swagger UI (Recommended)
**URL:** http://localhost:9000/docs

This is an interactive API documentation where you can test all 50+ admin endpoints.

### Steps:
1. Open http://localhost:9000/docs in your browser
2. Click the **"Authorize"** button (🔒 lock icon at top right)
3. Enter admin credentials:
   ```
   Email: admin@ecommerce.com
   Password: admin123
   ```
4. Click "Authorize" → "Close"
5. Now you can use any API endpoint!

---

## 📋 Available Admin Endpoints

### User Management
- `GET /users` - View all users
- `GET /users/{id}` - View specific user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Product Management
- `GET /products` - List all products
- `POST /products` - Create new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Order Management
- `GET /orders` - View all orders
- `GET /orders/{id}` - View specific order
- `PUT /orders/{id}` - Update order status
- `DELETE /orders/{id}` - Cancel order

### Inventory Management
- `GET /inventory` - Check stock levels
- `PUT /inventory/{id}` - Update inventory
- `GET /inventory/low-stock` - Get low stock alerts

### Review Management
- `GET /reviews` - View all reviews
- `PUT /reviews/{id}/approve` - Approve review
- `PUT /reviews/{id}/reject` - Reject review
- `DELETE /reviews/{id}` - Delete review

### Coupon Management
- `GET /coupons` - View all coupons
- `POST /coupons` - Create coupon
- `PUT /coupons/{id}` - Update coupon
- `DELETE /coupons/{id}` - Delete coupon

### Analytics & Reports
- `GET /admin/stats` - Dashboard statistics
- `GET /admin/stats/revenue` - Revenue reports
- `GET /admin/stats/products` - Product analytics
- `GET /admin/stats/users` - User analytics

### Refund Management
- `GET /refunds` - View all refunds
- `PUT /refunds/{id}/approve` - Approve refund
- `PUT /refunds/{id}/reject` - Reject refund

---

## 🚀 Using Swagger UI - Quick Examples

### Example 1: View All Orders
1. Expand `GET /orders`
2. Click "Try it out"
3. Click "Execute"
4. See all customer orders in the response

### Example 2: Create a New Product
1. Expand `POST /products`
2. Click "Try it out"
3. Fill in the request body:
```json
{
  "name": "New Product Name",
  "description": "Product description",
  "price": 99.99,
  "sale_price": 79.99,
  "cost_price": 50.00,
  "category": "electronics",
  "sku": "SKU-001",
  "brand": "Brand Name",
  "stock_quantity": 100,
  "min_stock_level": 10,
  "max_stock_level": 200,
  "is_featured": true
}
```
4. Click "Execute"
5. See the created product response

### Example 3: View Dashboard Stats
1. Expand `GET /admin/stats`
2. Click "Try it out"
3. Click "Execute"
4. See revenue, orders, users statistics

### Example 4: Approve a Review
1. Expand `PUT /reviews/{id}/approve`
2. Click "Try it out"
3. Enter review ID in path
4. Click "Execute"

---

## 🖥️ Want an Admin Dashboard UI?

Currently there's **no admin frontend**. If you want, I can create:

✅ **Admin Dashboard UI** with:
- Dashboard with stats visualization
- User management interface
- Product management interface
- Order management interface
- Review moderation interface
- Inventory management
- Analytics & reports

This would include:
- Admin-only routes
- Role-based navigation
- Data tables with filtering/searching
- Charts and graphs for analytics
- Forms for creating/editing data

**Would you like me to build this admin UI?**

---

## 🔧 Testing Admin Features (Current Way)

### 1. View All Products
```
GET http://localhost:9000/products
Headers: Authorization: Bearer {your_token}
```

### 2. Create a Product
```
POST http://localhost:9000/products
Headers: Authorization: Bearer {your_token}
Body: { "name": "...", "price": 99.99, ... }
```

### 3. View All Orders
```
GET http://localhost:9000/orders
Headers: Authorization: Bearer {your_token}
```

### 4. Get Dashboard Stats
```
GET http://localhost:9000/admin/stats
Headers: Authorization: Bearer {your_token}
```

---

## 📊 50+ API Endpoints Available

### Product Management (8 endpoints)
- List products with filters
- Get product details
- Create product
- Update product
- Delete product
- Search products
- Get featured products
- Get bestsellers

### Order Management (12 endpoints)
- List orders
- Get order details
- Create order
- Update order status
- Cancel order
- Get customer orders
- Filter orders by status
- Export orders

### User Management (8 endpoints)
- List users
- Get user details
- Update user
- Delete user
- Get user orders
- Update user role
- Reset user password
- Block/unblock user

### Review Management (7 endpoints)
- List reviews
- Get review details
- Approve review
- Reject review
- Delete review
- Get product reviews
- Get customer reviews

### Coupon Management (7 endpoints)
- List coupons
- Create coupon
- Update coupon
- Delete coupon
- Validate coupon
- Get active coupons
- Deactivate coupon

### Inventory Management (6 endpoints)
- Check inventory
- Update stock
- Get low stock alerts
- Adjust inventory
- Get inventory history
- Reserve stock

### Analytics (6 endpoints)
- Dashboard stats
- Revenue reports
- Product analytics
- User analytics
- Order analytics
- Sales trends

### Wishlist Management (4 endpoints)
- List wishlists
- Get user wishlist
- Add to wishlist
- Remove from wishlist

Plus many more...

---

## 🎯 Current Status

| Feature | Customer UI | Admin UI | API |
|---------|------------|----------|-----|
| Browse Products | ✅ | ❌ | ✅ |
| Add to Cart | ✅ | ❌ | ✅ |
| Checkout | ✅ | ❌ | ✅ |
| View Orders | ❌ | ❌ | ✅ |
| Manage Products | ❌ | ❌ | ✅ |
| Manage Users | ❌ | ❌ | ✅ |
| Analytics | ❌ | ❌ | ✅ |
| Review Moderation | ❌ | ❌ | ✅ |

**Legend:**
- ✅ = Fully implemented
- ❌ = Not implemented
- 🚧 = Partially implemented

---

## 💡 Recommendation

To use **admin features**, use **Swagger UI** at:
**http://localhost:9000/docs**

Or, would you like me to **build a complete Admin Dashboard UI** with React components for all admin functions?

