from flask import redirect
from . import error_handler


@error_handler.app_errorhandler(401)
def unauthorized_error(*_):
    return redirect('/login')


@error_handler.app_errorhandler(404)
def unauthorized_error(*_):
    return '<h1>404 Not Found </h1>'
