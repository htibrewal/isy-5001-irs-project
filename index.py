import streamlit as st

from helper import load_items_data

items_data = load_items_data()

st.title("Supply Chain Discovery and Recommendation System")
st.divider()

st.markdown("## Create your Purchase Order basket")

st.multiselect(
    "Select items based on name",
    items_data,
    format_func=lambda item: item[1],
)
