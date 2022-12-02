import os

from httpx import AsyncClient


ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL")


async def create_http_client():
    async with AsyncClient() as c:
        yield c
