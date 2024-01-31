from flask import Flask, render_template, session, redirect
from flask_session import Session
from database import connection

app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = connection("farm.db")


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/register")
def register():
    pass


@app.route("/login")
def login():
    pass


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
