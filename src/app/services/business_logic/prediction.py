from datetime import datetime
from decimal import Decimal

from DTO.ml_task_create_request import MlTaskCreateRequest
from core.exceptions import PredictionError
from services.queue.rabbitmq_connector import send_to_queue
from services.repositories import user as UserRepository
from services.repositories import ml_task as MLRepository
from DTO.ml_task_create_request import MlTaskCreateRequest
from models import MlTask, TaskStatus, Transaction, TransactionType, TransactionStatus
from services.repositories import transaction as TransactionRepository
from services.repositories import balance as BalanceRepository
from services.repositories import ml_task as MlTaskRepository
from DTO.ml_task_queue import MlTaskQueueRequest
from DTO.ml_task_update_request_simple import MlTaskUpdateRequestSimple

PRICE: Decimal = Decimal(5)

def add_prediction(data: MlTaskCreateRequest, session) :
    user = UserRepository.get_user_by_login(data.user_login, session)
    if user is None:
        raise PredictionError("User not found")
    task = MlTask(user_id=user.id, input_data=data.input_data, status=TaskStatus.New, price=PRICE)
    task = MLRepository.add_task(task,session)
    # создание транзакции
    transaction = Transaction(type=TransactionType.Credit, date=datetime.now(), cost=PRICE,
                              status=TransactionStatus.New, user_id=user.id)
    transaction = TransactionRepository.add_transaction(transaction, session)
    # проверка баланса
    if BalanceRepository.check_balance(PRICE, user.id, session):
        # при положительном балансе транзакции, списание средств
        BalanceRepository.credit_balance_by_user(PRICE, user.id, session)
        TransactionRepository.update_status_transaction(transaction.id, TransactionStatus.Done, session)
        task.status = TaskStatus.Waiting
        task = MLRepository.merge_task(task, session)
        task_to_queue = MlTaskQueueRequest(id=task.id, input_data=task.input_data)
        send_to_queue(task_to_queue)
    else:
        # при отрицательном балансе отмена транзакции
        TransactionRepository.update_status_transaction(transaction.id, TransactionStatus.Canceled, session)
        task.status = TaskStatus.Canceled
        task = MLRepository.merge_task(task, session)
    return task.id

def add_positive_result(data: MlTaskUpdateRequestSimple, session):
    task = MLRepository.get_task_by_id(task_id = data.id, session=session)
    if task is None:
        raise PredictionError("Task not found")
    task.answer = data.answer
    task.status = TaskStatus.Completed
    task = MLRepository.merge_task(task,session)
    return task.status

def add_negative_result(data: MlTaskCreateRequest, session):
    task = MLRepository.get_task_by_id(task_id = data.id, session=session)
    if task is None:
        raise PredictionError("Task not found")
    task.status = TaskStatus.UnsuccessfullCompleted
    task = MLRepository.merge_task(task,session)
    transaction = Transaction(type=TransactionType.Refund, date=datetime.now(), cost=PRICE,
                              status=TransactionStatus.New, user_id=task.user_id)
    transaction = TransactionRepository.add_transaction(transaction, session)
    BalanceRepository.deposit_balance_by_user(PRICE, task.user_id, session)
    TransactionRepository.update_status_transaction(transaction.id, TransactionStatus.Done, session)
    return task.status

def get_all_task(user_login:str, session):
    user = UserRepository.get_user_by_login(user_login, session)
    if user is None:
        raise PredictionError("User not found")
    return MlTaskRepository.get_all_tasks_by_user(user_id=user.id, session=session)
