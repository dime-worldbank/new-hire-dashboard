import streamlit as st
import pandas as pd
import utils

utils.onstart()

scto = utils.connect_survey_cto(server='dime_analytics')
uuid = None
base_link = 'https://survey.wb.surveycto.com/api/v2/forms/upi_information/submissions/'

# Set page title and layout
title = "Onboarding Status Dashboard"
st.set_page_config(page_title=title, layout="wide")
st.title(title)
st.markdown("Use the table below to view onboarding statuses. You can sort or search any column.")

# Get DataFrame from session state
if not 'source' in st.session_state:
    st.session_state['source'] = utils.read_source()

df = st.session_state['full']

# Dropdown to select name (searchable)
selected_name = st.selectbox(
    "Filter by name",
    options=["All"] + sorted(df['name'].dropna().unique().tolist())
)

# Filtering logic
filtered_df = df.copy()

def display_attachments(row: pd.Series, i:int=0):
    contract_data_links = {'passport_bio':'Passport', 'cv':'CV', 'uni_letter':'University Letter', 'hire_justification_1': 'Hire Justification 1', 'hire_justification_2': 'Hire Justification 2','tor':'TOR'}
    comp_hire = row['competitivehire']
    name = row['name']
    st.markdown(name)
    st.markdown('#### <u>Competetive Hire?</u>', unsafe_allow_html=True)
    st.markdown(comp_hire)
    for key,val in contract_data_links.items():
        button_key = val.replace(' ','_') + f'_{i}'
        link = row[key]
        st.markdown(f'#### <u>{val}</u>', unsafe_allow_html=True)
        fname = f"{name} - {val}.pdf"
        # contract form
        if 'http' in link:
            data = utils.get_attachment(link)
            st.download_button(fname, data, mime="application/pdf", file_name=fname,key=button_key)
        
        # ttl form
        elif len(link)>0:
            try:
                uuid = row['instanceID'].strip()
                link = f'https://survey.wb.surveycto.com/api/v2/forms/dime_new_hires/submissions/{uuid}/attachments/' + link.strip()
                data = utils.get_attachment(link)
                st.download_button(fname, data, mime="application/pdf", file_name=fname,key=button_key)
            except:
                st.markdown('file download error')
        # no data
        else:
            st.markdown('missing')


if selected_name != "All":
    filtered_df = filtered_df[filtered_df['name'] == selected_name]

# Display download links
if selected_name.lower() != 'all':
    filtered_df = filtered_df[filtered_df.apply(
        lambda row: row.astype(str).str.contains(selected_name, case=False).any(), axis=1
    )]
    if len(filtered_df) > 1:
        st.dataframe(filtered_df)
        for i,row in filtered_df.iterrows():
            st.markdown(row['endtime'])
            display_attachments(filtered_df.iloc[0],i)
            
    if len(filtered_df) == 1:
        display_attachments(filtered_df.iloc[0])
        
        
        """javascript:void(0);"""