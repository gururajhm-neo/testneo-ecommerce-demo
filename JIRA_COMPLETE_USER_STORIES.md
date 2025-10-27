# Complete JIRA User Stories - E-Commerce Testing Platform

**Epic**: E-Commerce Testing Platform Implementation  
**Total Stories**: 60+  
**Estimated Story Points**: 200+

---

## EPIC 1: Authentication & User Management (8 Stories)

### US-1: User Registration
**As a** new user  
**I want to** register an account with my email, username, and password  
**So that** I can access the platform and make purchases

**Acceptance Criteria**:
- User can register with unique email and username
- Password must be minimum 8 characters
- Email format validation
- Username uniqueness validation
- System returns user object with JWT tokens
- Email verification sent (simulated)
- Success message displayed

**Story Points**: 5

---

### US-2: User Login
**As a** registered user  
**I want to** login with my credentials  
**So that** I can access my account

**Acceptance Criteria**:
- User can login with email and password
- System validates credentials
- Returns JWT access token (30 min expiry)
- Returns JWT refresh token (7 days expiry)
- Stores tokens in localStorage
- Redirects based on user role
- Last login timestamp updated

**Story Points**: 3

---

### US-3: JWT Token Refresh
**As a** logged-in user  
**I want to** refresh my access token  
**So that** I stay authenticated without re-logging

**Acceptance Criteria**:
- System automatically refreshes token when expired
- Uses refresh token to get new access token
- Silent refresh in background
- User remains logged in seamlessly
- Refresh token rotation on each use

**Story Points**: 3

---

### US-4: Password Reset
**As a** user  
**I want to** reset my forgotten password  
**So that** I can regain account access

**Acceptance Criteria**:
- User can request password reset via email
- System generates secure reset token
- Token expires in 1 hour
- Email with reset link sent (simulated)
- User sets new password with token
- Old password invalidated

**Story Points**: 5

---

### US-5: View Profile
**As a** logged-in user  
**I want to** view my profile information  
**So that** I can see my account details

**Acceptance Criteria**:
- User can view email, username, name, role, join date
- View order history summary
- View wishlist count
- View review count
- Profile information displayed
- Success message handling

**Story Points**: 2

---

### US-6: Update Profile
**As a** user  
**I want to** update my profile information  
**So that** my account information is current

**Acceptance Criteria**:
- User can update first_name, last_name, phone
- Cannot change email or username
- Changes saved to database
- Success notification displayed
- Validation on all fields

**Story Points**: 3

---

### US-7: Change Password
**As a** user  
**I want to** change my password  
**So that** my account remains secure

**Acceptance Criteria**:
- User can change password
- Current password required
- New password validation (min 8 chars)
- Password confirmation match
- Old password invalidated
- Success message shown

**Story Points**: 3

---

### US-8: Logout
**As a** user  
**I want to** logout  
**So that** I can securely end my session

**Acceptance Criteria**:
- Logout button available
- Clears JWT tokens from localStorage
- Redirects to login page
- Session terminated on server
- Cart contents optionally saved

**Story Points**: 2

---

## EPIC 2: Product Catalog (12 Stories)

### US-9: Browse Products
**As a** customer  
**I want to** browse products by category  
**So that** I can discover products

**Acceptance Criteria**:
- Products displayed in grid/list view
- Show name, price, image, rating, stock
- Pagination support (10, 25, 50, 100 per page)
- Filter by category, price range, brand, rating
- Sort by price, name, rating, newest
- Lazy loading for images

**Story Points**: 5

---

### US-10: Search Products
**As a** customer  
**I want to** search for products  
**So that** I can quickly find specific items

**Acceptance Criteria**:
- Search bar on all pages
- Search by name, description, SKU, brand
- Real-time search suggestions
- Highlight search terms in results
- Results ranked by relevance
- Empty state if no results
- Clear search option

**Story Points**: 5

---

### US-11: Filter Products
**As a** customer  
**I want to** filter products  
**So that** I can narrow down my search

**Acceptance Criteria**:
- Filter by category
- Filter by price range
- Filter by brand
- Filter by rating
- Filter by stock availability
- Multiple filters combinable
- Clear filters button

**Story Points**: 3

---

