from enum import Enum

class Roles(Enum):
    User = 1
    Administrator = 2

class TaskStatus(Enum):
    New = 1
    Waiting = 2
    InProgress = 3
    Completed = 4
    Canceled = 5

class TransactionType(Enum):
    Credit = 1
    Debit = 2
    Refund = 3

class TransactionStatus(Enum):
    New = 1
    Waiting = 2
    InProgress = 3
    Done = 4
    Canceled = 5