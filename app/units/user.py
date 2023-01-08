from flask_login import UserMixin

__all__ = ['User']


class User(UserMixin):
    def __init__(self, data: dict) -> None:
        self.__data: dict = data

    def get_id(self) -> int:
        return self.__data['u_id']

    def get_data(self):
        return self.__data
