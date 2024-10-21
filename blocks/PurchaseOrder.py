from blocks.Buyer import Buyer
from blocks.LineItem import LineItem


class PurchaseOrder:
    def __init__(self, line_items: list[LineItem], buyer: Buyer):
        self.line_items = line_items
        self.buyer = buyer
