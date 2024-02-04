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
