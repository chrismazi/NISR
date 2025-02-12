import pandas as pd
import streamlit as st

# Allowed file types for upload
ALLOWED_FILE_TYPES = ["csv", "xlsx", "dta"]

def load_uploaded_file(uploaded_file):
    """
    Loads the uploaded dataset and returns a cleaned pandas DataFrame.
    Supports CSV, Excel, and Stata (.dta) file formats.
    
    Parameters:
        uploaded_file (BytesIO): File uploaded via Streamlit.
    
    Returns:
        pd.DataFrame: Processed DataFrame ready for analysis.
    """
    try:
        # Debug: show file name and extension
        st.write(f"Uploaded file: {uploaded_file.name}")
        file_extension = uploaded_file.name.split(".")[-1].lower()
        st.write(f"Detected file extension: {file_extension}")
        
        if file_extension not in ALLOWED_FILE_TYPES:
            st.error("Unsupported file format. Please upload a CSV, Excel, or Stata (.dta) file.")
            return None
        
        # Read file based on its extension
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif file_extension == "dta":
            try:
                df = pd.read_stata(uploaded_file, convert_categoricals=False)
            except Exception as e:
                st.error(f"Error reading .dta file: {e}")
                return None
        else:
            st.error("Unsupported file type encountered.")
            return None
        
        st.success(f"File uploaded successfully: {uploaded_file.name}")
        st.write("### Data Preview:")
        st.dataframe(df.head())
        return df
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None
