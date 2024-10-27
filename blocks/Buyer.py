class Buyer:
    def __init__(self, name: str, delivery_location: str, latitude: float = None, longitude: float = None):
        self.name = name
        self.delivery_location = delivery_location
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return self.name
