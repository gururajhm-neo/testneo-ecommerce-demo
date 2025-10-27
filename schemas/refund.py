from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class RefundStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSED = "processed"
    CANCELLED = "cancelled"

class RefundReason(str, Enum):
    DEFECTIVE_PRODUCT = "defective_product"
    WRONG_ITEM = "wrong_item"
    DAMAGED_IN_TRANSIT = "damaged_in_transit"
    NOT_AS_DESCRIBED = "not_as_described"
    CUSTOMER_CHANGE_MIND = "customer_change_mind"
    DUPLICATE_ORDER = "duplicate_order"
    PRICING_ERROR = "pricing_error"
    OTHER = "other"

class RefundCreate(BaseModel):
    order_id: int = Field(..., gt=0, description="Order ID")
    amount: float = Field(..., gt=0, description="Refund amount")
    reason: RefundReason = Field(..., description="Refund reason")
    description: Optional[str] = Field(None, max_length=1000, description="Refund description")
    customer_contact: Optional[str] = Field(None, max_length=100, description="Customer contact")
    
    @validator('amount')
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError('Refund amount must be positive')
        return v

class RefundUpdate(BaseModel):
    status: Optional[RefundStatus] = None
    refund_method: Optional[str] = Field(None, max_length=50, description="Refund method")
    refund_transaction_id: Optional[str] = Field(None, max_length=100, description="Refund transaction ID")
    return_shipping_label: Optional[str] = Field(None, max_length=255, description="Return shipping label")

class RefundResponse(BaseModel):
    id: int
    order_id: int
    user_id: int
    amount: float
    reason: str
    description: Optional[str]
    status: str
    processed_by: Optional[int]
    processed_at: Optional[datetime]
    refund_method: Optional[str]
    refund_transaction_id: Optional[str]
    customer_contact: Optional[str]
    return_shipping_label: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
