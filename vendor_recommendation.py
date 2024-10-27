import streamlit as st
from helper import load_items_data, load_ga_helper, load_delivery_time_rating_model, load_price_rating_model, \
    get_top_vendors


def vendor_recommendation_tab():
    items_data = load_items_data()
    electrical_parts, vendors, items_vendor_map = load_ga_helper()

    price_model = load_price_rating_model()
    delivery_time_model = load_delivery_time_rating_model()


    st.markdown("## Select Item to get Vendor Ratings")

    selected_item = st.selectbox(
        "Select item based on name",
        items_data,
        index=None,
        format_func=lambda item: item[1],
        key="item_name"
    )

    if st.button("Get Vendor Rating"):
        with st.spinner("Calculating vendor rating for you..."):

            st.markdown("### Top 5 Vendors rated on Price")

            price_top_vendors = get_top_vendors(price_model, selected_item[0], vendors)
            st.table(price_top_vendors)

            st.markdown("### Top 5 Vendors rated on Delivery Time")

            delivery_time_top_vendors = get_top_vendors(delivery_time_model, selected_item[0], vendors)
            st.table(delivery_time_top_vendors)
