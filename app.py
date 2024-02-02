from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from database import connection
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import alert, hx_redirect

app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def hello():
    if session.get("user_id") is None:
        return redirect("/login")
    return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    db = connection()
    # handle post
    username = request.form.get("username")
    password = request.form.get("password")
    repass = request.form.get("repassword")

    # validations
    if len(username) < 5:
        return alert("Username is too short")
    if password != repass:
        return alert("Passwords don't match!")
    if len(password) < 8:
        return alert("Password is too short")
    db.execute(
        "INSERT INTO users (username, pass) VALUES (?, ?)",
        [username, generate_password_hash(password)]
    )
    db.commit()
    rows = db.execute("SELECT id FROM users WHERE username=(?)", [
                      username]).fetchall()
    user_id = rows[0][0]
    session["user_id"] = user_id
    resp = hx_redirect("/")
    return resp


@app.route("/register/email", methods=["POST"])
def validate_email():
    username = request.form.get("username")
    if len(username) < 5:
        return alert("Username is too short")
    return ""


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    # handle POST
    username = request.form.get("username")
    password = request.form.get("password")

    if len(username) == 0:
        return alert("Please enter a valid username.")
    if len(password) == 0:
        return alert("Please type a password")

    cur = connection().cursor()
    row = cur.execute(
        "SELECT id, username, pass FROM users WHERE username = (?)", (
            username,)
    ).fetchone()
    if row is None:
        return alert("Username does not exist")

    id = row[0]
    pwhash = row[2]
    if check_password_hash(pwhash, password) is False:
        return alert("Incorrect password")
    session["user_id"] = id

    return hx_redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")
