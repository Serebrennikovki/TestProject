from datetime import datetime
from decimal import Decimal
from sqlmodel import Session

from database.database import get_session, init_db, engine
from models import User, Transaction
from models.enums import Roles, TransactionType, TransactionStatus
from services.repositories.user import create_user, get_all_users
from services.repositories.balance import add_balance, credit_balance_by_user, check_balance, deposit_balance_by_user
from services.repositories.transaction import add_transaction, update_status_transaction
print("service alive")

def deposit(user_id: int, amount: Decimal) -> None:
    transaction = Transaction(type=TransactionType.Debit, date=datetime.now(), cost=amount,status=TransactionStatus.New, user_id=user_id)
    transaction = add_transaction(transaction, session)
    deposit_balance_by_user(amount, user_id, session)
    update_status_transaction(transaction.id, TransactionStatus.Done, session)

def credit(user_id: int, amount: Decimal) -> None:
    transaction = Transaction(type=TransactionType.Credit, date=datetime.now(), cost=amount,status=TransactionStatus.New, user_id=user_id)
    transaction = add_transaction(transaction, session)
    if check_balance(amount, user_id, session):
        credit_balance_by_user(amount, user_id, session)
        update_status_transaction(transaction.id, TransactionStatus.Done, session)
    else:
        update_status_transaction(transaction.id, TransactionStatus.Canceled, session)

init_db()
print('Init db has been success')


test_user_0 = User(login='test0', password='test0', name='test0', role=Roles.Administrator)
test_user_1 = User(login='test1', password='test1', name='test1', role=Roles.User)
test_user_2 = User(login='test2', password='test2', role=Roles.User)

with Session(engine) as session:
    test_user_0 = create_user(test_user_0, session)
    add_balance(test_user_0.id, session)
    deposit(test_user_0.id, Decimal(10))
    credit(test_user_0.id, Decimal(20))
    test_user_1 = create_user(test_user_1, session)
    add_balance(test_user_1.id, session)
    deposit(test_user_1.id, Decimal(20))
    credit(test_user_1.id, Decimal(10))
    test_user_2 = create_user(test_user_2, session)
    add_balance(test_user_2.id, session)
    deposit(test_user_2.id, Decimal(30))
    credit(test_user_2.id, Decimal(15))
    users = get_all_users(session)




