from pydantic import BaseModel

class MlTaskQueueRequest(BaseModel):
    input_data: str
    id: int
