from flask import session, redirect, render_template, make_response
from functools import wraps


def hx_redirect(path: str):
    resp = make_response()
    resp.headers['HX-Redirect'] = path
    return resp


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def alert(message: str):
    return render_template("flash_message.html", message=message)
