from blocks.ElectricalPart import ElectricalPart
from blocks.Vendor import Vendor


class VendorItem:
    def __init__(self, item: ElectricalPart, vendor: Vendor, unit_price: float, tax_percent: float):
        self.item = item
        self.vendor = vendor
        self.unit_price = unit_price
        self.tax_percent = tax_percent

    def __repr__(self):
        return f"{self.item} at the rate of {self.unit_price}"

    # def get_unit_price(self):
    #     return self.unit_price

    # def part_matches(self, part: ElectricalPart):
    #     return self if part == self.item else None

    def calculate_price(self, quantity: int):
        return self.unit_price * (1 + self.tax_percent/100) * quantity
