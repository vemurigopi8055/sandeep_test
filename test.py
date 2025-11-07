import streamlit as st
import pandas as pd

# Title
st.title("📂 CSV File Uploader")

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Show file details
    st.subheader("File Details")
    st.write(f"Filename: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")

    # Display dataframe
    st.subheader("📊 Data Preview")
    st.dataframe(df)

    # Optionally show summary
    if st.checkbox("Show summary statistics"):
        st.write(df.describe())
else:
    st.info("Please upload a CSV file to continue.")
