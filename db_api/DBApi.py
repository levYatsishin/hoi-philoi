from postgres_api import PostgresApi
from images_api import ImageApi
from db_api.patterns import Singleton


class DBApi(metaclass=Singleton):
    def __init__(self) -> None:
        self._conn = None
        self._cursor = None
