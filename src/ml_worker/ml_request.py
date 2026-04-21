from pydantic import BaseModel

class MlRequest(BaseModel):
    model: str
    prompt: str