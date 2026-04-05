from decimal import Decimal

class MlModel:
    def __init__(self, id_model, name, description, price, method):
        self._id: int = id_model
        self._name: str = name
        self._description: str = description
        self._price: Decimal = price
        self._method_execution: str = method

    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def method(self):
        return self._method_execution