"""
User Model for E-commerce Testing API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from passlib.context import CryptContext
import secrets
from database import Base
import enum

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MODERATOR = "moderator"
    SUPPORT = "support"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), default=UserRole.CUSTOMER)
    
    # Address information
    default_shipping_address = Column(JSON, nullable=True)
    default_billing_address = Column(JSON, nullable=True)
    
    # Account metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    last_password_change = Column(DateTime, nullable=True)
    
    # Email verification
    email_verification_token = Column(String(255), unique=True, nullable=True)
    email_verification_sent_at = Column(DateTime, nullable=True)
    
    # Password reset
    password_reset_token = Column(String(255), unique=True, nullable=True)
    password_reset_sent_at = Column(DateTime, nullable=True)
    
    # Account preferences
    preferences = Column(JSON, nullable=True)  # {"newsletter": true, "marketing": false}
    
    # Relationships
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, email: str, username: str, password: str, first_name: str, 
                 last_name: str, phone: str = None, role: UserRole = UserRole.CUSTOMER):
        """Initialize user with required fields"""
        self.email = email
        self.username = username
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.role = role
        self.generate_verification_token()
    
    def set_password(self, password: str):
        """Hash and set password"""
        if password:
            self.password_hash = pwd_context.hash(password)
            self.last_password_change = datetime.utcnow()
    
    def verify_password(self, password: str) -> bool:
        """Check if provided password matches hash"""
        if not self.password_hash:
            return False
        return pwd_context.verify(password, self.password_hash)
    
    def generate_verification_token(self):
        """Generate a unique email verification token"""
        self.email_verification_token = secrets.token_urlsafe(32)
        self.email_verification_sent_at = datetime.utcnow()
    
    def generate_password_reset_token(self):
        """Generate a unique password reset token"""
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_sent_at = datetime.utcnow()
    
    def verify_email(self, token: str) -> bool:
        """Verify email with token"""
        if (self.email_verification_token == token and 
            self.email_verification_sent_at and 
            datetime.utcnow() - self.email_verification_sent_at < timedelta(hours=24)):
            self.is_email_verified = True
            self.is_verified = True
            self.email_verification_token = None
            return True
        return False
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password with token"""
        if (self.password_reset_token == token and 
            self.password_reset_sent_at and 
            datetime.utcnow() - self.password_reset_sent_at < timedelta(hours=1)):
            self.set_password(new_password)
            self.password_reset_token = None
            return True
        return False
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
    
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role in [UserRole.ADMIN, UserRole.MODERATOR]
    
    def can_access_admin_panel(self) -> bool:
        """Check if user can access admin panel"""
        return self.role in [UserRole.ADMIN, UserRole.MODERATOR, UserRole.SUPPORT]
    
    def get_full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert user to dictionary"""
        data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_email_verified": self.is_email_verified,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "default_shipping_address": self.default_shipping_address,
            "default_billing_address": self.default_billing_address,
            "preferences": self.preferences
        }
        
        if include_sensitive:
            data.update({
                "email_verification_token": self.email_verification_token,
                "password_reset_token": self.password_reset_token
            })
        
        return data
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
