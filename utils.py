import pandas as pd
import streamlit as st
import pysurveycto as pcto
from datetime import datetime

def onstart():
    if not 'key' in st.session_state:
        st.session_state['key'] = get_key()
    if not 'dime_support_scto' in st.session_state:
        st.session_state['dime_support_scto'] = connect_survey_cto('dime_support')
    if not 'dime_analytics_scto' in st.session_state:
        st.session_state['dime_analytics_scto'] = connect_survey_cto('dime_analytics')
    if not 'source' in st.session_state:
        st.session_state['source'] = read_source()
    if not 'contract_df' in st.session_state:
        get_contract_df()
    if not 'full_df' in st.session_state:
        st.session_state['full']=get_full_df()
    return

def connect_survey_cto(server='dime_support'): 
    server_name = "survey.wb"
    
    if server == 'dime_support':
        username = "zephyr428@gmail.com"
        password = "Br@nd1$hY0ur$k1ll$"
    elif server == 'dime_analytics':
        username = "eric.j.lysenko@gmail.com"
        password = "peshax-hakGem-gexzo1"
        
    scto = pcto.SurveyCTOObject(server_name, username, password)
    return scto
    
def read_source():
    scto = st.session_state['dime_support_scto']
    dataset_string = scto.get_server_dataset('dime_new_hires_readwrite')
    dataset = string_csv_to_df(dataset_string)
    
    return dataset

def string_csv_to_df(dataset_data):
    from io import StringIO

    csv_io = StringIO(dataset_data.strip())
    df = pd.read_csv(csv_io)

    return df
    
def write_dataset(df):
    scto = st.session_state['dime_support_scto']
    scto.upload_dataset(df, 'dime_new_hires_readwrite')
    
    # cast everything as string
    

    return

def get_subset(cols, fillna={}):
    if not 'full' in st.session_state:
        st.session_state['full'] = get_full_df()
        
        
    df = st.session_state['full'].copy()
    
    for col in cols:
        if not col in df.columns:
            df[col] = ''
    
    for col, val in fillna.items():
        df[col] = df[col].fillna(df[val])
        df.loc[df[col] == 'Other', col] = df[val]
    
    date_cols = ['constart','startdate','end']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    
    return df[cols]

def get_overview_df():
    overview_cols = ['name', 'upi', 'ttl_name', 'point_of_contact', 'ttl_unit', 'contract_process', 'consultanttype', 'contract_renewal', 'title', 'comments1', 'wb_email', 'data_handling', 'tech_onboard_status', 'git_train_status', 'nds_status', 'phrp_status', 'welcome_email_sent', 'letter_of_appointment', 'onboard_checklist', 'overview_comments']  
    
    fillna = {'ttl_name': 'ttl_other'}
    
    overview_df = get_subset(overview_cols, fillna)
    
    return overview_df


def get_upi_df():
    upi_cols = ['name', 'wb_worked', 'wb_past_travel', 'wb_spouse', 'wb_training', 'gender', 'dob', 'cob', 'nationality', 'address', 'city', 'state', 'postcode', 'country', 'title', 'upi_status', 'upi_initials']

    fillna = {'title': 'other_title'}

    upi_df = get_subset(upi_cols, fillna)
    
    return upi_df

def get_personal_information_df():
    personal_info_cols = ['name', 'gender', 'dob', 'email', 'phone', 'cob', 'nationality', 'coi_type1', 'coi_type2', 'coi_spouse', 'coi_publicoff']

    fillna = {}
    
    personal_info_df = get_subset(personal_info_cols, fillna)
    
    return personal_info_df

def get_contract_info_df():
    contract_info_cols = ['name', 'upi', 'constart', 'hqco', 'assignment', 'visa', 'ssn', 'coi_any', 'fee_matrix', 'fee_currency', 'fee', 'time_unit', 'dutystation', 'tier', 'ttl_name', 'startdate', 'end', 'assignment_length', 'work_schedule', 'chargecode', 'project', 'ds_updates']

    fillna = {'constart':'constart1', 
              'fee_matrix':'fee_matrix_o',
              'startdate': 'startdate1',
              'end':'end1'}
    
    contract_info_df = get_subset(contract_info_cols, fillna)
    
    return contract_info_df

