import streamlit as st
import pandas as pd
import utils

if "dataset" not in st.session_state:
    st.session_state["dataset"] = utils.read_dataset()

# Mock data – replace with actual data loading
df = st.session_state['dataset']

# Streamlit app
st.set_page_config(page_title="DIME Onboarding Tracker", layout="wide")
st.title("DIME Onboarding Dashboard")
st.markdown("Use the table below to view onboarding statuses. You can sort or search any column.")

# Search functionality
search_term = st.text_input("Search")

if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df
    
edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic") 
st.markdown("Press Enter or click outside the data before hitting 'Save'.")
submitted = st.button('Save')

if submitted:
    st.session_state['dataset'] = edited_df
    utils.write_dataset(edited_df)