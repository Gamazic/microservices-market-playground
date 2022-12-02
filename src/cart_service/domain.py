from uuid import UUID

from pydantic import BaseModel


class CartItem(BaseModel):
    item_id: UUID
    product_id: UUID


class Cart(BaseModel):
    __root__: list[CartItem]
