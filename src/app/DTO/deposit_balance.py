from decimal import Decimal

from pydantic import BaseModel, ValidationError, field_validator


class DepositBalance(BaseModel):
    user_login: str
    amount: Decimal

    @field_validator('user_login')
    @classmethod
    def validate_login(cls, value):
        if value == '':
            raise ValidationError('Поле user_login не может быть пустым')
        return value

    @field_validator('amount')
    @classmethod
    def validate_password(cls, value):
        if value <= 0:
            raise ValidationError('Поле amount должно быть положительным')
        return value