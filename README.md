# DIME Support New Hire Dashboard

## About

A Streamlit application to view DIME Support Data New Hire Data and make edits

## Requirements

* Python version 3.9 or higher

## Running Locally

`python -m streamlit run Overview.py`

## Generating Manifest

`rsconnect write-manifest streamlit . --overwrite --entrypoint Overview.py `

## Deploying to posit

git push your changes to have things automatically deploy to the server