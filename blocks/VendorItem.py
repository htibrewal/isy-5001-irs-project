from blocks.ElectricalPart import ElectricalPart
from blocks.Vendor import Vendor


class VendorItem:
    def __init__(self, item: ElectricalPart, vendor: Vendor, unit_price: float, tax_percent: float, delivery_days: int):
        self.item = item
        self.vendor = vendor
        self.unit_price = unit_price
        self.tax_percent = tax_percent
        self.delivery_days = delivery_days

    def __repr__(self):
        return f"{self.item.name} | Price = {self.unit_price: .2f} | Delivery Days = {self.delivery_days}"

    def __eq__(self, other):
        return hasattr(other, 'item') and hasattr(other, 'vendor') and self.item == other.item and self.vendor == other.vendor

    def calculate_price(self, quantity: int):
        return self.unit_price * (1 + self.tax_percent/100) * quantity

    def get_delivery_days(self):
        return self.delivery_days
