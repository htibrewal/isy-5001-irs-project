from dotenv import load_dotenv

from blocks.Vendor import Vendor
from load_data import load_purchase_order_data, fetch_vendors, fetch_electrical_parts, fetch_vendor_items

load_dotenv()

def main():
    electrical_parts = fetch_electrical_parts()

    # load purchase order data
    purchase_order_data = load_purchase_order_data()

    # build objects
    vendors: dict[str, Vendor] = fetch_vendors(purchase_order_data)

    items_vendor_map = fetch_vendor_items(purchase_order_data, electrical_parts, vendors)