### US-12: Sort Products
**As a** customer  
**I want to** sort products  
**So that** I can view them in my preferred order

**Acceptance Criteria**:
- Sort by price (low to high, high to low)
- Sort by name (A-Z, Z-A)
- Sort by newest first
- Sort by rating
- Sort by popularity
- Current sort option highlighted

**Story Points**: 2

---

### US-13: View Product Details
**As a** customer  
**I want to** view detailed product information  
**So that** I can make informed purchase decisions

**Acceptance Criteria**:
- Full product information displayed
- Multiple image gallery
- Price and sale price if discounted
- Stock availability status
- Description and specifications
- Reviews and ratings
- Add to cart button
- Add to wishlist button
- Similar products shown

**Story Points**: 8

---

### US-14: View Product Reviews
**As a** customer  
**I want to** view product reviews  
**So that** I can see what others think

**Acceptance Criteria**:
- Reviews displayed on product page
- Show reviewer name, rating, date, comment
- Filter by rating
- Sort by helpful, newest, highest rated
- Verified purchase badge
- Helpful vote count
- Pagination for reviews

**Story Points**: 5

---

### US-15: View Categories
**As a** customer  
**I want to** browse products by category  
**So that** I can find products in specific categories

**Acceptance Criteria**:
- List all categories
- Category images displayed
- Product count per category
- Featured categories highlighted
- Subcategory support
- Click to view category products

**Story Points**: 3

---

### US-16: View Featured Products
**As a** customer  
**I want to** see featured products  
**So that** I can discover popular items

**Acceptance Criteria**:
- Featured products section on homepage
- Products marked as featured displayed
- Visual indicator for featured status
- Click to view product details
- Grid layout with images

**Story Points**: 3

---

### US-17: View Bestsellers
**As a** customer  
**I want to** see bestseller products  
**So that** I can view top-selling items

**Acceptance Criteria**:
- Bestseller products section
- Products marked as bestseller displayed
- Sorted by sales volume
- Click to view product details
- Grid layout with images

**Story Points**: 3

---

### US-18: View Related Products
**As a** customer  
**I want to** see related products  
**So that** I can discover similar items

**Acceptance Criteria**:
- Show products from same category
- Show products from same brand
- Limit to 4-6 related products
- Display on product details page
- Click to view related product

**Story Points**: 5

---

### US-19: Product Comparison
**As a** customer  
**I want to** compare products side-by-side  
**So that** I can make better purchase decisions

**Acceptance Criteria**:
- Add products to comparison
- Maximum 4 products in comparison
- Side-by-side layout
- Compare key attributes
- Highlight differences
- Remove products from comparison

**Story Points**: 8

---

### US-20: Product Image Zoom
**As a** customer  
**I want to** zoom product images  
**So that** I can see product details clearly

**Acceptance Criteria**:
- Click to zoom image
- Hover to see larger preview
- Fullscreen image view
- Multiple images supported
- Previous/next navigation

**Story Points**: 5

---

## EPIC 3: Shopping Cart (8 Stories)

### US-21: Add to Cart
**As a** customer  
**I want to** add products to my shopping cart  
**So that** I can purchase multiple items together

**Acceptance Criteria**:
- Add product with quantity selection
- Validate stock availability
- Update cart total in real-time
- Show cart item count badge
- Cart persists across sessions
- Toast notification on success

**Story Points**: 5

---

### US-22: View Cart
**As a** customer  
**I want to** view my shopping cart  
**So that** I can review items before checkout

**Acceptance Criteria**:
- Display all cart items
- Show product image, name, price, quantity, subtotal
- Calculate subtotal, shipping, tax, total
- Display available coupons
- Continue shopping link
- Proceed to checkout button

**Story Points**: 3

---

### US-23: Update Cart Quantity
**As a** customer  
**I want to** modify item quantities in my cart  
**So that** I can adjust my order

**Acceptance Criteria**:
- Update item quantity controls
- Validate stock on quantity change
- Real-time price updates
- Success message shown
- Prevent negative quantities
- Cannot exceed stock availability

**Story Points**: 3

---

### US-24: Remove from Cart
**As a** customer  
**I want to** remove items from my cart  
**So that** I can manage my purchase list

