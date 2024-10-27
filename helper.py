import pandas as pd
import streamlit as st
import pickle

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

@st.cache_resource
def load_price_rating_model():
    price_model = pickle.load(open('models/price_svd_model.pkl', 'rb'))
    return price_model['model']

@st.cache_resource
def load_delivery_time_rating_model():
    delivery_time_model = pickle.load(open('models/delivery_time_svd_model.pkl', 'rb'))
    return delivery_time_model['model']


def get_top_vendors(model, item_code, vendors):
    preds = []
    for code in list(vendors.keys()):
        prediction = model.predict(code, item_code)
        preds.append([code, prediction.est])

    predictions_df = pd.DataFrame(preds, columns=['SUPPLIER_CODE', 'RATING']).sort_values(by='RATING', ascending=False)
    top_rated_vendors = predictions_df[:5].reset_index(drop=True)

    vendor_name = top_rated_vendors['SUPPLIER_CODE'].astype(str).map(
        lambda code: vendors[code].name if code in vendors else None
    )

    top_rated_vendors.insert(1, 'Vendor Name', vendor_name)
    return top_rated_vendors.rename({'SUPPLIER_CODE': 'Vendor Code', 'RATING': 'Rating'}, axis=1)
