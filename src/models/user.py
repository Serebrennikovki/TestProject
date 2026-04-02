from src.enums.roles import Roles

class User:
    def __init__(self, user_id, login, password, name, role):
        self._id: int = user_id
        self._login: str = login
        self.__password: str = password
        self._name: str = name
        self._role: Roles = role


    @property
    def login(self):
        return self._login

    @property
    def name(self):
        return self._name

    @property
    def role(self):
        return self._role

    def change_password(self, password: str):
        self.__password = password

    def change_role(self, role: Roles):
        self._role = role

    def change_name(self, name: str):
        self._name = name

    def change_login(self, login: str):
        self._login = login