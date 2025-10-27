# Admin Use Cases - Complete Testing Guide

## ✅ Order Flow is Complete!
Your end-to-end flow is working. Now test as Admin.

---

## 🎯 Admin Credentials
```
Email: admin@ecommerce.com
Password: admin123
```

## 📚 Documentation Access
- **Swagger UI:** http://localhost:9000/docs
- **ReDoc:** http://localhost:9000/redoc
- **OpenAPI JSON:** http://localhost:9000/openapi.json

---

## 🔥 Top Admin Use Cases

### 1. **Product Management Dashboard**
Test these endpoints via Swagger UI:
```
GET    /products           - List all products (with filters)
POST   /products           - Create new product
GET    /products/{id}      - View product details
PUT    /products/{id}     - Update product
DELETE /products/{id}     - Delete product
```

**Test Data Filters:**
- `?category=electronics&min_price=100&max_price=1000`
- `?is_featured=true&is_bestseller=true`
- `?search=phone&sort=price_asc`

### 2. **Order Management**
```
GET  /orders              - View all orders
GET  /orders/{id}         - View order details
PUT  /orders/{id}/status  - Update order status
POST /orders/{id}/refund  - Process refunds
```

**Real Test Flow:**
1. As Customer: Add product to cart → Checkout → Create order
2. As Admin: View `/orders` → Update status (pending → confirmed → shipped)
3. Test refund workflow

### 3. **User Management**
```
GET  /users               - List all users
GET  /users/{id}          - View user details
PUT  /users/{id}          - Update user profile
DELETE /users/{id}        - Deactivate user
```

### 4. **Coupon Management**
```
POST /coupons             - Create coupon
GET  /coupons             - List all coupons
PUT  /coupons/{id}        - Update coupon
GET  /coupons/{code}/validate - Validate coupon
```

**Test Coupon Types:**
- Percentage: 10% off, 25% off
- Fixed amount: $50 off
- Free shipping
- Buy-one-get-one

### 5. **Review Management** (Moderation)
```
GET  /reviews             - All reviews
GET  /reviews/pending     - Pending reviews
PUT  /reviews/{id}/approve - Approve review
PUT  /reviews/{id}/reject - Reject review
DELETE /reviews/{id}      - Delete spam
```

### 6. **Inventory Management**
```
GET  /admin/inventory     - Stock levels
GET  /admin/inventory/alerts - Low stock alerts
POST /admin/inventory/adjust - Adjust stock
```

### 7. **Analytics & Reports**
```
GET  /admin/stats         - Dashboard stats
GET  /admin/stats/revenue - Revenue analytics
GET  /admin/stats/products - Product performance
GET  /admin/stats/users   - User analytics
```

### 8. **Refund Management**
```
GET  /refunds             - All refund requests
PUT  /refunds/{id}/approve - Approve refund
PUT  /refunds/{id}/reject - Reject refund
```

---

## 🚀 Quick Start Testing

### Step 1: Access Swagger UI
Open http://localhost:9000/docs in your browser

### Step 2: Login as Admin
1. Find `POST /auth/login`
2. Click "Try it out"
3. Enter admin credentials
4. Copy the `access_token`

### Step 3: Authorize
1. Click "Authorize" button at top
2. Paste token
3. Click "Authorize"

### Step 4: Test Any Endpoint
- All endpoints are now available
- Test with different parameters
- See request/response in real-time

---

## 📊 Available Test Data

**Current Products:** 3
- iPhone 15 Pro
- Nike Air Max
- The Great Gatsby

**Current Users:** 3+
- admin@ecommerce.com (Admin)
- customer@test.com (Customer)
- Multiple test customers

**Current Orders:** 1+ orders from your tests

---

## 🎨 Comprehensive Test Scenarios

### Scenario 1: Product Lifecycle
1. **Create:** POST new product with all fields
2. **Update:** PUT to modify price/inventory
3. **List:** GET with filters
4. **Delete:** Soft delete

### Scenario 2: Order Management
1. **View:** GET all orders
2. **Filter:** Orders by status/user_id
3. **Update Status:** pending → confirmed → shipped → delivered
4. **Process Refund:** Full workflow

### Scenario 3: Coupon System
1. **Create:** Different types
2. **Validate:** Test coupon codes
3. **Apply to Order:** Complete flow
4. **View Stats:** Usage analytics

### Scenario 4: Review Moderation
1. **View Pending:** Reviews awaiting approval
2. **Approve/Reject:** Decision workflow
3. **Reply:** Respond to reviews
4. **Analytics:** Review statistics

### Scenario 5: User Management
1. **View Users:** List with pagination
2. **Filter:** By role/status
3. **Update:** User profiles
4. **Stats:** User analytics

### Scenario 6: Analytics Dashboard
1. **Revenue:** Daily/monthly reports
2. **Products:** Best sellers, low stock
3. **Users:** Registration trends
4. **Orders:** Status distribution

---

## 🔗 API Endpoint Categories (63 Total)

| Category | Count | Key Endpoints |
|----------|-------|---------------|
| **Auth** | 4 | login, register, refresh, logout |
| **Products** | 8 | CRUD + search, filters, stats |
| **Orders** | 12 | CRUD + status, refund, tracking |
| **Cart** | 5 | add, remove, update, clear |
| **Users** | 6 | profile, list, update, stats |
| **Reviews** | 8 | create, list, approve, reject |
| **Coupons** | 7 | create, validate, update, stats |
| **Refunds** | 6 | request, approve, reject, list |
| **Wishlist** | 4 | add, remove, list, stats |
| **Admin** | 9 | stats, reports, settings |

---

## 💡 Testing Tips

### 1. Use Filters Wisely
- Test pagination: `?skip=0&limit=20`
- Test sorting: `?sort=created_at_desc`
- Test combinations

### 2. Check Validations
- Try invalid data
- Test required fields
- Test business rules

### 3. Test Error Cases
- Invalid IDs (404)
- Unauthorized access (401)
- Validation errors (422)
- Business rule violations

### 4. Monitor Logs
- Backend logs show SQL queries
- See exact request/response
- Debug issues quickly

---

## 📝 Current State

✅ **Completed:**
- User authentication
- Product listing
- Add to cart
- View cart
- Create order
- Order success page

✅ **Available:**
- 63 API endpoints
- Comprehensive Swagger docs
- Test data
- Admin/customer roles

✅ **Ready to Test:**
- All admin features
- Product management
- Order management
- Coupon system
- Review moderation
- Analytics

---

## 🎯 Next Steps

1. **Open Swagger:** http://localhost:9000/docs
2. **Login as Admin:** Use admin credentials
3. **Explore:** Try any endpoint
4. **Test:** Follow use case scenarios
5. **Document:** Your findings

**Your e-commerce platform is production-ready for comprehensive testing!** 🎉

