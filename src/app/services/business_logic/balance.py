from datetime import datetime
from decimal import Decimal

from DTO.deposit_balance import DepositBalance
from models.enums import TransactionStatus, TransactionType
from models.transaction import Transaction
from core.exceptions import BalanceError
from services.repositories import balance as BalanceRepository
from services.repositories import user as UserRepository
from services.repositories import transaction as TransactionRepository
from sqlmodel import Session



def get_balance(user_login: str, session: Session):
        user = UserRepository.get_user_by_login(user_login, session)
        if user is None:
            raise BalanceError("User not found")
        budget = BalanceRepository.get_balance_by_user(user.id, session)
        if budget is None:
            raise BalanceError("Balance not found")
        return budget.balance

def add_deposit(deposit: DepositBalance, session: Session) -> Decimal : 
    user = UserRepository.get_user_by_login(deposit.user_login, session)
    if user is None:
            raise BalanceError("User not found")

    transaction = Transaction(type=TransactionType.Debit, date=datetime.now(), cost=deposit.amount,
                                  status=TransactionStatus.New, user_id=user.id)
    transaction = TransactionRepository.add_transaction(transaction, session)
    budget = BalanceRepository.deposit_balance_by_user(deposit.amount, user.id, session)
    TransactionRepository.update_status_transaction(transaction.id, TransactionStatus.Done, session)

    return budget.balance