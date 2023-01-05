from flask_login import UserMixin

__all__ = ['User']


class User(UserMixin):
    def __init__(self, u_user_id) -> None:
        self.__u_user_id = u_user_id

    def get_id(self) -> int:
        return self.__u_user_id
