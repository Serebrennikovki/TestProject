from pydantic import field_validator, BaseModel


class MlTaskCreateRequest(BaseModel):
    input_data: str
    user_login: str

    @field_validator('input_data')
    @classmethod
    def validate_input_data(cls, value):
        if value == '':
            raise ValueError('Поле input_data не может быть пустым')
        return value

    @field_validator('user_login')
    @classmethod
    def validate_password(cls, value):
        if value == '':
            raise ValueError('Поле user_login не может быть пустым')
        return value
