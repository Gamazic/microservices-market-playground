from uuid import UUID, uuid4

from fastapi import FastAPI, status
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from cart_service.domain import CartItem, Cart


FastAPIInstrumentor().instrument()
HTTPXClientInstrumentor().instrument()


app = FastAPI()


def get_mock_cart_item(item_id=None):
    if item_id is None:
        item_id = uuid4()
    return CartItem(item_id=item_id, product_id=uuid4())


@app.get("/cart", response_model=Cart)
async def get_cart():
    return Cart(__root__=[get_mock_cart_item(), get_mock_cart_item()])


@app.get("/cart/{item_id}", response_model=CartItem)
async def get_cart_item_by_id(item_id: UUID):
    return get_mock_cart_item(item_id)


@app.delete("/cart/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_by_item_id(item_id: UUID):
    return
