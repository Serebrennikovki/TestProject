import logging
from services.repositories import user as UserRepository

from fastapi import APIRouter, Depends, HTTPException,status
from DTO.user_response import UserResponse
from database.database import get_session

# Configure logging
logger = logging.getLogger(__name__)

user_route = APIRouter()

@user_route.get(
    "/{user_login}",
    status_code = status.HTTP_200_OK,
    response_model = UserResponse)
async def get_user(user_login: str, session=Depends(get_session)) -> UserResponse:
    user = UserRepository.get_user_by_login(user_login, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    userResponse = UserResponse(
        login=user.login,
        name=user.name,
        role=user.role)
    return userResponse