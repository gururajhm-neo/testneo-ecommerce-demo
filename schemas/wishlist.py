from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class WishlistItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID")

class WishlistItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    added_at: datetime
    product: Optional[Dict[str, Any]] = None  # Product details
    
    class Config:
        from_attributes = True
