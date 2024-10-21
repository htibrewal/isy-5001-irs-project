from blocks.ElectricalPart import ElectricalPart


class LineItem:
    def __init__(self, electrical_part: ElectricalPart, quantity: int):
        self.electrical_part = electrical_part
        self.quantity = quantity

    def __iter__(self):
        return iter((self.electrical_part, self.quantity))