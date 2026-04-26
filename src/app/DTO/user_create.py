from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    login: str
    password: str
    name: str

    @field_validator('login')
    @classmethod
    def validate_login(cls, value):
        if value == '':
            raise ValueError('Поле login не может быть пустым')
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if value == '':
            raise ValueError('Поле password не может быть пустым')
        return value

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        if value == '':
            raise ValueError('Поле name не может быть пустым')
        return value
