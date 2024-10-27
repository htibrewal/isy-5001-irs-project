import streamlit as st

from purchase_order_ga import purchase_order_ga_tab

# Remove these lines once testing in complete
# st.cache_data.clear()
# st.cache_resource.clear()

st.title("Supply Chain Discovery and Recommendation System")
st.divider()

purchase_order_ga_tab()
