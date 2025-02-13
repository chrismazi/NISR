import pandas as pd
import streamlit as st
import plotly.express as px
import ollama

@st.cache_data(show_spinner=False)
def calculate_poverty_distribution(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the average poverty level by province.
    
    Parameters:
        data (pd.DataFrame): DataFrame with 'province' and 'poverty' columns.
        
    Returns:
        pd.DataFrame: DataFrame with each province and its average poverty level.
    """
    try:
        poverty_df = data.groupby("province")["poverty"].mean().reset_index()
        poverty_df.rename(columns={"poverty": "avg_poverty"}, inplace=True)
        return poverty_df
    except Exception as e:
        st.error(f"Error calculating poverty distribution: {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def calculate_consumption_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate consumption statistics (mean, median, min, max) by province.
    
    Parameters:
        data (pd.DataFrame): DataFrame with 'province' and 'Consumption' columns.
        
    Returns:
        pd.DataFrame: DataFrame with consumption statistics for each province.
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
        data (pd.DataFrame): Input DataFrame.
        row_var (str): Column name for rows.
        col_var (str): Column name for columns.
        
    Returns:
        pd.DataFrame: Crosstab frequency table.
    """
    try:
        return pd.crosstab(data[row_var], data[col_var])
    except Exception as e:
        st.error(f"Error generating frequency table for {row_var} vs {col_var}: {e}")
        return pd.DataFrame()

def ask_gemma(query: str, context: str) -> str:
    """
    Query Gemma AI via Ollama using dashboard data context.
    
    Parameters:
        query (str): The user’s question.
        context (str): The data context from the dashboard.
        
    Returns:
        str: AI-generated response.
    """
    try:
        messages = [
            {"role": "system", "content": "You are an AI providing institutional insights based on dashboard data."},
            {"role": "user", "content": f"Dashboard Data Context:\n{context}\n\nUser Query: {query}"}
        ]
        response = ollama.chat(model="gemma:2b", messages=messages)
        return response['message']['content'] if response else "I couldn't generate an answer."
    except Exception as e:
        st.error(f"Error querying Gemma: {e}")
        return "Error querying AI."

@st.cache_data(show_spinner=False)
def plot_pie_chart(data: pd.DataFrame, names: str, values: str, title: str):
    """
    Create a pie chart using Plotly.
    
    Parameters:
        data (pd.DataFrame): DataFrame with data.
        names (str): Column for pie slice labels.
        values (str): Column for pie slice values.
        title (str): Chart title.
        
    Returns:
        plotly.graph_objs._figure.Figure or None: Generated pie chart.
    """
    try:
        fig = px.pie(data, names=names, values=values, title=title,
                     color_discrete_sequence=px.colors.qualitative.Set3)
        return fig
    except Exception as e:
        st.error(f"Error plotting pie chart: {e}")
        return None

@st.cache_data(show_spinner=False)
def plot_scatter_chart(data: pd.DataFrame, x: str, y: str, size: str, color: str, title: str):
    """
    Create a scatter chart using Plotly.
    
    Parameters:
        data (pd.DataFrame): DataFrame with data.
        x (str): Column for the x-axis.
        y (str): Column for the y-axis.
        size (str): Column to determine marker size.
        color (str): Column for marker color.
        title (str): Chart title.
        
    Returns:
        plotly.graph_objs._figure.Figure or None: Generated scatter chart.
    """
    try:
        fig = px.scatter(data, x=x, y=y, size=size, color=color, title=title,
                         color_discrete_sequence=px.colors.qualitative.Prism)
        return fig
    except Exception as e:
        st.error(f"Error plotting scatter chart: {e}")
        return None

@st.cache_data(show_spinner=False)
def plot_bar_chart(data: pd.DataFrame, x: str, y: str, color: str, title: str):
    """
    Create a bar chart using Plotly.
    
    Parameters:
        data (pd.DataFrame): DataFrame with data.
        x (str): Column for the x-axis.
        y (str): Column for the y-axis.
        color (str): Column for bar color.
        title (str): Chart title.
        
    Returns:
        plotly.graph_objs._figure.Figure or None: Generated bar chart.
    """
    try:
        fig = px.bar(data, x=x, y=y, color=color, title=title,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        return fig
    except Exception as e:
        st.error(f"Error plotting bar chart: {e}")
        return None

# ---------------------------
# Specific Chart Functions (As per your requirements)
# ---------------------------

def chart_poverty_distribution_by_province(data: pd.DataFrame):
    """
    Chart 1: Generate a pie chart showing poverty distribution by province.
    """
    df = calculate_poverty_distribution(data)
    return plot_pie_chart(df, names="province", values="avg_poverty", title="Poverty Rate by Province")

def chart_average_consumption_by_province(data: pd.DataFrame):
    """
    Chart 2: Generate a scatter chart showing average consumption by province.
    """
    df = data.groupby("province")["Consumption"].mean().reset_index()
    df.dropna(subset=["Consumption"], inplace=True)
    return plot_scatter_chart(df, x="province", y="Consumption", size="Consumption",
                              color="province", title="Average Consumption by Province")

def chart_top_5_districts_by_consumption(data: pd.DataFrame):
    """
    Chart 3: Generate a bar chart for the top 5 districts by consumption.
    """
    try:
        top_df = data.groupby("district")["Consumption"].mean().nlargest(5).reset_index()
        return plot_bar_chart(top_df, x="district", y="Consumption", color="district",
                              title="Top 5 Districts by Consumption")
    except Exception as e:
        st.error(f"Error plotting top 5 districts by consumption: {e}")
        return None

def chart_poverty_rate_by_gender(data: pd.DataFrame):
    """
    Chart 4: Generate a funnel chart showing poverty rate by gender.
    """
    try:
        df = data.groupby("s1q1")["poverty"].mean().reset_index()
        fig = px.funnel(df, x="poverty", y="s1q1", title="Poverty Rate by Gender",
                        color="s1q1", color_discrete_sequence=px.colors.qualitative.Dark2)
        return fig
    except Exception as e:
        st.error(f"Error plotting poverty rate by gender: {e}")
        return None

def chart_urban_vs_rural_consumption(data: pd.DataFrame):
    """
    Chart 5: Generate a box plot for urban vs rural consumption.
    Assumes the 'ur2_2012' column classifies urban vs rural.
    """
    try:
        fig = px.box(data, x="ur2_2012", y="Consumption", title="Urban vs Rural Consumption",
                     color="ur2_2012", color_discrete_sequence=px.colors.qualitative.Bold)
        return fig
    except Exception as e:
        st.error(f"Error plotting urban vs rural consumption: {e}")
        return None

def chart_poverty_distribution_by_education_level(data: pd.DataFrame):
    """
    Chart 6: Generate a stacked bar chart showing poverty distribution by education level.
    Assumes the 'education_level' column exists.
    """
    try:
        if "education_level" not in data.columns:
            st.error("Education level data is missing.")
            return None
        df = pd.crosstab(data["education_level"], data["poverty"]).reset_index()
        df = df.melt(id_vars=["education_level"], var_name="poverty_level", value_name="count")
        fig = px.bar(df, x="count", y="poverty_level", color="education_level", barmode="stack",
                     title="Poverty Distribution by Education Level",
                     labels={"count": "Count", "poverty_level": "Poverty Level", "education_level": "Education Level"},
                     color_discrete_sequence=px.colors.qualitative.T10)
        return fig
    except Exception as e:
        st.error(f"Error plotting poverty distribution by education level: {e}")
        return None
