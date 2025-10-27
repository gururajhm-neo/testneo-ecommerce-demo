from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MODERATOR = "moderator"
    SUPPORT = "support"

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=80, description="Username")
    password: str = Field(..., min_length=8, max_length=100, description="Password")
    first_name: str = Field(..., min_length=1, max_length=50, description="First name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Last name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    role: UserRole = Field(UserRole.CUSTOMER, description="User role")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric with underscores and hyphens only')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    default_shipping_address: Optional[Dict[str, Any]] = None
    default_billing_address: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None

class UserProfile(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    phone: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    is_email_verified: bool
    default_shipping_address: Optional[Dict[str, Any]]
    default_billing_address: Optional[Dict[str, Any]]
    preferences: Optional[Dict[str, Any]]
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    is_email_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    user: UserResponse
