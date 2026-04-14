from typing import Optional

from sqlmodel import SQLModel, Field
from .enums import Roles

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    login: str = Field(default=None, index=True)
    password: str
    name:Optional[str] = None
    role: Roles