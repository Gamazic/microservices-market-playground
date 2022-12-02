from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Order(BaseModel):
    product_id: UUID
    order_id: UUID
    datetime: datetime


class OrderInCreate(BaseModel):
    product_id: UUID


class ManyOrdersResponse(BaseModel):
    __root__: list[Order]

