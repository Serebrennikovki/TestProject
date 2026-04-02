from src.models.user import User
from decimal import Decimal


class Balance:
    def __init__(self, user: User):
        self._user: User = user
        self.__balance: Decimal = Decimal(0)

    @property
    def user(self):
        return self._user

    @property
    def balance(self):
        return self.__balance

    def deposit(self, balance):
        self.__balance =  self.__balance + balance

    def check_balance_for_operation(self, credit_balance: Decimal):
        return self.__balance - credit_balance > 0