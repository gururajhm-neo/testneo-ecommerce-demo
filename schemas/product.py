from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME_GARDEN = "home_garden"
    SPORTS = "sports"
    BEAUTY = "beauty"
    TOYS = "toys"
    AUTOMOTIVE = "automotive"
    HEALTH = "health"
    FOOD = "food"
    JEWELRY = "jewelry"
    FURNITURE = "furniture"
    MUSIC = "music"
    MOVIES = "movies"
    GARDENING = "gardening"

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    short_description: Optional[str] = Field(None, max_length=500, description="Short description")
    price: float = Field(..., gt=0, description="Product price")
    sale_price: Optional[float] = Field(None, gt=0, description="Sale price")
    cost_price: Optional[float] = Field(None, gt=0, description="Cost price")
    sku: str = Field(..., min_length=1, max_length=100, description="SKU")
    barcode: Optional[str] = Field(None, max_length=100, description="Barcode")
    upc: Optional[str] = Field(None, max_length=50, description="UPC")
    ean: Optional[str] = Field(None, max_length=50, description="EAN")
    category: ProductCategory = Field(..., description="Product category")
    subcategory: Optional[str] = Field(None, max_length=100, description="Subcategory")
    brand: Optional[str] = Field(None, max_length=100, description="Brand")
    manufacturer: Optional[str] = Field(None, max_length=100, description="Manufacturer")
    stock_quantity: int = Field(0, ge=0, description="Stock quantity")
    min_stock_level: int = Field(5, ge=0, description="Minimum stock level")
    max_stock_level: int = Field(1000, ge=0, description="Maximum stock level")
    weight: Optional[float] = Field(None, gt=0, description="Weight")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Dimensions")
    color: Optional[str] = Field(None, max_length=50, description="Color")
    size: Optional[str] = Field(None, max_length=50, description="Size")
    material: Optional[str] = Field(None, max_length=100, description="Material")
    images: Optional[List[str]] = Field(None, description="Product images")
    thumbnail: Optional[str] = Field(None, description="Thumbnail image")
    video_url: Optional[str] = Field(None, description="Video URL")
    meta_title: Optional[str] = Field(None, max_length=200, description="Meta title")
    meta_description: Optional[str] = Field(None, description="Meta description")
    tags: Optional[List[str]] = Field(None, description="Product tags")
    keywords: Optional[List[str]] = Field(None, description="SEO keywords")
    shipping_weight: Optional[float] = Field(None, gt=0, description="Shipping weight")
    requires_shipping: bool = Field(True, description="Requires shipping")
    is_digital: bool = Field(False, description="Is digital product")
    download_url: Optional[str] = Field(None, description="Download URL")
    warranty_period: Optional[int] = Field(None, ge=0, description="Warranty period in days")
    return_period: int = Field(30, ge=0, description="Return period in days")
    is_returnable: bool = Field(True, description="Is returnable")
    
    @validator('sale_price')
    def sale_price_less_than_price(cls, v, values):
        if v is not None and 'price' in values and v >= values['price']:
            raise ValueError('Sale price must be less than regular price')
        return v
    
    @validator('cost_price')
    def cost_price_less_than_price(cls, v, values):
        if v is not None and 'price' in values and v >= values['price']:
            raise ValueError('Cost price must be less than regular price')
        return v
    
    @validator('max_stock_level')
    def max_stock_greater_than_min(cls, v, values):
        if 'min_stock_level' in values and v <= values['min_stock_level']:
            raise ValueError('Maximum stock level must be greater than minimum stock level')
        return v

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    sale_price: Optional[float] = Field(None, gt=0)
    cost_price: Optional[float] = Field(None, gt=0)
    barcode: Optional[str] = Field(None, max_length=100)
    upc: Optional[str] = Field(None, max_length=50)
    ean: Optional[str] = Field(None, max_length=50)
    category: Optional[ProductCategory] = None
    subcategory: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)
    max_stock_level: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_bestseller: Optional[bool] = None
    is_new_arrival: Optional[bool] = None
    is_on_sale: Optional[bool] = None
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[Dict[str, float]] = None
    color: Optional[str] = Field(None, max_length=50)
    size: Optional[str] = Field(None, max_length=50)
    material: Optional[str] = Field(None, max_length=100)
    images: Optional[List[str]] = None
    thumbnail: Optional[str] = None
    video_url: Optional[str] = None
    meta_title: Optional[str] = Field(None, max_length=200)
    meta_description: Optional[str] = None
    tags: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    shipping_weight: Optional[float] = Field(None, gt=0)
    requires_shipping: Optional[bool] = None
    is_digital: Optional[bool] = None
    download_url: Optional[str] = None
    warranty_period: Optional[int] = Field(None, ge=0)
    return_period: Optional[int] = Field(None, ge=0)
    is_returnable: Optional[bool] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    short_description: Optional[str]
    price: float
    sale_price: Optional[float]
    cost_price: Optional[float]
    sku: str
    barcode: Optional[str]
    upc: Optional[str]
    ean: Optional[str]
    category: ProductCategory
    subcategory: Optional[str]
    brand: Optional[str]
    manufacturer: Optional[str]
    stock_quantity: int
    reserved_quantity: int
    min_stock_level: int
    max_stock_level: int
    is_active: bool
    is_featured: bool
    is_bestseller: bool
    is_new_arrival: bool
    is_on_sale: bool
    weight: Optional[float]
    dimensions: Optional[Dict[str, float]]
    color: Optional[str]
    size: Optional[str]
    material: Optional[str]
    images: Optional[List[str]]
    thumbnail: Optional[str]
    video_url: Optional[str]
    meta_title: Optional[str]
    meta_description: Optional[str]
    tags: Optional[List[str]]
    keywords: Optional[List[str]]
    average_rating: float
    total_reviews: int
    total_ratings: int
    shipping_weight: Optional[float]
    requires_shipping: bool
    is_digital: bool
    download_url: Optional[str]
    warranty_period: Optional[int]
    return_period: int
    is_returnable: bool
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ProductList(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
