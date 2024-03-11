from sqlite3 import Connection


class Farm:
    id: int
    user_id: int
    name: str
    country: str
    location: str

    def __init__(self, data):
        self.id = data[0]
        self.user_id = data[1]
        self.name = data[2]
        self.country = data[3]
        self.location = data[4]


class Cow:
    uuid: str
    id: int
    name: str
    birthday: str

    def __init__(self, row):
        self.uuid = row[0]
        self.id = row[1]
        self.name = row[2]
        self.birthday = row[3]


class Production:

    @staticmethod
    def _prod_from_row(rows):
        prod = []
        for r in rows:
            entry = {'date': r[2]}
            total_prod = float(r[0])
            entry['prod'] = total_prod
            entry['day_period'] = r[1]
            prod.append(entry)

        return prod

    @staticmethod
    def get_from(db: Connection, animal_uuid: str):
        rows = db.execute(
            "SELECT prod, day_period, date FROM production "
            "WHERE a_uuid = (?);",
            (animal_uuid,)).fetchall()
        return Production._prod_from_row(rows)

    @staticmethod
    def get_all(db: Connection, user_id: str):
        rows = db.execute(
            "SELECT prod, day_period, date FROM production "
            "WHERE user_id=(?);",
            (user_id,)).fetchall()

        return Production._prod_from_row(rows)

    @staticmethod
    def avg_per_animal(db: Connection, user_id: str):
        rows = db.execute(
            "SELECT animals.name, AVG(production.prod) FROM production "
            "JOIN animals ON animals.uuid = production.a_uuid "
            "WHERE production.user_id=(?) "
            "GROUP BY animals.uuid;",
            (user_id,)).fetchall()
        prod = []
        for row in rows:
            p = {"name": row[0], "avg": row[1]}
            prod.append(p)
        return prod

    def get_prod_per_day(db: Connection, user_id: str):
        rows = db.execute(
            "SELECT animals.name, animals.a_id, "
            "production.prod, production.date FROM production "
            "JOIN animals ON animals.uuid = production.a_uuid "
            "WHERE production.user_id=(?);"
            (user_id,)).fetchall()
        animals = {}
        for row in rows:
            a_name = row[0]
            prod = row[2]
            if a_name in animals:
                animals[a_name]
