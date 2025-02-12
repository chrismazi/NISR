import pandas as pd
import streamlit as st

def ensure_numeric_consumption(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convert the 'Consumption' column to numeric values.
    Any conversion errors will be coerced to NaN.
    
    Parameters:
        data (pd.DataFrame): Input DataFrame expected to have a 'Consumption' column.
        
    Returns:
        pd.DataFrame: DataFrame with the 'Consumption' column converted to numeric type.
    """
    if 'Consumption' not in data.columns:
        st.warning("'Consumption' column not found in the dataset.")
        return data
    data["Consumption"] = pd.to_numeric(data["Consumption"], errors="coerce")
    return data

def map_education_levels(data: pd.DataFrame, mapping: dict = None) -> pd.DataFrame:
    """
    Map raw education values from the 's4aq2' column to standardized categories.
    A new column 'education_level' is added to the DataFrame.
    
    Parameters:
        data (pd.DataFrame): Input DataFrame expected to have a 's4aq2' column.
        mapping (dict, optional): Custom mapping dictionary. Uses default mapping if None.
        
    Returns:
        pd.DataFrame: DataFrame with an added 'education_level' column.
    """
    if 's4aq2' not in data.columns:
        st.warning("'s4aq2' column not found in the dataset. Cannot map education levels.")
        data["education_level"] = None
        return data
    if mapping is None:
        mapping = {
            'Pre-primary': 'Nursery',
            'Primary 1': 'Primary',
            'Primary 2': 'Primary',
            'Primary 3': 'Primary',
            'Primary 4': 'Primary',
            'Primary 5': 'Primary',
            'Primary 6,7,8': 'Primary',
            'Not complete P1': 'Primary Dropout',
            'Secondary 1': 'Secondary',
            'Secondary 2': 'Secondary',
            'Secondary 3': 'Secondary',
            'Secondary 4': 'Secondary',
            'Secondary 5': 'Secondary',
            'Post primary 1': 'Post-Secondary',
            'Post primary 2': 'Post-Secondary',
            'Post primary 3': 'Post-Secondary',
            'Post primary 4': 'Post-Secondary',
            'Post primary 5': 'Post-Secondary',
            'Post primary 6,7,8': 'Post-Secondary',
            'University 1': 'Bachelors',
            'University 2': 'Bachelors',
            'University 3': 'Bachelors',
            'University 4': 'Masters',
            'University 5': 'Masters',
            'University 6': 'PhD',
            'University 7': 'PhD',
            'Missing': 'Unknown',
            'nan': 'Unknown',
            'Unknown': 'Unknown'
        }
    data["education_level"] = data["s4aq2"].map(mapping)
    return data

def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the DataFrame.
    For instance, fill missing 'Consumption' values with the median.
    
    Parameters:
        data (pd.DataFrame): Input DataFrame.
        
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    if "Consumption" in data.columns:
        median_consumption = data["Consumption"].median()
        data["Consumption"].fillna(median_consumption, inplace=True)
    return data

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Apply a series of transformations to the raw data.
    
    This includes:
    - Converting 'Consumption' to numeric.
    - Mapping raw education values (from 's4aq2') to a standardized 'education_level' column.
    - Handling missing values.
    
    Parameters:
        data (pd.DataFrame): Raw DataFrame loaded from the user’s file.
        
    Returns:
        pd.DataFrame: Cleaned and transformed DataFrame ready for further analysis.
    """
    data = ensure_numeric_consumption(data)
    data = map_education_levels(data)
    data = handle_missing_values(data)
    return data
