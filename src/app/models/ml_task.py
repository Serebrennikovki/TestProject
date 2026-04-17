from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from .enums import TaskStatus

class MlTask(SQLModel, table=True):
    __tablename__ = "ml_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    input_data:str
    answer:Optional[str]
    status: TaskStatus
    price: Decimal
    user_id: int = Field(default=None, foreign_key='users.id')