from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime

class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(1, gt=0, le=100, description="Quantity")
    selected_options: Optional[Dict[str, Any]] = Field(None, description="Selected options")
    
    @validator('quantity')
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        if v > 100:
            raise ValueError('Quantity cannot exceed 100')
        return v

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, le=100, description="Quantity")
    selected_options: Optional[Dict[str, Any]] = Field(None, description="Selected options")

class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    selected_options: Optional[Dict[str, Any]]
    added_at: datetime
    updated_at: datetime
    product: Optional[Dict[str, Any]] = None  # Product details
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_items: int
    total_amount: float
    item_count: int
