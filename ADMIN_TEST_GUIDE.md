# Admin Testing Guide - 50+ API Endpoints

## Overview
Your e-commerce API has **63 endpoints** covering all features. As an admin, you can test comprehensive scenarios.

## Admin Credentials
- **Email:** admin@ecommerce.com
- **Password:** admin123

## How to Run Comprehensive Tests

### Step 1: Populate Database
```bash
python populate_admin_data.py
```

### Step 2: Access API Documentation
Open: **http://localhost:9000/docs**

### Step 3: Login as Admin
Use the admin credentials to get an access token for all protected endpoints.

---

## Admin Use Cases by Feature (50+ Endpoints)

### 1. **Product Management** (8 endpoints)

#### Test Scenarios:
- **GET /products** - List all products with filters
  - Test: `?category=electronics&min_price=100&max_price=500`
  - Test: `?is_featured=true&is_bestseller=true`
  - Test: `?search=iPhone&sort=price_asc`

- **POST /products** - Create new product
  - Test with different categories
  - Test validation rules (e.g., sale_price < price)
  - Test SKU uniqueness

- **GET /products/{id}** - Get product details
- **PUT /products/{id}** - Update product
- **PATCH /products/{id}** - Partial update
- **DELETE /products/{id}** - Soft delete product
- **GET /products/categories** - List categories
- **GET /admin/products/stats** - Product statistics

### 2. **User Management** (6 endpoints)

- **GET /users** - List all users
  - Test pagination: `?skip=0&limit=20`
  - Test filters: `?role=customer&is_active=true`
  
- **GET /users/{id}** - Get user details
- **PUT /users/{id}** - Update user
- **DELETE /users/{id}** - Deactivate user
- **GET /admin/users/roles** - List user roles
- **GET /admin/users/stats** - User statistics

### 3. **Order Management** (12 endpoints)

- **GET /orders** - List all orders
  - Test filters: `?status=pending&user_id=2`
  - Test sorting: `?sort=created_at_desc`
  
- **GET /orders/{id}** - Get order details
- **PUT /orders/{id}** - Update order status
  - Test: Confirm → Processing → Shipped → Delivered
- **POST /orders/{id}/cancel** - Cancel order
- **POST /orders/{id}/refund** - Process refund
- **GET /orders/{id}/items** - Get order items
- **GET /orders/{id}/tracking** - Get tracking info
- **PUT /orders/{id}/status** - Change order status
- **GET /admin/orders/stats** - Order statistics
- **GET /admin/orders/pending** - Pending orders
- **GET /admin/orders/revenue** - Revenue reports
- **GET /admin/orders/recent** - Recent orders

### 4. **Review Management** (8 endpoints)

- **GET /reviews** - List all reviews
  - Test filters: `?product_id=1&status=pending`
  - Test: `?rating=5&is_approved=true`
  
- **GET /reviews/{id}** - Get review details
- **PUT /reviews/{id}/approve** - Approve review
- **PUT /reviews/{id}/reject** - Reject review
- **DELETE /reviews/{id}** - Delete review
- **POST /reviews/{id}/reply** - Reply to review
- **GET /admin/reviews/pending** - Pending reviews
- **GET /admin/reviews/stats** - Review statistics

### 5. **Coupon Management** (7 endpoints)

- **POST /coupons** - Create coupon
  - Test different types: percentage, fixed, free_shipping
  - Test validation rules
  
- **GET /coupons** - List all coupons
  - Test filters: `?is_active=true`
  
- **GET /coupons/{id}** - Get coupon details
- **PUT /coupons/{id}** - Update coupon
- **DELETE /coupons/{id}** - Deactivate coupon
- **GET /admin/coupons/stats** - Coupon statistics
- **POST /coupons/{code}/validate** - Validate coupon code

### 6. **Refund Management** (6 endpoints)

- **GET /refunds** - List all refunds
  - Test filters: `?status=pending&user_id=2`
  
- **GET /refunds/{id}** - Get refund details
- **PUT /refunds/{id}/approve** - Approve refund
- **PUT /refunds/{id}/reject** - Reject refund
- **POST /refunds/{id}/process** - Process refund payment
- **GET /admin/refunds/stats** - Refund statistics

### 7. **Analytics & Reports** (8 endpoints)

- **GET /admin/stats** - Overall statistics
- **GET /admin/stats/revenue** - Revenue analytics
  - Test date ranges: `?start_date=2024-01-01&end_date=2024-12-31`
  
