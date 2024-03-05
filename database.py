import sqlite3

__db_url = "farm.db"


def connection() -> sqlite3.Connection:
    con = sqlite3.connect(__db_url)
    con.row_factory = sqlite3.Row
    return con


def get_username(db: sqlite3.Connection, user_id: str) -> str:
    row = db.execute(
        "SELECT username FROM users WHERE id = (?);", (user_id,)).fetchone()
    return row[0]


def get_animal_count(db: sqlite3.Connection, user_id) -> str:
    row = db.execute(
        "SELECT COUNT(name) FROM animals WHERE user_id = (?);", (user_id,)).fetchone()
    return row[0]


def get_avg_prod(db: sqlite3.Connection, user_id: str) -> str:
    row = db.execute(
        "SELECT AVG(prod) FROM production WHERE user_id = (?);", (user_id,)).fetchone()
    return row[0]
