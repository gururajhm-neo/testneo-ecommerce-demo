"""
Product Model for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON, Float, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class ProductCategory(enum.Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME_GARDEN = "home_garden"
    SPORTS = "sports"
    BEAUTY = "beauty"
    TOYS = "toys"
    AUTOMOTIVE = "automotive"
    HEALTH = "health"
    FOOD = "food"
    JEWELRY = "jewelry"
    FURNITURE = "furniture"
    MUSIC = "music"
    MOVIES = "movies"
    GARDENING = "gardening"

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    
    # Pricing
    price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=True)
    cost_price = Column(Float, nullable=True)  # For profit calculation
    
    # Product identification
    sku = Column(String(100), unique=True, nullable=False, index=True)
    barcode = Column(String(100), nullable=True, index=True)
    upc = Column(String(50), nullable=True)  # Universal Product Code
    ean = Column(String(50), nullable=True)  # European Article Number
    
    # Categorization
    category = Column(String(50), nullable=False, index=True)  # Using String instead of Enum to avoid SQLAlchemy enum mismatch
    subcategory = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True, index=True)
    manufacturer = Column(String(100), nullable=True)
    
    # Inventory
    stock_quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)  # Items in carts/orders
    min_stock_level = Column(Integer, default=5)
    max_stock_level = Column(Integer, default=1000)
    
    # Status flags
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    is_bestseller = Column(Boolean, default=False)
    is_new_arrival = Column(Boolean, default=False)
    is_on_sale = Column(Boolean, default=False)
    
    # Physical attributes
    weight = Column(Float, nullable=True)  # in kg
    dimensions = Column(JSON, nullable=True)  # {"length": 10, "width": 5, "height": 2}
    color = Column(String(50), nullable=True)
    size = Column(String(50), nullable=True)
    material = Column(String(100), nullable=True)
    
    # Media
    images = Column(JSON, nullable=True)  # ["url1", "url2"]
    thumbnail = Column(String(255), nullable=True)
    video_url = Column(String(255), nullable=True)
    
    # SEO and marketing
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # ["tag1", "tag2"]
    keywords = Column(JSON, nullable=True)  # ["keyword1", "keyword2"]
    
    # Ratings and reviews
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    total_ratings = Column(Integer, default=0)
    
    # Shipping
    shipping_weight = Column(Float, nullable=True)
    requires_shipping = Column(Boolean, default=True)
    is_digital = Column(Boolean, default=False)
    download_url = Column(String(255), nullable=True)
    
    # Warranty and returns
    warranty_period = Column(Integer, nullable=True)  # in days
    return_period = Column(Integer, default=30)  # in days
    is_returnable = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="product", cascade="all, delete-orphan")
    inventory_transactions = relationship("InventoryTransaction", back_populates="product", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_product_category_brand', 'category', 'brand'),
        Index('idx_product_price_range', 'price'),
        Index('idx_product_stock_status', 'stock_quantity', 'is_active'),
        Index('idx_product_featured', 'is_featured', 'is_active'),
    )
    
    def __init__(self, name: str, price: float, category: ProductCategory, sku: str, 
                 description: str = None, brand: str = None):
        """Initialize product with required fields"""
        self.name = name
        self.price = price
        self.category = category
        self.sku = sku
        self.description = description
        self.brand = brand
        self.published_at = datetime.utcnow()
    
    @property
    def available_quantity(self) -> int:
        """Get available quantity (stock - reserved)"""
        return max(0, self.stock_quantity - self.reserved_quantity)
    
    @property
    def is_in_stock(self) -> bool:
        """Check if product is in stock"""
        return self.available_quantity > 0
    
    @property
    def is_low_stock(self) -> bool:
        """Check if product is low on stock"""
        return 0 < self.available_quantity <= self.min_stock_level
    
    @property
    def is_out_of_stock(self) -> bool:
        """Check if product is out of stock"""
        return self.available_quantity <= 0
    
    @property
    def current_price(self) -> float:
        """Get current price (sale price if available, otherwise regular price)"""
        return self.sale_price if self.sale_price else self.price
    
    @property
    def discount_percentage(self) -> float:
        """Calculate discount percentage"""
        if self.sale_price and self.price > 0:
            return ((self.price - self.sale_price) / self.price) * 100
        return 0.0
    
    @property
    def profit_margin(self) -> float:
        """Calculate profit margin"""
        if self.cost_price and self.current_price > 0:
            return ((self.current_price - self.cost_price) / self.current_price) * 100
        return 0.0
    
    def reserve_quantity(self, quantity: int) -> bool:
        """Reserve quantity for cart/order"""
        if self.available_quantity >= quantity:
            self.reserved_quantity += quantity
            return True
        return False
    
    def release_quantity(self, quantity: int):
        """Release reserved quantity"""
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
    
    def update_stock(self, quantity: int, transaction_type: str):
        """Update stock quantity"""
        if transaction_type == "in":
            self.stock_quantity += quantity
        elif transaction_type == "out":
            self.stock_quantity = max(0, self.stock_quantity - quantity)
        
        # Update on_sale flag
        self.is_on_sale = bool(self.sale_price and self.sale_price < self.price)
    
    def update_rating(self, new_rating: float):
        """Update product rating"""
        self.total_ratings += 1
        self.total_reviews += 1
        
        # Calculate new average rating
        total_rating_sum = (self.average_rating * (self.total_ratings - 1)) + new_rating
        self.average_rating = total_rating_sum / self.total_ratings
    
    def to_dict(self) -> dict:
        """Convert product to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "price": self.price,
            "sale_price": self.sale_price,
            "current_price": self.current_price,
            "discount_percentage": self.discount_percentage,
            "sku": self.sku,
            "barcode": self.barcode,
            "category": self.category.value,
            "subcategory": self.subcategory,
            "brand": self.brand,
            "manufacturer": self.manufacturer,
            "stock_quantity": self.stock_quantity,
            "available_quantity": self.available_quantity,
            "is_in_stock": self.is_in_stock,
            "is_low_stock": self.is_low_stock,
            "is_out_of_stock": self.is_out_of_stock,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "is_bestseller": self.is_bestseller,
            "is_new_arrival": self.is_new_arrival,
            "is_on_sale": self.is_on_sale,
            "weight": self.weight,
            "dimensions": self.dimensions,
            "color": self.color,
            "size": self.size,
            "material": self.material,
            "images": self.images,
            "thumbnail": self.thumbnail,
            "tags": self.tags,
            "average_rating": self.average_rating,
            "total_reviews": self.total_reviews,
            "requires_shipping": self.requires_shipping,
            "is_digital": self.is_digital,
            "warranty_period": self.warranty_period,
            "return_period": self.return_period,
            "is_returnable": self.is_returnable,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None
        }
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"
