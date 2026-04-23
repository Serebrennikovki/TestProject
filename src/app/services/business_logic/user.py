from sqlmodel import Session
from core.exceptions import UserError
from core.security import hash_password
from models.enums import Roles
from models.user import User
from services.repositories import user as UserRepository
from services.repositories import balance as BalanceRepository

from DTO.user_create import UserCreate

def create_user(data:UserCreate, session: Session):
    if UserRepository.get_user_by_login(data.login, session):
        raise UserError("User with this login already exists")
    
    user = User(
            password=hash_password(data.password),
            login=data.login,
            name=data.name,
            role=Roles.User,
        )
    UserRepository.create_user(user, session)
    BalanceRepository.add_balance(user.id, session)
    return {"message": "User successfully registered"}