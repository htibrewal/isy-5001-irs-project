import pandas as pd
import streamlit as st

@st.cache_data
def load_items_data():
    data = pd.read_csv("data/item_data.csv", index_col=0)

    # filtering items having more than 1 item code - TEMP CHANGES
    data = filter_items_by_count(data)

    items_data = [(row['ITEM_CODE'], row['ITEM_NAME']) for _, row in data.iterrows()]
    return items_data

def filter_items_by_count(data):
    item_grouped = data.groupby('ITEM_NAME')['ITEM_CODE'].nunique().reset_index()
    return item_grouped[item_grouped['ITEM_CODE'] == 1]