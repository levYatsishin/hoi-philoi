import time

from images_api import ImageApi
from postgres_api import PostgresApi
import datetime
import os

DB_PASSWORD = os.environ["POSTGRES_PASS"]
DB_IP = os.environ["POSTGRES_IP"]

MINIO_API_HOST = os.environ["POSTGRES_IP"] + ":9000"
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]

postgres_conf = {'db_host': DB_IP, 'db_port': '5432', 'db_name': 'postgres', 'db_user': 'admin',
                 'db_pass': DB_PASSWORD}
minio_conf = {'address': MINIO_API_HOST, 'access_key': MINIO_ACCESS_KEY, 'secret_key': MINIO_SECRET_KEY}

if __name__ == "__main__":
    postgres_api = PostgresApi()
    image_api = ImageApi()

    postgres_api.connect(**postgres_conf)
    image_api.connect(**minio_conf)

    print(postgres_api.get_user_by('u_id', 1))
    postgres_api.create_post()

    # with open('../mushrooms.jpg', 'rb') as file:
    #     size = os.stat('../mushrooms.jpg').st_size
    #     image_api.upload_image(file, 'mushrooms.jpg', size)

    data = image_api.get_image("mushrooms.jpg")
    with open('downloaded_mushrooms.jpg', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)

    postgres_api.close_connection()
