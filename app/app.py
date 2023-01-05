from secrets import token_hex
from flask import Flask
from flask_login import LoginManager

from db_api import DBApi

from website import web_app
from auth import auth_app

__all__ = []


class App:
    def __init__(self):
        self.flask: Flask = Flask(__name__)
        self.flask.config["SECRET_KEY"] = token_hex(16)
        self.flask.threaded = True

        self.flask.register_blueprint(web_app)
        self.flask.register_blueprint(auth_app)

        login_manager = LoginManager()
        login_manager.init_app(self.flask)

        @login_manager.user_loader
        def user_loader(user_id):
            from units import User
            return User(user_id)

        DBApi()

    def run(self, host='0.0.0.0', debug=False, port=4000):
        self.flask.run(host=host, debug=debug, port=port)


app = App()

app.run(debug=True)
