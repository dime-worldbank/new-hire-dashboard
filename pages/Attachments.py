import streamlit as st
import pandas as pd
import utils
from datetime import datetime

scto = utils.connect_survey_cto()

def get_form_data(form_id, format='json', oldest_completion_date=datetime(2004, 1, 1)):
    
    form_data = scto.get_form_data(form_id, format=format, oldest_completion_date=oldest_completion_date)
    
    return form_data
    
def get_attachment_urls(form_data,form_id,uuid):
    attachment_urls = {}
    
    for record in form_data:
        attachment_base_url = f'https://survey.wb.surveycto.com/api/v2/forms/{form_id}/submissions/{uuid}/'
        for field, value in record.items():
            if attachment_base_url in value:
                if not uuid in attachment_urls.keys():
                    attachment_urls[uuid] = {}
                attachment_urls[uuid][field] = value

    return attachment_urls

def attachment_urls(uuid):
    """Returns all attachment urls"""
    form_id = 'dime_new_hires'
    
    form_data = get_form_data(form_id)

    attachment_urls = get_attachment_urls(form_data,form_id,uuid)
    
    return attachment_urls

# Set page title and layout
title = "Onboarding Status Dashboard"
st.set_page_config(page_title=title, layout="wide")
st.title(title)
st.markdown("Use the table below to view onboarding statuses. You can sort or search any column.")

# Get DataFrame from session state
if not 'source' in st.session_state:
    st.session_state['source'] = utils.read_source()
df = st.session_state['source']

# Dropdown to select name (searchable)
selected_name = st.selectbox(
    "Filter by name",
    options=["All"] + sorted(df['name'].dropna().unique().tolist())
)

# Filtering logic
filtered_df = df.copy()[['name','KEY']]

if selected_name != "All":
    filtered_df = filtered_df[filtered_df['name'] == selected_name]

if selected_name.lower() != 'all':
    filtered_df = filtered_df[filtered_df.apply(
        lambda row: row.astype(str).str.contains(selected_name, case=False).any(), axis=1
    )]
    if len(filtered_df) == 1:
        uuid = filtered_df.iloc[0]['KEY'].split(':')[-1]
        st.markdown(uuid)

attachment_urls(uuid)
    
    