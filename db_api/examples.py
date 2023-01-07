from db_api import ImageApi
from postgres_api import PostgresApi
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("POSTGRES_PASS")
DB_IP = os.getenv("POSTGRES_IP")
MINIO_API_HOST = os.getenv("POSTGRES_IP") + ":9000"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

postgres_conf = {'db_host': DB_IP, 'db_port': '5432', 'db_name': 'postgres', 'db_user': 'admin',
                 'db_pass': DB_PASSWORD}
minio_conf = {'address': MINIO_API_HOST, 'access_key': MINIO_ACCESS_KEY, 'secret_key': MINIO_SECRET_KEY}

if __name__ == "__main__":
    postgres_api = PostgresApi()
    image_api = ImageApi()

    postgres_api.connect(**postgres_conf)
    image_api.connect(**minio_conf)

    postgres_api.create_user({'name': "Иван Ларин", 'username': "larin", 'mail': "l@l.ru", 'password_hash': "pass"})
    postgres_api.create_event({'u_id_user': 1, 'content': "Встреча", 'publication_date': datetime.now(),
                               'time_start': datetime.now(), 'time_end': datetime.now(), 'location': "Головинка"})

    postgres_api.create_post({'u_id_user': 1, 'content': 'hi', 'publication_date': datetime.now()})
    postgres_api.change_like_state(1, 1)
    print(postgres_api.get_user_by('u_id', 1)['tags'])

    print(postgres_api.get_users_by_tags(['gay']))

    # data = image_api.get_image("mushrooms.jpg")
    # with open('downloaded_mushrooms.jpg', 'wb') as file_data:
    #     for d in data.stream(32*1024):
    #         file_data.write(d)

    postgres_api.close_connection()
