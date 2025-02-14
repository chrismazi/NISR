import streamlit as st
import pandas as pd
import plotly.express as px

from Loader import load_uploaded_file
from transformer import transform_data
from insights import (
    chart_poverty_distribution_by_province,
    chart_average_consumption_by_province,
    chart_top_5_districts_by_consumption,
    chart_poverty_rate_by_gender,
    chart_urban_vs_rural_consumption,
    chart_poverty_distribution_by_education_level,
    ask_gemma
)

from pdf_report import generate_pdf_report  # Moved to the top with other imports

st.title("Poverty and Consumption Insights Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload your dataset (CSV, Excel, or Stata .dta)", type=["csv", "xlsx", "dta"])
if uploaded_file:
    raw_data = load_uploaded_file(uploaded_file)
    if raw_data is not None:
        data = transform_data(raw_data)
        st.write("### Transformed Data Preview")
        st.dataframe(data.head())

        # Sidebar Filters
        st.sidebar.header("Filters")
        provinces = list(data["province"].dropna().unique())
        genders = list(data["s1q1"].dropna().unique())
        selected_province = st.sidebar.selectbox("Select Province", ["All"] + provinces)
        selected_gender = st.sidebar.selectbox("Select Gender (s1q1)", ["All"] + genders)

        filtered_data = data.copy()
        if selected_province != "All":
            filtered_data = filtered_data[filtered_data["province"] == selected_province]
        if selected_gender != "All":
            filtered_data = filtered_data[filtered_data["s1q1"] == selected_gender]

        # Sidebar: AI Insights - User Prompt
        st.sidebar.subheader("💬 Ask NISR AI for Insights")
        user_query = st.sidebar.text_input("Enter your question about the charts:")
        if user_query:
            # Prepare context from key charts using filtered data
            context = (
                f"Poverty Rate by Province Data: {chart_poverty_distribution_by_province(filtered_data).to_dict()}\n"
                f"Average Consumption by Province Data: {chart_average_consumption_by_province(filtered_data).to_dict()}\n"
                f"Top 5 Districts by Consumption Data: {chart_top_5_districts_by_consumption(filtered_data).to_dict()}\n"
                f"Poverty Rate by Gender Data: {chart_poverty_rate_by_gender(filtered_data).to_dict()}\n"
                f"Urban vs Rural Consumption Data: {chart_urban_vs_rural_consumption(filtered_data).to_dict()}\n"
            )
            ai_response = ask_gemma(user_query, context)
            st.sidebar.write("**NISR AI:**", ai_response)

        # Sidebar: Frequency Table Generator
        st.sidebar.subheader("Generate Frequency Table")
        freq_options = [
            "None",
            "Poverty by Province",
            "Poverty by Gender",
            "Poverty by Education Level",
            "Education Level by Province",
            "Province by Gender",
            "Gender by Education Level"
        ]
        selected_freq = st.sidebar.selectbox("Select Analysis for Frequency Table", freq_options)
        if selected_freq != "None":
            if selected_freq == "Poverty by Province":
                freq_table = pd.crosstab(filtered_data["province"], filtered_data["poverty"])
            elif selected_freq == "Poverty by Gender":
                freq_table = pd.crosstab(filtered_data["s1q1"], filtered_data["poverty"])
            elif selected_freq == "Poverty by Education Level":
                if "education_level" in filtered_data.columns:
                    freq_table = pd.crosstab(filtered_data["education_level"], filtered_data["poverty"])
                else:
                    freq_table = pd.DataFrame({"Error": ["Education level data is missing"]})
            elif selected_freq == "Education Level by Province":
                if "education_level" in filtered_data.columns:
                    freq_table = pd.crosstab(filtered_data["province"], filtered_data["education_level"])
                else:
                    freq_table = pd.DataFrame({"Error": ["Education level data is missing"]})
            elif selected_freq == "Province by Gender":
                freq_table = pd.crosstab(filtered_data["province"], filtered_data["s1q1"])
            elif selected_freq == "Gender by Education Level":
                if "education_level" in filtered_data.columns:
                    freq_table = pd.crosstab(filtered_data["s1q1"], filtered_data["education_level"])
                else:
                    freq_table = pd.DataFrame({"Error": ["Education level data is missing"]})

            st.sidebar.write("### Frequency Table")
            st.sidebar.dataframe(freq_table)
            csv = freq_table.to_csv().encode('utf-8')
            st.sidebar.download_button(
                label="Download Frequency Table as CSV",
                data=csv,
                file_name=f"{selected_freq.replace(' ', '_').lower()}_frequency_table.csv",
                mime="text/csv"
            )

        # PDF Report Generation Section
        if st.sidebar.button("Generate PDF Report"):
            # Create a dictionary of frequency tables
            freq_tables = {}
            try:
                freq_tables["Poverty by Province"] = pd.crosstab(filtered_data["province"], filtered_data["poverty"])
            except Exception:
                freq_tables["Poverty by Province"] = pd.DataFrame({"Error": ["Data not available"]})
            try:
                freq_tables["Poverty by Gender"] = pd.crosstab(filtered_data["s1q1"], filtered_data["poverty"])
            except Exception:
                freq_tables["Poverty by Gender"] = pd.DataFrame({"Error": ["Data not available"]})

            ai_interpretation = "AI-generated conclusions go here. (This should be generated dynamically.)"
            pdf_buffer = generate_pdf_report(freq_tables, ai_interpretation)
            st.sidebar.download_button(
                label="Download PDF Report",
                data=pdf_buffer,
                file_name="Institution_Report.pdf",
                mime="application/pdf"
            )

        # Display charts using filtered data
        st.subheader("Poverty Distribution by Province")
        fig1 = chart_poverty_distribution_by_province(filtered_data)
        if fig1:
            st.plotly_chart(fig1)

        st.subheader("Average Consumption by Province")
        fig2 = chart_average_consumption_by_province(filtered_data)
        if fig2:
            st.plotly_chart(fig2)

        st.subheader("Top 5 Districts by Consumption")
        fig3 = chart_top_5_districts_by_consumption(filtered_data)
        if fig3:
            st.plotly_chart(fig3)

        st.subheader("Poverty Rate by Gender")
        fig4 = chart_poverty_rate_by_gender(filtered_data)
        if fig4:
            st.plotly_chart(fig4)

        st.subheader("Urban vs Rural Consumption")
        fig5 = chart_urban_vs_rural_consumption(filtered_data)
        if fig5:
            st.plotly_chart(fig5)

        st.subheader("Poverty Distribution by Education Level")
        fig6 = chart_poverty_distribution_by_education_level(filtered_data)
        if fig6:
            st.plotly_chart(fig6)
