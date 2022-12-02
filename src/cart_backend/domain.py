from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class CartItem(BaseModel):
    item_id: UUID
    product_id: UUID


class Cart(BaseModel):
    __root__: list[CartItem]


class OrderInCreate(BaseModel):
    item_id: UUID


class OrderInResponse(BaseModel):
    product_id: UUID
    order_id: UUID
    datetime: datetime
