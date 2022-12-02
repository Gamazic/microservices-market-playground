from datetime import datetime
from uuid import UUID, uuid4

import aio_pika
from fastapi import FastAPI, status
from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from common.rmq import get_connection, QUEUE_NAME
from order_service.domain import Order, OrderInCreate, ManyOrdersResponse


AioPikaInstrumentor().instrument()
FastAPIInstrumentor().instrument()
HTTPXClientInstrumentor().instrument()

app = FastAPI()


async def put_to_queue(body: bytes):
    connection = await get_connection()

    async with connection:
        routing_key = QUEUE_NAME
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=routing_key,
        )


@app.get("/order", response_model=ManyOrdersResponse)
async def get_orders():
    return ManyOrdersResponse(__root__=[Order(
        product_id=uuid4(),
        order_id=uuid4(),
        datetime=datetime.now())
    ])


@app.get("/order/{order_id}", response_model=Order)
async def get_order_by_id(order_id: UUID):
    return Order(
        product_id=uuid4(),
        order_id=order_id,
        datetime=datetime.now()
    )


@app.post("/order", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(body: OrderInCreate):
    item_id = body.product_id
    order_id = uuid4()
    curr_dt = datetime.now()
    order = Order(product_id=item_id, order_id=order_id, datetime=curr_dt)
    await put_to_queue(order.json().encode())
    return order
