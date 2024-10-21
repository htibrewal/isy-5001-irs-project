class Vendor:
    def __init__(self, id: str, name: str, location: str = None, latitude: float = None, longitude: float = None):
        self.id = id
        self.name = name
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"{self.name} ({self.location})" if self.location is not None else self.name
