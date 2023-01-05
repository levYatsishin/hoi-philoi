from os import environ

api_config = [environ["POSTGRES_IP"], 5432, 'postgres', 'admin', environ["POSTGRES_PASS"]]
