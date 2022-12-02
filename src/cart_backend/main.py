from httpx import AsyncClient
from fastapi import FastAPI, status, Depends, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from cart_backend.domain import CartItem, Cart, OrderInCreate, OrderInResponse
from common.http import create_http_client, ORDER_SERVICE_URL, CART_SERVICE_URL


FastAPIInstrumentor().instrument()
HTTPXClientInstrumentor().instrument()


app = FastAPI()


@app.get("/cart",
         response_model=Cart)
async def get_cart(http_client: AsyncClient = Depends(create_http_client)):
    get_cart_response = await http_client.get(CART_SERVICE_URL)
    if get_cart_response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    cart = Cart.parse_raw(get_cart_response.content)
    return cart


@app.post("/order",
          response_model=OrderInResponse,
          status_code=status.HTTP_201_CREATED)
async def make_order(
        body: OrderInCreate,
        http_client: AsyncClient = Depends(create_http_client)
):
    cart_item_id = body.item_id
    cart_item_response = await http_client.get(f"{CART_SERVICE_URL}/{cart_item_id}")
    if cart_item_response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    cart_item = CartItem.parse_raw(cart_item_response.content)
    create_order_response = await http_client.post(ORDER_SERVICE_URL,
                                                   json={"product_id": str(cart_item.product_id)})
    if create_order_response.status_code != status.HTTP_201_CREATED:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    delete_from_cart_response = await http_client.delete(f"{CART_SERVICE_URL}/{cart_item_id}")
    if delete_from_cart_response.status_code != status.HTTP_204_NO_CONTENT:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    order_in_response = OrderInResponse.parse_raw(create_order_response.content)
    return order_in_response
