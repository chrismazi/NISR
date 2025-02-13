import streamlit as st
from Loader import load_uploaded_file
from transformer import transform_data
from insights import (
    calculate_poverty_distribution,
    calculate_consumption_statistics,
    generate_frequency_table,
    plot_pie_chart,
    plot_scatter_chart,
    plot_bar_chart
)

st.title("Autamation Data Analysis Dashboard")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx", "dta"])
if uploaded_file:
    raw_data = load_uploaded_file(uploaded_file)
    if raw_data is not None:
        # Transform the data
        data = transform_data(raw_data)
        
        # Display basic data preview
        st.write("### Transformed Data Preview")
        st.dataframe(data.head())
        
        # Example: Calculate and display poverty distribution
        poverty_df = calculate_poverty_distribution(data)
        st.write("### Poverty Distribution by Province")
        st.dataframe(poverty_df)
        pie_fig = plot_pie_chart(poverty_df, names="province", values="avg_poverty", title="Poverty Rate by Province")
        if pie_fig: 
            st.plotly_chart(pie_fig)
        
        # Example: Consumption statistics
        consumption_stats = calculate_consumption_statistics(data)
        st.write("### Consumption Statistics by Province")
        st.dataframe(consumption_stats)
        
        # Example: Generate frequency table for Poverty by Education Level
        if "education_level" in data.columns:
            freq_table = generate_frequency_table(data, row_var="education_level", col_var="poverty")
            st.write("### Frequency Table: Poverty by Education Level")
            st.dataframe(freq_table)
