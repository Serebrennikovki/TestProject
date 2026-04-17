from pydantic import BaseModel


class UserResponse(BaseModel):
    login: str
    name: str
    role: str