"""
Review Model for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Index, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    
    # Review content
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String(200), nullable=True)
    comment = Column(Text, nullable=True)
    
    # Review status
    is_verified_purchase = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    is_helpful = Column(Boolean, default=False)
    
    # Review metadata
    helpful_votes = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_review_product_rating', 'product_id', 'rating'),
        Index('idx_review_user_product', 'user_id', 'product_id'),
        Index('idx_review_approved', 'is_approved', 'product_id'),
    )
    
    def __init__(self, user_id: int, product_id: int, rating: int, title: str = None, comment: str = None):
        """Initialize review"""
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.title = title
        self.comment = comment
    
    def approve(self):
        """Approve the review"""
        self.is_approved = True
        self.approved_at = datetime.utcnow()
    
    def reject(self):
        """Reject the review"""
        self.is_approved = False
        self.approved_at = None
    
    def mark_helpful(self):
        """Mark review as helpful"""
        self.helpful_votes += 1
        self.total_votes += 1
        self.is_helpful = self.helpful_votes > self.total_votes / 2
    
    def mark_not_helpful(self):
        """Mark review as not helpful"""
        self.total_votes += 1
        self.is_helpful = self.helpful_votes > self.total_votes / 2
    
    def to_dict(self) -> dict:
        """Convert review to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "title": self.title,
            "comment": self.comment,
            "is_verified_purchase": self.is_verified_purchase,
            "is_approved": self.is_approved,
            "is_helpful": self.is_helpful,
            "helpful_votes": self.helpful_votes,
            "total_votes": self.total_votes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None
        }
    
    def __repr__(self):
        return f"<Review(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, rating={self.rating})>"
