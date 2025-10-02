"""
Order data models for AutomationExercise testing framework.
"""
from typing import List, Optional
from pydantic import BaseModel


class OrderItem(BaseModel):
    """Order item model."""
    product_id: int
    quantity: int
    price: float


class Order(BaseModel):
    """Order model."""
    order_id: int
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: str


class OrderResponse(BaseModel):
    """Order response model."""
    responseCode: int
    message: str
    order: Optional[Order] = None