def get_attachment(url,server='dime_analytics'):
    if server == 'dime_analytics':
        scto = st.session_state['dime_analytics_scto']
    elif server == 'dime_support':
        scto = st.session_state['dime_support_scto']
    
    attachment = scto.get_attachment(url, st.session_state['key'])

    return attachment    

def get_form_data(scto, form_id, format='json', oldest_completion_date=datetime(2004, 1, 1),key=None):
    
    form_data = scto.get_form_data(form_id, format=format, oldest_completion_date=oldest_completion_date,key=st.session_state['key'])
    
    return form_data

def clean_phone(series):
    return series.astype(str).str.replace(r'\D+', '', regex=True)

def get_full_df():
    ttl_df = st.session_state['source']
    contr_df = get_contract_df()
    
    if 'name' not in contr_df:
        contr_df['name'] = contr_df['first_name'] + ' ' + contr_df['last_name']
    
    contr_df['new hire comments'] = contr_df['comments']
    ttl_df['_phone_clean'] = clean_phone(ttl_df.get('phone', pd.Series(dtype=str)))
    contr_df['_phone_clean'] = clean_phone(contr_df.get('phone', pd.Series(dtype=str)))

    updated_df = ttl_df.copy()
    overlapping_cols = list(set(contr_df.columns) & set(ttl_df.columns))
    for col_to_exclude in ['email', 'name', 'phone']:
        if col_to_exclude in overlapping_cols:
            overlapping_cols.remove(col_to_exclude)
    
    # Email check
    merged_on_email = pd.merge(
        ttl_df[['email', 'name', 'phone'] + overlapping_cols],
        contr_df[['email', 'name', 'phone'] + overlapping_cols],
        on='email',
        suffixes=('', '_contr'),
        how='left'
    )

    for col in overlapping_cols:
        contr_col = f"{col}_contr"
        updated_df[col] = merged_on_email[col].combine_first(merged_on_email[contr_col])

    still_missing_mask = updated_df[overlapping_cols].isna().any(axis=1)
    ttl_missing = updated_df.loc[still_missing_mask]
    
    # Name check
    merged_on_name = pd.merge(
        ttl_missing[['name'] + overlapping_cols],
        contr_df[['name'] + overlapping_cols],
        on='name',
        suffixes=('', '_contr'),
        how='left'
    )

    for col in overlapping_cols:
        contr_col = f"{col}_contr"
        updated_df.loc[still_missing_mask, col] = merged_on_name[col].combine_first(merged_on_name[contr_col])

    updated_df.drop(columns=['_phone_clean'], inplace=True, errors='ignore')
    updated_df.fillna('', inplace=True)
    
    return updated_df

    
def get_attachment_urls(form_data,form_id,uuid):
    attachment_urls = {}
    
    for record in form_data:
        base_uuid = record['instanceID']
        attachment_base_url = f'https://survey.wb.surveycto.com/api/v2/forms/{form_id}/submissions/{base_uuid}/'
        for field, value in record.items():
            if attachment_base_url in value:
                if not uuid in attachment_urls.keys():
                    attachment_urls[uuid] = {}
                attachment_urls[uuid][field] = value

    return attachment_urls

def attachment_urls(scto, uuid,key=None):
    """Returns all attachment urls"""
    
    form_id = 'upi_information'
    form_data = get_form_data(scto, form_id, key=st.session_state['key'])

    attachment_urls = get_attachment_urls(form_data, form_id, uuid)
    
    return attachment_urls

