import streamlit as st
import pandas as pd

# Mock data — replace with your actual source (CSV, Excel, or DB)
data = {
    "Name": ["Alice Smith", "Bob Johnson"],
    "UPI": ["123456", "789012"],
    "Contract start date": ["2024-01-15", "2024-03-01"],
    "HQ based?": ["Yes", "No"],
    "Type of Hire": ["STC", "ETC"],
    "Visa": ["G4", "None"],
    "SSN": ["XXX-XX-1234", "XXX-XX-5678"],
    "Any conflict of interest": ["No", "Yes"],
    "Fee matrix": ["A", "B"],
    "Fee currency": ["USD", "EUR"],
    "Fee": [500, 450],
    "Unit of Measurement": ["Day", "Day"],
    "Work Location": ["Washington, DC", "Paris"],
    "Tier": ["1", "2"],
    "TTL": ["Dr. Green", "Ms. Blue"],
    "Desired start date": ["2024-01-10", "2024-02-20"],
    "End date": ["2024-06-15", "2024-08-30"],
    "Duration Commited": ["5 months", "6 months"],
    "Work schedule": ["Full-time", "Part-time"],
    "Cost object": ["WB123456", "WB789012"],
    ")": ["", ""],  # Looks like a typo/stray column — keep or drop as needed
    "DS Updates": ["Pending", "Completed"]
}

# Create DataFrame
df = pd.DataFrame(data)

# App config
st.set_page_config(page_title="Contract & Onboarding Tracker", layout="wide")
st.title("Contract Management Dashboard")

st.markdown("This table displays current consultant contract data, including HR flags and status updates.")

# Search functionality
query = st.text_input("Search by Name, TTL, or Work Location")

if query:
    filtered_df = df[
        df["Name"].str.contains(query, case=False) |
        df["TTL"].str.contains(query, case=False) |
        df["Work Location"].str.contains(query, case=False)
    ]
else:
    filtered_df = df

# Show the data
st.dataframe(filtered_df, use_container_width=True)
