import os

import aio_pika


QUEUE_NAME = os.getenv("QUEUE_NAME")


async def get_connection():
    user = os.getenv("RABBITMQ_DEFAULT_USER")
    password = os.getenv("RABBITMQ_DEFAULT_PASS")
    host = os.getenv("RABBITMQ_HOST")
    connection = await aio_pika.connect_robust(
        f"amqp://{user}:{password}@{host}/",
    )
    return connection
