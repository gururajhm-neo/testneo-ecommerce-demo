from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    RETURNED = "returned"
    FAILED = "failed"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    CRYPTO = "crypto"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    DECLINED = "declined"

class ShippingMethod(str, Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    SAME_DAY = "same_day"
    PICKUP = "pickup"

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, le=100, description="Quantity")
    selected_options: Optional[Dict[str, Any]] = Field(None, description="Selected options")
    
    @validator('quantity')
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        if v > 100:
            raise ValueError('Quantity cannot exceed 100')
        return v

class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_items=1, max_items=50, description="Order items")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    shipping_method: ShippingMethod = Field(ShippingMethod.STANDARD, description="Shipping method")
    shipping_address: Dict[str, Any] = Field(..., description="Shipping address")
    billing_address: Optional[Dict[str, Any]] = Field(None, description="Billing address")
    customer_notes: Optional[str] = Field(None, max_length=1000, description="Customer notes")
    coupon_code: Optional[str] = Field(None, max_length=50, description="Coupon code")
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Order must contain at least one item')
        if len(v) > 50:
            raise ValueError('Order cannot contain more than 50 items')
        return v
    
    @validator('shipping_address')
    def validate_shipping_address(cls, v):
        required_fields = ['street', 'city', 'state', 'postal_code', 'country']
        for field in required_fields:
            if field not in v or not v[field]:
                raise ValueError(f'Shipping address must contain {field}')
        return v

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    tracking_number: Optional[str] = Field(None, max_length=100, description="Tracking number")
    tracking_url: Optional[str] = Field(None, max_length=255, description="Tracking URL")
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    internal_notes: Optional[str] = Field(None, max_length=1000, description="Internal notes")

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    product_name: Optional[str]
    product_sku: Optional[str]
    product_image: Optional[str]
    selected_options: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    status: OrderStatus
    total_amount: float
    subtotal: float
    tax_amount: float
    shipping_amount: float
    discount_amount: float
    handling_fee: float
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    payment_details: Optional[Dict[str, Any]]
    payment_transaction_id: Optional[str]
    payment_gateway: Optional[str]
    shipping_method: ShippingMethod
    shipping_address: Dict[str, Any]
    billing_address: Dict[str, Any]
    tracking_number: Optional[str]
    tracking_url: Optional[str]
    estimated_delivery: Optional[datetime]
    actual_delivery: Optional[datetime]
    customer_notes: Optional[str]
    internal_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    confirmed_at: Optional[datetime]
    processed_at: Optional[datetime]
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

class OrderList(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
