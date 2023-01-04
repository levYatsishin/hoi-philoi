from flask import Flask
# from flask_login import LoginManager

from db_api import DBApi

__all__ = []

app: Flask = Flask(__name__)

app.config['secret_key'] = 'Very secret key'

app.threaded = True

# login_manager = LoginManager()
# login_manager.init_app(app)

api = DBApi()


@app.route('/')
def index() -> str:
    return 'Hello world!'


app.run(host='0.0.0.0', debug=True, port=4000)
