import pandas as pd
import streamlit as st
import plotly.express as px

def calculate_poverty_distribution(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the average poverty level by province.
    
    Parameters:
        data (pd.DataFrame): The input DataFrame, expected to have 'province' and 'poverty' columns.
        
    Returns:
        pd.DataFrame: A DataFrame with average poverty per province.
    """
    try:
        poverty_df = data.groupby("province")["poverty"].mean().reset_index()
        poverty_df.rename(columns={"poverty": "avg_poverty"}, inplace=True)
        return poverty_df
    except Exception as e:
        st.error(f"Error calculating poverty distribution: {e}")
        return pd.DataFrame()

def calculate_consumption_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate consumption statistics (mean, median, min, and max) by province.
    
    Parameters:
        data (pd.DataFrame): The input DataFrame, expected to have 'province' and 'Consumption' columns.
        
    Returns:
        pd.DataFrame: A DataFrame containing the statistics per province.
    """
    try:
        stats_df = data.groupby("province")["Consumption"].agg(
            mean_consumption="mean", 
            median_consumption="median", 
            min_consumption="min", 
            max_consumption="max"
        ).reset_index()
        return stats_df
    except Exception as e:
        st.error(f"Error calculating consumption statistics: {e}")
        return pd.DataFrame()

def generate_frequency_table(data: pd.DataFrame, row_var: str, col_var: str) -> pd.DataFrame:
    """
    Generate a frequency table (crosstab) for two specified variables.
    
    Parameters:
        data (pd.DataFrame): The input DataFrame.
        row_var (str): The column name to use for rows.
        col_var (str): The column name to use for columns.
        
    Returns:
        pd.DataFrame: A crosstab frequency table.
    """
    try:
        freq_table = pd.crosstab(data[row_var], data[col_var])
        return freq_table
    except Exception as e:
        st.error(f"Error generating frequency table for {row_var} and {col_var}: {e}")
        return pd.DataFrame()

def plot_pie_chart(data: pd.DataFrame, names: str, values: str, title: str):
    """
    Create a pie chart using Plotly.
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        names (str): The column name for pie slices.
        values (str): The column name for pie slice values.
        title (str): Chart title.
        
    Returns:
        plotly.graph_objs._figure.Figure: The generated pie chart.
    """
    try:
        fig = px.pie(data, names=names, values=values, title=title, color_discrete_sequence=px.colors.qualitative.Set3)
        return fig
    except Exception as e:
        st.error(f"Error plotting pie chart: {e}")
        return None

def plot_scatter_chart(data: pd.DataFrame, x: str, y: str, size: str, color: str, title: str):
    """
    Create a scatter chart using Plotly.
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        size (str): Column name to determine marker size.
        color (str): Column name for marker color.
        title (str): Chart title.
        
    Returns:
        plotly.graph_objs._figure.Figure: The generated scatter chart.
    """
    try:
        fig = px.scatter(data, x=x, y=y, size=size, color=color, title=title, 
                         color_discrete_sequence=px.colors.qualitative.Prism)
        return fig
    except Exception as e:
        st.error(f"Error plotting scatter chart: {e}")
        return None

def plot_bar_chart(data: pd.DataFrame, x: str, y: str, color: str, title: str):
    """
    Create a bar chart using Plotly.
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        color (str): Column name for bar colors.
        title (str): Chart title.
        
    Returns:
        plotly.graph_objs._figure.Figure: The generated bar chart.
    """
    try:
        fig = px.bar(data, x=x, y=y, color=color, title=title, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        return fig
    except Exception as e:
        st.error(f"Error plotting bar chart: {e}")
        return None
