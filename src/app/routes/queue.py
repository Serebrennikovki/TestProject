from typing import Dict
import json
from fastapi import APIRouter, status, Depends
from services.queue.rabbitmq_connector import send_to_queue
from DTO.ml_task_queue import MlTaskQueueRequest
import logging

logger = logging.getLogger(__name__)

queue_route = APIRouter()

@queue_route.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model = Dict[str, str])
async def put_to_queue(message: MlTaskQueueRequest):
    send_to_queue(message)
    return {"статус":"сообщение в очереди"}