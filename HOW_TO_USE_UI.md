# How to Use the E-Commerce UI

## 🚀 Quick Start

### 1. Access the Application
Open your browser and go to: **http://localhost:3000**

---

## 👤 Test Accounts

### Customer Account
```
Email: customer@test.com
Password: customer123
```

### Admin Account
```
Email: admin@ecommerce.com
Password: admin123
```

---

## 🛒 Complete Shopping Flow (As Customer)

### Step 1: Browse Products
1. You should see the landing page
2. Click **"Products"** in the navigation
3. View all available products

### Step 2: View Product Details
1. Click on any product card
2. See full product information:
   - Name, description, price
   - Stock availability
   - Product images
   - Add to cart button

### Step 3: Add to Cart
1. On product detail page, adjust quantity
2. Click **"Add to Cart"** button
3. You'll see a success message
4. Cart icon in nav will show item count

### Step 4: View Cart
1. Click the cart icon in navigation
2. See all items in your cart
3. Adjust quantities (+/- buttons)
4. Remove items (trash icon)
5. See order summary with total

### Step 5: Proceed to Checkout
1. Click **"Proceed to Checkout"**
2. Fill out shipping information:
   - Address
   - City
   - State
   - ZIP Code
   - Country
3. Select payment method (Credit Card or Cash on Delivery)
4. Click **"Place Order"**

### Step 6: Order Confirmation
1. See order success page
2. View order number
3. See total amount and shipping details
4. Click "Continue Shopping"

---

## 🔐 Login Flow

### Option 1: From Homepage
1. Click **"Login"** in top navigation
2. Enter credentials
3. You'll be redirected to products page

### Option 2: Already on Products
- If not logged in, adding to cart will prompt you to login

---

## 🛍️ What You Can Do in the UI

### As Customer:
✅ **Browse Products**
- View all products
- Search products
- Filter by category

✅ **Product Details**
- Full product information
- Images and descriptions
- Check availability

✅ **Shopping Cart**
- Add multiple items
- Adjust quantities
- Remove items
- See total price

✅ **Checkout**
- Enter shipping address
- Choose payment method
- Place orders
- View order confirmation

---

## 👨‍💼 Admin Actions (via API)

While the UI is for customers, admins can use the **API** for management:

### Access Swagger UI:
**http://localhost:9000/docs**

### What Admin Can Do via API:

1. **View All Orders**
   - GET `/orders` - See all customer orders

2. **Manage Products**
   - POST `/products` - Create new products
   - PUT `/products/{id}` - Update existing products
   - DELETE `/products/{id}` - Remove products

3. **View Users**
   - GET `/users` - List all users
   - GET `/users/{id}` - View user details

4. **Manage Coupons**
   - POST `/coupons` - Create discount codes
   - GET `/coupons` - List all coupons

5. **Review Moderation**
   - GET `/reviews` - View all reviews
   - PUT `/reviews/{id}/approve` - Approve reviews

6. **Analytics**
   - GET `/admin/stats` - Dashboard stats
   - GET `/admin/stats/revenue` - Revenue reports

---

## 🎯 Current UI Features

### ✅ Working Pages:
- **Home** - Landing page
- **Products** - Browse all products
- **Product Detail** - Individual product view
- **Cart** - Shopping cart
- **Checkout** - Order placement
- **Order Success** - Confirmation page
- **Login** - Authentication
- **Register** - User registration

### 🎨 UI Features:
- **Responsive Design** - Works on mobile/tablet/desktop
- **Real-time Cart Updates** - Cart count in navigation
- **Product Search** - Find products easily
- **Price Display** - Shows regular and sale prices
- **Stock Status** - Shows availability
- **User Profile** - Display logged-in user

---

## 📱 How to Use Each Page

### Home Page (`/`)
- Beautiful landing page
- Links to products
- Call-to-action buttons

### Products Page (`/products`)
- Grid of all products
- Product cards with:
  - Image thumbnail
  - Product name
  - Price (with sale price)
  - "View Details" button

### Product Detail Page (`/products/:id`)
- Full-size images
- Complete description
- Price with discounts
- Stock availability
- Quantity selector
- "Add to Cart" button

### Cart Page (`/cart`)
- List of all cart items
- Product thumbnails
- Quantity controls (+/-)
- Item totals
- Order summary
- Total price
- "Proceed to Checkout" button

### Checkout Page (`/checkout`)
- Shipping address form:
  - Street address
  - City
  - State
  - ZIP Code
  - Country
- Payment method selection:
  - Credit/Debit Card
  - Cash on Delivery
- Order summary
- "Place Order" button

### Order Success Page (`/order-success/:id`)
- Confirmation message
- Order number
- Total amount
- Shipping address
- Payment method
- "Continue Shopping" button

### Login Page (`/login`)
- Email input
- Password input
- Login button
- Link to register

### Register Page (`/register`)
- Full registration form
- Email/Password/Username
- Register button
- Link to login

---

## 🎯 Testing Workflow

### Scenario 1: First-time User
1. Visit http://localhost:3000
2. Browse products on homepage
3. Click "Products" in nav
4. Click a product to view details
5. Add to cart
6. Click cart icon
7. Click "Proceed to Checkout"
8. **You'll be redirected to Login** (because checkout requires auth)
9. Login or register
10. Complete checkout

### Scenario 2: Returning User
1. Click "Login" in nav
2. Enter credentials
3. Browse products
4. Add items to cart
5. Go to cart
6. Checkout
7. Place order
8. See success page

---

## 🔧 Troubleshooting

### Issue: "Can't see products"
**Solution:** Make sure backend is running on port 9000

### Issue: "Cart is empty after adding items"
**Solution:** Make sure you're logged in before adding to cart

### Issue: "Checkout button not working"
**Solution:** Make sure you've entered all required shipping fields

### Issue: "Orders failing with 422 error"
**Solution:** 
1. Check that backend is running with latest code
2. Make sure all shipping address fields are filled
3. Try with Cash on Delivery payment method

---

## ✨ Tips

1. **Hard Refresh**: If UI seems stuck, press `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)

2. **Check Console**: Open browser DevTools (F12) to see any errors

3. **Check Backend Logs**: Your terminal where `python main.py` is running shows all API requests

4. **Test Both Users**: Try customer and admin workflows

5. **Use Swagger**: Test API directly at http://localhost:9000/docs for advanced features

---

## 🎉 Ready to Test!

**Your end-to-end flow is fully functional:**
- ✅ Login/Register
- ✅ Browse Products  
- ✅ View Details
- ✅ Add to Cart
- ✅ View Cart
- ✅ Checkout
- ✅ Order Success

**Go ahead and test it!** 🚀

