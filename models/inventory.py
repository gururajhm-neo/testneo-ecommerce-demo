"""
Inventory Transaction Model for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Index, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class TransactionType(enum.Enum):
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"
    RESERVED = "reserved"
    RELEASED = "released"
    DAMAGED = "damaged"
    RETURNED = "returned"

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    
    # Transaction details
    transaction_type = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    reference = Column(String(100), nullable=True)  # order_id, manual_adjustment, etc.
    reference_type = Column(String(50), nullable=True)  # "order", "manual", "return", etc.
    
    # Additional details
    notes = Column(Text, nullable=True)
    unit_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    
    # User who made the transaction
    created_by = Column(Integer, nullable=True)  # user_id
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_transactions")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_inventory_product_type', 'product_id', 'transaction_type'),
        Index('idx_inventory_reference', 'reference', 'reference_type'),
        Index('idx_inventory_created', 'created_at'),
    )
    
    def __init__(self, product_id: int, transaction_type: str, quantity: int, 
                 reference: str = None, reference_type: str = None, notes: str = None,
                 unit_cost: float = None, created_by: int = None):
        """Initialize inventory transaction"""
        self.product_id = product_id
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.reference = reference
        self.reference_type = reference_type
        self.notes = notes
        self.unit_cost = unit_cost
        self.created_by = created_by
        
        # Calculate total cost
        if unit_cost:
            self.total_cost = unit_cost * quantity
    
    def to_dict(self) -> dict:
        """Convert inventory transaction to dictionary"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "reference": self.reference,
            "reference_type": self.reference_type,
            "notes": self.notes,
            "unit_cost": self.unit_cost,
            "total_cost": self.total_cost,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<InventoryTransaction(id={self.id}, product_id={self.product_id}, type='{self.transaction_type}', quantity={self.quantity})>"
