from datetime import datetime
from decimal import Decimal
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from services.queue.rabbitmq_connector import send_to_queue
from services.repositories import user as UserService
from services.repositories import ml_task as MLService
from DTO.ml_task_create_request import MlTaskCreateRequest
from database.database import get_session
from models import MlTask, TaskStatus, Transaction, TransactionType, TransactionStatus
from DTO.ml_task_update_request import MlTaskUpdateRequest
from services.repositories import transaction as TransactionService
from services.repositories import balance as BalanceService
from DTO.ml_task_queue import MlTaskQueueRequest

predict_route = APIRouter()

logger = logging.getLogger(__file__)

PRICE: Decimal = Decimal(5)

@predict_route.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model = int)
async def predict(data: MlTaskCreateRequest, session=Depends(get_session)):
    user = UserService.get_user_by_login(data.user_login, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    task = MlTask(user_id=user.id, input_data=data.input_data, status=TaskStatus.New, price=PRICE)
    task = MLService.add_task(task,session)
    # создание транзакции
    transaction = Transaction(type=TransactionType.Credit, date=datetime.now(), cost=PRICE,
                              status=TransactionStatus.New, user_id=user.id)
    transaction = TransactionService.add_transaction(transaction, session)
    # проверка баланса
    if BalanceService.check_balance(PRICE, user.id, session):
        # при положительном балансе транзакции, списание средств
        BalanceService.credit_balance_by_user(PRICE, user.id, session)
        TransactionService.update_status_transaction(transaction.id, TransactionStatus.Done, session)
        task.status = TaskStatus.Waiting
        task = MLService.merge_task(task, session)
        task_to_queue = MlTaskQueueRequest(id=task.id, input_data=task.input_data)
        send_to_queue(task_to_queue)
    else:
        # при отрицательном балансе отмена транзакции
        TransactionService.update_status_transaction(transaction.id, TransactionStatus.Canceled, session)
        task.status = TaskStatus.Canceled
        task = MLService.merge_task(task, session)
    return task.id

@predict_route.post("/update",
    status_code=status.HTTP_200_OK,
    response_model = int)
async def update_predict(data: MlTaskUpdateRequest, session=Depends(get_session)):
    logger.info(f'запрос {data}')
    task = MLService.get_task_by_id(task_id = data.id, session=session)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.answer = data.answer
    task.status = data.status
    task = MLService.merge_task(task,session)
    return task.status