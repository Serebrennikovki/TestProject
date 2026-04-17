from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, status
from services.repositories import user as UserService
from services.repositories import balance as BalanceService
from services.repositories import transaction as TransactionService
from database.database import get_session
from DTO.deposit_balance import DepositBalance
from models import Transaction, TransactionType, TransactionStatus

balance_route = APIRouter()

@balance_route.get(
    "/{user_login}",
    status_code=status.HTTP_200_OK,
    response_model=Decimal)
async def balance(user_login: str, session=Depends(get_session)):
        user = UserService.get_user_by_login(user_login, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        budget = BalanceService.get_balance_by_user(user.id, session)
        if budget is None:
            raise HTTPException(status_code=404, detail="Balance not found")
        return budget.balance

@balance_route.post(
    "/deposit",
    status_code=status.HTTP_200_OK,
    response_model=Decimal)
async def balance(deposit: DepositBalance, session=Depends(get_session)):
        user = UserService.get_user_by_login(deposit.user_login, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        transaction = Transaction(type=TransactionType.Debit, date=datetime.now(), cost=deposit.amount,
                                  status=TransactionStatus.New, user_id=user.id)
        transaction = TransactionService.add_transaction(transaction, session)
        budget = BalanceService.deposit_balance_by_user(deposit.amount, user.id, session)
        TransactionService.update_status_transaction(transaction.id, TransactionStatus.Done, session)

        return budget.balance




