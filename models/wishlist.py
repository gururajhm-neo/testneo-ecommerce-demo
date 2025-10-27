"""
Wishlist Item Model for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, DateTime, Index, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    
    # Timestamps
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_wishlist_user_product', 'user_id', 'product_id'),
    )
    
    def __init__(self, user_id: int, product_id: int):
        """Initialize wishlist item"""
        self.user_id = user_id
        self.product_id = product_id
    
    def to_dict(self) -> dict:
        """Convert wishlist item to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "added_at": self.added_at.isoformat() if self.added_at else None
        }
    
    def __repr__(self):
        return f"<WishlistItem(id={self.id}, user_id={self.user_id}, product_id={self.product_id})>"
