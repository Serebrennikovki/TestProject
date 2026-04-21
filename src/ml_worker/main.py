import json
import pika
import requests
import logging
from ml_request import MlRequest
from config import get_settings
from task_request import  TaskRequest
from task_response import TaskResponse
from handle_ollama import ollama_stream_to_string

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


settings = get_settings()

logger = logging.getLogger(__name__)
# Настройка логирования
connection_params = pika.ConnectionParameters(
    host=settings.RABBITMQ_HOST,  # Замените на адрес вашего RabbitMQ сервера
    port=settings.RABBITMQ_PORT,          # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username=settings.RABBITMQ_USER,  # Имя пользователя по умолчанию
        password=settings.RABBITMQ_PASS   # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
queue_name = 'ml_task_queue'
channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)
channel.basic_qos(prefetch_count=1)  # берем по 1 задаче

def send_answer_positive(request:TaskRequest, answer: str):
    url =f'http://{settings.HOST_APP}:8080/api/predicts/update/positive'
    resp = TaskResponse(id=request.id, answer=answer)
    response=requests.post(url, json=resp.model_dump())
    logger.info(f'Sending response  {response}')

def send_answer_negative(request:TaskRequest):
    url =f'http://{settings.HOST_APP}:8080/api/predicts/update'
    resp = TaskResponse(id=TaskResponse.id)
    response=requests.post(url, json=resp.model_dump())
    logger.info(f'Sending response  {response}')


def get_predict(taskRequest:TaskRequest):
    try:
        response = ollama_stream_to_string(prompt=taskRequest.input_data)
        logger.info(f'Получили данные от ML {response}')
        send_answer_positive(taskRequest,response)
    except e:
        send_answer_negative(taskRequest)
        raise Exception(f'Произошла ошибка при запросе к Ollama: {e}')


# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    task =TaskRequest(**message)
    get_predict(taskRequest=task)
    ch.basic_ack(delivery_tag=method.delivery_tag) # Ручное подтверждение обработки сообщения

# Подписка на очередь и установка обработчика сообщений
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False  # Автоматическое подтверждение обработки сообщений
)

logger.info('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()