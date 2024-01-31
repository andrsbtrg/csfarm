import sqlite3


def connection(arg: str) -> sqlite3.Cursor:
    con = sqlite3.connect(arg)
    cur = con.cursor()
    return cur
