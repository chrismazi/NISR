import streamlit as st
from Loader import load_uploaded_file  # Ensure this matches your file name (case-sensitive)
from transformer import transform_data

st.title("Data Upload Prototype with Transformation")

uploaded_file = st.file_uploader("Upload your dataset (CSV, Excel, or Stata .dta)", type=["csv", "xlsx", "dta"])

if uploaded_file:
    df = load_uploaded_file(uploaded_file)
    if df is not None:
        st.write("### Raw Data Preview:")
        st.dataframe(df.head())
        # Transform the data
        df_transformed = transform_data(df)
        st.write("### Transformed Data Preview:")
        st.dataframe(df_transformed.head())
