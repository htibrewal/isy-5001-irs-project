import os
import pandas as pd
from dotenv import load_dotenv

from blocks.ElectricalPart import ElectricalPart
from blocks.LineItem import LineItem
from blocks.Vendor import Vendor
from blocks.VendorItem import VendorItem

load_dotenv()

def fetch_electrical_parts() -> dict[str, ElectricalPart]:
    electrical_parts_data = pd.read_csv(os.path.join(os.getenv('PROCESSED_DATA_FOLDER_PATH'), 'electrical_parts_final.csv'))

    electrical_parts = dict()
    for _, electrical_part in electrical_parts_data.iterrows():
        part_id = electrical_part['PART_ID_CLEANED']

        electrical_parts[str(part_id)] = ElectricalPart(
            part_id,
            electrical_part['PART_NAME'],
            description=electrical_part['PART_DESCRIPTION'],
            width=electrical_part['WIDTH_(MM)'],
            height=electrical_part['HEIGHT_(MM)'],
            depth=electrical_part['DEPTH_(MM)'],
            weight=electrical_part['WEIGHT_(KG)']
        )

    return electrical_parts


def load_purchase_order_data() -> pd.DataFrame:
    purchase_order_data = pd.read_csv(os.path.join(os.getenv('PROCESSED_DATA_FOLDER_PATH'), 'filtered_data_final.csv'))
    return purchase_order_data


def fetch_vendors(purchase_order_data: pd.DataFrame) -> dict[str, Vendor]:
    vendors = dict()
    vendor_mapping = purchase_order_data.groupby('SUPPLIER_CODE')['SUPPLIER_NAME'].first().reset_index()

    for _, vendor_info in vendor_mapping.iterrows():
        supplier_code = vendor_info['SUPPLIER_CODE']

        vendors[supplier_code] = Vendor(vendor_info['SUPPLIER_CODE'], vendor_info['SUPPLIER_NAME'])

    return vendors


def fetch_vendor_items(purchase_order_data: pd.DataFrame, electrical_parts: dict[str, ElectricalPart], vendors: dict[str, Vendor]) -> dict[ElectricalPart, list[VendorItem]]:
    items_vendor_map = dict()

    for _, line_item in purchase_order_data.iterrows():
        item_code = line_item['ITEM_CODE_CLEANED']
        vendor_code = line_item['SUPPLIER_CODE']

        electrical_part = electrical_parts[str(item_code)]
        vendor = vendors[vendor_code]

        if electrical_part not in items_vendor_map:
            items_vendor_map[electrical_part] = []

        tax_percent = line_item['TAX_AMOUNT(LC)']/line_item['ITEM_VALUE'] * 100
        vendor_item = VendorItem(electrical_part, vendor, line_item['PRICE'], tax_percent)

        if vendor_item not in items_vendor_map[electrical_part]:
            items_vendor_map[electrical_part].append(vendor_item)

    return items_vendor_map

def build_line_items(raw_data: dict[str, int], electrical_parts: dict[str, ElectricalPart]) -> list[LineItem]:
    line_items = list()

    for item_code, quantity in raw_data.items():
        electrical_part = electrical_parts[item_code]
        line_items.append(LineItem(electrical_part, quantity))

    return line_items
