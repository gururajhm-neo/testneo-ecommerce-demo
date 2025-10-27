"""
Order and OrderItem Models for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON, Float, Text, Index, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database import Base
import enum
import uuid

class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    RETURNED = "returned"
    FAILED = "failed"

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    CRYPTO = "crypto"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    DECLINED = "declined"

class ShippingMethod(enum.Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    SAME_DAY = "same_day"
    PICKUP = "pickup"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Order details
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    total_amount = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    shipping_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    handling_fee = Column(Float, default=0.0)
    
    # Payment information
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    payment_details = Column(JSON, nullable=True)  # Store payment-specific data
    payment_transaction_id = Column(String(100), nullable=True)
    payment_gateway = Column(String(50), nullable=True)
    
    # Shipping information
    shipping_method = Column(Enum(ShippingMethod), default=ShippingMethod.STANDARD)
    shipping_address = Column(JSON, nullable=False)
    billing_address = Column(JSON, nullable=False)
    tracking_number = Column(String(100), nullable=True, index=True)
    tracking_url = Column(String(255), nullable=True)
    estimated_delivery = Column(DateTime, nullable=True)
    actual_delivery = Column(DateTime, nullable=True)
    
    # Customer information
    customer_notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    coupons = relationship("OrderCoupon", back_populates="order", cascade="all, delete-orphan")
    refunds = relationship("Refund", back_populates="order", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_order_user_status', 'user_id', 'status'),
        Index('idx_order_payment_status', 'payment_status'),
        Index('idx_order_created_date', 'created_at'),
        Index('idx_order_tracking', 'tracking_number'),
    )
    
    def __init__(self, user_id: int, payment_method: PaymentMethod, 
                 shipping_address: dict, billing_address: dict):
        """Initialize order with required fields"""
        self.user_id = user_id
        self.payment_method = payment_method
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.order_number = self.generate_order_number()
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number"""
        return f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    def calculate_totals(self):
        """Calculate order totals"""
        self.subtotal = sum(item.total_price for item in self.order_items)
        self.tax_amount = self.subtotal * 0.10  # 10% tax rate
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_amount - self.discount_amount + self.handling_fee
    
    def add_item(self, product_id: int, quantity: int, unit_price: float):
        """Add item to order"""
        total_price = unit_price * quantity
        order_item = OrderItem(
            order_id=self.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )
        self.order_items.append(order_item)
        self.calculate_totals()
    
    def update_status(self, new_status: OrderStatus):
        """Update order status with timestamp"""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        # Set specific timestamps based on status
        if new_status == OrderStatus.CONFIRMED:
            self.confirmed_at = datetime.utcnow()
        elif new_status == OrderStatus.PROCESSING:
            self.processed_at = datetime.utcnow()
        elif new_status == OrderStatus.SHIPPED:
            self.shipped_at = datetime.utcnow()
        elif new_status == OrderStatus.DELIVERED:
            self.delivered_at = datetime.utcnow()
            self.actual_delivery = datetime.utcnow()
        elif new_status == OrderStatus.CANCELLED:
            self.cancelled_at = datetime.utcnow()
    
    def can_cancel(self) -> bool:
        """Check if order can be cancelled"""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def can_refund(self) -> bool:
        """Check if order can be refunded"""
        return self.status in [OrderStatus.DELIVERED, OrderStatus.SHIPPED] and self.payment_status == PaymentStatus.COMPLETED
    
    def get_shipping_address_string(self) -> str:
        """Get formatted shipping address string"""
        addr = self.shipping_address
        return f"{addr.get('street', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('postal_code', '')}"
    
    def to_dict(self) -> dict:
        """Convert order to dictionary"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "user_id": self.user_id,
            "status": self.status.value,
            "total_amount": self.total_amount,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "shipping_amount": self.shipping_amount,
            "discount_amount": self.discount_amount,
            "handling_fee": self.handling_fee,
            "payment_method": self.payment_method.value,
            "payment_status": self.payment_status.value,
            "payment_transaction_id": self.payment_transaction_id,
            "payment_gateway": self.payment_gateway,
            "shipping_method": self.shipping_method.value,
            "shipping_address": self.shipping_address,
            "billing_address": self.billing_address,
            "tracking_number": self.tracking_number,
            "tracking_url": self.tracking_url,
            "estimated_delivery": self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            "actual_delivery": self.actual_delivery.isoformat() if self.actual_delivery else None,
            "customer_notes": self.customer_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "shipped_at": self.shipped_at.isoformat() if self.shipped_at else None,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
            "order_items": [item.to_dict() for item in self.order_items]
        }
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status.value}')>"

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Additional item details
    product_name = Column(String(200), nullable=True)  # Snapshot of product name
    product_sku = Column(String(100), nullable=True)   # Snapshot of product SKU
    product_image = Column(String(255), nullable=True) # Snapshot of product image
    
    # Item-specific options
    selected_options = Column(JSON, nullable=True)  # {"color": "red", "size": "L"}
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
    def __init__(self, order_id: int, product_id: int, quantity: int, unit_price: float):
        """Initialize order item"""
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = quantity * unit_price
    
    def to_dict(self) -> dict:
        """Convert order item to dictionary"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "product_name": self.product_name,
            "product_sku": self.product_sku,
            "product_image": self.product_image,
            "selected_options": self.selected_options,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
