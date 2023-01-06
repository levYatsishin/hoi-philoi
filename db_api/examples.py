import time

from postgres_api import PostgresApi
from images_api import ImageApi
import datetime
import os

DB_PASSWORD = os.environ["POSTGRES_PASS"]
DB_IP = os.environ["POSTGRES_IP"]

MINIO_API_HOST = os.environ["POSTGRES_IP"] + ":9000"
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]

if __name__ == "__main__":
    db_api = PostgresApi()
    db_api2 = PostgresApi()
    db_api.connect(DB_IP, '5432', 'postgres', 'admin', DB_PASSWORD)
    db_api3 = PostgresApi()

    print(f"Singleton is working: {db_api is db_api3}")
    print(db_api3.get_user_by(u_id_user=13))
    db_api.close_connection()

    image_api = ImageApi()
    image_api.connect(MINIO_API_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)

    # with open('../mushrooms.jpg', 'rb') as file:
    #     size = os.stat('../mushrooms.jpg').st_size
    #     image_api.upload_image(file, 'mushrooms.jpg', size)

    data = image_api.get_image("mushrooms.jpg")
    with open('downloaded_mushrooms.jpg', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
