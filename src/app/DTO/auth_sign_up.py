from pydantic import BaseModel, ValidationError, field_validator


class AuthSignup(BaseModel):
    login: str
    password: str

    @field_validator('login')
    @classmethod
    def validate_login(cls, value):
        if value == '':
            raise ValidationError('Поле login не может быть пустым')
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if value == '':
            raise ValidationError('Поле password не может быть пустым')
        return value