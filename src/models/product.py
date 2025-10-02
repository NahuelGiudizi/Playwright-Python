"""
Product data models for AutomationExercise testing framework.
"""
from typing import List, Optional
from pydantic import BaseModel


class ProductCategory(BaseModel):
    """Product category model."""
    usertype: str
    category: str


class Product(BaseModel):
    """Product model."""
    id: int
    name: str
    price: str
    brand: str
    category: ProductCategory


class ProductsResponse(BaseModel):
    """Products API response model."""
    responseCode: int
    products: List[Product]


class SearchProductResponse(BaseModel):
    """Search product API response model."""
    responseCode: int
    products: List[Product]


class Brand(BaseModel):
    """Brand model."""
    id: int
    brand: str


class BrandsResponse(BaseModel):
    """Brands API response model."""
    responseCode: int
    brands: List[Brand]
