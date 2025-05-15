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

def connect_survey_cto(): 
    server_name = "survey.wb"
    username = ""
    password = ""

    scto = pcto.SurveyCTOObject(server_name, username, password)
    return scto
    
def read_dataset():
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

    return

def get_overview_df():
    pass

def get_contract_information_df():
    pass