**Acceptance Criteria**:
- Remove individual items
- Confirmation dialog
- Update cart total immediately
- Success notification
- Empty cart state handled

**Story Points**: 2

---

### US-25: Clear Cart
**As a** customer  
**I want to** clear my entire cart  
**So that** I can start fresh

**Acceptance Criteria**:
- Clear all items button
- Confirmation dialog
- Cart emptied
- Show empty cart message
- Success notification

**Story Points**: 2

---

### US-26: Cart Validation
**As a** customer  
**I want to** have my cart validated  
**So that** I can ensure items are still available

**Acceptance Criteria**:
- Check stock availability
- Remove out-of-stock items
- Update prices if changed
- Warn about limited stock
- Auto-update quantities

**Story Points**: 5

---

### US-27: Save Cart for Later
**As a** customer  
**I want to** save my cart for later  
**So that** I can complete purchase later

**Acceptance Criteria**:
- Save cart contents
- Retrieve saved cart
- 30-day retention period
- Notification on expired cart
- Continue shopping option

**Story Points**: 5

---

### US-28: Move to Wishlist
**As a** customer  
**I want to** move cart items to wishlist  
**So that** I can save them for later

**Acceptance Criteria**:
- Move item to wishlist from cart
- Confirmation message
- Item removed from cart
- Added to wishlist
- Quick access to wishlist

**Story Points**: 3

---

## EPIC 4: Coupons & Discounts (6 Stories)

### US-29: Apply Coupon
**As a** customer  
**I want to** apply discount coupons to my order  
**So that** I can save money

**Acceptance Criteria**:
- Enter coupon code
- Validate coupon eligibility
- Check order minimum amount
- Calculate discount amount
- Display discount in order summary
- Show final total with discount
- Error message for invalid/expired coupons

**Story Points**: 5

---

### US-30: Remove Coupon
**As a** customer  
**I want to** remove applied coupons  
**So that** I can change my discount

**Acceptance Criteria**:
- Remove button on applied coupon
- Recalculate totals
- Update order summary
- Success message
- Show original total

**Story Points**: 2

---

### US-31: View Available Coupons
**As a** customer  
**I want to** see available coupons  
**So that** I can use discount codes

**Acceptance Criteria**:
- List of available coupons
- Show coupon details (code, discount, expiry)
- Active coupons highlighted
- Discount amount displayed
- Terms and conditions shown
- Click to apply

**Story Points**: 3

---

### US-32: Coupon Eligibility Check
**As a** system  
**I want to** validate coupon eligibility  
**So that** I can apply discounts correctly

**Acceptance Criteria**:
- Check minimum order amount
- Check expiry date
- Check usage limits
- Check customer eligibility
- Check product restrictions
- Return clear error messages

**Story Points**: 5

---

### US-33: Multiple Coupon Types
**As a** system  
**I want to** support different discount types  
**So that** I can offer various promotions

**Acceptance Criteria**:
- Percentage discounts (e.g., 20% off)
- Fixed amount discounts (e.g., $50 off)
- Free shipping discounts
- Each type calculated correctly
- Display discount type clearly

**Story Points**: 5

---

### US-34: Coupon Usage Tracking
**As a** system  
**I want to** track coupon usage  
**So that** I can enforce limits

**Acceptance Criteria**:
- Increment usage count
- Track per-user usage
- Track total usage
- Enforce maximum limits
- Display usage statistics

**Story Points**: 3

---

## EPIC 5: Checkout & Orders (12 Stories)

### US-35: Review Order
**As a** customer  
**I want to** review my order before checkout  
**So that** I can verify all details

**Acceptance Criteria**:
- Review all cart items
- Verify quantities and prices
- Review applied coupons
- Check totals calculation
- Edit cart option available
- Proceed to checkout button

**Story Points**: 3

---

### US-36: Enter Shipping Address
**As a** customer  
**I want to** provide my shipping address  
**So that** my order can be delivered

**Acceptance Criteria**:
- Enter full name, address, city, state, postal code, country
- Save addresses for reuse
- Validate address format
- Select from saved addresses
- Same as billing checkbox

**Story Points**: 5

---

### US-37: Enter Billing Address
**As a** customer  
**I want to** provide my billing address  
**So that** my payment can be processed

