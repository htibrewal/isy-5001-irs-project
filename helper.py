import pandas as pd
import streamlit as st

from blocks.Vendor import Vendor
from load_data import fetch_electrical_parts, load_purchase_order_data, fetch_vendors, fetch_vendor_items
from multi_vendor_ga import MultiVendorGA


@st.cache_data
def load_items_data():
    data = pd.read_csv("cleaned_datasets/item_data.csv", index_col=0)

    # filtering items having more than 1 item code - TEMP CHANGES
    data = filter_items_by_count(data)

    items_data = [(row['ITEM_CODE'], row['ITEM_NAME']) for _, row in data.iterrows()]
    return items_data

def filter_items_by_count(data):
    item_grouped = data.groupby('ITEM_NAME').agg(
        ITEM_CODE=('ITEM_CODE', 'first'),  # keeps one ITEM_CODE per group
        ITEM_CODE_COUNT=('ITEM_CODE', 'nunique')
    ).reset_index()

    return item_grouped[item_grouped['ITEM_CODE_COUNT'] == 1]


@st.cache_resource
def load_ga_helper():
    electrical_parts = fetch_electrical_parts()
    purchase_order_data = load_purchase_order_data()
    vendors: dict[str, Vendor] = fetch_vendors(purchase_order_data)
    items_vendor_map = fetch_vendor_items(purchase_order_data, electrical_parts, vendors)

    return electrical_parts, vendors, items_vendor_map

@st.cache_resource
def load_multiple_vendor_ga(_items_vendor_map):
    return MultiVendorGA(_items_vendor_map)
