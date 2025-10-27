"""
Coupon and OrderCoupon Models for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Float, Text, Index, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database import Base
import enum

class DiscountType(enum.Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    FREE_SHIPPING = "free_shipping"

class Coupon(Base):
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Discount details
    discount_type = Column(String(20), nullable=False)  # "percentage", "fixed", "free_shipping"
    discount_value = Column(Float, nullable=False)
    minimum_order_amount = Column(Float, default=0.0)
    maximum_discount = Column(Float, nullable=True)
    
    # Usage limits
    max_uses = Column(Integer, nullable=True)
    current_uses = Column(Integer, default=0)
    max_uses_per_user = Column(Integer, default=1)
    max_uses_per_order = Column(Integer, default=1)
    
    # Validity
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    # Restrictions
    applicable_categories = Column(JSON, nullable=True)  # ["electronics", "clothing"]
    applicable_products = Column(JSON, nullable=True)    # [1, 2, 3] - product IDs
    excluded_products = Column(JSON, nullable=True)      # [4, 5, 6] - product IDs
    minimum_items = Column(Integer, default=1)
    maximum_items = Column(Integer, nullable=True)
    
    # Customer restrictions
    new_customers_only = Column(Boolean, default=False)
    existing_customers_only = Column(Boolean, default=False)
    customer_groups = Column(JSON, nullable=True)  # ["vip", "premium"]
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_coupons = relationship("OrderCoupon", back_populates="coupon", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_coupon_validity', 'is_active', 'valid_from', 'valid_until'),
        Index('idx_coupon_usage', 'current_uses', 'max_uses'),
    )
    
    def __init__(self, code: str, name: str, discount_type: str, discount_value: float,
                 valid_from: datetime, valid_until: datetime):
        """Initialize coupon"""
        self.code = code
        self.name = name
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.valid_from = valid_from
        self.valid_until = valid_until
    
    def is_valid(self, order_amount: float = 0, user_id: int = None, product_ids: list = None) -> tuple[bool, str]:
        """Check if coupon is valid for given conditions"""
        # Check if active
        if not self.is_active:
            return False, "Coupon is not active"
        
        # Check validity period
        now = datetime.utcnow()
        if now < self.valid_from or now > self.valid_until:
            return False, "Coupon is not valid at this time"
        
        # Check usage limits
        if self.max_uses and self.current_uses >= self.max_uses:
            return False, "Coupon usage limit reached"
        
        # Check minimum order amount
        if order_amount < self.minimum_order_amount:
            return False, f"Order must be at least ${self.minimum_order_amount}"
        
        # Check product restrictions
        if product_ids:
            if self.applicable_products and not any(pid in self.applicable_products for pid in product_ids):
                return False, "Coupon not applicable to selected products"
            
            if self.excluded_products and any(pid in self.excluded_products for pid in product_ids):
                return False, "Coupon not applicable to selected products"
        
        return True, "Coupon is valid"
    
    def calculate_discount(self, order_amount: float) -> float:
        """Calculate discount amount for given order amount"""
        if self.discount_type == "percentage":
            discount = order_amount * (self.discount_value / 100)
            if self.maximum_discount:
                discount = min(discount, self.maximum_discount)
            return discount
        elif self.discount_type == "fixed":
            return min(self.discount_value, order_amount)
        elif self.discount_type == "free_shipping":
            return 5.0  # Standard shipping cost
        return 0.0
    
    def increment_usage(self):
        """Increment usage count"""
        self.current_uses += 1
    
    def to_dict(self) -> dict:
        """Convert coupon to dictionary"""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "discount_type": self.discount_type,
            "discount_value": self.discount_value,
            "minimum_order_amount": self.minimum_order_amount,
            "maximum_discount": self.maximum_discount,
            "max_uses": self.max_uses,
            "current_uses": self.current_uses,
            "max_uses_per_user": self.max_uses_per_user,
            "valid_from": self.valid_from.isoformat() if self.valid_from else None,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "is_active": self.is_active,
            "applicable_categories": self.applicable_categories,
            "applicable_products": self.applicable_products,
            "excluded_products": self.excluded_products,
            "new_customers_only": self.new_customers_only,
            "existing_customers_only": self.existing_customers_only,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<Coupon(id={self.id}, code='{self.code}', discount_type='{self.discount_type}')>"

class OrderCoupon(Base):
    __tablename__ = "order_coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=False, index=True)
    discount_amount = Column(Float, nullable=False)
    
    # Timestamps
    applied_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="coupons")
    coupon = relationship("Coupon", back_populates="order_coupons")
    
    def __init__(self, order_id: int, coupon_id: int, discount_amount: float):
        """Initialize order coupon"""
        self.order_id = order_id
        self.coupon_id = coupon_id
        self.discount_amount = discount_amount
    
    def to_dict(self) -> dict:
        """Convert order coupon to dictionary"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "coupon_id": self.coupon_id,
            "discount_amount": self.discount_amount,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None
        }
    
    def __repr__(self):
        return f"<OrderCoupon(id={self.id}, order_id={self.order_id}, coupon_id={self.coupon_id})>"
