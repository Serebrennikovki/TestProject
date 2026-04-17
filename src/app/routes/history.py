from sys import prefix
from typing import List
from services.repositories import transaction as TransactionService
from services.repositories import user as UserService
from fastapi import APIRouter, Depends, status, HTTPException
from models import Transaction

from database.database import get_session

history_route = APIRouter()

@history_route.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[Transaction],
)
async def get_history(session=Depends(get_session)):
    return TransactionService.get_all_transactions(session)

@history_route.get(
    "/{user_login}",
    status_code=status.HTTP_200_OK,
    response_model=List[Transaction],
)
async def get_history(user_login:str, session=Depends(get_session)):
    user = UserService.get_user_by_login(user_login, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return TransactionService.get_all_transactions_by_user(user.id, session)