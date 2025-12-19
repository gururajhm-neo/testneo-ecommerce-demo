"""
E-commerce Testing API - Main Application
Industry-best-practice internal testing product for comprehensive API testing
"""
from fastapi import FastAPI, Depends, HTTPException, status, Query, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import uuid
import json
import secrets
import traceback

# Import database and models
from database import get_db, init_db
from models import *
from config import settings

# Import schemas
from schemas import *

# Import enums from models
from models.order import PaymentMethod, PaymentStatus, ShippingMethod, OrderStatus

# Import services
from services.auth_service import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    await create_sample_data()
    yield
    # Shutdown
    pass

# Create FastAPI app
app = FastAPI(
    title="E-commerce Testing API",
    description="""
    **Industry-best-practice internal testing product** for comprehensive API testing.
    
    This API provides a complete e-commerce system with complex business rules, 
    validation scenarios, and edge cases for thorough testing of your TestNeo platform.
    
    ## Features
    - **User Management**: Registration, authentication, role-based access
    - **Product Catalog**: Categories, inventory, pricing, reviews
    - **Shopping Cart**: Add/remove items, quantity management
    - **Order Processing**: Complex order flow with payment methods
    - **Coupons & Discounts**: Various discount types and validation rules
    - **Reviews & Ratings**: Product reviews with moderation
    - **Wishlist**: Save products for later
    - **Refunds**: Complete refund workflow
    - **Admin Panel**: Order management, product management
    - **Business Rules**: Complex validation and cross-field dependencies
    
    ## Testing Scenarios
    - **oneOf/anyOf**: Payment methods, order statuses
    - **Enums**: Product categories, user roles, payment statuses
    - **Nested Objects**: Addresses, payment details, order items
    - **Arrays**: Product images, tags, order items
    - **Validation Rules**: Cross-field validation, business logic
    - **Role-based Permissions**: Admin vs customer APIs
    - **State Management**: Order status transitions, inventory updates
    
    ## Business Rules
    - Complex validation scenarios
    - Cross-field dependencies
    - State-based business logic
    - Inventory management
    - Coupon validation
    - Payment processing
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware - must be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Global exception handler to ensure CORS headers are always included
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler that ensures CORS headers are included"""
    # Get origin from request
    origin = request.headers.get("origin")
    
    # Check if origin is allowed
    if origin and origin in settings.cors_origins:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    else:
        headers = {}
    
    # Handle HTTPException
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=headers
        )
    
    # Handle validation errors
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
            headers=headers
        )
    
    # Handle other exceptions
    print(f"Unhandled exception: {exc}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers=headers
    )

# Security
security = HTTPBearer()

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to E-commerce Testing API",
        "version": "1.0.0",
        "description": "Industry-best-practice internal testing product for comprehensive API testing",
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.utcnow().isoformat(),
        "features": [
            "User Management with JWT Authentication",
            "Product Catalog with Categories and Inventory",
            "Shopping Cart Management",
            "Order Processing with Multiple Payment Methods",
            "Coupons and Discounts with Complex Validation",
            "Reviews and Ratings System",
            "Wishlist Functionality",
            "Refund Management",
            "Admin Panel with Role-based Access",
            "Comprehensive Business Rules and Validation"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "E-commerce Testing API",
        "version": "1.0.0",
        "database": "SQLite",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "running"
    }

# API Information endpoint
@app.get("/api/info")
async def api_info():
    """Get comprehensive API information for testing"""
    return {
        "api_name": "E-commerce Testing API",
        "version": "1.0.0",
        "description": "Industry-best-practice internal testing product",
        "endpoints": {
            "authentication": [
                "POST /auth/register - User registration",
                "POST /auth/login - User login",
                "POST /auth/refresh - Refresh token",
                "POST /auth/logout - User logout"
            ],
            "users": [
                "GET /users/me - Get current user",
                "PUT /users/me - Update user profile",
                "GET /users/{user_id} - Get user by ID (admin)",
                "GET /users - List users (admin)"
            ],
            "products": [
                "GET /products - List products with filters",
                "GET /products/{product_id} - Get product details",
                "POST /products - Create product (admin)",
                "PUT /products/{product_id} - Update product (admin)",
                "DELETE /products/{product_id} - Delete product (admin)"
            ],
            "cart": [
                "GET /cart - Get user's cart",
                "POST /cart - Add item to cart",
                "PUT /cart/{item_id} - Update cart item",
                "DELETE /cart/{item_id} - Remove from cart",
                "DELETE /cart - Clear cart"
            ],
            "orders": [
                "POST /orders - Create order",
                "GET /orders - Get user's orders",
                "GET /orders/{order_id} - Get order details",
                "PUT /orders/{order_id} - Update order (admin)",
                "DELETE /orders/{order_id} - Cancel order"
            ],
            "reviews": [
                "POST /reviews - Create product review",
                "GET /reviews/{product_id} - Get product reviews",
                "PUT /reviews/{review_id} - Update review",
                "DELETE /reviews/{review_id} - Delete review"
            ],
            "coupons": [
                "POST /coupons - Create coupon (admin)",
                "GET /coupons - List coupons (admin)",
                "GET /coupons/{code} - Validate coupon",
                "PUT /coupons/{coupon_id} - Update coupon (admin)"
            ],
            "wishlist": [
                "GET /wishlist - Get user's wishlist",
                "POST /wishlist - Add to wishlist",
                "DELETE /wishlist/{item_id} - Remove from wishlist"
            ],
            "refunds": [
                "POST /refunds - Request refund",
                "GET /refunds - Get user's refunds",
                "PUT /refunds/{refund_id} - Update refund (admin)"
            ],
            "admin": [
                "GET /admin/orders - All orders (admin)",
                "GET /admin/reviews - All reviews (admin)",
                "PUT /admin/reviews/{review_id}/approve - Approve review (admin)",
                "GET /admin/stats - E-commerce statistics (admin)"
            ]
        },
        "business_rules": [
            "User registration requires unique email and username",
            "Password must be at least 8 characters",
            "Product SKU must be unique",
            "Order total must be within limits",
            "Coupon validation with complex rules",
            "Inventory management with reservations",
            "Payment method validation",
            "Cross-field validation scenarios",
            "Role-based access control",
            "State-based business logic"
        ],
        "testing_scenarios": [
            "Happy path testing",
            "Error handling and validation",
            "Edge cases and boundary conditions",
            "Performance testing with large datasets",
            "Security testing (authentication, authorization)",
            "Business rule validation",
            "Data integrity testing",
            "API versioning scenarios",
            "Rate limiting and throttling",
            "Integration testing scenarios"
        ]
    }

