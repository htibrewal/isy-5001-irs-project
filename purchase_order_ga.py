import streamlit as st

from blocks.PurchaseOrder import PurchaseOrder
from helper import load_items_data, load_ga_helper, load_multiple_vendor_ga
from load_data import build_line_items
from optimisation_type import OptimisationType


items_data = load_items_data()
electrical_parts, vendors, items_vendor_map = load_ga_helper()
multiple_vendor_ga = load_multiple_vendor_ga(items_vendor_map)

def purchase_order_ga_tab():
    st.markdown("## Create your Purchase Order basket")

    optimizations = [(OptimisationType.COST, "Cost"), (OptimisationType.DELIVERY, "Delivery Time")]
    optimise = st.radio("Select Optimization Criterion:", optimizations, format_func=lambda x: str(x[1]))

    # Initialize lists to store selected items and specified numbers
    selected_items = []
    quantities = []

    no_items_in_basket = 5
    for i in range(no_items_in_basket):
        col1, col2 = st.columns(2)

        with col1:
            selected_item = st.selectbox(
                "Select item based on name",
                items_data,
                index=None,
                format_func=lambda item: item[1],
                key=f"item_{i}"
            )

            if selected_item is not None:
                selected_items.append(str(selected_item[0]))

        # Place the number_input in the second column of the row
        with col2:
            quantity = st.number_input(
                "Specify quantity for selected item", min_value=1, step=1, key=f"number_{i}"
            )
            quantities.append(quantity)

    if st.button("Submit basket"):
        with st.spinner("Fetching best vendor for you..."):
            order = dict()

            for i in range(len(selected_items)):
                item = selected_items[i]
                if order.get(item) is None:
                    order[item] = quantities[i]
                else:
                    order[item] += quantities[i]

            purchase_order = PurchaseOrder(build_line_items(order, electrical_parts))
            multiple_vendors = multiple_vendor_ga.solve(purchase_order, optimise[0])

            vendor_list = [{'Selected Item': item.name, 'Recommended Vendor': vendor_item.vendor.name} for
                           item, vendor_item in multiple_vendors.items()]

            st.write("Recommended Vendors:")
            st.table(vendor_list)

            st.write(multiple_vendor_ga.print_fitness_score(purchase_order, multiple_vendors, optimise[0]))
