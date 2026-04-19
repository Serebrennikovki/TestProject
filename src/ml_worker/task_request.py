from pydantic import ValidationError, BaseModel, field_validator

class TaskRequest(BaseModel):
    input_data: str
    id: int


    @field_validator('id')
    @classmethod
    def validate_id(cls, value):
        if value < 0:
            raise ValidationError('Поле id не может быть отрицательным')
        return value

    @field_validator('input_data')
    @classmethod
    def validate_id(cls, value):
        if value == '':
            raise ValidationError('Поле input_data не может быть пустым')
        return value