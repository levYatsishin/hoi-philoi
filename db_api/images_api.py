from minio import Minio
from loguru import logger
import traceback

from .patterns import Singleton


class ImageApi(metaclass=Singleton):
    def __init__(self):
        self._minio_client = None

    def connect(self, address, access_key, secret_key):
        self._minio_client = Minio(address, access_key=access_key, secret_key=secret_key, secure=False)

    def upload_image(self, image_data: any, image_name: str, size: int) -> str | None:
        """
        This function uploads image

        :return: If successful returns name of uploaded image else None
        """

        try:
            self._minio_client.put_object('images', image_name, image_data, size)
            return str(image_name)

        except Exception as e:
            logger.error(f"Error: {e}\n Traceback: {traceback.format_exc()}")
            return None

    def get_image(self, image_name: str) -> bytes | None:
        """
        This function returns image from minio db by link

        :param image_name: Image name in minio db
        :return: Image to render
        """

        try:
            data = self._minio_client.get_object('images', image_name)
            return data

        except Exception as e:
            logger.error(f"Error: {e}\n Traceback: {traceback.format_exc()}")
            return None
