import streamlit as st
import pandas as pd

# Sample/mock data – replace with actual data loading or connect to a database
data = {
    "Name": ["Alice Smith", "Carlos Diaz"],
    "Gender": ["Female", "Male"],
    "DOB": ["1990-05-12", "1982-03-22"],
    "E-mail": ["alice@example.com", "carlos@example.com"],
    "Phone number": ["+1-202-555-0101", "+34-600-123-456"],
    "Country of birth": ["USA", "Spain"],
    "Nationality": ["American", "Spanish"],
    "Has type 1 relative": ["No", "Yes"],
    "Has type 2 relative": ["No", "No"],
    "Has spouse in WBG": ["Yes", "No"],
    "Is public official": ["No", "Yes"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit app layout
st.set_page_config(page_title="WBG Compliance Tracker", layout="wide")
st.title("Profile Compliance Dashboard")

st.markdown("This dashboard displays profile data with flags for potential compliance considerations.")

# Search input
search_query = st.text_input("Search by name or nationality")

# Filter DataFrame
if search_query:
    filtered_df = df[
        df["Name"].str.contains(search_query, case=False) |
        df["Nationality"].str.contains(search_query, case=False)
    ]
else:
    filtered_df = df

# Display table
st.dataframe(filtered_df, use_container_width=True)
