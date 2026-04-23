from sqlmodel import Session
from services.repositories import user as UserRepository
from services.repositories import transaction as TransactionRepository
from core.exceptions import HistoryError

def get_history(user_login: str, session: Session):
    user = UserRepository.get_user_by_login(user_login, session)
    if user is None:
        raise HistoryError("User not found")
    return TransactionRepository.get_all_transactions_by_user(user.id, session)