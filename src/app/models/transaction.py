from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field

from .enums import TransactionStatus, TransactionType


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: TransactionType
    date: datetime
    cost: Decimal
    status: TransactionStatus
    user_id: int = Field(default=None, foreign_key='users.id')