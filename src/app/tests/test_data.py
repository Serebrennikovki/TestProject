from datetime import datetime
from decimal import Decimal

from sqlmodel import Session

from services.repositories.transaction import add_transaction, update_status_transaction
from core.security import hash_password
from models.enums import Roles, TransactionStatus, TransactionType
from models.transaction import Transaction
from models.user import User
from services.repositories.user import create_user
from services.repositories.balance import add_balance, check_balance, credit_balance_by_user, deposit_balance_by_user




def __deposit(user_id: int, amount: Decimal, session: Session) -> None:
    transaction = Transaction(type=TransactionType.Debit, date=datetime.now(), cost=amount,status=TransactionStatus.New, user_id=user_id)
    transaction = add_transaction(transaction, session)
    deposit_balance_by_user(amount, user_id, session)
    update_status_transaction(transaction.id, TransactionStatus.Done, session)

def __credit(user_id: int, amount: Decimal, session: Session) -> None:
    transaction = Transaction(type=TransactionType.Credit, date=datetime.now(), cost=amount,status=TransactionStatus.New, user_id=user_id)
    transaction = add_transaction(transaction, session)
    if check_balance(amount, user_id, session):
        credit_balance_by_user(amount, user_id, session)
        update_status_transaction(transaction.id, TransactionStatus.Done, session)
    else:
        update_status_transaction(transaction.id, TransactionStatus.Canceled, session)

def add_test_data( session: Session):
    user = User(login='test', password=hash_password('test'), name='test', role=Roles.User)
    user = create_user(user, session)
    add_balance(user.id, session)
    __deposit(user.id, Decimal(10), session)
    __credit(user.id, Decimal(20), session)