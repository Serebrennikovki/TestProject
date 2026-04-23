from typing import Dict
from fastapi import APIRouter, status, Depends, HTTPException, Response
import logging
from models import User
from database.database import get_session
from services.repositories import user as UserRepository
from core.security import hash_password, verify_password
from DTO.user_create import UserCreate
from DTO.auth_sign_up import AuthSignup
from services.repositories import balance as BalanceRepository

from models import Roles

# Configure logging
logger = logging.getLogger(__name__)

auth_route = APIRouter()

@auth_route.post(
    '/signup',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with name, login and password")
async def signup(data: UserCreate, session=Depends(get_session)) -> Dict[str, str]:
        if UserRepository.get_user_by_login(data.login, session):
            logger.warning(f"Signup attempt with existing login: {data.login}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this login already exists"
            )
        logger.info(f"New user registered: {data.password}")
        user = User(
            password=hash_password(data.password),
            login=data.login,
            name=data.name,
            role=Roles.User,
        )
        UserRepository.create_user(user, session)
        BalanceRepository.add_balance(user.id, session)
        logger.info(f"New user registered: {data.name}")
        return {"message": "User successfully registered"}

@auth_route.post(
    '/signin',
    status_code=status.HTTP_200_OK,
    summary="User Authentification",
    description="Register a new user with name, login and password")
async def signin(data: AuthSignup, session=Depends(get_session)):
    user =  UserRepository.get_user_by_login(data.login, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    return {"message": "User successfully logged in"}
