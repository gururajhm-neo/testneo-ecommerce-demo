"""
Refund Model for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Index, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class RefundStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSED = "processed"
    CANCELLED = "cancelled"

class RefundReason(enum.Enum):
    DEFECTIVE_PRODUCT = "defective_product"
    WRONG_ITEM = "wrong_item"
    DAMAGED_IN_TRANSIT = "damaged_in_transit"
    NOT_AS_DESCRIBED = "not_as_described"
    CUSTOMER_CHANGE_MIND = "customer_change_mind"
    DUPLICATE_ORDER = "duplicate_order"
    PRICING_ERROR = "pricing_error"
    OTHER = "other"

class Refund(Base):
    __tablename__ = "refunds"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Refund details
    amount = Column(Float, nullable=False)
    reason = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending", index=True)
    
    # Processing details
    processed_by = Column(Integer, nullable=True)  # Admin user ID
    processed_at = Column(DateTime, nullable=True)
    refund_method = Column(String(50), nullable=True)  # "original_payment", "store_credit"
    refund_transaction_id = Column(String(100), nullable=True)
    
    # Customer information
    customer_contact = Column(String(100), nullable=True)
    return_shipping_label = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="refunds")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_refund_status', 'status'),
        Index('idx_refund_user', 'user_id'),
        Index('idx_refund_created', 'created_at'),
    )
    
    def __init__(self, order_id: int, user_id: int, amount: float, reason: str, description: str = None):
        """Initialize refund"""
        self.order_id = order_id
        self.user_id = user_id
        self.amount = amount
        self.reason = reason
        self.description = description
    
    def approve(self, processed_by: int, refund_method: str = "original_payment"):
        """Approve the refund"""
        self.status = "approved"
        self.processed_by = processed_by
        self.refund_method = refund_method
        self.processed_at = datetime.utcnow()
    
    def reject(self, processed_by: int, reason: str = None):
        """Reject the refund"""
        self.status = "rejected"
        self.processed_by = processed_by
        self.processed_at = datetime.utcnow()
        if reason:
            self.description = f"Rejected: {reason}"
    
    def process(self, transaction_id: str):
        """Mark refund as processed"""
        self.status = "processed"
        self.refund_transaction_id = transaction_id
        self.processed_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert refund to dictionary"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "reason": self.reason,
            "description": self.description,
            "status": self.status,
            "processed_by": self.processed_by,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "refund_method": self.refund_method,
            "refund_transaction_id": self.refund_transaction_id,
            "customer_contact": self.customer_contact,
            "return_shipping_label": self.return_shipping_label,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Refund(id={self.id}, order_id={self.order_id}, amount={self.amount}, status='{self.status}')>"