**Acceptance Criteria**:
- Enter billing information
- Same as shipping option
- Validate billing address
- Save billing addresses
- Select from saved addresses

**Story Points**: 3

---

### US-38: Select Shipping Method
**As a** customer  
**I want to** choose shipping method  
**So that** I can select delivery speed

**Acceptance Criteria**:
- Display shipping options
- Show shipping costs and delivery times
- Standard shipping free over $50
- Express shipping option available
- Selected option highlighted

**Story Points**: 3

---

### US-39: Enter Payment Information
**As a** customer  
**I want to** enter payment details  
**So that** I can complete my purchase

**Acceptance Criteria**:
- Select payment method (Credit/Debit, PayPal, etc.)
- Enter card number, CVV, expiry
- Validate card format
- Show security badge
- Store payment method securely

**Story Points**: 5

---

### US-40: Place Order
**As a** customer  
**I want to** complete my purchase  
**So that** I receive the products

**Acceptance Criteria**:
- Validate all required information
- Check stock availability
- Validate coupon eligibility
- Process payment (simulated)
- Create order record
- Reserve inventory
- Send confirmation email (simulated)
- Redirect to order confirmation

**Story Points**: 8

---

### US-41: Order Confirmation
**As a** customer  
**I want to** see order confirmation  
**So that** I know my order was successful

**Acceptance Criteria**:
- Display order number
- Show order total
- List ordered items
- Show shipping address
- Estimated delivery date
- Continue shopping button

**Story Points**: 3

---

### US-42: View Order History
**As a** customer  
**I want to** view my order history  
**So that** I can track my purchases

**Acceptance Criteria**:
- List all user orders
- Display order number, date, total, status
- Sort by most recent first
- Filter by status
- Pagination support

**Story Points**: 3

---

### US-43: View Order Details
**As a** customer  
**I want to** view detailed order information  
**So that** I can see what I ordered

**Acceptance Criteria**:
- Show complete order information
- List all order items with quantities
- Display addresses
- Show payment method
- Display order timeline
- Show total breakdown

**Story Points**: 5

---

### US-44: Track Order Status
**As a** customer  
**I want to** track my order status  
**So that** I know when it will arrive

**Acceptance Criteria**:
- Display current order status
- Show status history
- Estimated delivery date
- Tracking number (if available)
- Order status timeline

**Story Points**: 5

---

### US-45: Cancel Order
**As a** customer  
**I want to** cancel my order  
**So that** I can avoid receiving unwanted items

**Acceptance Criteria**:
- Cancel button on pending orders
- Confirmation dialog
- Restore inventory
- Process refund
- Update order status
- Email notification (simulated)

**Story Points**: 5

---

### US-46: Download Invoice
**As a** customer  
**I want to** download order invoices  
**So that** I can keep records

**Acceptance Criteria**:
- Download button on order details
- Generate PDF invoice
- Include all order information
- Professional invoice format
- Download starts immediately

**Story Points**: 8

---

## EPIC 6: Reviews & Ratings (8 Stories)

### US-47: Write Product Review
**As a** customer  
**I want to** write reviews for products  
**So that** I can share my experience

**Acceptance Criteria**:
- Rate product 1-5 stars
- Write review title and comment
- Upload photos (optional)
- Mark as verified purchase if applicable
- Submit review
- Success message shown

**Story Points**: 5

---

### US-48: Edit Review
**As a** customer  
**I want to** edit my reviews  
**So that** I can update my feedback

**Acceptance Criteria**:
- Edit button on own reviews
- Update rating and comment
- Save changes
- Success notification
- Review updated immediately

**Story Points**: 3

---

### US-49: Delete Review
**As a** customer  
**I want to** delete my reviews  
**So that** I can remove my feedback

**Acceptance Criteria**:
- Delete button on own reviews
- Confirmation dialog
- Review removed
- Success message
- Cannot delete if approved by admin

**Story Points**: 2

---

### US-50: Vote Helpful
**As a** customer  
**I want to** mark reviews as helpful  
**So that** I can highlight useful feedback

**Acceptance Criteria**:
- Helpful button on reviews
- Increment helpful count
- Prevent duplicate votes
- Show total helpful votes
- Highlight most helpful reviews

