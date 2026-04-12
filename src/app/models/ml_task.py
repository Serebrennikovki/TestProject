# from src.app.enums.task_status import TaskStatus
# from src.app.models.ml_model import MlModel
# from src.app.models.user import User
#
#
#     def change_status(self, status: TaskStatus):
#         self._status = status
from typing import Optional

from sqlmodel import SQLModel, Field
from .enums import TaskStatus
from .ml_model import MLModel
from .user import User


class MlTask(SQLModel, table=True):
    __tablename__ = "ml_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    input_data:str
    launch_method: str
    status: TaskStatus
    ml_model: int = Field(default=None, foreign_key='ml_models.id')
    user: int = Field(default=None, foreign_key='users.id')