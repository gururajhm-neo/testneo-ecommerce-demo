from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime

class ReviewCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5)")
    title: Optional[str] = Field(None, max_length=200, description="Review title")
    comment: Optional[str] = Field(None, max_length=2000, description="Review comment")
    
    @validator('rating')
    def rating_range(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating (1-5)")
    title: Optional[str] = Field(None, max_length=200, description="Review title")
    comment: Optional[str] = Field(None, max_length=2000, description="Review comment")

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    title: Optional[str]
    comment: Optional[str]
    is_verified_purchase: bool
    is_approved: bool
    is_helpful: bool
    helpful_votes: int
    total_votes: int
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime]
    user: Optional[Dict[str, Any]] = None  # User details
    
    class Config:
        from_attributes = True
