from flask import Markup, render_template, request
from werkzeug.exceptions import HTTPException, default_exceptions


def errorHandler(error):
    if isinstance(error, HTTPException):
        msg = Markup(error.get_description(request.environ))
        code = error.code
        name = error.name
    else:
        msg = ("We encountered an error while trying to fulfill your request")
        code = 500
        name = 'Internal Server Error'

    return render_template([f"errors/{code}.html", "errors/500.html"], title=f"{code} - {name}", code=code, msg=msg)


def init(app):
    for exception in default_exceptions:
        app.register_error_handler(exception, errorHandler)

    app.register_error_handler(Exception, errorHandler)
