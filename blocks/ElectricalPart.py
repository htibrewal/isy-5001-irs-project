class ElectricalPart:
    def __init__(self, id: str, name: str, width: float = None, height: float = None, depth: float = None, weight: float = None, description: str = None):
        self.id = id
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.description = description
        self.vendors_dict = {}

    def __repr__(self):
        return f"{self.id} | {self.name}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return hasattr(other, 'id') and self.id == other.id
