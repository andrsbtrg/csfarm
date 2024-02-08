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
    resp = make_response(render_template(
        "flash_message.html", message=message))
    resp.headers['HX-Retarget'] = "#alerts"
    return resp


# def search_places(country: str, place: str) -> []:
#     nominatim = Nominatim()
#     result = nominatim.query(f"{place}, {country}")
#     json = result.toJSON()
#     if len(json) == 0:
#         return []
#     return json


def format_day_period(day_period):
    if day_period == "am":
        return "Morning"
    elif day_period == "pm":
        return "Afternoon"
    return "NA"
