from blocks.Vendor import Vendor
from blocks.VendorItem import VendorItem


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

    # def add_vendor(self, vendor: Vendor, unit_price: float, tax_percent: float) -> None:
    #     self.vendors_dict[vendor.name] = VendorItem(self, vendor, unit_price, tax_percent)