**Story Points**: 3

---

### US-51: Filter Reviews by Rating
**As a** customer  
**I want to** filter reviews by rating  
**So that** I can see specific ratings

**Acceptance Criteria**:
- Filter by 5-star, 4-star, etc.
- Show filtered results
- Clear filter option
- Count per rating shown

**Story Points**: 3

---

### US-52: Sort Reviews
**As a** customer  
**I want to** sort reviews  
**So that** I can see most relevant first

**Acceptance Criteria**:
- Sort by most helpful
- Sort by newest
- Sort by highest rated
- Sort by lowest rated
- Current sort highlighted

**Story Points**: 2

---

### US-53: Report Inappropriate Review
**As a** customer  
**I want to** report inappropriate reviews  
**So that** I can maintain community quality

**Acceptance Criteria**:
- Report button on reviews
- Select reason for reporting
- Submit report
- Thank you message
- Admin notified

**Story Points**: 3

---

### US-54: View Verified Purchases Only
**As a** customer  
**I want to** filter verified purchase reviews  
**So that** I can see authentic feedback

**Acceptance Criteria**:
- Checkbox to show only verified purchases
- Filter reviews accordingly
- Clear visual indicator for verified
- Count of verified vs non-verified

**Story Points**: 3

---

## EPIC 7: Wishlist (5 Stories)

### US-55: Add to Wishlist
**As a** customer  
**I want to** add products to wishlist  
**So that** I can save them for later

**Acceptance Criteria**:
- Add to wishlist button on products
- Product saved to wishlist
- Success notification
- Wishlist count updated
- Remove from wishlist option

**Story Points**: 3

---

### US-56: View Wishlist
**As a** customer  
**I want to** view my wishlist  
**So that** I can see saved products

**Acceptance Criteria**:
- Display all wishlist items
- Show product details
- Remove from wishlist button
- Add to cart button
- Empty state if wishlist is empty

**Story Points**: 3

---

### US-57: Remove from Wishlist
**As a** customer  
**I want to** remove items from wishlist  
**So that** I can manage my saved items

**Acceptance Criteria**:
- Remove button on wishlist items
- Confirm removal
- Item removed immediately
- Success notification
- Wishlist updated

**Story Points**: 2

---

### US-58: Move Wishlist to Cart
**As a** customer  
**I want to** move wishlist items to cart  
**So that** I can purchase saved items

**Acceptance Criteria**:
- Add to cart button on wishlist items
- Check stock availability
- Add to cart
- Remove from wishlist
- Success notification

**Story Points**: 3

---

### US-59: Share Wishlist
**As a** customer  
**I want to** share my wishlist  
**So that** others can see my saved products

**Acceptance Criteria**:
- Share button
- Copy wishlist link
- Email wishlist
- Success notification
- Private wishlist option

**Story Points**: 5

---

## EPIC 8: Admin Dashboard (5 Stories)

### US-60: View Dashboard Statistics
**As an** admin  
**I want to** view key business metrics  
**So that** I understand business performance

**Acceptance Criteria**:
- Total revenue displayed
- Order count and trends
- User count
- Product count
- Recent activity feed
- Quick action buttons

**Story Points**: 8

---

### US-61: View Sales Analytics
**As an** admin  
**I want to** view sales analytics  
**So that** I can track business trends

**Acceptance Criteria**:
- Sales charts displayed
- Revenue by period (day/week/month)
- Product category breakdown
- Payment method distribution
- Growth trends
- Export analytics data

**Story Points**: 8

---

### US-62: View Inventory Alerts
**As an** admin  
**I want to** see inventory alerts  
**So that** I can manage stock levels

**Acceptance Criteria**:
- Low stock alerts (≤5 units)
- Out of stock products
- Alert count badge
- Click to view products
- Urgent alerts highlighted

**Story Points**: 5

---

### US-63: View Recent Orders
**As an** admin  
**I want to** see recent orders  
**So that** I can track latest activity

**Acceptance Criteria**:
- List of 10 most recent orders
- Order number, customer, date, amount, status
- Quick status update
- Click to view details
- Real-time updates

**Story Points**: 3

---

### US-64: Export Data
**As an** admin  
**I want to** export data  
**So that** I can analyze it externally

