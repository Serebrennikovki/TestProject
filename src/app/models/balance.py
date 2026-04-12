# from src.app.models.user import User
# from decimal import Decimal
#
#
# class Balance:
#     def __init__(self, user: User):
#         self._user: User = user
#         self.__balance: Decimal = Decimal(0)
#

from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


class Balance(SQLModel, table=True):
    __tablename__ = "balances"

    id: Optional[int] = Field(default=None, primary_key=True)
    balance: Decimal = Field(default=0, nullable=False)
    user_id: int = Field(default=None, foreign_key='users.id', index=True)