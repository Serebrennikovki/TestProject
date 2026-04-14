from typing import Optional

from sqlmodel import SQLModel, Field
from decimal import Decimal


class MLModel(SQLModel, table=True):
    __tablename__ = "ml_models"

    id: Optional[int] = Field(default=None, primary_key=True)
    name:str
    description:str
    method_execution:str
    price: Decimal