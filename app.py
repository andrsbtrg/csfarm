from flask import Flask, render_template, session, redirect, request, jsonify
from flask_session import Session
from database import connection
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import alert, hx_redirect, search_places, requires_login, format_day_period
from datetime import datetime
from models import Farm, Cow, Production
from uuid import uuid4

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


@requires_login
@app.route("/farm", methods=["GET", "POST"])
def farm():
    db = connection()
    user_id = session["user_id"]
    if request.method == "GET":
        row = db.execute(
            "SELECT * from farms where user_id = (?)", (user_id,)).fetchone()
        if row is None:
            countries = []
            with open("countries.txt") as file:
                for line in file.readlines():
                    countries.append(line.strip())
            return render_template("farm_new.html", countries=countries)
        farm = Farm(row)
        return render_template("farm.html", farm=farm)

    # handle post
    name = request.form.get("farm-name")
    if len(name) == 0:
        return alert("Farm name cannot be empty")
    country = request.form.get("country")
    location = request.form.get("location")
    created_at = datetime.now()
    values = (user_id, name, country, location, created_at)
    db.execute(
        "INSERT INTO farms (user_id, name, country, location, created_at)"
        "VALUES (?, ?, ?, ?, ?);",
        values)
    db.commit()
    return hx_redirect("/farm")


@requires_login
@app.route("/farm/locate", methods=["POST"])
def find_locations():
    country = request.form.get("country")
    location = request.form.get("location")
    locations = []
    if country != "" and len(location) > 3:
        locations = search_places(country, location)
    print(locations)
    return render_template("location_input.html", locations=locations)


@requires_login
@app.route("/animals", methods=["GET", "POST"])
def animals():
    if request.method == "GET":
        db = connection()
        user_id = session["user_id"]
        rows = db.execute(
            "SELECT uuid, a_id, name, birthday, img FROM animals "
            "WHERE user_id = (?)",
            (user_id,)).fetchall()
        cows = []
        for row in rows:
            cow = Cow(row)
            cows.append(cow)
        return render_template("animals.html", cows=cows)
    # handle post
    a_id = request.form.get("tag")
    name = request.form.get("name")
    birthday = request.form.get("birthday")
    if birthday == "":
        birthday = datetime.now().date()
    user_id = session["user_id"]
    # verify tag doesnt exist
    db = connection()
    tags = db.execute(
        "SELECT a_id, name FROM animals "
        "WHERE user_id=(?);", (user_id,)).fetchall()
    for tag in tags:
        if str(tag[0]) == a_id:
            return alert(f"This tag is already used by {tag[1]} ")
    uid = uuid4().__str__()
    data = (uid, a_id, user_id, name, birthday)
    db.execute(
        "INSERT INTO animals "
        "(uuid, a_id, user_id, name, birthday, created_at, modified_at)"
        "VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'));",
        data)
    db.commit()
    return hx_redirect("/animals")


@requires_login
@app.route("/milk", methods=["GET", "POST"])
def milk():
    if request.method == "GET":
        return render_template("milk.html")
    # handle post
    db = connection()
    user_id = session["user_id"]

    dt = request.form.get("date")
    ampm = request.form.get("ampm")
    name = request.form.get("name")
    if name == "":
        return alert("Cow name shoudn't be empty")
    row = db.execute(
        "SELECT uuid, a_id, name, birthday, img FROM animals "
        "WHERE user_id = (?) AND name = (?)",
        (user_id, name)).fetchone()
    cow = Cow(row)

    # check if already been milked
    milked = db.execute(
        "SELECT modified_at FROM production "
        "WHERE a_uuid = (?)"
        "AND day_period = (?)"
        "AND date = (?)", (cow.uuid, ampm, dt,)
    ).fetchall()
    if len(milked) > 0:
        print(milked)
        return alert(
            f"{cow.name} was already milked on {
                format_day_period(ampm)} {dt}: "
            f"Updated at {milked[0][0]}"
        )
    return render_template("milk_row.html", cow=cow, datetime=dt, ampm=ampm)


@app.route("/milk/record", methods=["POST"])
def record_milk():
    known_keys = ["datetime", "day-period"]
    datetime = request.form.get(known_keys[0])
    day_period = request.form.get(known_keys[1])
    user_id = session["user_id"]

    prods = {}
    for key in request.form:
        if key not in known_keys:
            animal_id = key.split('.')[1]
            prods[animal_id] = request.form[key]

    data = []
    for key in prods:
        record = []
        record.append(user_id)
        record.append(key)
        a_production = float(prods[key])
        record.append(a_production)
        record.append(day_period)
        record.append(datetime)

        data.append(tuple(record))

    db = connection()
    for x in data:

        db.execute(
            "INSERT INTO production ("
            "user_id, a_uuid, prod, day_period, date, created_at, modified_at)"
            "VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now') )",
            x)
    db.commit()
    return render_template("milk_table.html")


@requires_login
@app.route("/analytics", methods=["GET"])
def analytics():
    animal = request.args.get("id", None)
    return render_template("analytics.html", animal=animal)


@requires_login
@app.route("/get_barchart_data")
def get_barchart_data():
    """
    JSON
    """
    id = request.args.get("id", None)
    user_id = session["user_id"]
    db = connection()
    if id is None:
        prod = Production.get_all(db, user_id)
    else:
        row = db.execute(
            "SELECT uuid FROM animals WHERE a_id=(?) AND user_id=(?);",
            (id, user_id,)).fetchone()
        if row is None:
            prod = []
        else:
            a_uuid = row[0]
            prod = Production.get_from(db, a_uuid)
    prod.sort(key=lambda x: x["date"])
    return jsonify(prod)


@requires_login
@app.route("/get_avg_per_animal")
def get_avg_per_animal():
    id = request.args.get("id", None)
    user_id = session["user_id"]
    db = connection()
    prod = Production.avg_per_animal(db, user_id)
    prod.sort(key=lambda x: x["avg"], reverse=True)
    return jsonify(prod)


@requires_login
@app.route("/animals/search")
def search_animals():
    query = request.args.get("name")
    if query == "":
        return render_template("datalist.html", id="cows", elems=[])
    user_id = session["user_id"]

    db = connection()
    rows = db.execute(
        "SELECT name FROM animals WHERE name LIKE (?) AND user_id = (?)", (
            f"{query}%", user_id,)).fetchall()
    names = [row[0] for row in rows]
    return render_template("datalist.html", id="cows", elems=names)


@requires_login
@app.route("/animals/names")
def list_animals():
    db = connection()
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT a_id, name FROM animals WHERE user_id = (?)",
        (user_id,)).fetchall()
    names = [{"name": f"{row[0]} - {row[1]}", "value": row[1]} for row in rows]
    return render_template("datalist.html", id="cows", elems=names)


@requires_login
@app.route("/animals/ids")
def list_animals_ids():
    db = connection()
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT a_id, name FROM animals WHERE user_id = (?)",
        (user_id,)).fetchall()
    names = [{"name": f"{row[0]} - {row[1]}", "value": row[0]} for row in rows]
    return render_template("datalist.html", id="cowids", elems=names)
