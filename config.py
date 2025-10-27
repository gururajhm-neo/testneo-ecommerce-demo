"""
Configuration settings for E-commerce Testing API
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from datetime import timedelta
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    app_name: str = "E-commerce Testing API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 9000
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS settings
    cors_origins: List[str] = [
        "http://localhost:9999",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
        "http://127.0.0.1:9999",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8080",
        "http://44.202.138.57:3001",
        "http://44.202.138.57:3000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_headers: List[str] = ["Content-Type", "Authorization"]
    
    # Database settings
    database_url: str = "sqlite:///./ecommerce.db"
    
    # Business rules
    max_cart_items: int = 50
    max_order_amount: float = 10000.0
    min_order_amount: float = 1.0
    max_coupon_uses_per_user: int = 5
    max_reviews_per_product_per_user: int = 1
    max_wishlist_items: int = 100
    
    # Inventory settings
    low_stock_threshold: int = 5
    out_of_stock_threshold: int = 0
    
    # Payment settings
    supported_payment_methods: List[str] = [
        "credit_card", "debit_card", "paypal", "bank_transfer", "cash_on_delivery"
    ]
    
    # Shipping settings
    free_shipping_threshold: float = 50.0
    standard_shipping_cost: float = 5.0
    express_shipping_cost: float = 15.0
    
    # Tax settings
    tax_rate: float = 0.10  # 10% tax rate
    
    # Validation settings
    min_password_length: int = 8
    max_password_length: int = 100
    min_username_length: int = 3
    max_username_length: int = 80
    
    # Rate limiting
    rate_limit_enabled: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()
