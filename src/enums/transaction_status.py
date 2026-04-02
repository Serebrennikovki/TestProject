from enum import Enum


class TransactionStatus(Enum):
    New = 1
    Waiting = 2
    InProgress = 3
    Done = 4
    Canceled = 5
