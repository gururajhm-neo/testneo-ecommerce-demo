from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class CouponCreate(BaseModel):
    code: str = Field(..., min_length=3, max_length=50, description="Coupon code")
    name: str = Field(..., min_length=1, max_length=100, description="Coupon name")
    description: Optional[str] = Field(None, description="Coupon description")
    discount_type: str = Field(..., description="Discount type (percentage, fixed, free_shipping)")
    discount_value: float = Field(..., gt=0, description="Discount value")
    minimum_order_amount: float = Field(0.0, ge=0, description="Minimum order amount")
    maximum_discount: Optional[float] = Field(None, gt=0, description="Maximum discount amount")
    max_uses: Optional[int] = Field(None, gt=0, description="Maximum uses")
    max_uses_per_user: int = Field(1, gt=0, description="Maximum uses per user")
    max_uses_per_order: int = Field(1, gt=0, description="Maximum uses per order")
    valid_from: datetime = Field(..., description="Valid from date")
    valid_until: datetime = Field(..., description="Valid until date")
    applicable_categories: Optional[List[str]] = Field(None, description="Applicable categories")
    applicable_products: Optional[List[int]] = Field(None, description="Applicable product IDs")
    excluded_products: Optional[List[int]] = Field(None, description="Excluded product IDs")
    minimum_items: int = Field(1, gt=0, description="Minimum items required")
    maximum_items: Optional[int] = Field(None, gt=0, description="Maximum items allowed")
    new_customers_only: bool = Field(False, description="New customers only")
    existing_customers_only: bool = Field(False, description="Existing customers only")
    customer_groups: Optional[List[str]] = Field(None, description="Customer groups")
    
    @validator('valid_until')
    def valid_until_after_valid_from(cls, v, values):
        if 'valid_from' in values and v <= values['valid_from']:
            raise ValueError('Valid until must be after valid from')
        return v
    
    @validator('discount_type')
    def valid_discount_type(cls, v):
        valid_types = ['percentage', 'fixed', 'free_shipping']
        if v not in valid_types:
            raise ValueError(f'Discount type must be one of: {valid_types}')
        return v
    
    @validator('discount_value')
    def validate_discount_value(cls, v, values):
        if 'discount_type' in values:
            if values['discount_type'] == 'percentage' and v > 100:
                raise ValueError('Percentage discount cannot exceed 100%')
        return v

class CouponUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    discount_value: Optional[float] = Field(None, gt=0)
    minimum_order_amount: Optional[float] = Field(None, ge=0)
    maximum_discount: Optional[float] = Field(None, gt=0)
    max_uses: Optional[int] = Field(None, gt=0)
    max_uses_per_user: Optional[int] = Field(None, gt=0)
    max_uses_per_order: Optional[int] = Field(None, gt=0)
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: Optional[bool] = None
    applicable_categories: Optional[List[str]] = None
    applicable_products: Optional[List[int]] = None
    excluded_products: Optional[List[int]] = None
    minimum_items: Optional[int] = Field(None, gt=0)
    maximum_items: Optional[int] = Field(None, gt=0)
    new_customers_only: Optional[bool] = None
    existing_customers_only: Optional[bool] = None
    customer_groups: Optional[List[str]] = None

class CouponResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    discount_type: str
    discount_value: float
    minimum_order_amount: float
    maximum_discount: Optional[float]
    max_uses: Optional[int]
    current_uses: int
    max_uses_per_user: int
    max_uses_per_order: int
    valid_from: datetime
    valid_until: datetime
    is_active: bool
    applicable_categories: Optional[List[str]]
    applicable_products: Optional[List[int]]
    excluded_products: Optional[List[int]]
    minimum_items: int
    maximum_items: Optional[int]
    new_customers_only: bool
    existing_customers_only: bool
    customer_groups: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CouponValidation(BaseModel):
    code: str = Field(..., description="Coupon code to validate")
    order_amount: float = Field(..., gt=0, description="Order amount")
    user_id: Optional[int] = Field(None, description="User ID for validation")
    product_ids: Optional[List[int]] = Field(None, description="Product IDs in order")
    item_count: int = Field(..., gt=0, description="Number of items in order")
