import asyncio
import logging

import aio_pika
from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor

from common.rmq import get_connection, QUEUE_NAME
from common.logger import load_yaml_logging_config


AioPikaInstrumentor().instrument()

logger = logging.getLogger("amqp_microservice")


async def process_message(
        message: aio_pika.abc.AbstractIncomingMessage
):
    async with message.process():
        logger.info(message.body)
        await asyncio.sleep(1)
        logger.info(str(message.body) + "x2")


async def main() -> None:
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(QUEUE_NAME, auto_delete=False)
        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    load_yaml_logging_config("warehouse_service/log_conf.yml")
    asyncio.run(main())

