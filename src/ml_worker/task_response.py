from typing import Optional
from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: int
    answer: Optional[str]