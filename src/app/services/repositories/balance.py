from decimal import Decimal

from sqlmodel import select, Session

from models import Balance


def get_balance_by_user(user_id:int, session: Session) -> Balance:
    return session.exec(select(Balance).where(Balance.user_id == user_id)).first()

def add_balance(user_id: int, session: Session) -> Balance:
    balance = Balance(amount=0, user_id=user_id)
    session.add(balance)
    session.commit()
    session.refresh(balance)
    return balance

def deposit_balance_by_user(amount:Decimal, user_id:int, session: Session) -> Balance:
    balance = session.exec(select(Balance).where(Balance.user_id == user_id)).first()
    if balance is None:
        balance = add_balance(user_id, session)

    balance.balance = balance.balance + amount
    session.add(balance)
    session.commit()
    session.refresh(balance)
    return balance


def credit_balance_by_user(amount: Decimal, user_id: int, session: Session) -> Balance:
    balance = session.exec(select(Balance).where(Balance.user_id == user_id)).first()
    if balance is None:
       balance = add_balance(user_id, session)

    balance.balance = balance.balance - amount
    session.add(balance)
    session.commit()
    session.refresh(balance)
    return balance


def check_balance(amount: Decimal, user_id: int, session: Session) -> bool:
    balance = session.exec(select(Balance).where(Balance.user_id == user_id)).first()
    if balance is None:
        raise Exception(f'нет баланса для пользователя с таким id={user_id}')

    return balance.balance - amount >= 0