# Sample data creation
async def create_sample_data():
    """Create comprehensive sample data for testing"""
    from database import SessionLocal
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    db = SessionLocal()
    try:
        # Check if data already exists
        user_count = db.query(User).count()
        if user_count > 0:
            print("Sample data already exists, skipping creation")
            return
        
        print("Creating comprehensive sample data...")
        
        # Create admin user
        admin_user = User(
            email="admin@ecommerce.com",
            username="admin",
            password="admin123",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN
        )
        admin_user.is_active = True
        admin_user.is_verified = True
        admin_user.is_email_verified = True
        db.add(admin_user)
        
        # Create test customer
        customer = User(
            email="customer@test.com",
            username="customer",
            password="customer123",
            first_name="John",
            last_name="Doe",
            role=UserRole.CUSTOMER
        )
        customer.is_active = True
        customer.is_verified = True
        customer.is_email_verified = True
        db.add(customer)
        
        # Create moderator
        moderator = User(
            email="moderator@ecommerce.com",
            username="moderator",
            password="moderator123",
            first_name="Moderator",
            last_name="User",
            role=UserRole.MODERATOR
        )
        moderator.is_active = True
        moderator.is_verified = True
        moderator.is_email_verified = True
        db.add(moderator)
        
        db.commit()
        
        # Create sample products
        products = [
            Product(
                name="iPhone 15 Pro Max",
                description="Latest iPhone with advanced features and titanium design",
                price=1199.99,
                sale_price=1099.99,
                cost_price=800.00,
                category=ProductCategory.ELECTRONICS,
                sku="IPHONE-15-PRO-MAX",
                barcode="1234567890123",
                brand="Apple",
                manufacturer="Apple Inc.",
                stock_quantity=50,
                min_stock_level=10,
                is_featured=True,
                is_bestseller=True,
                weight=0.221,
                dimensions={"length": 15.9, "width": 7.7, "height": 0.8},
                color="Natural Titanium",
                material="Titanium",
                images=[
                    "https://example.com/iphone15pro1.jpg",
                    "https://example.com/iphone15pro2.jpg",
                    "https://example.com/iphone15pro3.jpg"
                ],
                thumbnail="https://example.com/iphone15pro_thumb.jpg",
                tags=["smartphone", "apple", "5g", "camera", "premium"],
                keywords=["iphone", "smartphone", "apple", "mobile"],
                warranty_period=365,
                return_period=30
            ),
            Product(
                name="Nike Air Max 270",
                description="Comfortable running shoes with Air Max technology for maximum cushioning",
                price=129.99,
                sale_price=99.99,
                cost_price=60.00,
                category=ProductCategory.SPORTS,
                sku="NIKE-AIR-MAX-270",
                barcode="9876543210987",
                brand="Nike",
                manufacturer="Nike Inc.",
                stock_quantity=100,
                min_stock_level=20,
                is_featured=True,
                weight=0.8,
                dimensions={"length": 30, "width": 12, "height": 8},
                color="Black/White",
                size="10",
                material="Mesh and synthetic",
                images=["https://example.com/nike2701.jpg", "https://example.com/nike2702.jpg"],
                thumbnail="https://example.com/nike270_thumb.jpg",
                tags=["running", "shoes", "comfortable", "athletic"],
                keywords=["nike", "running", "shoes", "athletic"],
                warranty_period=90,
                return_period=30
            ),
            Product(
                name="The Great Gatsby",
                description="Classic American novel by F. Scott Fitzgerald about the Jazz Age",
                price=12.99,
                cost_price=5.00,
                category=ProductCategory.BOOKS,
                sku="BOOK-GATSBY",
                barcode="4567891234567",
                brand="Scribner",
                manufacturer="Simon & Schuster",
                stock_quantity=200,
                min_stock_level=50,
                is_bestseller=True,
                weight=0.3,
                dimensions={"length": 20, "width": 13, "height": 2},
                color="Black",
                material="Paper",
                images=["https://example.com/gatsby1.jpg"],
                thumbnail="https://example.com/gatsby_thumb.jpg",
                tags=["classic", "fiction", "literature", "american"],
                keywords=["gatsby", "classic", "fiction", "literature"],
                warranty_period=None,
                return_period=30
            ),
            Product(
                name="Samsung 4K Smart TV",
                description="55-inch 4K Ultra HD Smart TV with HDR and built-in streaming apps",
                price=699.99,
                cost_price=450.00,
                category=ProductCategory.ELECTRONICS,
                sku="SAMSUNG-TV-55-4K",
                barcode="7891234567890",
                brand="Samsung",
                manufacturer="Samsung Electronics",
                stock_quantity=25,
                min_stock_level=5,
                is_featured=True,
                weight=15.5,
                dimensions={"length": 123, "width": 70, "height": 5},
                color="Black",
                material="Plastic and metal",
                images=["https://example.com/samsungtv1.jpg", "https://example.com/samsungtv2.jpg"],
                thumbnail="https://example.com/samsungtv_thumb.jpg",
                tags=["tv", "4k", "smart", "hdr", "entertainment"],
                keywords=["samsung", "tv", "4k", "smart", "television"],
                warranty_period=730,
                return_period=30
            ),
            Product(
                name="Levi's 501 Original Jeans",
                description="Classic straight fit jeans with button fly and timeless style",
                price=59.99,
                sale_price=49.99,
                cost_price=25.00,
                category=ProductCategory.CLOTHING,
                sku="LEVIS-501-ORIGINAL",
                barcode="3216549873210",
                brand="Levi's",
                manufacturer="Levi Strauss & Co.",
                stock_quantity=150,
                min_stock_level=30,
                is_bestseller=True,
                weight=0.5,
                dimensions={"length": 80, "width": 30, "height": 2},
                color="Blue",
                size="32x32",
                material="Denim",
                images=["https://example.com/levis5011.jpg", "https://example.com/levis5012.jpg"],
                thumbnail="https://example.com/levis501_thumb.jpg",
                tags=["jeans", "denim", "classic", "casual"],
                keywords=["levis", "jeans", "denim", "casual"],
                warranty_period=None,
                return_period=30
            )
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        
        # Create sample coupons
        coupons = [
            Coupon(
                code="WELCOME10",
                name="Welcome Discount",
                description="10% off your first order",
                discount_type="percentage",
                discount_value=10.0,
                minimum_order_amount=50.0,
                max_uses=100,
                max_uses_per_user=1,
                valid_from=datetime.utcnow(),
                valid_until=datetime.utcnow() + timedelta(days=365),
                is_active=True
            ),
            Coupon(
                code="FREESHIP",
                name="Free Shipping",
                description="Free shipping on orders over $100",
                discount_type="free_shipping",
                discount_value=5.0,
                minimum_order_amount=100.0,
                max_uses=50,
                max_uses_per_user=1,
                valid_from=datetime.utcnow(),
                valid_until=datetime.utcnow() + timedelta(days=30),
                is_active=True
            ),
            Coupon(
                code="SAVE20",
                name="20% Off Electronics",
                description="20% off all electronics",
                discount_type="percentage",
                discount_value=20.0,
                minimum_order_amount=100.0,
                maximum_discount=200.0,
                applicable_categories=["electronics"],
                max_uses=25,
                max_uses_per_user=2,
                valid_from=datetime.utcnow(),
                valid_until=datetime.utcnow() + timedelta(days=60),
                is_active=True
            )
        ]
        
        for coupon in coupons:
            db.add(coupon)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = register_user(db, user_data)
        # Convert User model to UserResponse
        return UserResponse(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            role=db_user.role,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            is_email_verified=db_user.is_email_verified,
            created_at=db_user.created_at,
            last_login=db_user.last_login
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT tokens"""
    try:
        return login_user(db, user_data)
    except HTTPException:
        # Re-raise HTTP exceptions (401, etc.)
        raise
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_trace = traceback.format_exc()
        print(f"Login endpoint error: {str(e)}")
        print(f"Traceback: {error_trace}")
        # Print to stderr as well for better visibility
        import sys
        sys.stderr.write(f"Login endpoint error: {str(e)}\n")
        sys.stderr.write(f"Traceback: {error_trace}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value},
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.get("/users/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user

@app.put("/users/me", response_model=UserProfile)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """List all users (admin only)"""
    # Use raw SQL to avoid enum conversion issues
    from sqlalchemy import text
    query = text("""
        SELECT id, email, username, first_name, last_name, phone, is_active, 
               is_verified, role, created_at, updated_at
        FROM users
        LIMIT :limit OFFSET :skip
    """)
    result = db.execute(query, {"limit": limit, "skip": skip})
    users = []
    for row in result:
        role = row.role.lower() if row.role else 'customer'  # Convert to lowercase for API
        users.append({
            'id': row.id,
            'email': row.email,
            'username': row.username,
            'first_name': row.first_name,
            'last_name': row.last_name,
            'phone': row.phone,
            'is_active': bool(row.is_active),
            'is_verified': bool(row.is_verified),
            'is_email_verified': False,  # Default value
            'role': role,
            'created_at': row.created_at,
            'updated_at': row.updated_at,
            'last_login': None,  # Default value
        })
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user by ID (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields (exclude password_hash and other sensitive fields)
    allowed_fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'is_verified']
    
    for field, value in user_update.items():
        if field in allowed_fields and hasattr(user, field):
            # Convert role to uppercase if it's a role field
            if field == 'role' and isinstance(value, str):
                value = value.upper()
            setattr(user, field, value)
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user.to_dict()

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# ============================================================================
# PRODUCT ENDPOINTS
# ============================================================================

@app.get("/products", response_model=ProductList)
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[ProductCategory] = Query(None),
    brand: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    search: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    on_sale: Optional[bool] = Query(None),
    in_stock: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """List products with filtering and pagination"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if category:
        query = query.filter(Product.category == category)
    if brand:
        query = query.filter(Product.brand == brand)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if search:
        query = query.filter(
            Product.name.contains(search) | 
            Product.description.contains(search) |
            Product.brand.contains(search)
        )
    if featured is not None:
        query = query.filter(Product.is_featured == featured)
    if on_sale is not None:
        query = query.filter(Product.is_on_sale == on_sale)
    if in_stock is not None:
        if in_stock:
            query = query.filter(Product.stock_quantity > 0)
        else:
            query = query.filter(Product.stock_quantity == 0)
    
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    
    return ProductList(
        products=products,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=(total + limit - 1) // limit
    )

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new product (admin only)"""
    # Check if SKU already exists
    if db.query(Product).filter(Product.sku == product_data.sku).first():
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update product (admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for field, value in product_data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete product (admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# ============================================================================
# CART ENDPOINTS
# ============================================================================

@app.get("/cart", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's cart"""
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    
    # Convert cart items to response format with product details
    cart_items_data = []
    total_amount = 0
    
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            price = product.sale_price if product.sale_price else product.price
            total_amount += price * item.quantity
            
            # Create cart item with product dict
            item_data = {
                "id": item.id,
                "user_id": item.user_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "selected_options": item.selected_options,
                "added_at": item.added_at,
                "updated_at": item.updated_at,
                "product": product.to_dict() if hasattr(product, 'to_dict') else None
            }
            cart_items_data.append(item_data)
    
    return CartResponse(
        items=cart_items_data,
        total_items=len(cart_items_data),
        total_amount=total_amount,
        item_count=len(cart_items_data)
    )

@app.post("/cart", response_model=CartItemResponse, status_code=201)
async def add_to_cart(
    cart_item: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Check if product exists and is active
    product = db.query(Product).filter(Product.id == cart_item.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check stock availability
    if product.stock_quantity < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Check if item already in cart
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == cart_item.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += cart_item.quantity
        existing_item.selected_options = cart_item.selected_options
        db.commit()
        db.refresh(existing_item)
        
        # Create response with product info
        result = CartItemResponse(
            id=existing_item.id,
            user_id=existing_item.user_id,
            product_id=existing_item.product_id,
            quantity=existing_item.quantity,
            selected_options=existing_item.selected_options,
            added_at=existing_item.added_at,
            updated_at=existing_item.updated_at,
            product=product.to_dict() if hasattr(product, 'to_dict') else None
        )
        return result
    else:
        # Create new cart item
        db_cart_item = CartItem(
            user_id=current_user.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            selected_options=cart_item.selected_options
        )
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)
        
        # Create response with product info
        result = CartItemResponse(
            id=db_cart_item.id,
            user_id=db_cart_item.user_id,
            product_id=db_cart_item.product_id,
            quantity=db_cart_item.quantity,
            selected_options=db_cart_item.selected_options,
            added_at=db_cart_item.added_at,
            updated_at=db_cart_item.updated_at,
            product=product.to_dict() if hasattr(product, 'to_dict') else None
        )
        return result

@app.put("/cart/{item_id}", response_model=CartItemResponse)
async def update_cart_item(
    item_id: int,
    cart_item_update: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update cart item"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Check stock availability
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if product and product.stock_quantity < cart_item_update.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    cart_item.quantity = cart_item_update.quantity
    cart_item.selected_options = cart_item_update.selected_options
    db.commit()
    db.refresh(cart_item)
    return cart_item

@app.delete("/cart/{item_id}")
async def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@app.delete("/cart")
async def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear user's cart"""
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Cart cleared"}

# ============================================================================
# ORDER ENDPOINTS
# ============================================================================

@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new order"""
    # Validate cart items
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate totals
    subtotal = 0
    order_items = []
    
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or not product.is_active:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not available")
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        
        price = product.sale_price if product.sale_price else product.price
        total_price = price * item.quantity
        subtotal += total_price
        
        order_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": price,
            "total_price": total_price,
            "product_name": product.name,
            "product_sku": product.sku,
            "product_image": product.thumbnail,
            "selected_options": item.selected_options
        })
    
    # Apply coupon if provided
    discount_amount = 0
    if order_data.coupon_code:
        coupon = db.query(Coupon).filter(
            Coupon.code == order_data.coupon_code,
            Coupon.is_active == True
        ).first()
        
        if coupon and coupon.valid_from <= datetime.utcnow() <= coupon.valid_until:
            if coupon.discount_type == "percentage":
                discount_amount = subtotal * (coupon.discount_value / 100)
                if coupon.maximum_discount:
                    discount_amount = min(discount_amount, coupon.maximum_discount)
            elif coupon.discount_type == "fixed":
                discount_amount = coupon.discount_value
            elif coupon.discount_type == "free_shipping":
                discount_amount = settings.standard_shipping_cost
    
    # Calculate shipping
    shipping_amount = 0
    if subtotal < settings.free_shipping_threshold:
        if order_data.shipping_method == "express":
            shipping_amount = settings.express_shipping_cost
        else:
            shipping_amount = settings.standard_shipping_cost
    
    # Calculate tax
    tax_amount = (subtotal - discount_amount) * settings.tax_rate
    
    # Calculate total
    total_amount = subtotal - discount_amount + shipping_amount + tax_amount
    
    # Validate order amount limits
    if total_amount < settings.min_order_amount:
        raise HTTPException(status_code=400, detail=f"Order minimum is ${settings.min_order_amount}")
    if total_amount > settings.max_order_amount:
        raise HTTPException(status_code=400, detail=f"Order maximum is ${settings.max_order_amount}")
    
    # Convert string enums to enum instances
    payment_method_enum = PaymentMethod[order_data.payment_method.upper().replace('-', '_')]
    shipping_method_enum = ShippingMethod[order_data.shipping_method.upper().replace('-', '_')]
    
    # Create order
    db_order = Order(
        user_id=current_user.id,
        payment_method=payment_method_enum,
        shipping_address=order_data.shipping_address,
        billing_address=order_data.billing_address or order_data.shipping_address
    )
    
    # Set additional order details
    db_order.subtotal = subtotal
    db_order.tax_amount = tax_amount
    db_order.shipping_amount = shipping_amount
    db_order.discount_amount = discount_amount
    db_order.total_amount = total_amount
    db_order.shipping_method = shipping_method_enum
    db_order.customer_notes = order_data.customer_notes
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item_data in order_items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        
        # Set additional fields
        db_order_item.product_name = item_data["product_name"]
        db_order_item.product_sku = item_data["product_sku"]
        db_order_item.product_image = item_data.get("product_image")
        db_order_item.selected_options = item_data.get("selected_options")
        
        db.add(db_order_item)
        
        # Update product stock
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock_quantity -= item_data["quantity"]
        product.reserved_quantity += item_data["quantity"]
    
    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    
    db.commit()
    db.refresh(db_order)
    
    return db_order

@app.get("/orders", response_model=List[OrderResponse])
async def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[OrderStatus] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's orders"""
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get order details"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@app.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update order (admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Handle status update - convert string to enum if needed
    if 'status' in order_update:
        status_value = order_update['status']
        if isinstance(status_value, str):
            try:
                order_update['status'] = OrderStatus[status_value]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status_value}")
    
    for field, value in order_update.items():
        if hasattr(order, field):
            setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order

@app.delete("/admin/orders/{order_id}")
async def admin_cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Cancel order (admin only - can cancel any order)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Order is already cancelled")
    
    order.status = OrderStatus.CANCELLED
    order.cancelled_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Order cancelled successfully"}

@app.delete("/orders/{order_id}")
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")
    
    order.status = OrderStatus.CANCELLED
    order.cancelled_at = datetime.utcnow()
    
    # Restore product stock
    for item in order.order_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity += item.quantity
            product.reserved_quantity -= item.quantity
    
    db.commit()
    return {"message": "Order cancelled successfully"}

# ============================================================================
# REVIEW ENDPOINTS
# ============================================================================

@app.post("/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a product review"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == review_data.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already reviewed this product
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.product_id == review_data.product_id
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
    
    # Check if user has purchased the product (for verified purchase)
    has_purchased = db.query(OrderItem).join(Order).filter(
        OrderItem.product_id == review_data.product_id,
        Order.user_id == current_user.id,
        Order.status == OrderStatus.DELIVERED
    ).first() is not None
    
    db_review = Review(
        user_id=current_user.id,
        product_id=review_data.product_id,
        rating=review_data.rating,
        title=review_data.title,
        comment=review_data.comment,
        is_verified_purchase=has_purchased
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # Update product rating
    product_reviews = db.query(Review).filter(
        Review.product_id == review_data.product_id,
        Review.is_approved == True
    ).all()
    
    if product_reviews:
        total_rating = sum(r.rating for r in product_reviews)
        product.average_rating = total_rating / len(product_reviews)
        product.total_reviews = len(product_reviews)
        product.total_ratings = total_rating
        db.commit()
    
    return db_review

@app.get("/reviews/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get product reviews"""
    reviews = db.query(Review).filter(
        Review.product_id == product_id,
        Review.is_approved == True
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews

@app.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update review"""
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == current_user.id
    ).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    for field, value in review_update.dict(exclude_unset=True).items():
        setattr(review, field, value)
    
    db.commit()
    db.refresh(review)
    return review

@app.delete("/admin/reviews/{review_id}")
async def admin_delete_review(
    review_id: int,
    current_user: User = Depends(get_current_moderator_user),
    db: Session = Depends(get_db)
):
    """Delete review (admin/moderator only)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}

@app.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete review"""
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == current_user.id
    ).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}

# ============================================================================
# COUPON ENDPOINTS
# ============================================================================

@app.post("/coupons", response_model=CouponResponse, status_code=201)
async def create_coupon(
    coupon_data: CouponCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new coupon (admin only)"""
    # Check if coupon code already exists
    if db.query(Coupon).filter(Coupon.code == coupon_data.code).first():
        raise HTTPException(status_code=400, detail="Coupon code already exists")
    
    db_coupon = Coupon(**coupon_data.dict())
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

@app.get("/coupons", response_model=List[CouponResponse])
async def list_coupons(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """List all coupons (admin only)"""
    coupons = db.query(Coupon).offset(skip).limit(limit).all()
    return coupons

@app.get("/coupons/{code}")
async def validate_coupon(
    code: str,
    order_amount: float = Query(..., gt=0),
    user_id: Optional[int] = Query(None),
    product_ids: Optional[List[int]] = Query(None),
    item_count: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """Validate coupon code"""
    coupon = db.query(Coupon).filter(
        Coupon.code == code,
        Coupon.is_active == True
    ).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    # Check validity period
    now = datetime.utcnow()
    if now < coupon.valid_from or now > coupon.valid_until:
        raise HTTPException(status_code=400, detail="Coupon is not valid")
    
    # Check minimum order amount
    if order_amount < coupon.minimum_order_amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Minimum order amount is ${coupon.minimum_order_amount}"
        )
    
    # Check item count
    if item_count < coupon.minimum_items:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum {coupon.minimum_items} items required"
        )
    
    if coupon.maximum_items and item_count > coupon.maximum_items:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {coupon.maximum_items} items allowed"
        )
    
    # Check usage limits
    if coupon.max_uses and coupon.current_uses >= coupon.max_uses:
        raise HTTPException(status_code=400, detail="Coupon usage limit reached")
    
    if user_id:
        # Check user usage
        user_usage = db.query(OrderCoupon).join(Order).filter(
            OrderCoupon.coupon_id == coupon.id,
            Order.user_id == user_id
        ).count()
        
        if user_usage >= coupon.max_uses_per_user:
            raise HTTPException(status_code=400, detail="Coupon usage limit reached for user")
    
    # Calculate discount
    if coupon.discount_type == "percentage":
        discount_amount = order_amount * (coupon.discount_value / 100)
        if coupon.maximum_discount:
            discount_amount = min(discount_amount, coupon.maximum_discount)
    elif coupon.discount_type == "fixed":
        discount_amount = coupon.discount_value
    elif coupon.discount_type == "free_shipping":
        discount_amount = settings.standard_shipping_cost
    else:
        discount_amount = 0
    
    return {
        "coupon": coupon,
        "discount_amount": discount_amount,
        "is_valid": True
    }

@app.put("/coupons/{coupon_id}", response_model=CouponResponse)
async def update_coupon(
    coupon_id: int,
    coupon_update: CouponUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update coupon (admin only)"""
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    for field, value in coupon_update.dict(exclude_unset=True).items():
        setattr(coupon, field, value)
    
    db.commit()
    db.refresh(coupon)
    return coupon

# ============================================================================
# WISHLIST ENDPOINTS
# ============================================================================

@app.get("/wishlist", response_model=List[WishlistItemResponse])
async def get_wishlist(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's wishlist"""
    wishlist_items = db.query(WishlistItem).filter(WishlistItem.user_id == current_user.id).all()
    return wishlist_items

@app.post("/wishlist", response_model=WishlistItemResponse, status_code=201)
async def add_to_wishlist(
    wishlist_item: WishlistItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add item to wishlist"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == wishlist_item.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if already in wishlist
    existing_item = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.product_id == wishlist_item.product_id
    ).first()
    
    if existing_item:
        raise HTTPException(status_code=400, detail="Item already in wishlist")
    
    db_wishlist_item = WishlistItem(
        user_id=current_user.id,
        product_id=wishlist_item.product_id
    )
    
    db.add(db_wishlist_item)
    db.commit()
    db.refresh(db_wishlist_item)
    return db_wishlist_item

@app.delete("/wishlist/{item_id}")
async def remove_from_wishlist(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove item from wishlist"""
    wishlist_item = db.query(WishlistItem).filter(
        WishlistItem.id == item_id,
        WishlistItem.user_id == current_user.id
    ).first()
    
    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    
    db.delete(wishlist_item)
    db.commit()
    return {"message": "Item removed from wishlist"}

# ============================================================================
# REFUND ENDPOINTS
# ============================================================================

@app.post("/refunds", response_model=RefundResponse, status_code=201)
async def create_refund(
    refund_data: RefundCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create refund request"""
    # Check if order exists and belongs to user
    order = db.query(Order).filter(
        Order.id == refund_data.order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status not in [OrderStatus.DELIVERED, OrderStatus.SHIPPED]:
        raise HTTPException(status_code=400, detail="Order not eligible for refund")
    
    # Check if refund amount is valid
    if refund_data.amount > order.total_amount:
        raise HTTPException(status_code=400, detail="Refund amount cannot exceed order total")
    
    db_refund = Refund(
        order_id=refund_data.order_id,
        user_id=current_user.id,
        amount=refund_data.amount,
        reason=refund_data.reason.value,
        description=refund_data.description,
        customer_contact=refund_data.customer_contact
    )
    
    db.add(db_refund)
    db.commit()
    db.refresh(db_refund)
    return db_refund

@app.get("/refunds", response_model=List[RefundResponse])
async def get_user_refunds(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's refunds"""
    refunds = db.query(Refund).filter(Refund.user_id == current_user.id).all()
    return refunds

@app.put("/refunds/{refund_id}", response_model=RefundResponse)
async def update_refund(
    refund_id: int,
    refund_update: RefundUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update refund (admin only)"""
    refund = db.query(Refund).filter(Refund.id == refund_id).first()
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    
    for field, value in refund_update.dict(exclude_unset=True).items():
        setattr(refund, field, value)
    
    if refund_update.status:
        refund.processed_by = current_user.id
        refund.processed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(refund)
    return refund

# ============================================================================
# INVENTORY MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/inventory", response_model=List[dict])
async def get_inventory(
    low_stock: Optional[bool] = Query(None),
    category: Optional[ProductCategory] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get inventory report (admin only)"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if low_stock:
        query = query.filter(Product.stock_quantity <= Product.min_stock_level)
    if category:
        query = query.filter(Product.category == category)
    
    products = query.offset(skip).limit(limit).all()
    
    inventory_report = []
    for product in products:
        inventory_report.append({
            "product_id": product.id,
            "name": product.name,
            "sku": product.sku,
            "category": product.category.value,
            "current_stock": product.stock_quantity,
            "reserved_stock": product.reserved_quantity,
            "available_stock": product.stock_quantity - product.reserved_quantity,
            "min_stock_level": product.min_stock_level,
            "is_low_stock": product.stock_quantity <= product.min_stock_level,
            "is_out_of_stock": product.stock_quantity == 0,
            "cost_price": product.cost_price,
            "selling_price": product.price,
            "inventory_value": product.stock_quantity * product.cost_price
        })
    
    return inventory_report

@app.put("/inventory/{product_id}/adjust")
async def adjust_inventory(
    product_id: int,
    adjustment_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Adjust product inventory (admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    adjustment_type = adjustment_data.get("type")  # "add", "subtract", "set"
    quantity = adjustment_data.get("quantity", 0)
    reason = adjustment_data.get("reason", "Manual adjustment")
    
    old_quantity = product.stock_quantity
    
    if adjustment_type == "add":
        product.stock_quantity += quantity
    elif adjustment_type == "subtract":
        product.stock_quantity = max(0, product.stock_quantity - quantity)
    elif adjustment_type == "set":
        product.stock_quantity = max(0, quantity)
    else:
        raise HTTPException(status_code=400, detail="Invalid adjustment type")
    
    db.commit()
    
    return {
        "product_id": product_id,
        "old_quantity": old_quantity,
        "new_quantity": product.stock_quantity,
        "adjustment": product.stock_quantity - old_quantity,
        "reason": reason,
        "adjusted_by": current_user.id,
        "adjusted_at": datetime.utcnow().isoformat()
    }

# ============================================================================
# BATCH OPERATIONS ENDPOINTS
# ============================================================================

@app.post("/products/batch")
async def batch_create_products(
    products_data: List[dict],
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Batch create products (admin only)"""
    created_products = []
    errors = []
    
    for i, product_data in enumerate(products_data):
        try:
            # Check if SKU already exists
            if db.query(Product).filter(Product.sku == product_data.get("sku")).first():
                errors.append({"index": i, "error": f"SKU {product_data.get('sku')} already exists"})
                continue
            
            db_product = Product(**product_data)
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            created_products.append(db_product.id)
            
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
            db.rollback()
    
    return {
        "created_count": len(created_products),
        "error_count": len(errors),
        "created_product_ids": created_products,
        "errors": errors
    }

@app.put("/products/batch")
async def batch_update_products(
    updates_data: List[dict],
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Batch update products (admin only)"""
    updated_products = []
    errors = []
    
    for i, update_data in enumerate(updates_data):
        try:
            product_id = update_data.get("id")
            if not product_id:
                errors.append({"index": i, "error": "Product ID required"})
                continue
            
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                errors.append({"index": i, "error": f"Product {product_id} not found"})
                continue
            
            for field, value in update_data.items():
                if field != "id" and hasattr(product, field):
                    setattr(product, field, value)
            
            db.commit()
            updated_products.append(product_id)
            
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
            db.rollback()
    
    return {
        "updated_count": len(updated_products),
        "error_count": len(errors),
        "updated_product_ids": updated_products,
        "errors": errors
    }

@app.delete("/products/batch")
async def batch_delete_products(
    product_ids: List[int],
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Batch delete products (admin only)"""
    deleted_count = 0
    errors = []
    
    for product_id in product_ids:
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                errors.append({"product_id": product_id, "error": "Product not found"})
                continue
            
            # Check if product has active orders
            active_orders = db.query(OrderItem).join(Order).filter(
                OrderItem.product_id == product_id,
                Order.status.in_([OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.PROCESSING])
            ).first()
            
            if active_orders:
                errors.append({"product_id": product_id, "error": "Product has active orders"})
                continue
            
            db.delete(product)
            deleted_count += 1
            
        except Exception as e:
            errors.append({"product_id": product_id, "error": str(e)})
    
    if deleted_count > 0:
        db.commit()
    
    return {
        "deleted_count": deleted_count,
        "error_count": len(errors),
        "errors": errors
    }

# ============================================================================
# ADVANCED SEARCH ENDPOINTS
# ============================================================================

@app.post("/search/products")
async def advanced_product_search(
    search_criteria: dict,
    db: Session = Depends(get_db)
):
    """Advanced product search with multiple criteria"""
    query = db.query(Product).filter(Product.is_active == True)
    
    # Text search
    if search_text := search_criteria.get("text"):
        query = query.filter(
            Product.name.contains(search_text) |
            Product.description.contains(search_text) |
            Product.brand.contains(search_text) |
            Product.sku.contains(search_text)
        )
    
    # Price range
    if price_range := search_criteria.get("price_range"):
        if min_price := price_range.get("min"):
            query = query.filter(Product.price >= min_price)
        if max_price := price_range.get("max"):
            query = query.filter(Product.price <= max_price)
    
    # Categories
    if categories := search_criteria.get("categories"):
        query = query.filter(Product.category.in_(categories))
    
    # Brands
    if brands := search_criteria.get("brands"):
        query = query.filter(Product.brand.in_(brands))
    
    # Stock status
    if stock_status := search_criteria.get("stock_status"):
        if stock_status == "in_stock":
            query = query.filter(Product.stock_quantity > 0)
        elif stock_status == "out_of_stock":
            query = query.filter(Product.stock_quantity == 0)
        elif stock_status == "low_stock":
            query = query.filter(Product.stock_quantity <= Product.min_stock_level)
    
    # Rating filter
    if min_rating := search_criteria.get("min_rating"):
        query = query.filter(Product.average_rating >= min_rating)
    
    # Tags
    if tags := search_criteria.get("tags"):
        for tag in tags:
            query = query.filter(Product.tags.contains([tag]))
    
    # Sorting
    sort_by = search_criteria.get("sort_by", "name")
    sort_order = search_criteria.get("sort_order", "asc")
    
    if hasattr(Product, sort_by):
        sort_column = getattr(Product, sort_by)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # Pagination
    skip = search_criteria.get("skip", 0)
    limit = search_criteria.get("limit", 20)
    
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    
    return {
        "products": products,
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit,
        "total_pages": (total + limit - 1) // limit,
        "search_criteria": search_criteria
    }

@app.get("/search/suggestions")
async def search_suggestions(
    q: str = Query(..., min_length=2),
    type: str = Query("all", regex="^(all|products|brands|categories)$"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get search suggestions"""
    suggestions = []
    
    if type in ["all", "products"]:
        # Product name suggestions
        products = db.query(Product.name).filter(
            Product.name.contains(q),
            Product.is_active == True
        ).limit(limit).all()
        suggestions.extend([{"type": "product", "value": p.name} for p in products])
    
    if type in ["all", "brands"]:
        # Brand suggestions
        brands = db.query(Product.brand).filter(
            Product.brand.contains(q),
            Product.is_active == True
        ).distinct().limit(limit).all()
        suggestions.extend([{"type": "brand", "value": b.brand} for b in brands])
    
    if type in ["all", "categories"]:
        # Category suggestions (enum values)
        category_matches = [
            {"type": "category", "value": cat.value}
            for cat in ProductCategory
            if q.lower() in cat.value.lower()
        ]
        suggestions.extend(category_matches[:limit])
    
    return {"suggestions": suggestions[:limit]}

# ============================================================================
# ANALYTICS AND REPORTING ENDPOINTS
# ============================================================================

@app.get("/analytics/sales")
async def sales_analytics(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    group_by: str = Query("day", regex="^(day|week|month|year)$"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get sales analytics (admin only)"""
    query = db.query(Order).filter(Order.status == OrderStatus.DELIVERED)
    
    # Date filtering
    if start_date:
        query = query.filter(Order.delivered_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Order.delivered_at <= datetime.fromisoformat(end_date))
    
    orders = query.all()
    
    # Group by time period
    sales_data = {}
    for order in orders:
        if not order.delivered_at:
            continue
            
        if group_by == "day":
            key = order.delivered_at.date().isoformat()
        elif group_by == "week":
            key = f"{order.delivered_at.year}-W{order.delivered_at.isocalendar()[1]}"
        elif group_by == "month":
            key = f"{order.delivered_at.year}-{order.delivered_at.month:02d}"
        else:  # year
            key = str(order.delivered_at.year)
        
        if key not in sales_data:
            sales_data[key] = {"revenue": 0, "orders": 0, "items": 0}
        
        sales_data[key]["revenue"] += order.total_amount
        sales_data[key]["orders"] += 1
        sales_data[key]["items"] += len(order.order_items)
    
    # Calculate totals
    total_revenue = sum(data["revenue"] for data in sales_data.values())
    total_orders = sum(data["orders"] for data in sales_data.values())
    total_items = sum(data["items"] for data in sales_data.values())
    
    return {
        "sales_data": sales_data,
        "summary": {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_items": total_items,
            "average_order_value": total_revenue / total_orders if total_orders > 0 else 0,
            "period": f"{start_date or 'all'} to {end_date or 'all'}",
            "group_by": group_by
        }
    }

@app.get("/analytics/products/top-selling")
async def top_selling_products(
    limit: int = Query(10, ge=1, le=100),
    period_days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get top selling products (admin only)"""
    cutoff_date = datetime.utcnow() - timedelta(days=period_days)
    
    # Query to get top selling products
    results = db.query(
        OrderItem.product_id,
        Product.name,
        Product.sku,
        db.func.sum(OrderItem.quantity).label('total_sold'),
        db.func.sum(OrderItem.total_price).label('total_revenue'),
        db.func.count(OrderItem.id).label('order_count')
    ).join(Product).join(Order).filter(
        Order.status == OrderStatus.DELIVERED,
        Order.delivered_at >= cutoff_date
    ).group_by(
        OrderItem.product_id, Product.name, Product.sku
    ).order_by(
        db.func.sum(OrderItem.quantity).desc()
    ).limit(limit).all()
    
    top_products = []
    for result in results:
        top_products.append({
            "product_id": result.product_id,
            "name": result.name,
            "sku": result.sku,
            "total_sold": result.total_sold,
            "total_revenue": float(result.total_revenue),
            "order_count": result.order_count,
            "average_price": float(result.total_revenue) / result.total_sold
        })
    
    return {
        "top_products": top_products,
        "period_days": period_days,
        "total_products": len(top_products)
    }

@app.get("/analytics/customers/insights")
async def customer_insights(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get customer insights and segmentation (admin only)"""
    # Customer value analysis
    customer_stats = db.query(
        Order.user_id,
        User.email,
        User.first_name,
        User.last_name,
        db.func.count(Order.id).label('total_orders'),
        db.func.sum(Order.total_amount).label('total_spent'),
        db.func.avg(Order.total_amount).label('avg_order_value'),
        db.func.max(Order.created_at).label('last_order_date')
    ).join(User).filter(
        Order.status == OrderStatus.DELIVERED
    ).group_by(
        Order.user_id, User.email, User.first_name, User.last_name
    ).all()
    
    # Segment customers
    high_value_customers = []
    repeat_customers = []
    new_customers = []
    
    for stat in customer_stats:
        customer_data = {
            "user_id": stat.user_id,
            "email": stat.email,
            "name": f"{stat.first_name} {stat.last_name}",
            "total_orders": stat.total_orders,
            "total_spent": float(stat.total_spent),
            "avg_order_value": float(stat.avg_order_value),
            "last_order_date": stat.last_order_date.isoformat()
        }
        
        if stat.total_spent > 1000:
            high_value_customers.append(customer_data)
        if stat.total_orders > 3:
            repeat_customers.append(customer_data)
        if stat.total_orders == 1:
            new_customers.append(customer_data)
    
    return {
        "high_value_customers": sorted(high_value_customers, key=lambda x: x["total_spent"], reverse=True)[:20],
        "repeat_customers": sorted(repeat_customers, key=lambda x: x["total_orders"], reverse=True)[:20],
        "new_customers": sorted(new_customers, key=lambda x: x["last_order_date"], reverse=True)[:20],
        "summary": {
            "total_customers": len(customer_stats),
            "high_value_count": len(high_value_customers),
            "repeat_customer_count": len(repeat_customers),
            "new_customer_count": len(new_customers)
        }
    }

# ============================================================================
# FILE UPLOAD ENDPOINTS
# ============================================================================

@app.post("/upload/product-images/{product_id}")
async def upload_product_images(
    product_id: int,
    files: List[bytes] = [],
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Upload product images (admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    uploaded_files = []
    errors = []
    
    for i, file_content in enumerate(files):
        try:
            # Simulate file upload (in real implementation, save to storage)
            file_id = str(uuid.uuid4())
            filename = f"product_{product_id}_{file_id}.jpg"
            file_url = f"https://storage.example.com/products/{filename}"
            
            uploaded_files.append({
                "filename": filename,
                "url": file_url,
                "size": len(file_content),
                "type": "image/jpeg"
            })
            
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
    
    # Update product images
    current_images = product.images or []
    new_urls = [f["url"] for f in uploaded_files]
    product.images = current_images + new_urls
    
    if not product.thumbnail and new_urls:
        product.thumbnail = new_urls[0]
    
    db.commit()
    
    return {
        "product_id": product_id,
        "uploaded_count": len(uploaded_files),
        "error_count": len(errors),
        "uploaded_files": uploaded_files,
        "errors": errors,
        "total_images": len(product.images)
    }

# ============================================================================
# COMPLEX VALIDATION ENDPOINTS
# ============================================================================

@app.post("/validate/order")
async def validate_order_complex(
    order_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Complex order validation with business rules"""
    validation_results = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "calculations": {}
    }
    
    # Validate customer eligibility
    if current_user.orders and len(current_user.orders) == 0:
        # First-time customer restrictions
        if order_data.get("total_amount", 0) > 500:
            validation_results["errors"].append("First-time customers limited to $500")
            validation_results["is_valid"] = False
    
    # Validate shipping address
    shipping_address = order_data.get("shipping_address", {})
    if not shipping_address.get("country"):
        validation_results["errors"].append("Shipping country required")
        validation_results["is_valid"] = False
    
    # International shipping restrictions
    if shipping_address.get("country") != "US":
        restricted_categories = [ProductCategory.ELECTRONICS.value]
        for item in order_data.get("items", []):
            product = db.query(Product).filter(Product.id == item.get("product_id")).first()
            if product and product.category.value in restricted_categories:
                validation_results["warnings"].append(f"International shipping restrictions for {product.name}")
    
    # Bulk order discounts
    total_items = sum(item.get("quantity", 0) for item in order_data.get("items", []))
    if total_items >= 10:
        validation_results["warnings"].append("Eligible for bulk discount")
        validation_results["calculations"]["bulk_discount_eligible"] = True
    
    # Payment method validation
    payment_method = order_data.get("payment_method")
    if payment_method == "bank_transfer" and order_data.get("total_amount", 0) < 100:
        validation_results["errors"].append("Bank transfer minimum $100")
        validation_results["is_valid"] = False
    
    # Stock availability with reservations
    for item in order_data.get("items", []):
        product = db.query(Product).filter(Product.id == item.get("product_id")).first()
        if product:
            available_stock = product.stock_quantity - product.reserved_quantity
            if available_stock < item.get("quantity", 0):
                validation_results["errors"].append(f"Insufficient stock for {product.name}")
                validation_results["is_valid"] = False
    
    return validation_results

# ============================================================================
# DISCOUNT AND PROMOTION ENDPOINTS
# ============================================================================

@app.post("/promotions")
async def create_promotion(
    promotion_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create complex promotion with multiple conditions (admin only)"""
    # Complex promotion validation
    promotion_type = promotion_data.get("type")  # "buy_x_get_y", "spend_amount_get_percent", "category_discount"
    conditions = promotion_data.get("conditions", {})
    
    if promotion_type == "buy_x_get_y":
        if not all(k in conditions for k in ["buy_quantity", "get_quantity", "product_ids"]):
            raise HTTPException(status_code=400, detail="Missing buy_x_get_y conditions")
    
    # Simulate promotion creation
    promotion_id = str(uuid.uuid4())
    
    return {
        "promotion_id": promotion_id,
        "type": promotion_type,
        "conditions": conditions,
        "created_at": datetime.utcnow().isoformat(),
        "status": "active"
    }

@app.post("/promotions/{promotion_id}/apply")
async def apply_promotion(
    promotion_id: str,
    cart_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Apply promotion to cart with complex calculations"""
    cart_items = cart_data.get("items", [])
    promotion_discount = 0
    applied_items = []
    
    # Simulate complex promotion logic
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.get("product_id")).first()
        if product:
            # Example: Category-based discount
            if product.category == ProductCategory.ELECTRONICS:
                discount = item.get("quantity", 0) * product.price * 0.15
                promotion_discount += discount
                applied_items.append({
                    "product_id": product.id,
                    "original_price": product.price,
                    "discount": discount,
                    "final_price": product.price - (discount / item.get("quantity", 1))
                })
    
    return {
        "promotion_id": promotion_id,
        "total_discount": promotion_discount,
        "applied_items": applied_items,
        "savings_percentage": (promotion_discount / sum(item.get("total", 0) for item in cart_items)) * 100 if cart_items else 0
    }

# ============================================================================
# NOTIFICATION AND COMMUNICATION ENDPOINTS
# ============================================================================

@app.post("/notifications/send")
async def send_notification(
    notification_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Send notifications to users (admin only)"""
    notification_type = notification_data.get("type")  # "email", "sms", "push"
    recipients = notification_data.get("recipients", [])
    message = notification_data.get("message", "")
    
    sent_notifications = []
    failed_notifications = []
    
    for recipient_id in recipients:
        user = db.query(User).filter(User.id == recipient_id).first()
        if user:
            # Simulate notification sending
            notification_id = str(uuid.uuid4())
            sent_notifications.append({
                "notification_id": notification_id,
                "recipient_id": recipient_id,
                "recipient_email": user.email,
                "type": notification_type,
                "status": "sent",
                "sent_at": datetime.utcnow().isoformat()
            })
        else:
            failed_notifications.append({
                "recipient_id": recipient_id,
                "error": "User not found"
            })
    
    return {
        "sent_count": len(sent_notifications),
        "failed_count": len(failed_notifications),
        "sent_notifications": sent_notifications,
        "failed_notifications": failed_notifications
    }

@app.get("/notifications/{user_id}")
async def get_user_notifications(
    user_id: int,
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Simulate notification retrieval
    notifications = [
        {
            "id": str(uuid.uuid4()),
            "type": "order_shipped",
            "title": "Your order has been shipped",
            "message": "Order #ORD-20250101-ABC123 has been shipped and is on its way",
            "is_read": False,
            "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "type": "promotion",
            "title": "Special discount available",
            "message": "Get 20% off on electronics this weekend",
            "is_read": True,
            "created_at": (datetime.utcnow() - timedelta(days=1)).isoformat()
        }
    ]
    
    if unread_only:
        notifications = [n for n in notifications if not n["is_read"]]
    
    return {"notifications": notifications, "total": len(notifications)}

# ============================================================================
# REPORTING AND EXPORT ENDPOINTS
# ============================================================================

@app.get("/reports/sales/export")
async def export_sales_report(
    format: str = Query("csv", regex="^(csv|excel|pdf)$"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Export sales report in various formats (admin only)"""
    # Simulate report generation
    orders = db.query(Order).filter(Order.status == OrderStatus.DELIVERED)
    
    if start_date:
        orders = orders.filter(Order.delivered_at >= datetime.fromisoformat(start_date))
    if end_date:
        orders = orders.filter(Order.delivered_at <= datetime.fromisoformat(end_date))
    
    order_data = orders.all()
    
    # Generate export data
    export_data = []
    for order in order_data:
        export_data.append({
            "order_id": order.id,
            "order_number": order.order_number,
            "customer_email": order.user.email,
            "total_amount": order.total_amount,
            "status": order.status.value,
            "created_at": order.created_at.isoformat(),
            "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None
        })
    
    # Simulate file generation
    file_id = str(uuid.uuid4())
    filename = f"sales_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{format}"
    
    return {
        "file_id": file_id,
        "filename": filename,
        "format": format,
        "download_url": f"/downloads/{file_id}",
        "record_count": len(export_data),
        "generated_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
    }

@app.get("/reports/inventory/low-stock")
async def low_stock_report(
    threshold_percentage: float = Query(20.0, ge=0, le=100),
    category: Optional[ProductCategory] = Query(None),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Generate low stock report with recommendations (admin only)"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.all()
    
    low_stock_items = []
    for product in products:
        stock_percentage = (product.stock_quantity / product.min_stock_level * 100) if product.min_stock_level > 0 else 100
        
        if stock_percentage <= threshold_percentage:
            # Calculate recommended reorder quantity
            avg_daily_sales = 2  # Simulate average daily sales
            lead_time_days = 7   # Simulate supplier lead time
            safety_stock = avg_daily_sales * 3  # 3 days safety stock
            
            reorder_point = (avg_daily_sales * lead_time_days) + safety_stock
            recommended_order = max(reorder_point - product.stock_quantity, product.min_stock_level)
            
            low_stock_items.append({
                "product_id": product.id,
                "name": product.name,
                "sku": product.sku,
                "category": product.category.value,
                "current_stock": product.stock_quantity,
                "min_stock_level": product.min_stock_level,
                "stock_percentage": round(stock_percentage, 2),
                "status": "critical" if stock_percentage <= 10 else "low",
                "recommended_reorder_quantity": recommended_order,
                "estimated_stockout_date": (datetime.utcnow() + timedelta(days=product.stock_quantity // max(avg_daily_sales, 1))).date().isoformat(),
                "supplier": product.manufacturer,
                "last_restock_date": (datetime.utcnow() - timedelta(days=30)).date().isoformat()  # Simulate
            })
    
    # Sort by urgency (lowest stock percentage first)
    low_stock_items.sort(key=lambda x: x["stock_percentage"])
    
    return {
        "low_stock_items": low_stock_items,
        "total_items": len(low_stock_items),
        "critical_items": len([item for item in low_stock_items if item["status"] == "critical"]),
        "threshold_percentage": threshold_percentage,
        "generated_at": datetime.utcnow().isoformat(),
        "recommendations": [
            "Consider setting up automatic reorder alerts",
            "Review supplier lead times for critical items",
            "Implement just-in-time inventory for fast-moving products"
        ]
    }

# ============================================================================
# INTEGRATION AND WEBHOOK ENDPOINTS
# ============================================================================

@app.post("/webhooks/payment")
async def payment_webhook(
    webhook_data: dict,
    webhook_signature: str = "",
    db: Session = Depends(get_db)
):
    """Handle payment provider webhooks"""
    event_type = webhook_data.get("event_type")
    payment_id = webhook_data.get("payment_id")
    order_id = webhook_data.get("order_id")
    
    # Simulate webhook signature validation
    if not webhook_signature:
        raise HTTPException(status_code=401, detail="Missing webhook signature")
    
    # Process different webhook events
    if event_type == "payment.succeeded":
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.payment_status = "paid"
            order.status = OrderStatus.CONFIRMED
            db.commit()
            
            return {"status": "processed", "action": "order_confirmed"}
    
    elif event_type == "payment.failed":
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.payment_status = "failed"
            order.status = OrderStatus.CANCELLED
            db.commit()
            
            return {"status": "processed", "action": "order_cancelled"}
    
    return {"status": "ignored", "event_type": event_type}

@app.post("/integrations/sync/products")
async def sync_products_from_external(
    sync_config: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Sync products from external system (admin only)"""
    external_system = sync_config.get("system")  # "shopify", "woocommerce", "magento"
    sync_mode = sync_config.get("mode", "incremental")  # "full", "incremental"
    
    # Simulate external system integration
    synced_products = []
    errors = []
    
    # Mock external product data
    external_products = [
        {
            "external_id": "ext_001",
            "name": "External Product 1",
            "price": 99.99,
            "sku": "EXT-001",
            "category": "electronics"
        },
        {
            "external_id": "ext_002",
            "name": "External Product 2",
            "price": 49.99,
            "sku": "EXT-002",
            "category": "clothing"
        }
    ]
    
    for ext_product in external_products:
        try:
            # Check if product already exists
            existing_product = db.query(Product).filter(Product.sku == ext_product["sku"]).first()
            
            if existing_product and sync_mode == "incremental":
                # Update existing product
                existing_product.price = ext_product["price"]
                existing_product.name = ext_product["name"]
                synced_products.append({"action": "updated", "product_id": existing_product.id, "sku": ext_product["sku"]})
            elif not existing_product:
                # Create new product
                new_product = Product(
                    name=ext_product["name"],
                    price=ext_product["price"],
                    sku=ext_product["sku"],
                    category=ProductCategory.ELECTRONICS if ext_product["category"] == "electronics" else ProductCategory.CLOTHING,
                    stock_quantity=100,  # Default stock
                    description=f"Product synced from {external_system}"
                )
                db.add(new_product)
                db.commit()
                db.refresh(new_product)
                synced_products.append({"action": "created", "product_id": new_product.id, "sku": ext_product["sku"]})
                
        except Exception as e:
            errors.append({"sku": ext_product["sku"], "error": str(e)})
    
    return {
        "sync_summary": {
            "total_processed": len(external_products),
            "successful": len(synced_products),
            "errors": len(errors)
        },
        "synced_products": synced_products,
        "errors": errors,
        "external_system": external_system,
        "sync_mode": sync_mode,
        "synced_at": datetime.utcnow().isoformat()
    }

# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@app.get("/admin/orders", response_model=List[OrderResponse])
async def admin_list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[OrderStatus] = Query(None),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """List all orders (admin only)"""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@app.get("/admin/reviews", response_model=List[ReviewResponse])
async def admin_list_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    approved: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_moderator_user),
    db: Session = Depends(get_db)
):
    """List all reviews (moderator/admin only)"""
    query = db.query(Review)
    
    if approved is not None:
        query = query.filter(Review.is_approved == approved)
    
    reviews = query.order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    # Add product information to each review
    from models.product import Product
    result = []
    for review in reviews:
        product = db.query(Product).filter(Product.id == review.product_id).first()
        review_dict = review.to_dict()
        if product:
            review_dict['product'] = product.to_dict()
            review_dict['product_name'] = product.name
        result.append(review_dict)
    
    return result

@app.put("/admin/reviews/{review_id}/approve")
async def approve_review(
    review_id: int,
    current_user: User = Depends(get_current_moderator_user),
    db: Session = Depends(get_db)
):
    """Approve review (moderator/admin only)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.is_approved = True
    review.approved_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Review approved successfully"}

@app.put("/admin/reviews/{review_id}/reject")
async def reject_review(
    review_id: int,
    current_user: User = Depends(get_current_moderator_user),
    db: Session = Depends(get_db)
):
    """Reject review (moderator/admin only)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.is_approved = False
    db.commit()
    
    return {"message": "Review rejected successfully"}

@app.get("/admin/stats")
async def admin_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive e-commerce statistics (admin only)"""
    # User statistics
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    new_users_today = db.query(User).filter(
        User.created_at >= datetime.utcnow().date()
    ).count()
    
    # Product statistics
    total_products = db.query(Product).count()
    active_products = db.query(Product).filter(Product.is_active == True).count()
    low_stock_products = db.query(Product).filter(
        Product.stock_quantity <= Product.min_stock_level
    ).count()
    out_of_stock_products = db.query(Product).filter(Product.stock_quantity == 0).count()
    
    # Order statistics
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == OrderStatus.PENDING).count()
    completed_orders = db.query(Order).filter(Order.status == OrderStatus.DELIVERED).count()
    cancelled_orders = db.query(Order).filter(Order.status == OrderStatus.CANCELLED).count()
    
    # Revenue statistics
    from sqlalchemy import func
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status == OrderStatus.DELIVERED
    ).scalar() or 0
    
    today_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status == OrderStatus.DELIVERED,
        Order.delivered_at >= datetime.utcnow().date()
    ).scalar() or 0
    
    # Review statistics
    total_reviews = db.query(Review).count()
    pending_reviews = db.query(Review).filter(Review.is_approved == False).count()
    approved_reviews = db.query(Review).filter(Review.is_approved == True).count()
    
    # Coupon statistics
    total_coupons = db.query(Coupon).count()
    active_coupons = db.query(Coupon).filter(Coupon.is_active == True).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "new_today": new_users_today
        },
        "products": {
            "total": total_products,
            "active": active_products,
            "low_stock": low_stock_products,
            "out_of_stock": out_of_stock_products
        },
        "orders": {
            "total": total_orders,
            "pending": pending_orders,
            "completed": completed_orders,
            "cancelled": cancelled_orders
        },
        "revenue": {
            "total": float(total_revenue),
            "today": float(today_revenue)
        },
        "reviews": {
            "total": total_reviews,
            "pending": pending_reviews,
            "approved": approved_reviews
        },
        "coupons": {
            "total": total_coupons,
            "active": active_coupons
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        log_level="info"
    )
