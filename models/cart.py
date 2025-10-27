"""
Cart Item Model for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    quantity = Column(Integer, default=1)
    
    # Item-specific options
    selected_options = Column(JSON, nullable=True)  # {"color": "red", "size": "L"}
    
    # Timestamps
    added_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    
    def __init__(self, user_id: int, product_id: int, quantity: int = 1, selected_options: dict = None):
        """Initialize cart item"""
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.selected_options = selected_options
    
    def to_dict(self) -> dict:
        """Convert cart item to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "selected_options": self.selected_options,
            "added_at": self.added_at.isoformat() if self.added_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<CartItem(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"
