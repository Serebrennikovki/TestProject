import pika
import logging
import json
from pydantic import BaseModel

QUEUE_NAME = "ml_task_queue"

logger = logging.getLogger(__file__)

connection_params = pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,         # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username='user',  # Имя пользователя по умолчанию
        password='password'
    ),
    heartbeat=30,
    blocked_connection_timeout=10,
)

def send_to_queue(message:BaseModel):

    json_send = json.dumps(message.model_dump()).encode('utf-8')

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    logger.debug(f'send message to queue {message}')
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json_send
    )

    # Закрытие соединения
    connection.close()