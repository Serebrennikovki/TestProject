from typing import List
from services.repositories import transaction as TransactionRepository
from services.repositories import user as UserRepository
from fastapi import APIRouter, Depends, status, HTTPException
from models import Transaction
from services.business_logic import history as HistoryService
from core.exceptions import HistoryError 

from database.database import get_session

history_route = APIRouter()

@history_route.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[Transaction],
)
async def get_history(session=Depends(get_session)):
    return TransactionRepository.get_all_transactions(session)

@history_route.get(
    "/{user_login}",
    status_code=status.HTTP_200_OK,
    response_model=List[Transaction],
)
async def get_history(user_login:str, session=Depends(get_session)):
    try:
        history = HistoryService.get_history(user_login, session)
    except HistoryError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return history