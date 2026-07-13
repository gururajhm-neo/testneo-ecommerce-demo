"""
Configuration settings for E-commerce Testing API
"""
from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Any
import json
import os


DEFAULT_CORS_ORIGINS = [
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
    "http://34.229.255.219:3001",
    "http://34.229.255.219:3000",
    "http://testneo-ecom.testneo.ai",
    "https://testneo-ecom.testneo.ai",
    "http://testneo-ecom.testneo.ai:3001",
    "https://testneo-ecom.testneo.ai:3001",
]


def _parse_str_list(value: Any, default: List[str] | None = None) -> List[str]:
    """Accept JSON lists, comma-separated strings, or a single string."""
    if value is None:
        return list(default or [])
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return list(default or [])
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except json.JSONDecodeError:
                pass
        if "," in text:
            return [part.strip() for part in text.split(",") if part.strip()]
        return [text]
    return list(default or [])


def _normalize_list_env_vars() -> None:
    """
    pydantic-settings JSON-decodes list fields from the environment before validators run.
    Normalize empty / CSV / plain URL values so Settings() does not crash on EC2.
    """
    list_env_keys = (
        "CORS_ORIGINS",
        "CORS_ALLOW_METHODS",
        "CORS_ALLOW_HEADERS",
        "SUPPORTED_PAYMENT_METHODS",
    )
    for key in list_env_keys:
        if key not in os.environ:
            continue
        raw = os.environ.get(key, "")
        if raw is None or not str(raw).strip():
            # Empty override → drop so class defaults apply
            os.environ.pop(key, None)
            continue
        text = str(raw).strip()
        if text.startswith("["):
            continue
        os.environ[key] = json.dumps(_parse_str_list(text))


_normalize_list_env_vars()


class Settings(BaseSettings):
    """Application settings"""

    app_name: str = "E-commerce Testing API"
    app_version: str = "1.0.0"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 9000

    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    cors_origins: List[str] = DEFAULT_CORS_ORIGINS
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    database_url: str = "sqlite:///./ecommerce.db"

    max_cart_items: int = 50
    max_order_amount: float = 10000.0
    min_order_amount: float = 1.0
    max_coupon_uses_per_user: int = 5
    max_reviews_per_product_per_user: int = 1
    max_wishlist_items: int = 100

    low_stock_threshold: int = 5
    out_of_stock_threshold: int = 0

    supported_payment_methods: List[str] = [
        "credit_card",
        "debit_card",
        "paypal",
        "bank_transfer",
        "cash_on_delivery",
    ]

    free_shipping_threshold: float = 50.0
    standard_shipping_cost: float = 5.0
    express_shipping_cost: float = 15.0

    tax_rate: float = 0.10

    min_password_length: int = 8
    max_password_length: int = 100
    min_username_length: int = 3
    max_username_length: int = 80

    rate_limit_enabled: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    @field_validator(
        "cors_origins",
        "cors_allow_methods",
        "cors_allow_headers",
        "supported_payment_methods",
        mode="before",
    )
    @classmethod
    def parse_list_fields(cls, value: Any) -> Any:
        return _parse_str_list(value)

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
