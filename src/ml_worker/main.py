import json
import pika
import requests
import time
import logging
from task_request import  TaskRequest
from task_response import TaskResponse

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

HOST = 'app'

logger = logging.getLogger(__name__)
# Настройка логирования
connection_params = pika.ConnectionParameters(
    host='rabbitmq',  # Замените на адрес вашего RabbitMQ сервера
    port=5672,          # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username='user',  # Имя пользователя по умолчанию
        password='password'   # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
queue_name = 'ml_task_queue'
channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)
channel.basic_qos(prefetch_count=1)  # берем по 1 задаче

def send_answer(request:TaskRequest):
    url =f'http://{HOST}:8080/api/predicts/update'
    logger.info(f'Sending request to {url}')
    answer_text = f'response for request : {request}'
    answer =TaskResponse(
        id=request.id,
        status=4,
        answer=answer_text)
    logger.info(f'Sending answer {answer}')
    response=requests.post(url, json=answer.model_dump())
    logger.info(f'Sending response  {response}')
    if response.ok:
        print("Сообщение отправлено!")
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")

# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    task =TaskRequest(**message)
    send_answer(task)
    ch.basic_ack(delivery_tag=method.delivery_tag) # Ручное подтверждение обработки сообщения

# Подписка на очередь и установка обработчика сообщений
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False  # Автоматическое подтверждение обработки сообщений
)

logger.info('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()