- **GET /admin/stats/products** - Product performance
- **GET /admin/stats/users** - User analytics
- **GET /admin/stats/orders** - Order metrics
- **GET /admin/reports/daily** - Daily reports
- **GET /admin/reports/monthly** - Monthly reports
- **GET /admin/reports/export** - Export data

### 8. **Inventory Management** (7 endpoints)

- **GET /admin/inventory** - List all inventory
  - Test filters: `?low_stock=true&category=electronics`
  
- **POST /admin/inventory/adjust** - Adjust stock
- **GET /admin/inventory/reports** - Stock reports
- **POST /admin/inventory/bulk** - Bulk update
- **GET /admin/inventory/alerts** - Low stock alerts
- **GET /admin/inventory/movements** - Stock movements
- **POST /admin/inventory/transfer** - Transfer inventory

### 9. **Wishlist Management** (Admin view) (3 endpoints)

- **GET /admin/wishlists** - All user wishlists
- **GET /admin/wishlists/stats** - Wishlist statistics
- **GET /admin/wishlists/top-products** - Most wished products

### 10. **System Management** (5 endpoints)

- **GET /admin/settings** - Get system settings
- **PUT /admin/settings** - Update settings
- **GET /admin/health** - System health check
- **GET /admin/logs** - System logs
- **POST /admin/cache/clear** - Clear cache

---

## Recommended Test Flow

### Phase 1: Product Management (10 mins)
1. Create 5-10 diverse products
2. Update product prices
3. Mark products as featured/bestsellers
4. Search and filter products
5. View product statistics

### Phase 2: Order Management (15 mins)
1. View all orders with filters
2. Update order status (pending → confirmed → shipped)
3. Process a refund for a cancelled order
4. View order revenue reports
5. Export order data

### Phase 3: Review & Content (10 mins)
1. Approve pending reviews
2. Reply to customer reviews
3. Reject spam reviews
4. View review statistics

### Phase 4: Coupon Management (10 mins)
1. Create different coupon types
2. Test coupon validation
3. Update coupon limits
4. View coupon usage stats

### Phase 5: Analytics (10 mins)
1. View dashboard statistics
2. Check revenue reports
3. Analyze product performance
4. Review user analytics
5. Export reports

### Phase 6: Inventory (10 mins)
1. Check low stock alerts
2. Adjust inventory levels
3. View stock movements
4. Bulk update inventory

---

## Quick API Testing Commands

### Using curl:
```bash
# Login
curl -X POST http://localhost:9000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecommerce.com","password":"admin123"}'

# Save token
TOKEN="your_token_here"

# Get all products
curl -H "Authorization: Bearer $TOKEN" http://localhost:9000/products

# Create coupon
curl -X POST http://localhost:9000/coupons \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code":"TEST10","discount_type":"percentage","discount_value":10}'

# Get admin stats
curl -H "Authorization: Bearer $TOKEN" http://localhost:9000/admin/stats
```

### Using Python:
```python
import requests

token = "your_token"
headers = {"Authorization": f"Bearer {token}"}

# Get all orders
orders = requests.get("http://localhost:9000/orders", headers=headers).json()

# Create product
product = requests.post("http://localhost:9000/products", 
  json={"name":"Test Product","price":99.99,"category":"electronics","sku":"TEST-001"},
  headers=headers).json()
```

---

## Test Data Available

After running `populate_admin_data.py`:
- ✅ 10+ Products (Electronics, Clothing, Books)
- ✅ 5 Coupons (Different types)
- ✅ Multiple Categories
- ✅ Rich metadata (tags, keywords, images)

---

## Advanced Testing Scenarios

### 1. Complex Business Rules
- Test coupon stack validation
- Test inventory constraints
- Test order status transitions
- Test role-based permissions

### 2. Edge Cases
- Test empty cart checkout
- Test out-of-stock orders
- Test expired coupons
- Test invalid user inputs

### 3. Performance Testing
- Test with large datasets
- Test pagination limits
- Test concurrent requests
- Test database queries

### 4. Integration Testing
- Test complete order flow
- Test coupon application
- Test refund workflow
- Test review moderation

---

## Documentation
- **OpenAPI Spec:** http://localhost:9000/openapi.json
- **Swagger UI:** http://localhost:9000/docs
- **ReDoc:** http://localhost:9000/redoc

