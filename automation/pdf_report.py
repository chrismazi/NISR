import io
import math
import pandas as pd
from fpdf import FPDF
import streamlit as st
import os

class PDFReport(FPDF):
    def header(self):
        """Draw header on each page."""
        self.set_font("DejaVuSans", "B", 12)
        self.cell(0, 10, "Poverty and Consumption Insights Report", ln=True, align="C")
        self.ln(2)

    def footer(self):
        """Draw footer on each page."""
        self.set_y(-15)
        self.set_font("DejaVuSans", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def draw_table(pdf: FPDF, df: pd.DataFrame, title: str):
    """
    Draw a professional table in the PDF.
    
    Parameters:
        pdf (FPDF): The PDF report instance.
        df (pd.DataFrame): The DataFrame to be rendered as a table.
        title (str): Title for the table section.
    """
    pdf.set_font("DejaVuSans", "B", 14)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(2)
    
    if df.empty:
        pdf.set_font("DejaVuSans", "", 12)
        pdf.cell(0, 10, "No data available.", ln=True)
        pdf.ln(5)
        return
    
    # Ensure DataFrame is all strings for printing
    df = df.astype(str)
    
    # Prepare header list: if the DataFrame has an index name, include it.
    headers = []
    if df.index.name:
        headers.append(str(df.index.name))
    else:
        headers.append("Index")
    headers.extend(df.columns.tolist())
    
    # Calculate column widths based on page width (using margins)
    page_width = pdf.w - 2 * pdf.l_margin
    num_cols = len(headers)
    # Slightly reduce each column’s width to prevent text from clipping
    col_width = (page_width / num_cols) - 2  # <-- CHANGED

    # Set header font and print headers with border
    pdf.set_font("DejaVuSans", "B", 10)
    for header in headers:
        pdf.cell(col_width, 8, str(header), border=1, align="C")
    pdf.ln(8)
    
    # Set regular font for data rows
    pdf.set_font("DejaVuSans", "", 10)
    
    # Iterate over DataFrame rows
    for idx, row in df.iterrows():
        pdf.cell(col_width, 8, str(idx), border=1, align="C")
        for val in row:
            pdf.cell(col_width, 8, val, border=1, align="C")
        pdf.ln(8)
    pdf.ln(5)

def generate_pdf_report(freq_tables: dict, ai_interpretation: str) -> io.BytesIO:
    """
    Generate a polished PDF report that includes a cover page, table of contents,
    sections with professional tables, and a conclusions section with AI interpretation.
    
    Parameters:
        freq_tables (dict): A dictionary where keys are table titles and values are DataFrames.
        ai_interpretation (str): AI-generated conclusions and recommendations.
        
    Returns:
        BytesIO: In-memory buffer containing the generated PDF report.
    """
    # Switch to Landscape orientation for more horizontal space
    pdf = PDFReport(orientation='L')  # <-- CHANGED
    
    # Reduce margins slightly to avoid text cutting
    pdf.set_auto_page_break(auto=True, margin=10)  # <-- CHANGED
    
    # Add Unicode fonts.
    # Ensure the font files are in your project directory or update the paths accordingly.
    pdf.add_font("DejaVuSans", "", os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"), uni=True)
    pdf.add_font("DejaVuSans", "B", os.path.join(os.path.dirname(__file__), "DejaVuSans-Bold.ttf"), uni=True)
    pdf.add_font("DejaVuSans", "I", os.path.join(os.path.dirname(__file__), "DejaVuSans-Oblique.ttf"), uni=True)
    
    # --- Cover Page ---
    pdf.add_page()
    pdf.set_font("DejaVuSans", "B", 24)
    pdf.cell(0, 20, "EICV Poverty and Consumption Insights Report", ln=True, align="C")
    pdf.set_font("DejaVuSans", "", 16)
    pdf.cell(0, 10, "National Institute of Statistics Rwanda", ln=True, align="C")
    pdf.cell(0, 10, "Year: 2024", ln=True, align="C")
    pdf.ln(30)
    
    # --- Foreword ---
    pdf.add_page()
    pdf.set_font("DejaVuSans", "B", 18)
    pdf.cell(0, 10, "Foreword", ln=True)
    pdf.ln(5)
    pdf.set_font("DejaVuSans", "", 12)
    foreword_text = (
        "This report provides a comprehensive analysis of poverty and consumption patterns based on the uploaded dataset. "
        "The frequency tables and visualizations included are generated automatically through our institutional data analytics pipeline. "
        "The conclusions section provides NISR AI-generated insights to support evidence-based decision making."
    )
    pdf.multi_cell(0, 10, foreword_text)
    pdf.ln(10)
    
    # --- Table of Contents ---
    pdf.add_page()
    pdf.set_font("DejaVuSans", "B", 18)
    pdf.cell(0, 10, "Table of Contents", ln=True)
    pdf.ln(5)
    pdf.set_font("DejaVuSans", "", 12)
    toc_items = [
        "1. Foreword",
        "2. Frequency Table Analyses",
        "   a. " + " | ".join(freq_tables.keys()),
        "3. NISR AI-Generated Conclusions"
    ]
    for item in toc_items:
        pdf.cell(0, 8, item, ln=True)
    pdf.ln(10)
    
    # --- Frequency Table Analyses ---
    pdf.add_page()
    pdf.set_font("DejaVuSans", "B", 18)
    pdf.cell(0, 10, "Frequency Table Analyses", ln=True)
    pdf.ln(5)
    for title, table in freq_tables.items():
        draw_table(pdf, table, title)
    
    # --- Conclusions and Recommendations ---
    pdf.add_page()
    pdf.set_font("DejaVuSans", "B", 18)
    pdf.cell(0, 10, "NISR AI-Generated Conclusions", ln=True)
    pdf.ln(5)
    pdf.set_font("DejaVuSans", "", 12)
    pdf.multi_cell(0, 10, ai_interpretation)
    
    # Save PDF to an in-memory buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# ---------------------------
# Example usage (for testing purposes):
if __name__ == "__main__":
    data = {
        "province": ["Kigali", "Kigali", "Northern", "Eastern", "Kigali", "Southern", "Northern"],
        "poverty": [1, 0, 1, 0, 1, 0, 1],
        "s1q1": ["Male", "Female", "Female", "Male", "Female", "Male", "Male"],
        "education_level": ["Primary", "Secondary", "Primary", "Unknown", "Secondary", "Primary", "Primary"],
        "ur2_2012": ["Urban", "Urban", "Rural", "Rural", "Urban", "Rural", "Rural"]
    }
    df = pd.DataFrame(data)
    
    freq_tables = {
        "Poverty by Province": pd.crosstab(df["province"], df["poverty"]),
        "Poverty by Gender": pd.crosstab(df["s1q1"], df["poverty"]),
        "Poverty by Education Level": pd.crosstab(df["education_level"], df["poverty"]),
        "Education Level by Province": pd.crosstab(df["province"], df["education_level"]),
        "Province by Gender": pd.crosstab(df["province"], df["s1q1"]),
       # "Gender by Education Level": pd.crosstab(df["s1q1"], df["education_level"]),
       # "Urban vs Rural Consumption Frequency": pd.crosstab(
           # df["ur2_2012"], 
           # pd.cut([100,200,150,300,250,400,350], bins=3)
        #)
    }
    
    ai_interpretation = (
        "The AI analysis indicates significant disparities across regions. "
        "Kigali shows a higher incidence of poverty in conjunction with lower average consumption levels, "
        "suggesting potential areas for targeted intervention. Additionally, the data reveals gender-based differences "
        "in poverty levels that warrant further investigation."
    )
    
    pdf_buffer = generate_pdf_report(freq_tables, ai_interpretation)
    
    with open("Institution_Report.pdf", "wb") as f:
        f.write(pdf_buffer.getbuffer())
