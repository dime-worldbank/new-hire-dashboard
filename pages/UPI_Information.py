import streamlit as st
import pandas as pd

# Sample/mock data — replace with actual data loading
data = {
    "Name": ["Alice Smith", "Bob Jones"],
    "First name": ["Alice", "Bob"],
    "Last name": ["Smith", "Jones"],
    "Worked for the Bank?": ["Yes", "No"],
    "Travelled on WBG business?": ["No", "Yes"],
    "Spouse or dependent of WBG staff?": ["No", "Yes"],
    "Attended Bank traning?": ["Yes", "No"],
    "Gender": ["Female", "Male"],
    "DOB": ["1990-05-12", "1985-11-23"],
    "Country of birth": ["USA", "Canada"],
    "Nationality": ["American", "Canadian"],
    "Address": ["123 Bank St", "456 Finance Ave"],
    "City": ["Washington", "Toronto"],
    "State": ["DC", "ON"],
    "Postcode": ["20006", "M5H 2N2"],
    "Country": ["USA", "Canada"],
    "Comments": ["Clearance pending", "Onboarded"],
    "Status": ["Pending", "Completed"],
    "Initials": ["AS", "BJ"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Streamlit setup
st.set_page_config(page_title="WBG Profile Tracker", layout="wide")
st.title("WBG Personnel Tracker")

st.markdown("This table shows staff background and onboarding information. Use the filter below to search by name.")

# Search bar
search = st.text_input("Search by name")
if search:
    filtered_df = df[df["Name"].str.contains(search, case=False)]
else:
    filtered_df = df

# Display table
st.dataframe(filtered_df, use_container_width=True)
