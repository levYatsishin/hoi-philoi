from flask import Flask

__all__ = []

app: Flask = Flask(__name__)

app.config['secret_key'] = 'Very secret key'

app.threaded = True


@app.route('/')
def index() -> str:
    return 'Hello world!'


app.run(host='0.0.0.0', debug=True, port=4000)
