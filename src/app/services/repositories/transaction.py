from typing import List

from sqlmodel import Session, select

from models import Transaction
from models.enums import TransactionStatus


def get_all_transactions(session: Session) -> List[Transaction]:
    results = session.exec(select(Transaction)).all()
    return list(results)

def get_all_transactions_by_user(user_id:int, session: Session) -> List[Transaction]:
    results = session.exec(select(Transaction).where(Transaction.user_id == user_id)).all()
    return list(results)

def add_transaction(transaction:Transaction, session: Session) -> Transaction:
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

def update_status_transaction(id: int, status: TransactionStatus, session: Session) -> None:
    transaction = session.exec(select(Transaction).where(Transaction.id == id)).first()
    if transaction is None:
        raise Exception(f"Транзакция с id = {id} не найдена")
    transaction.status = status
    session.add(transaction)
    session.commit()
    session.refresh(transaction)