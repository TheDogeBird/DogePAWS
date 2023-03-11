# Models/inventory.py
from pydantic import BaseModel
from typing import List

from .product import Product

class Inventory(BaseModel):
    store: str
    products: List[Product]
