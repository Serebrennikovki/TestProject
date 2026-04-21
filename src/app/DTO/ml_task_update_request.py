from .ml_task_update_request_simple import MlTaskUpdateRequestSimple

from models.enums import TaskStatus


class MlTaskUpdateRequest(MlTaskUpdateRequestSimple):
    status: TaskStatus
