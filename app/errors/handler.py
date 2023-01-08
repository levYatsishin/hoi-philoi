from flask import redirect, render_template
from . import error_handler


@error_handler.app_errorhandler(401)
def unauthorized_error(*_):
    return redirect('/login')


@error_handler.app_errorhandler(404)
def unauthorized_error(*_):
    return render_template('errors/404.html')
