from src.enums.task_status import TaskStatus
from src.models.ml_model import MlModel
from src.models.user import User

class MlTask:
    def __init__(self, id_task, input_data, launch_method, status, model, user):
        self._id: int = id_task
        self._input_data: str = input_data
        self._launch_method: str = launch_method
        self._status: TaskStatus = status
        self._ml_model: MlModel = model
        self._user: User = user

    @property
    def id(self):
        return self._id

    @property
    def input_data(self):
        return self._input_data

    @property
    def launch_method(self):
        return self._launch_method

    @property
    def status(self):
        return self._status

    @property
    def model(self):
        return self._ml_model

    @property
    def user(self):
        return self._user

    def change_status(self, status: TaskStatus):
        self._status = status