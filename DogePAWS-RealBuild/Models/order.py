# Models/order.py
from pydantic import BaseModel
from typing import List

from .product import Product

class Order(BaseModel):
    customer_name: str
    order_date: str
    products: List[Product]
    total_cost: float
