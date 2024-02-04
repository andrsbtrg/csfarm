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
    id: int
    name: str
    age: float
    data: float

    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.age = row[2]
        self.data = 3.14
