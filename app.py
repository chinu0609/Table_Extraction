import streamlit as st
import pandas as pd
from io import BytesIO
import pdfplumber as pdf
from img2table.document import PDF
from pdf_processing import get_tables,get_tables_scanned




st.title("📄 Table Extraction from PDF")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")
    
    # Select PDF type
    pdf_type = st.radio("Select PDF Type:", ("Only Text", "Scanned"))
    dfs = None 
    if pdf_type == "Scanned":
        dfs = get_tables_scanned(PDF(uploaded_file))
    else:
        dfs = get_tables(pdf.open(uploaded_file))
    
    
    if dfs:
        # Show extracted tables
        for i, df in enumerate(dfs):
            st.write(f"### Extracted Table {i+1}")
            st.dataframe(df)

        # Function to save DataFrames as an Excel file
        def save_dfs_to_excel(dfs):
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                for i, df in enumerate(dfs):
                    df.to_excel(writer, sheet_name=f"Table_{i+1}")
            output.seek(0)
            return output

        # Download button
        excel_data = save_dfs_to_excel(dfs)
        st.download_button(
            label="📥 Download All Tables as Excel",
            data=excel_data,
            file_name="extracted_tables.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No tables extracted. Check the PDF content.")
