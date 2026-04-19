from typing import Optional
from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: int
    status: int
    answer: Optional[str]