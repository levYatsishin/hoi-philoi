from matcher import Matcher
from db_api import PostgresApi

from dotenv import load_dotenv
import os

load_dotenv()

DB_PASSWORD = os.getenv("POSTGRES_PASS")
DB_IP = os.getenv("POSTGRES_IP")
postgres_conf = {'db_host': DB_IP, 'db_port': '5432', 'db_name': 'postgres', 'db_user': 'admin',
                 'db_pass': DB_PASSWORD}

postgres_api = PostgresApi()
postgres_api.connect(**postgres_conf)

matcher = Matcher(postgres_api)

user = postgres_api.get_user_by('username', 'leo')

matched_users = matcher.get_matching_users(user)
print(matched_users)

postgres_api.close_connection()
