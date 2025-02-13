import streamlit as st
from Loader import load_uploaded_file
from transformer import transform_data
from insights import (
    chart_poverty_distribution_by_province,
    chart_average_consumption_by_province,
    chart_top_5_districts_by_consumption,
    chart_poverty_rate_by_gender,
    chart_urban_vs_rural_consumption,
    chart_poverty_distribution_by_education_level
)

st.title("Poverty and Consumption Insights Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV, Excel, or Stata .dta)", type=["csv", "xlsx", "dta"])

if uploaded_file:
    raw_data = load_uploaded_file(uploaded_file)
    if raw_data is not None:
        data = transform_data(raw_data)
        st.write("### Transformed Data Preview")
        st.dataframe(data.head())

        # Sidebar Filters
        st.sidebar.header("Filters")
        selected_province = st.sidebar.selectbox("Select Province", ["All"] + list(data["province"].dropna().unique()))
        selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + list(data["s1q1"].dropna().unique()))

        # Apply filters
        filtered_data = data.copy()
        if selected_province != "All":
            filtered_data = filtered_data[filtered_data["province"] == selected_province]
        if selected_gender != "All":
            filtered_data = filtered_data[filtered_data["s1q1"] == selected_gender]

        # Sidebar - Frequency Table Options
        st.sidebar.subheader("Generate Frequency Table")
        freq_options = [
            "None",
            "Poverty by Province",
            "Poverty by Gender",
            "Poverty by Education Level"
        ]
        selected_freq = st.sidebar.selectbox("Select Analysis for Frequency Table", freq_options)

        if selected_freq != "None":
            if selected_freq == "Poverty by Province":
                freq_table = data.pivot_table(index="province", columns="poverty", aggfunc="size", fill_value=0)
            elif selected_freq == "Poverty by Gender":
                freq_table = data.pivot_table(index="s1q1", columns="poverty", aggfunc="size", fill_value=0)
            elif selected_freq == "Poverty by Education Level":
                freq_table = data.pivot_table(index="education_level", columns="poverty", aggfunc="size", fill_value=0)
            
            st.sidebar.write("### Frequency Table")
            st.sidebar.dataframe(freq_table)

        # Display charts with filtered data
        st.subheader("Poverty Distribution by Province")
        fig1 = chart_poverty_distribution_by_province(filtered_data)
        if fig1: st.plotly_chart(fig1)
        
        st.subheader("Average Consumption by Province")
        fig2 = chart_average_consumption_by_province(filtered_data)
        if fig2: st.plotly_chart(fig2)
        
        st.subheader("Top 5 Districts by Consumption")
        fig3 = chart_top_5_districts_by_consumption(filtered_data)
        if fig3: st.plotly_chart(fig3)
        
        st.subheader("Poverty Rate by Gender")
        fig4 = chart_poverty_rate_by_gender(filtered_data)
        if fig4: st.plotly_chart(fig4)
        
        st.subheader("Urban vs Rural Consumption")
        fig5 = chart_urban_vs_rural_consumption(filtered_data)
        if fig5: st.plotly_chart(fig5)
        
        st.subheader("Poverty Distribution by Education Level")
        fig6 = chart_poverty_distribution_by_education_level(filtered_data)
        if fig6: st.plotly_chart(fig6)
