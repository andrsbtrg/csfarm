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
