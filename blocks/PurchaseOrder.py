from blocks.Buyer import Buyer
from blocks.LineItem import LineItem


class PurchaseOrder:
    def __init__(self, line_items: list[LineItem], buyer: Buyer = None):
        self.line_items = line_items
        self.buyer = buyer

    def __repr__(self):
        return f"PurchaseOrder of size: {len(self.line_items)}"

