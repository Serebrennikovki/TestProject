from datetime import datetime
from decimal import Decimal
from src.app.enums.transaction_status import *
from src.app.enums.transaction_type import *

class Transaction:

    def __init__(self,
                 transaction_type,
                 transaction_date,
                 transaction_amount,
                 transaction_cost,
                 transaction_status):
        self._type: TransactionType = transaction_type
        self._date: datetime = transaction_date
        self._amount: int = transaction_amount
        self._cost: Decimal = transaction_cost
        self._status: TransactionStatus = transaction_status


    @property
    def type(self):
        return self._type

    @property
    def date(self):
        return self._date

    @property
    def amount(self):
        return self._amount

    @property
    def cost(self):
        return self._cost

    @property
    def status(self):
        return self._status


    def change_status(self, new_status: TransactionStatus):
        self._status = new_status