**Acceptance Criteria**:
- Export products to CSV
- Export orders to Excel
- Export users to CSV
- Schedule exports
- Download files

**Story Points**: 5

---

## EPIC 9: Admin Product Management (8 Stories)

### US-65: List Products (Admin)
**As an** admin  
**I want to** view all products  
**So that** I can manage the catalog

**Acceptance Criteria**:
- All products displayed in table
- Search, filter, sort functionality
- Pagination support
- Bulk selection
- Quick view option

**Story Points**: 5

---

### US-66: Add Product
**As an** admin  
**I want to** add new products  
**So that** I can expand catalog

**Acceptance Criteria**:
- Create product form
- Enter name, price, SKU, category, description
- Upload images
- Set stock levels
- Mark as featured/bestseller
- Validate all fields
- Success notification

**Story Points**: 8

---

### US-67: Edit Product
**As an** admin  
**I want to** edit existing products  
**So that** I can update product information

**Acceptance Criteria**:
- Edit product form pre-filled
- Update any product field
- Add/remove images
- Change stock quantity
- Update featured/bestseller flags
- Save changes

**Story Points**: 5

---

### US-68: Delete Product
**As an** admin  
**I want to** delete products  
**So that** I can remove outdated items

**Acceptance Criteria**:
- Delete button
- Confirmation dialog
- Check for active orders
- Soft delete (is_active=False)
- Bulk delete option
- Success message

**Story Points**: 3

---

### US-69: Manage Stock Levels
**As an** admin  
**I want to** manage product stock  
**So that** inventory is accurate

**Acceptance Criteria**:
- Update stock quantities
- Set min/max stock levels
- Receive low stock alerts
- Adjust inventory
- Track stock movements
- Bulk stock updates

**Story Points**: 5

---

### US-70: Bulk Product Operations
**As an** admin  
**I want to** perform bulk actions  
**So that** I can manage products efficiently

**Acceptance Criteria**:
- Select multiple products
- Bulk activate/deactivate
- Bulk category change
- Bulk price updates
- Bulk delete
- Confirmation dialog

**Story Points**: 8

---

### US-71: Upload Product Images
**As an** admin  
**I want to** upload product images  
**So that** products have visual representation

**Acceptance Criteria**:
- Upload multiple images
- Drag-and-drop support
- Image preview
- Delete images
- Set primary image
- Image optimization

**Story Points**: 8

---

### US-72: Set Featured Products
**As an** admin  
**I want to** mark products as featured  
**So that** they appear prominently

**Acceptance Criteria**:
- Toggle featured flag
- Bulk mark as featured
- Featured products displayed on homepage
- Visual indicator in admin panel

**Story Points**: 3

---

## EPIC 10: Admin Order Management (10 Stories)

### US-73: View All Orders
**As an** admin  
**I want to** view all orders  
**So that** I can fulfill them

**Acceptance Criteria**:
- All orders displayed
- Search, filter, sort
- Status color coding
- Pagination
- Export option

**Story Points**: 5

---

### US-74: Filter Orders by Status
**As an** admin  
**I want to** filter orders by status  
**So that** I can focus on specific orders

**Acceptance Criteria**:
- Filter by Pending, Processing, Shipped, etc.
- Quick filter buttons
- Multiple status selection
- Clear filter option

**Story Points**: 3

---

### US-75: Update Order Status
**As an** admin  
**I want to** update order status  
**So that** I can track fulfillment

**Acceptance Criteria**:
- Status dropdown per order
- Status transition validation
- Update timestamp
- Inventory adjusted on shipment
- Success notification

**Story Points**: 5

---

### US-76: View Order Details
**As an** admin  
**I want to** view complete order information  
**So that** I can fulfill accurately

**Acceptance Criteria**:
- Full order details modal
- Customer information
- Shipping and billing addresses
- Order items list
- Payment information
- Status history

**Story Points**: 5

---

### US-77: Cancel Order (Admin)
**As an** admin  
**I want to** cancel orders  
**So that** I can handle cancellations

**Acceptance Criteria**:
- Cancel button on orders
- Confirmation dialog
- Restore inventory
- Process refund (simulated)
- Update status to Cancelled

**Story Points**: 5

---

