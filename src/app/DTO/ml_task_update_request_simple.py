from typing import Optional

from pydantic import BaseModel, field_validator

class MlTaskUpdateRequestSimple(BaseModel):
    id: int
    answer: Optional[str]


    @field_validator('id')
    @classmethod
    def validate_id(cls, value):
        if value < 0:
            raise ValueError('Поле id не может быть отрицательным')
        return value
