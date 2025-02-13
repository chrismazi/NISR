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
        # Show file name and extension for debugging
        st.write(f"Uploaded file: {uploaded_file.name}")
        file_extension = uploaded_file.name.split(".")[-1].lower()
        st.write(f"Detected file extension: {file_extension}")
        
        if file_extension not in ALLOWED_FILE_TYPES:
            st.error("Unsupported file format. Please upload a CSV, Excel, or Stata (.dta) file.")
            return None
        
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif file_extension == "dta":
            try:
                # Attempt to read with conversion for value labels
                df = pd.read_stata(uploaded_file, convert_categoricals=True)
            except Exception as e:
                st.error(f"Error reading .dta with convert_categoricals=True: {e}")
                st.info("Falling back to convert_categoricals=False...")
                df = pd.read_stata(uploaded_file, convert_categoricals=False)
            
            # For categorical columns, ensure empty string is an allowed category
            cat_cols = df.select_dtypes(include=["category"]).columns
            for col in cat_cols:
                if "" not in df[col].cat.categories:
                    df[col] = df[col].cat.add_categories([""])
                df[col] = df[col].fillna("")
                df[col] = df[col].astype(str)
        else:
            st.error("Unsupported file type encountered.")
            return None
        
        st.success(f"File uploaded successfully: {uploaded_file.name}")
        st.write("### Columns in the dataset:")
        st.write(df.columns.tolist())
        st.write("### Data Preview (first 10 rows):")
        st.dataframe(df.head(10))
        return df
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None
