# DIME Support New Hire Dashboard

## About this example

A Streamlit application to view DIME Support Data New Hire Data and make edits

## Requirements

* Python version 3.9 or higher

## Running Locally

`python -m streamlit run app.py`

## Generating Manifest

`rsconnect write-manifest streamlit . --overwrite`

## Deploying to posit

`rsconnect deploy streamlit --server https://datanalytics.worldbank.org/ --api-key <API Key> ./`