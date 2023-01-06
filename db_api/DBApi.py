from loguru import logger

from postgres_api import PostgresApi
from images_api import ImageApi
from db_api.patterns import Singleton


class DBApi(metaclass=Singleton):
    def __init__(self) -> None:
        self.image_api = ImageApi()
        self.postgres_api = PostgresApi()

    def connect(self, postgres_config: dict, minio_config: dict) -> None:
        """
        Connects to all data bases

        :param postgres_config: postgres_config.keys() == (db_host, db_port, db_name, db_user, db_pass)
        :param minio_config: minio_config.keys() == (address, access_key, secret_key)
        :return:
        """

        logger.debug("DB: Connecting")
        self.image_api.connect(**minio_config)
        self.postgres_api.connect(**postgres_config)
        logger.debug("DB: Connected")

    def close_connection(self) -> None:
        """
        Closes all connections

        :return:
        """

        self.postgres_api.close_connection()

    # Minio DB Functions
    def upload_image(self, *args):
        return self.image_api.upload_image(*args)

    def get_image(self, *args):
        return self.image_api.get_image(*args)

    # Postgresql DB Functions
    def create_post(self, *args):
        return self.postgres_api.create_post(*args)

    def create_user(self, *args):
        return self.postgres_api.create_user(*args)

    def get_user_by(self, **kwargs):
        return self.postgres_api.get_user_by(**kwargs)

    def get_posts_by(self, **kwargs):
        return self.postgres_api.get_posts_by(**kwargs)

    def change_like_state(self, *args):
        return self.postgres_api.postgres_api(*args)

    def _drop_all_tables(self):
        return self.postgres_api.drop_all_tables()


