import sqlite3

__db_url = "farm.db"


def connection() -> sqlite3.Connection:
    con = sqlite3.connect(__db_url)
    con.row_factory = sqlite3.Row
    return con
