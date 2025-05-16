# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data", "About"])

# Main content
if page == "Home":
    st.title("Welcome to My Streamlit App")
    st.write("This is a basic Streamlit app structure.")

    name = st.text_input("Enter your name:")
    if name:
        st.success(f"Hello, {name}!")

elif page == "Data":
    st.title("Data Viewer")

    # Example data
    df = pd.DataFrame({
        "A": np.random.randn(10),
        "B": np.random.rand(10),
        "C": np.random.randint(1, 100, 10)
    })

    st.dataframe(df)

    # Plot
    st.line_chart(df)

elif page == "About":
    st.title("About")
    st.markdown("""
    This is a simple multi-page Streamlit app template.
    
    Built with ❤️ using [Streamlit](https://streamlit.io).
    """)

# Footer
st.markdown("---")
st.caption("© 2025 My Streamlit App")
