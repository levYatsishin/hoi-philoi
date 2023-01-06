import time

from postgres_api import DBApi
from images_api import ImageApi
import datetime
import os

DB_PASSWORD = os.environ["POSTGRES_PASS"]
DB_IP = os.environ["POSTGRES_IP"]

MINIO_API_HOST = os.environ["POSTGRES_IP"] + ":9000"
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]

if __name__ == "__main__":
    db_api = DBApi()
    db_api2 = DBApi()
    db_api.connect(DB_IP, '5432', 'postgres', 'admin', DB_PASSWORD)
    db_api3 = DBApi()

    print(f"Singleton is working: {db_api is db_api3}")

    image_api = ImageApi()
    image_api.connect(MINIO_API_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)

    # with open('../mushrooms.jpg', 'rb') as file:
    #     size = os.stat('../mushrooms.jpg').st_size
    #     image_api.upload_image(file, 'mushrooms.jpg', size)

    data = image_api.get_image("mushrooms.jpg")
    with open('downloaded_mushrooms.jpg', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
