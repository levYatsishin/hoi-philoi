from secrets import token_hex

from flask import Flask
from flask_login import LoginManager

from website import web_app
from auth import auth_app

from db_api import DBApi
from api_config import api_config

__all__ = ['App']


class App:
    def __init__(self):
        self.flask: Flask = Flask(__name__)
        self.flask.config["SECRET_KEY"] = token_hex(16)
        self.flask.threaded = False  # True

        self.flask.register_blueprint(web_app)
        self.flask.register_blueprint(auth_app)

        login_manager = LoginManager()
        login_manager.init_app(self.flask)

        @login_manager.user_loader
        def user_loader(user_id):
            from units import User
            return User(user_id)

        DBApi(*api_config)

    def run(self, host='0.0.0.0', debug=False, port=4000):
        self.flask.run(host=host, debug=debug, port=port)
