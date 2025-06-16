import pandas as pd
import streamlit as st
import pysurveycto as pcto

# Example data
data = {
    "section": ["overview", "upi", "personal", "contact", "upi"],
    "name": ["Item A", "UPI ID 1", "Name 1", "Email 1", "UPI ID 2"],
    "value": ["Some notes", "abc@upi", "John Doe", "john@example.com", "xyz@upi"],
}
df = pd.DataFrame(data)

def connect_survey_cto(server='dime_support'): 
    server_name = "survey.wb"
    
    
    username = "zephyr428@gmail.com"
    password = "Br@nd1$hY0ur$k1ll$"

    scto = pcto.SurveyCTOObject(server_name, username, password)
    return scto
    
def read_source():
    scto = connect_survey_cto()
    dataset_string = scto.get_server_dataset('dime_new_hires_readwrite')
    dataset = string_csv_to_df(dataset_string)
    
    return dataset

def string_csv_to_df(dataset_data):
    from io import StringIO

    csv_io = StringIO(dataset_data.strip())
    df = pd.read_csv(csv_io)

    return df
    
def write_dataset(df):
    scto = connect_survey_cto()
    scto.upload_dataset(df, 'dime_new_hires_readwrite')
    
    # cast everything as string
    

    return

def get_subset(cols, fillna={}):
    if not 'source' in st.session_state:
        st.session_state['source'] = read_source()
        
        
    df = st.session_state['source'].copy()
    
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

def boilerplace(section='overview',title = 'DIME Onboarding Tracker'):
    if not section in st.session_state:
        
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
        
    edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic", hide_index=True,
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