def get_contract_df():
    if not 'contract_df' in st.session_state:
        scto = st.session_state['dime_analytics_scto']
        st.session_state['contract_df'] = get_form_data(scto,'upi_information',key=st.session_state['key'])
        df = st.session_state['contract_df']
    else:
        df = st.session_state['contract_df']
        
    return pd.DataFrame(df)

def boilerplace(section='overview',title = 'DIME Onboarding Tracker'):
    if not section in st.session_state:
        if not 'contract_df' in st.session_state:
            get_contract_df()
        if section == 'overview':
            df = get_overview_df()
            st.session_state[section] = df
        elif section == 'upi':
            df = get_upi_df()
            st.session_state[section] = df
        elif section == 'personal_information':
            df = get_personal_information_df()
            st.session_state[section] = df
        elif section == 'contract_information':
            df = get_contract_info_df()
            st.session_state[section] = df
    else:
        df = st.session_state[section]
        
    # Streamlit app
    st.set_page_config(page_title=title, layout="wide")
    st.title(title)
    st.markdown("Use the table below to view onboarding statuses. You can sort or search any column.")

    # Search functionality
    search_term = st.text_input("Search")

    if search_term:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = df
        
    edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="fixed", hide_index=True,
             column_config = {
                'name': 'Name',
                'upi': 'UPI',
                'ttl_name': 'TTL',
                'point_of_contact': 'Point of contact',
                'ttl_unit': 'Unit',
                'contract_process': 'DIME Support action needed',
                'consultanttype': 'Contract type',
                'contract_renewal': 'Contract action',
                'title': 'Title',
                'comments1': 'Comments',
                'wb_email': 'WB e-mail status',
                'data_handling': 'Handle confidential data',
                'tech_onboard_status': 'Technical onboarding status',
                'git_train_status': 'GitHub training status',
                'nds_status': 'NDA status',
                'phrp_status': 'PHRP status',
                'welcome_email_sent': 'Welcome Email Sent',
                'letter_of_appointment': 'Letter of appointment',
                'onboard_checklist': 'Onboarding Checklist',
                'overview_comments': 'Comments',
            
                'wb_worked': 'Worked for the Bank?',
                'wb_past_travel': 'Travelled on WBG business?',
                'wb_spouse': 'Spouse or dependent of',
                'wb_training': 'Attended Ban',
                'gender': 'Gender',
                'dob': 'DOB',
                'cob': 'Country of birth',
                'nationality': 'Nationality',
                'address': 'Address',
                'city': 'City',
                'state': 'State',
                'postcode': 'Postcode',
                'country': 'Country',
                'upi_status': 'Status',
                'upi_initials': 'Initials',
            
                'email': 'E-mail',
                'phone': 'Phone number',
                'coi_type1': 'Has type 1 relative',
                'coi_type2': 'Has type 2 relative',
                'coi_spouse': 'Has spouse in W',
                'coi_publicoff': 'Is public offici',
            
                'constart': st.column_config.DateColumn('Contract start date'),
                'hqco': 'HQ based?',
                'assignment': 'Type of Hire',
                'visa': 'Visa',
                'ssn': 'SSN',
                'coi_any': 'Any conflict of',
                'fee_matrix': 'Fee matrix',
                'fee_currency': 'Fee currency',
                'fee': 'Fee',
                'time_unit': 'Unit of Measu',
                'dutystation': 'Work Location',
                'tier': 'Tier',
                'startdate': st.column_config.DateColumn('Desired start date'),
                'end': st.column_config.DateColumn('End date'),
                'assignment_length': 'Duration Commited',
                'work_schedule': 'Work schedule',
                'chargecode': 'Cost obj',
                'project': 'Project',
                'ds_updates': 'DS Updates',
                'endtime': 'Request Date'
            }
        ) 
    
    st.markdown("Press Enter or click outside the data before hitting `Save`.")
    submitted = st.button('Save')
    
    if submitted:
        st.session_state[section] = edited_df
        
def get_key():
    with open("UPI.txt", "rb") as key_file:
        key_bytes = key_file.read()
        
    return key_bytes