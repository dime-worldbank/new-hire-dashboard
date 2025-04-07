import streamlit as st
import pandas as pd

# Mock data – replace with actual data loading
data = {
    "Name": ["Alice Smith", "Bob Jones"],
    "UPI": ["123456", "654321"],
    "TTL": ["Dr. Adams", "Dr. Brown"],
    "Point of contact": ["John Doe", "Jane Roe"],
    "Unit": ["DIME", "DEC"],
    "Start date": ["2023-01-01", "2023-02-15"],
    "DIME Support action needed": ["Yes", "No"],
    "Contract type": ["STC", "ETC"],
    "Contract action": ["New", "Extension"],
    "Title": ["Research Assistant", "Data Scientist"],
    "Comments": ["N/A", "Urgent onboarding"],
    "WB e-mail status": ["Pending", "Completed"],
    "Handle confidential data": ["Yes", "No"],
    "Technical onboarding status": ["In progress", "Completed"],
    "GitHub training status": ["Not started", "Completed"],
    "NDA status": ["Signed", "Pending"],
    "Data security assessment": ["Pending", "Completed"],
    "PHRP status": ["Pending", "Approved"],
    "Welcome Email Sent": ["Yes", "No"],
    "bmitte": ["Yes", "No"],
    "Onboarding Checklist": ["Started", "Completed"],
    "DIME Analytics Welcome Email /Comments": ["Sent", "Scheduled"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.set_page_config(page_title="DIME Onboarding Tracker", layout="wide")
st.title("DIME Onboarding Dashboard")

st.markdown("Use the table below to view onboarding statuses. You can sort or search any column.")

# Search functionality
search_term = st.text_input("Search by Name or Title")

if search_term:
    filtered_df = df[df["Name"].str.contains(search_term, case=False) | df["Title"].str.contains(search_term, case=False)]
else:
    filtered_df = df

st.dataframe(filtered_df, use_container_width=True)
