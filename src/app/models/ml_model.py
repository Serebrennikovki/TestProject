# from decimal import Decimal
#
# class MlModel:
#     def __init__(self, id_model, name, description, price, method):
#         self._id: int = id_model
#         self._name: str = name
#         self._description: str = description
#         self._price: Decimal = price
#         self._method_execution: str = method
#
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