### US-78: Process Refunds
**As an** admin  
**I want to** process refunds  
**So that** I can handle returns

**Acceptance Criteria**:
- Refund button on orders
- Full or partial refund
- Refund reason
- Refund amount calculation
- Refund status tracking

**Story Points**: 8

---

### US-79: Export Orders
**As an** admin  
**I want to** export orders  
**So that** I can analyze sales data

**Acceptance Criteria**:
- Export to CSV/Excel
- Filter before export
- Include all order details
- Date range selection
- Download file

**Story Points**: 5

---

### US-80: Print Invoice
**As an** admin  
**I want to** print invoices  
**So that** I can provide to customers

**Acceptance Criteria**:
- Print invoice button
- Format for printing
- Include all details
- Professional layout
- PDF generation

**Story Points**: 5

---

### US-81: Order Search
**As an** admin  
**I want to** search orders  
**So that** I can find specific orders

**Acceptance Criteria**:
- Search by order number
- Search by customer email
- Search by customer name
- Real-time results
- Highlight search terms

**Story Points**: 3

---

### US-82: View Order Timeline
**As an** admin  
**I want to** see order timeline  
**So that** I can track order progress

**Acceptance Criteria**:
- Status history display
- Timeline visualization
- Timestamp for each status
- User who made change (if applicable)
- Complete order lifecycle

**Story Points**: 5

---

## EPIC 11: Admin User Management (8 Stories)

### US-83: List All Users
**As an** admin  
**I want to** view all users  
**So that** I can manage accounts

**Acceptance Criteria**:
- User table display
- Search, filter, sort
- Show email, name, role, status
- Pagination
- Quick actions

**Story Points**: 3

---

### US-84: Create User
**As an** admin  
**I want to** create user accounts  
**So that** I can add employees

**Acceptance Criteria**:
- Create user form
- Enter email, username, password
- Assign role
- Set active status
- Success notification

**Story Points**: 5

---

### US-85: Edit User
**As an** admin  
**I want to** edit user information  
**So that** I can update accounts

**Acceptance Criteria**:
- Edit user form
- Update name, role, status
- Cannot change email
- Cannot self-modify role
- Save changes

**Story Points**: 5

---

### US-86: Delete User
**As an** admin  
**I want to** delete user accounts  
**So that** I can remove inactive users

**Acceptance Criteria**:
- Delete button
- Confirmation dialog
- Check for orders
- Soft delete
- Success notification

**Story Points**: 3

---

### US-87: Manage User Roles
**As an** admin  
**I want to** assign user roles  
**So that** I can control access

**Acceptance Criteria**:
- Role dropdown
- Assign Customer, Admin, Moderator, Support
- Cannot change own role
- Success notification
- Immediate effect

**Story Points**: 5

---

### US-88: Activate/Deactivate Users
**As an** admin  
**I want to** control user access  
**So that** I can manage active accounts

**Acceptance Criteria**:
- Toggle active status
- Active users can login
- Inactive users blocked
- Bulk activation/deactivation
- Success notification

**Story Points**: 3

---

### US-89: View User Activity
**As an** admin  
**I want to** view user activity  
**So that** I can monitor accounts

**Acceptance Criteria**:
- Display last login
- View order history
- Review count
- Registration date
- Activity timeline

**Story Points**: 5

---

### US-90: Reset User Password (Admin)
**As an** admin  
**I want to** reset user passwords  
**So that** I can help users regain access

**Acceptance Criteria**:
- Reset password button
- Generate temporary password
- Email password (simulated)
- Force password change on login
- Success notification

**Story Points**: 5

---

## EPIC 12: Admin Review Management (5 Stories)

### US-91: View All Reviews
**As an** admin  
**I want to** view all reviews  
**So that** I can moderate content

**Acceptance Criteria**:
- Review list display
- Show product, user, rating, comment, status
- Filter by status
- Sort by date, rating
- Pagination

**Story Points**: 3

---

### US-92: Approve Reviews
**As an** admin  
**I want to** approve reviews  
**So that** they appear on products

**Acceptance Criteria**:
- Approve button per review
- Status updates to Approved
- Review appears on product page
- Success notification
- Bulk approve option

**Story Points**: 3

---

