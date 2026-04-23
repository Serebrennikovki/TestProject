from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, status
from database.database import get_session
from DTO.deposit_balance import DepositBalance
from models import Transaction, TransactionType, TransactionStatus
from services.business_logic import balance as BalanceService
from core.exceptions import BalanceError

balance_route = APIRouter()

@balance_route.get(
    "/{user_login}",
    status_code=status.HTTP_200_OK,
    response_model=Decimal)
async def balance(user_login: str, session=Depends(get_session)):
        try:
            balance = BalanceService.get_balance(user_login, session)
        except BalanceError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return balance

@balance_route.post(
    "/deposit",
    status_code=status.HTTP_200_OK,
    response_model=Decimal)
async def balance(deposit: DepositBalance, session=Depends(get_session)):
        try:
            balance = BalanceService.add_deposit(deposit, session)
        except BalanceError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return balance




