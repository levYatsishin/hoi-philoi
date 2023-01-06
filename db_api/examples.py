import time

from DBApi import DBApi
import datetime
import os

DB_PASSWORD = os.environ["POSTGRES_PASS"]
DB_IP = os.environ["POSTGRES_IP"]

MINIO_API_HOST = os.environ["POSTGRES_IP"] + ":9000"
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]

if __name__ == "__main__":
    postgres_conf = {'db_host': DB_IP, 'db_port': '5432', 'db_name': 'postgres', 'db_user': 'admin',
                     'db_pass': DB_PASSWORD}
    minio_conf = {'address': MINIO_API_HOST, 'access_key': MINIO_ACCESS_KEY, 'secret_key': MINIO_SECRET_KEY}

    db_api = DBApi()
    db_api.connect(postgres_conf, minio_conf)
    db_api2 = DBApi()

    print(f"Singleton is working: {db_api is db_api2}")
    print(db_api.get_user_by(u_id_user=1))

    # with open('../mushrooms.jpg', 'rb') as file:
    #     size = os.stat('../mushrooms.jpg').st_size
    #     image_api.upload_image(file, 'mushrooms.jpg', size)

    data = db_api.get_image("mushrooms.jpg")
    with open('downloaded_mushrooms.jpg', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)

    db_api.close_connection()
