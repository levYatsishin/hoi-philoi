from os.path import isfile
from secrets import token_hex

from flask import Flask
from flask_login import LoginManager

from auth import auth_app
from errors import error_handler
from website import web_app

from db_api import DBApi
from api_config import api_config

__all__ = ['App']


class App:
    def __init__(self, secret_key_path='secret_key'):
        self.flask: Flask = Flask(__name__)

        if not isfile(secret_key_path):
            with open(secret_key_path, 'w') as file:
                file.write(token_hex(16))

        with open(secret_key_path) as file:
            secret_key = file.read()

        self.flask.config["SECRET_KEY"] = secret_key
        self.flask.threaded = True

        self.flask.register_blueprint(auth_app)
        self.flask.register_blueprint(error_handler)
        self.flask.register_blueprint(web_app)

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.flask)

        self.api = DBApi()
        self.api.connect(*api_config)

        @self.login_manager.user_loader
        def user_loader(user_id):
            from units import User
            return User(self.api.get_user_by(u_id_user=user_id))

    def run(self, host='0.0.0.0', debug=False, port=4000):
        self.flask.run(host=host, debug=debug, port=port)
