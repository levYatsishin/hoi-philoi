import atexit

from dotenv import dotenv_values
from flask import Flask
from flask_login import LoginManager

from app.auth import auth_app
from app.errors import error_handler
from app.website import web_app
from db_api import PostgresApi

__all__ = ['App']


class App:
    def __init__(self):
        self.flask: Flask = Flask(__name__)

        config = dotenv_values('.env')

        self.debug = True if config['DEBUG'] == 'true' else False

        self.flask.config["SECRET_KEY"] = config['SECRET_KEY']
        self.flask.threaded = True

        self.flask.register_blueprint(auth_app)
        self.flask.register_blueprint(error_handler)
        self.flask.register_blueprint(web_app)

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.flask)

        self.api = PostgresApi()
        self.api.connect(config['db_ip'], config['db_port'], config['db_name'], config['db_user'], config['db_pass'])

        atexit.register(self.stop)

        @self.login_manager.user_loader
        def user_loader(user_id):
            from app.units import User
            print(user_id, type(user_id))
            return User(self.api.get_user_by('u_id', user_id))

    def run(self, host='0.0.0.0', port=4000):
        self.flask.run(host=host, debug=self.debug, port=port)

    @staticmethod
    def stop():
        PostgresApi().close_connection()