### US-93: Reject Reviews
**As an** admin  
**I want to** reject reviews  
**So that** inappropriate content is hidden

**Acceptance Criteria**:
- Reject button per review
- Optional rejection reason
- Status updates to Rejected
- Review hidden from customers
- Success notification

**Story Points**: 3

---

### US-94: Delete Reviews
**As an** admin  
**I want to** delete reviews  
**So that** I can remove inappropriate content

**Acceptance Criteria**:
- Delete button
- Confirmation dialog
- Review deleted permanently
- Product rating recalculated
- Success notification

**Story Points**: 3

---

### US-95: View Review Statistics
**As an** admin  
**I want to** see review statistics  
**So that** I can track content quality

**Acceptance Criteria**:
- Total review count
- Approved vs pending count
- Average rating
- Reviews by product
- Reviews by user

**Story Points**: 5

---

## EPIC 13: Admin Coupon Management (8 Stories)

### US-96: List Coupons
**As an** admin  
**I want to** view all coupons  
**So that** I can manage promotions

**Acceptance Criteria**:
- Coupon list display
- Show code, name, discount, usage, status
- Filter by active/inactive
- Sort by code, usage, expiry
- Search functionality

**Story Points**: 3

---

### US-97: Create Coupon
**As an** admin  
**I want to** create discount coupons  
**So that** I can offer promotions

**Acceptance Criteria**:
- Create coupon form
- Set code, name, discount type, value
- Set minimum order amount
- Set usage limits
- Set validity dates
- Success notification

**Story Points**: 5

---

### US-98: Edit Coupon
**As an** admin  
**I want to** edit existing coupons  
**So that** I can update promotion details

**Acceptance Criteria**:
- Edit coupon form pre-filled
- Update discount details
- Change validity dates
- Modify usage limits
- Save changes

**Story Points**: 5

---

### US-99: Delete Coupon
**As an** admin  
**I want to** delete coupons  
**So that** I can remove expired promotions

**Acceptance Criteria**:
- Delete button
- Confirmation dialog
- Coupon deleted
- Cannot be used after deletion
- Success notification

**Story Points**: 2

---

### US-100: Toggle Coupon Active Status
**As an** admin  
**I want to** enable/disable coupons  
**So that** I can control active promotions

**Acceptance Criteria**:
- Toggle active status
- Instant effect
- Inactive coupons cannot be used
- Visual indicator of status
- Success notification

**Story Points**: 2

---

### US-101: View Coupon Usage
**As an** admin  
**I want to** view coupon usage statistics  
**So that** I can track promotion effectiveness

**Acceptance Criteria**:
- Total uses displayed
- Uses by user
- Remaining uses
- Usage history
- Performance metrics

**Story Points**: 5

---

### US-102: Set Coupon Restrictions
**As an** admin  
**I want to** set coupon restrictions  
**So that** I can target specific promotions

**Acceptance Criteria**:
- Set product restrictions
- Set category restrictions
- Set customer type restrictions
- Set new customer only
- Set order minimum requirements

**Story Points**: 8

---

### US-103: Duplicate Coupon
**As an** admin  
**I want to** duplicate existing coupons  
**So that** I can create similar promotions quickly

**Acceptance Criteria**:
- Duplicate button
- Pre-filled form with original data
- Generate new unique code
- Edit before saving
- Success notification

**Story Points**: 3

---

## SUMMARY

**Total User Stories**: 103  
**Total Epic Groups**: 13  
**Estimated Total Story Points**: 300+

**Epic Breakdown**:
- Authentication & User Management: 8 stories
- Product Catalog: 12 stories
- Shopping Cart: 8 stories
- Coupons & Discounts: 6 stories
- Checkout & Orders: 12 stories
- Reviews & Ratings: 8 stories
- Wishlist: 5 stories
- Admin Dashboard: 5 stories
- Admin Product Management: 8 stories
- Admin Order Management: 10 stories
- Admin User Management: 8 stories
- Admin Review Management: 5 stories
- Admin Coupon Management: 8 stories

**All stories include**:
- Clear user perspective ("As a...")
- Business benefit ("I want to...")
- Value proposition ("So that...")
- Detailed acceptance criteria
- Estimated story points

---

**End of Complete JIRA User Stories**

